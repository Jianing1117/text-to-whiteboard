#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用AI频繁记录自己，是普通人成本最低的改命
→ Excalidraw 白板生成脚本 v6（多卡片多色 · 去黄底 · 彩色文字强化）

配色规则（v6）：
  1. 全部浅色卡片，没有深色背景
  2. 卡片内不混色：底色和装饰线必须同色族
  3. 标题及附近元素颜色统一，不加不匹配的下划线
  4. 主要标题默认 INK（黑色），强化板块则整块统一一色
  5. 多卡片（3+ 张并列）优先使用多色区分
  6. 不出现黄底小卡片；黄色强化改为白底 + 金色文字
"""

import json, uuid, sys

# ── 色板系统 v5 ────────────────────────────────────────
WHITE   = "#FFFFFF"
C0      = "#F4F7F9"   # 画布背景（极浅冷白）

# 蓝族
C1      = "#DDE7ED"   # 浅蓝底
C2      = "#C3D4DE"   # 中浅蓝（分隔线、次级底色）
C3      = "#9FB5C3"   # 中蓝（细线、箭头）
C4      = "#6D8FA0"   # 深蓝（蓝族文字、竖线、章节标题装饰）
C5      = "#3D5A6A"   # 最深蓝（章节标题文字、强调文字）

# 四模块四色（浅底 + 深字成对）
BLUE_L  = "#DDE7ED";  BLUE_D  = "#3D6A82"  # 蓝（模块一）
GREEN_L = "#E2EDDF";  GREEN_D = "#3A6B42"  # 绿（模块二）
YELLOW_L= "#F5F0DC";  YELLOW_D= "#7A6020"  # 黄（模块三）
ROSE_L  = "#F2E8E6";  ROSE_D  = "#8F3F3A"  # 玫瑰红（模块四）

# 强化色（整块统一用，不混）
GOLD    = "#B8882A"   # 金/黄（强化板块文字，如命运公式）
GOLD_L  = "#F5F0DC"   # 金黄浅底（强化板块底色）

# 文字
INK     = "#1E2A30"   # 主黑色文字（大多数标题/梗概）
INK_M   = "#506570"   # 中等文字
INK_L   = "#8FA0A8"   # 浅色/次要文字

elements = []

def uid():
    return str(uuid.uuid4())

# ── 文字宽度估算（中英文混排友好）──────────────────────

def estimate_text_width(text, size):
    """估算文字渲染宽度，中英文混排友好"""
    width = 0
    for char in text:
        if '\u4e00' <= char <= '\u9fff':  # 中文字符
            width += size * 0.95
        elif char.isupper():  # 大写英文
            width += size * 0.65
        else:  # 小写英文、数字、符号
            width += size * 0.45
    return max(int(width), 80)

# ── 边界检查函数 ──────────────────────────────────────

def check_bounds(elements):
    """检查所有文字元素是否超出其所在卡片的边界，输出警告"""
    # 收集所有"大卡片"（宽度 > 100px，高度 > 40px，排除装饰性细矩形）
    rects = []
    for e in elements:
        if e["type"] == "rectangle" and e["width"] > 100 and e["height"] > 40:
            rects.append({
                "x": e["x"], "y": e["y"],
                "x2": e["x"] + e["width"],
                "y2": e["y"] + e["height"],
                "w": e["width"], "h": e["height"]
            })

    warnings = []
    for e in elements:
        if e["type"] != "text":
            continue
        tx, ty = e["x"], e["y"]
        tw, th = e["width"], e["height"]
        text_right = tx + tw
        text_bottom = ty + th

        # 找到最匹配的卡片：文字左上角在卡片内，且卡片面积最小
        best_rect = None
        best_area = float('inf')
        for r in rects:
            # 文字左上角必须严格在卡片内部（x 和 y 都要在范围内）
            if r["x"] + 4 <= tx < r["x2"] - 4 and r["y"] + 4 <= ty < r["y2"] - 4:
                area = r["w"] * r["h"]
                if area < best_area:
                    best_area = area
                    best_rect = r

        if best_rect:
            rx2, ry2 = best_rect["x2"], best_rect["y2"]
            # 检查是否超出右边界（留 16px 余量）
            if text_right > rx2 - 16:
                warnings.append(f"⚠️ 右边界超出: \"{e['text'][:15]}...\" ({int(text_right)} > {int(rx2)})")
            # 检查是否超出下边界（留 8px 余量）
            if text_bottom > ry2 - 8:
                warnings.append(f"⚠️ 下边界超出: \"{e['text'][:15]}...\" ({int(text_bottom)} > {int(ry2)})")

    if warnings:
        print("\n🔍 边界检查结果：")
        for w in warnings[:10]:  # 只显示前10条
            print(f"  {w}")
        if len(warnings) > 10:
            print(f"  ... 还有 {len(warnings) - 10} 条警告")
        print(f"\n  共 {len(warnings)} 个警告，请检查！\n")
    else:
        print("✅ 边界检查通过，无文字超出卡片")

    return warnings

# ── 对齐检查函数 ──────────────────────────────────────

def check_alignment(elements, tolerance=8):
    """检查卡片是否左右对齐，输出警告"""
    # 收集所有"大卡片"
    cards = []
    for e in elements:
        if e["type"] == "rectangle" and e["width"] > 100 and e["height"] > 40:
            cards.append({
                "x": e["x"],
                "y": e["y"],
                "x2": e["x"] + e["width"],
                "y2": e["y"] + e["height"],
                "w": e["width"],
                "h": e["height"]
            })

    if not cards:
        return []

    # 按 y 坐标分组（同一行的卡片 y 坐标相近）
    rows = {}
    for card in cards:
        y_key = round(card["y"] / 50) * 50  # 50px 容差
        if y_key not in rows:
            rows[y_key] = []
        rows[y_key].append(card)

    warnings = []

    # 检查每行的左边界和右边界是否对齐
    row_boundaries = []
    for y_key, row_cards in sorted(rows.items()):
        if len(row_cards) >= 2:  # 只检查有 2+ 卡片的行
            left_edge = min(c["x"] for c in row_cards)
            right_edge = max(c["x2"] for c in row_cards)
            row_boundaries.append({
                "y": y_key,
                "left": left_edge,
                "right": right_edge,
                "count": len(row_cards)
            })

    # 检查所有行的边界是否一致
    if len(row_boundaries) >= 2:
        left_edges = [r["left"] for r in row_boundaries]
        right_edges = [r["right"] for r in row_boundaries]

        min_left, max_left = min(left_edges), max(left_edges)
        min_right, max_right = min(right_edges), max(right_edges)

        if max_left - min_left > tolerance:
            warnings.append(f"⚠️ 左边界不对齐: 最左 {int(min_left)} vs 最右 {int(max_left)} (差距 {int(max_left - min_left)}px)")
            for r in row_boundaries:
                if r["left"] != min_left:
                    warnings.append(f"    行 y={r['y']}: 左边界={int(r['left'])}")

        if max_right - min_right > tolerance:
            warnings.append(f"⚠️ 右边界不对齐: 最左 {int(min_right)} vs 最右 {int(max_right)} (差距 {int(max_right - min_right)}px)")
            for r in row_boundaries:
                if r["right"] != max_right:
                    warnings.append(f"    行 y={r['y']}: 右边界={int(r['right'])}")

    if warnings:
        print("\n📐 对齐检查结果：")
        for w in warnings[:15]:
            print(f"  {w}")
        print(f"\n  共 {len(warnings)} 个警告，请调整卡片位置！\n")
    else:
        print("✅ 对齐检查通过，卡片左右对齐")

    return warnings

# ── 基础构建函数 ──────────────────────────────────────

def el_rect(x, y, w, h, bg=C1, stroke="transparent", sw=0, r=8):
    return {
        "id": uid(), "type": "rectangle",
        "x": x, "y": y, "width": w, "height": h,
        "backgroundColor": bg, "strokeColor": stroke,
        "strokeWidth": sw, "roughness": 0,
        "roundness": {"type": 3, "value": r},
        "fillStyle": "solid", "opacity": 100,
        "angle": 0, "seed": 1,
        "isDeleted": False, "version": 1, "versionNonce": 1,
        "groupIds": [], "frameId": None, "boundElements": [],
        "updated": 1, "link": None, "locked": False
    }

def el_line(x, y, w, color=C2, sw=1):
    return {
        "id": uid(), "type": "line",
        "x": x, "y": y, "width": w, "height": 0,
        "points": [[0, 0], [w, 0]],
        "strokeColor": color, "backgroundColor": "transparent",
        "strokeWidth": sw, "roughness": 0,
        "fillStyle": "solid", "opacity": 100,
        "angle": 0, "seed": 1,
        "startBinding": None, "endBinding": None,
        "startArrowhead": None, "endArrowhead": None,
        "isDeleted": False, "version": 1, "versionNonce": 1,
        "groupIds": [], "frameId": None, "boundElements": [],
        "updated": 1, "link": None, "locked": False
    }

def el_text(x, y, text, size=15, color=INK, w=None, align="left", family=1):
    # 使用中英文混排友好的宽度估算
    tw = w if w else estimate_text_width(text, size)
    return {
        "id": uid(), "type": "text",
        "x": x, "y": y, "width": tw, "height": size * 1.5,
        "text": text, "fontSize": size, "fontFamily": family,
        "textAlign": align, "verticalAlign": "top",
        "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "roughness": 0, "opacity": 100,
        "angle": 0, "seed": 1,
        "isDeleted": False, "version": 1, "versionNonce": 1,
        "groupIds": [], "frameId": None, "boundElements": [],
        "updated": 1, "link": None, "locked": False,
        "containerId": None, "lineHeight": 1.5,
        "autoResize": True
    }

def el_arrow(x1, y1, x2, y2, color=C3, sw=1.5):
    return {
        "id": uid(), "type": "arrow",
        "x": x1, "y": y1,
        "width": abs(x2 - x1), "height": abs(y2 - y1),
        "points": [[0, 0], [x2 - x1, y2 - y1]],
        "strokeColor": color, "backgroundColor": "transparent",
        "strokeWidth": sw, "roughness": 0,
        "fillStyle": "solid", "opacity": 100,
        "angle": 0, "seed": 1,
        "startBinding": None, "endBinding": None,
        "startArrowhead": None, "endArrowhead": "arrow",
        "isDeleted": False, "version": 1, "versionNonce": 1,
        "groupIds": [], "frameId": None, "boundElements": [],
        "updated": 1, "link": None, "locked": False
    }

def section_label(x, y, text, w=1100):
    """章节标题：左侧 C4 深蓝竖线 + INK 黑色文字（主标题默认黑色）"""
    elements.append(el_rect(x, y, 4, 42, C4, C4, 0, 2))
    elements.append(el_text(x + 20, y + 8, text, 24, INK, w - 20))

# ════════════════════════════════════════════════════
#  开始绘制
# ════════════════════════════════════════════════════
PAGE_X = 60
PAGE_W = 1100
Y = 0

# ────────────────────────────────────────────────────
# 标题区：浅蓝底，全部蓝色系，不混其他颜色
# ────────────────────────────────────────────────────
TITLE_H = 148
elements.append(el_rect(PAGE_X, Y, PAGE_W, TITLE_H, C1, "transparent", 0, 12))
# 左侧深蓝竖条（同色族装饰，不混色）
elements.append(el_rect(PAGE_X, Y, 12, TITLE_H, C4, C4, 0, 6))

# 主标题（黑色，清晰为主）
elements.append(el_text(PAGE_X + 36, Y + 24, "用 AI 频繁记录自己", 42, INK, 760))
# 副标题（深蓝，同色族）
elements.append(el_text(PAGE_X + 36, Y + 82, "是普通人成本最低的改命方式", 22, C4, 760))
# 小字副信息（浅蓝，退到背景）
elements.append(el_text(PAGE_X + 36, Y + 120, "jianing · 加宁慢慢来", 11, C3, 280))

Y += TITLE_H + 28

# ────────────────────────────────────────────────────
# 命运公式条幅：白底 + 金色文字（无黄底卡片，减少量感）
# ────────────────────────────────────────────────────
elements.append(el_rect(PAGE_X, Y, PAGE_W, 60, WHITE, "transparent", 0, 8))
elements.append(el_rect(PAGE_X, Y, 3, 60, GOLD, GOLD, 0, 2))
elements.append(el_text(PAGE_X + 20, Y + 8,
    "命运的底层公式：想法  →  情绪  →  行为  →  结果  →  命运", 16, GOLD, PAGE_W - 30))
elements.append(el_text(PAGE_X + 20, Y + 34,
    "高频记录 + AI = 把「命运复利」的周期从 1 年压缩到 1 天", 13, GOLD, PAGE_W - 30))
Y += 80

elements.append(el_line(PAGE_X, Y, PAGE_W, C2, 1))
Y += 36

# ────────────────────────────────────────────────────
# 一、为什么「高频记录 + AI」能改命？
# ────────────────────────────────────────────────────
section_label(PAGE_X, Y, "一、为什么「高频记录 + AI」能改命？")
Y += 52

# 4 张卡片：四色区分（蓝/绿/黄/玫瑰红），符合多卡片多色规则
card_w, card_h = 238, 152
card_gap = 24
theories = [
    ("乔哈里视窗",    "The Johari Window",
     "AI 是无利益冲突的镜子\n精准指出你的盲目区",    BLUE_L, BLUE_D),
    ("控制论反馈闭环", "Cybernetics Loop",
     "把按年复盘压缩到按天\n极大缩短纠偏周期",       GREEN_L, GREEN_D),
    ("霍桑效应",     "Hawthorne Effect",
     "被观察时行为自动改善\n觉察感让你及时刹车",     YELLOW_L, YELLOW_D),
    ("数字分身基础",  "Digital Twin",
     "持续记录 = 训练AI\n是链接AI时代的敲门砖",     ROSE_L, ROSE_D),
]
total_tw = len(theories) * card_w + (len(theories) - 1) * card_gap
tx_start = PAGE_X + (PAGE_W - total_tw) // 2
for i, (title, sub, body, bg, accent) in enumerate(theories):
    cx = tx_start + i * (card_w + card_gap)
    elements.append(el_rect(cx, Y, card_w, card_h, bg, "transparent", 0, 10))
    # 顶部细线：同色族
    elements.append(el_rect(cx, Y, card_w, 3, accent, accent, 0, 2))
    elements.append(el_text(cx + 16, Y + 16, title, 15, accent, card_w - 32))
    elements.append(el_text(cx + 16, Y + 36, sub, 11, INK_L, card_w - 32))
    body_lines = body.split("\n")
    for j, bl in enumerate(body_lines):
        elements.append(el_text(cx + 16, Y + 68 + j * 28, bl, 13, INK_M, card_w - 32))

Y += card_h + 52

elements.append(el_line(PAGE_X, Y, PAGE_W, C2, 1))
Y += 36

# ────────────────────────────────────────────────────
# 二、为什么你总是记录失败？
# ────────────────────────────────────────────────────
section_label(PAGE_X, Y, "二、为什么你总是记录失败？")
Y += 52

# 左右双栏：统一浅蓝族，不混色
# 标题用 INK 黑色（主标题默认黑色规则）
col_w = 490
pain_items = [
    "太费时间：要求排版、要求文笔",
    "经常忘记：没有习惯触发点",
    "没什么好记的：只等大事才记",
    "记完不知怎么处理：没有闭环",
]
fix_items = [
    "语音记录，主打低阻力输入",
    "到点提醒找你，外力建立触发",
    "小情绪/小决策/小灵感都值得记",
    "把 AI 当数据分析师，形成飞轮",
]

panel_h = 40 + len(pain_items) * 44 + 20

# 左：痛点（C0 底 + C3 左竖线，文字 INK）
elements.append(el_rect(PAGE_X, Y, col_w, panel_h, C0, "transparent", 0, 10))
elements.append(el_rect(PAGE_X, Y, 3, panel_h, C3, C3, 0, 4))
elements.append(el_text(PAGE_X + 20, Y + 12, "记录失败的 4 大痛点", 14, INK, col_w - 40))
for i, item in enumerate(pain_items):
    elements.append(el_text(PAGE_X + 20, Y + 46 + i * 44, item, 13, INK_M, col_w - 40))

# 中间箭头（蓝色）
arr_mx = PAGE_X + col_w + 10
elements.append(el_arrow(arr_mx, Y + panel_h // 2, arr_mx + 58, Y + panel_h // 2, C4, 2))

# 右：解法（C1 底 + C4 左竖线，文字 INK）
rx = PAGE_X + col_w + 80
elements.append(el_rect(rx, Y, col_w, panel_h, C1, "transparent", 0, 10))
elements.append(el_rect(rx, Y, 3, panel_h, C4, C4, 0, 4))
elements.append(el_text(rx + 20, Y + 12, "破局解法：低阻力 + 自动化闭环", 14, INK, col_w - 40))
for i, item in enumerate(fix_items):
    elements.append(el_text(rx + 20, Y + 46 + i * 44, item, 13, INK_M, col_w - 40))

Y += panel_h + 48

# A.I.R. 系统
# 标题黑色，无下划线（规则3：不加不匹配颜色的下划线）
elements.append(el_text(PAGE_X, Y, "A.I.R. 系统：重塑自己的三步框架", 15, INK, PAGE_W))
Y += 38

# A.I.R. 三步卡片：三色区分（蓝/绿/玫瑰红），每张同色自洽
air_steps = [
    ("A", "Awareness",     "无痛采集", "降低记录门槛\n只做信息的搬运工",    BLUE_L,   BLUE_D),
    ("I", "Insight",       "深度洞察", "利用AI涌现能力\n发现隐藏行为模式",  GREEN_L,  GREEN_D),
    ("R", "Recalibration", "行为校准", "生成具体行动指令\n微调明天",         ROSE_L,   ROSE_D),
]

aw, ah = 310, 114
a_gap = 52
atotal = len(air_steps) * aw + (len(air_steps) - 1) * a_gap
ax = PAGE_X + (PAGE_W - atotal) // 2
for i, (letter, en, cn, desc, bg, tc) in enumerate(air_steps):
    bx = ax + i * (aw + a_gap)
    elements.append(el_rect(bx, Y, aw, ah, bg, "transparent", 0, 10))
    # 顶部细线：同色族
    elements.append(el_rect(bx, Y, aw, 3, tc, tc, 0, 2))
    elements.append(el_text(bx + 18, Y + 14, letter, 38, tc, 48))
    elements.append(el_text(bx + 66, Y + 16, cn, 17, INK, 180))
    elements.append(el_text(bx + 66, Y + 40, en, 11, INK_L, 180))
    desc_lines = desc.split("\n")
    for j, dl in enumerate(desc_lines):
        elements.append(el_text(bx + 18, Y + 74 + j * 22, dl, 12, INK_M, aw - 36))
    if i < len(air_steps) - 1:
        elements.append(el_arrow(bx + aw + 5, Y + ah // 2, bx + aw + a_gap - 5, Y + ah // 2, C3, 1.5))

Y += ah + 60
elements.append(el_line(PAGE_X, Y, PAGE_W, C2, 1))
Y += 36

# ────────────────────────────────────────────────────
# 三、4 大记录模块（四色区分）
# 规则5：4个模块需要视觉区分，使用4色（蓝/绿/黄/玫瑰红）
# 每张卡片内部颜色自洽，不混色
# ────────────────────────────────────────────────────
section_label(PAGE_X, Y, "三、4 大记录模块（把 AI 当首席数据分析师）")
Y += 52

modules = [
    {
        "title": "模块一：记情绪",
        "sub": "破解「自动反应」",
        "points": [
            "突发情绪是观察自己最好的窗口",
            "理论：CBT / ACT / 情绪ABC / 佛法",
            "三步走：共情 → 分析 → 整合行动",
            "Prompt：情绪陪伴助手 + 情绪周报",
        ],
        "bg": BLUE_L, "accent": BLUE_D,
    },
    {
        "title": "模块二：记决策",
        "sub": "训练「决策画像」",
        "points": [
            "长期差异来自反复做了哪些决定",
            "DRIFT框架：D / R / I / F / T",
            "区分恐惧幻想 vs 真实 Trade-off",
            "Prompt：决策记录 + 决策教练",
        ],
        "bg": GREEN_L, "accent": GREEN_D,
    },
    {
        "title": "模块三：记灵感",
        "sub": "搭建「第二大脑」",
        "points": [
            "来了没记，记了没展开 = 废稿",
            "框架：种子 → 展开 → 验证",
            "你产生火花，AI 负责结构化",
            "Prompt：灵感收集周报",
        ],
        "bg": YELLOW_L, "accent": YELLOW_D,
    },
    {
        "title": "模块四：记日记",
        "sub": "每日能量「微调」",
        "points": [
            "日记是每天的「收口」，不需长篇",
            "内容：睡眠 / 状态 / 习惯 / 感恩",
            "每周让AI做模式识别分析",
            "Prompt：数字分身采访官 + 日记模版",
        ],
        "bg": ROSE_L, "accent": ROSE_D,
    },
]

mod_w, mod_h = 490, 196
mod_gap_x, mod_gap_y = 80, 28
for i, mod in enumerate(modules):
    col = i % 2
    row = i // 2
    mx = PAGE_X + col * (mod_w + mod_gap_x)
    my = Y + row * (mod_h + mod_gap_y)
    bg     = mod["bg"]
    accent = mod["accent"]

    elements.append(el_rect(mx, my, mod_w, mod_h, bg, "transparent", 0, 10))
    # 左竖线：同色族深色，不混其他颜色
    elements.append(el_rect(mx, my, 3, mod_h, accent, accent, 0, 3))
    # 标题：同色族深色（需要区分，所以用 accent 而非黑色）
    elements.append(el_text(mx + 20, my + 16, mod["title"], 16, accent, mod_w - 40))
    # 副标题：黑色（次级信息用黑不用彩色）
    elements.append(el_text(mx + 20, my + 38, mod["sub"], 12, INK_L, mod_w - 40))
    # 细分隔线：同色族
    elements.append(el_line(mx + 20, my + 58, mod_w - 40, accent, 0.6))
    # 条目：INK_M 黑灰色
    for j, pt in enumerate(mod["points"]):
        elements.append(el_rect(mx + 20, my + 75 + j * 28 + 6, 4, 4, accent, accent, 0, 2))
        elements.append(el_text(mx + 32, my + 75 + j * 28, pt, 13, INK_M, mod_w - 52))

Y += 2 * (mod_h + mod_gap_y) + 56
elements.append(el_line(PAGE_X, Y, PAGE_W, C2, 1))
Y += 36

# ────────────────────────────────────────────────────
# 四、避坑指南
# 规则：浅色底 + 蓝族竖线 + 黑色文字（不大面积用彩色）
# ────────────────────────────────────────────────────
section_label(PAGE_X, Y, "四、避坑指南：为什么有人用 AI 记录却失败了？")
Y += 52

pitfalls = [
    ("× 过度追求排版和逻辑",
     "记录的本质是真实而非好看。哪怕错别字连篇，AI 也能看懂。摩擦力越小，越能坚持。"),
    ("× 把 AI 当成安慰剂",
     "不要让 AI 总是夸你。要设定 AI 为客观、一针见血、甚至有些毒舌的教练角色。"),
    ("× 只看不做",
     "AI 给出的明日微调建议，第二天不执行就失去意义。哪怕最简单的指令，也要完成它。"),
]
pw, ph = PAGE_W, 80
for i, (title, body) in enumerate(pitfalls):
    py = Y + i * (ph + 14)
    bg = C1 if i % 2 == 0 else C0
    elements.append(el_rect(PAGE_X, py, pw, ph, bg, "transparent", 0, 8))
    elements.append(el_rect(PAGE_X, py, 3, ph, C4, C4, 0, 3))
    # 标题用 INK 黑色（主标题默认黑，不需要强化）
    elements.append(el_text(PAGE_X + 20, py + 12, title, 14, INK, 500))
    elements.append(el_text(PAGE_X + 20, py + 38, body, 12, INK_M, pw - 44))

Y += len(pitfalls) * (ph + 14) + 56

# ────────────────────────────────────────────────────
# 五、金句结语
# 规则：白底 + 金色文字（无黄底卡片，减少量感；顶部金色细线做分界）
# ────────────────────────────────────────────────────
elements.append(el_rect(PAGE_X, Y, PAGE_W, 120, WHITE, "transparent", 0, 12))
# 顶部金色细线（轻量点缀，不做大面积底色）
elements.append(el_rect(PAGE_X, Y, PAGE_W, 2, GOLD, GOLD, 0, 0))
elements.append(el_text(PAGE_X + 40, Y + 22,
    "命运，就是你每天行为习惯的复利总和。", 22, GOLD, PAGE_W - 80))
elements.append(el_text(PAGE_X + 40, Y + 62,
    "从 NPC  →  主动调试自己人生代码的超级玩家", 15, GOLD, PAGE_W - 80))
elements.append(el_text(PAGE_X + 40, Y + 92,
    "今晚就按下录音键，对 AI 说出你的第一段碎碎念。", 13, YELLOW_D, PAGE_W - 80))
Y += 160

# ────────────────────────────────────────────────────
# 底部品牌签名（居中，手写体 jianing）
# ────────────────────────────────────────────────────
Y += 32
line_w = 370
inner_w = 260
sig_x = PAGE_X + (PAGE_W - inner_w - line_w * 2 - 32) // 2
elements.append(el_line(sig_x, Y + 14, line_w, C2, 1))
elements.append(el_line(sig_x + line_w + inner_w + 32, Y + 14, line_w, C2, 1))

elements.append({
    "id": uid(), "type": "text",
    "x": sig_x + line_w + 16, "y": Y,
    "width": 130, "height": 30,
    "text": "加宁慢慢来", "fontSize": 14, "fontFamily": 1,
    "textAlign": "left", "verticalAlign": "top",
    "strokeColor": INK_L, "backgroundColor": "transparent",
    "fillStyle": "solid", "roughness": 0, "opacity": 100,
    "angle": 0, "seed": 1,
    "isDeleted": False, "version": 1, "versionNonce": 1,
    "groupIds": [], "frameId": None, "boundElements": [],
    "updated": 1, "link": None, "locked": False,
    "containerId": None, "lineHeight": 1.5, "autoResize": True
})
elements.append({
    "id": uid(), "type": "text",
    "x": sig_x + line_w + 148, "y": Y,
    "width": 20, "height": 30,
    "text": "·", "fontSize": 14, "fontFamily": 1,
    "textAlign": "center", "verticalAlign": "top",
    "strokeColor": C3, "backgroundColor": "transparent",
    "fillStyle": "solid", "roughness": 0, "opacity": 100,
    "angle": 0, "seed": 1,
    "isDeleted": False, "version": 1, "versionNonce": 1,
    "groupIds": [], "frameId": None, "boundElements": [],
    "updated": 1, "link": None, "locked": False,
    "containerId": None, "lineHeight": 1.5, "autoResize": True
})
# "jianing" 手写字体（fontFamily: 3 = Virgil）
elements.append({
    "id": uid(), "type": "text",
    "x": sig_x + line_w + 172, "y": Y - 3,
    "width": 100, "height": 34,
    "text": "jianing", "fontSize": 20, "fontFamily": 3,
    "textAlign": "left", "verticalAlign": "top",
    "strokeColor": C4, "backgroundColor": "transparent",
    "fillStyle": "solid", "roughness": 0, "opacity": 100,
    "angle": 0, "seed": 1,
    "isDeleted": False, "version": 1, "versionNonce": 1,
    "groupIds": [], "frameId": None, "boundElements": [],
    "updated": 1, "link": None, "locked": False,
    "containerId": None, "lineHeight": 1.5, "autoResize": True
})

Y += 60

# ════════════════════════════════════════════════════
#  输出文件
# ════════════════════════════════════════════════════
out_path = "/Users/jnx/Desktop/用AI记录改命-白板.excalidraw"
if len(sys.argv) >= 3 and sys.argv[1] == "--output":
    out_path = sys.argv[2]

# 边界检查（输出前必须执行）
check_bounds(elements)
check_alignment(elements)

output = {
    "type": "excalidraw",
    "version": 2,
    "source": "https://excalidraw.com",
    "elements": elements,
    "appState": {
        "viewBackgroundColor": "#FFFFFF",
        "gridSize": None,
        "scrollX": 0,
        "scrollY": 0,
        "zoom": {"value": 0.75}
    },
    "files": {}
}

with open(out_path, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"✅ 生成完成：{out_path}")
print(f"📐 白板高度约：{Y}px")
print("👉 打开方式：excalidraw.com → 左上角菜单 → Open → 选择文件")
