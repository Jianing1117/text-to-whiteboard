#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简洁模式白板生成脚本模板
Simple Mode Whiteboard Generator Template

特点：
- 黑白文字为主，适合演讲/演示
- 最小化颜色使用（仅强调色点缀）
- 快速生成，轻量输出
"""

import json, uuid, sys

# ── 简洁模式配色 ────────────────────────────────────────
WHITE   = "#FFFFFF"
BLACK   = "#000000"
GRAY    = "#666666"
GRAY_L  = "#999999"

# 强调色（少量使用）
MIST_BLUE = "#C8D9E6"
MIST_PINK = "#E8CECA"

elements = []

def uid():
    return str(uuid.uuid4())

# ── 基础构建函数 ──────────────────────────────────────

def el_rect(x, y, w, h, bg=WHITE, stroke="#E0E0E0", sw=1, r=8):
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

def el_text(x, y, text, size=16, color=BLACK, w=None, align="left"):
    tw = w if w else max(len(text) * size * 0.6, 80)
    return {
        "id": uid(), "type": "text",
        "x": x, "y": y, "width": tw, "height": size * 1.5,
        "text": text, "fontSize": size, "fontFamily": 1,
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

def el_line(x, y, w, color="#E0E0E0", sw=1):
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

def el_arrow(x1, y1, x2, y2, color=GRAY_L, sw=1.5):
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

# ════════════════════════════════════════════════════
#  模板：标题 + 要点列表
# ════════════════════════════════════════════════════

def build_simple_list(title, sections, output_path):
    """
    构建简洁的列表式白板

    Args:
        title: 主标题
        sections: [{"title": "章节名", "items": ["项目1", "项目2"]}, ...]
        output_path: 输出文件路径
    """
    PAGE_X = 60
    PAGE_W = 800
    Y = 40

    # 主标题
    elements.append(el_text(PAGE_X, Y, title, 32, BLACK, PAGE_W))
    Y += 60

    # 分隔线
    elements.append(el_line(PAGE_X, Y, PAGE_W, "#E0E0E0", 2))
    Y += 30

    # 各章节
    for i, section in enumerate(sections):
        # 章节标题（带强调色圆点）
        accent_color = MIST_BLUE if i % 2 == 0 else MIST_PINK
        elements.append(el_rect(PAGE_X, Y + 5, 12, 12, accent_color, accent_color, 0, 6))
        elements.append(el_text(PAGE_X + 24, Y, section["title"], 20, BLACK, PAGE_W - 24))
        Y += 35

        # 项目列表
        for item in section["items"]:
            elements.append(el_text(PAGE_X + 24, Y, f"• {item}", 14, GRAY, PAGE_W - 24))
            Y += 28

        Y += 20  # 章节间距

    # 输出文件
    output = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {
            "viewBackgroundColor": "#FFFFFF",
            "gridSize": None,
            "scrollX": 0, "scrollY": 0,
            "zoom": {"value": 1}
        },
        "files": {}
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ 生成完成：{output_path}")
    print(f"📐 白板高度约：{Y}px")

# ════════════════════════════════════════════════════
#  模板：横向卡片流程
# ════════════════════════════════════════════════════

def build_simple_flow(title, steps, output_path):
    """
    构建简洁的横向流程白板

    Args:
        title: 主标题
        steps: ["步骤1", "步骤2", "步骤3", ...]
        output_path: 输出文件路径
    """
    PAGE_X = 60
    Y = 40

    # 主标题
    elements.append(el_text(PAGE_X, Y, title, 32, BLACK, 800))
    Y += 70

    # 计算卡片布局
    card_w = min(180, (800 - (len(steps) - 1) * 40) // len(steps))
    card_h = 80
    gap = 40
    total_w = len(steps) * card_w + (len(steps) - 1) * gap
    start_x = PAGE_X + (800 - total_w) // 2

    for i, step in enumerate(steps):
        cx = start_x + i * (card_w + gap)

        # 卡片背景（交替强调色）
        bg = MIST_BLUE if i % 2 == 0 else MIST_PINK
        elements.append(el_rect(cx, Y, card_w, card_h, bg, "transparent", 0, 8))

        # 步骤编号
        elements.append(el_text(cx + card_w // 2 - 10, Y + 15, str(i + 1), 24, BLACK, 20, "center"))

        # 步骤文字
        elements.append(el_text(cx + 10, Y + 50, step, 14, BLACK, card_w - 20, "center"))

        # 箭头（除最后一个）
        if i < len(steps) - 1:
            elements.append(el_arrow(cx + card_w + 5, Y + card_h // 2,
                                     cx + card_w + gap - 5, Y + card_h // 2, GRAY_L, 1.5))

    Y += card_h + 50

    # 输出文件
    output = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {
            "viewBackgroundColor": "#FFFFFF",
            "gridSize": None,
            "scrollX": 0, "scrollY": 0,
            "zoom": {"value": 1}
        },
        "files": {}
    }

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ 生成完成：{output_path}")
    print(f"📐 白板高度约：{Y}px")

# ════════════════════════════════════════════════════
#  主程序示例
# ════════════════════════════════════════════════════

if __name__ == "__main__":
    # 示例：列表式白板
    build_simple_list(
        title="今日计划",
        sections=[
            {"title": "上午", "items": ["完成周报", "回复邮件"]},
            {"title": "下午", "items": ["团队会议", "项目评审"]},
            {"title": "晚上", "items": ["读书 30 分钟"]}
        ],
        output_path="/Users/jnx/Desktop/simple_list.excalidraw"
    )

    # 示例：流程式白板
    # build_simple_flow(
    #     title="用户注册流程",
    #     steps=["填写信息", "邮箱验证", "完善资料", "开始使用"],
    #     output_path="/Users/jnx/Desktop/simple_flow.excalidraw"
    # )
