# Text to Whiteboard

[English](#english) | [中文](#中文)

---

<a name="english"></a>
## English

Transform any structured text content into beautiful, editable Excalidraw whiteboard diagrams automatically.

### 🎯 What This Does

This Claude Code skill converts your Markdown, Word documents, or plain text into professional `.excalidraw` files that you can open, edit, and share at [excalidraw.com](https://excalidraw.com).

**Perfect for:**
- 📚 Converting articles and notes into visual knowledge maps
- 🎓 Creating training and presentation materials
- 🚀 Visualizing processes and workflows
- ✨ Building shareable infographics and concept diagrams

### ✨ Features

- **8 Professional Color Themes** - Jianing Fav, Professional Blue, Finance Graph, Minimal Pitch, Soft Pastel, Paper & Ink, Vintage Editorial, Dark Mode
- **Custom Brand Support** - Use your own logo, colors, or brand name
- **Smart Diagram Selection** - Automatically chooses the best visualization type
- **Fully Editable Output** - All elements in Excalidraw are editable
- **Multi-Language Support** - Works with Chinese, English, Japanese, Korean, and more
- **Multiple Input Formats** - Markdown, Word, TXT, or direct text paste

### 📦 Installation

#### Option 1: Download .skill file

1. Download `text-to-whiteboard-v2.skill` from [Releases](https://github.com/YOUR_USERNAME/text-to-whiteboard/releases)
2. In Claude Code, run:
   ```
   /skill install path/to/text-to-whiteboard-v2.skill
   ```

#### Option 2: Manual Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/YOUR_USERNAME/text-to-whiteboard.git
   cd text-to-whiteboard
   ```

2. Copy to your Claude Code skills directory:
   ```bash
   cp -r . ~/.claude/skills/text-to-whiteboard
   ```

### 🚀 Quick Start

Just ask Claude to visualize your content:

```
User: "把这篇文章做成白板"
User: "Convert this article to Excalidraw"
User: "Make a knowledge map from this content"
User: "可视化这个流程"
```

### 🎨 Interactive Flow

When you create a whiteboard, Claude will guide you through:

**Step 1: Choose Color Scheme**
- **Option A**: Browse 8 preset themes (opens preview page)
- **Option B**: Upload custom colors (image / VI document)
- **Option C**: Use default (Jianing Fav)

**Step 2: Choose Branding**
- **Option A**: Use your name (enter your name)
- **Option B**: Upload custom brand (logo / colors)
- **Option C**: Skip (no branding)

### 📖 Color Themes

| Theme | Chinese | Best For |
|-------|---------|----------|
| Jianing Fav | 加宁最爱 | General use (default) |
| Professional Blue | 专业蓝 | Business, tech |
| Finance Graph | 金融图表 | Data analysis |
| Minimal Pitch | 极简路演 | Startup pitch |
| Soft Pastel | 柔和粉彩 | Education |
| Paper & Ink | 纸墨书香 | Literary, notes |
| Vintage Editorial | 复古编辑 | Magazine style |
| Dark Mode | 深色模式 | Presentation |

### 📊 Supported Diagram Types

- **Flowcharts & Process Diagrams** - Steps, workflows, timelines
- **Concept Maps** - Theories, categories, frameworks
- **Comparison Charts** - Pros/cons, alternatives, before/after
- **Knowledge Graphs** - Mind maps, concept networks

### 🛠️ Technical Details

- **Output Format:** `.excalidraw` (JSON-based)
- **Platform:** [excalidraw.com](https://excalidraw.com)
- **Editability:** All elements fully editable
- **Resolution:** Vector-based, unlimited zoom
- **File Size:** Typically 10-100KB

### 🤝 Contributing

Contributions welcome:
- Report bugs
- Suggest new features
- Add new color themes
- Improve documentation
- Submit pull requests

### 📝 License

MIT License - Free to use, modify, and distribute

---

<a name="中文"></a>
## 中文

将任何结构化文本内容自动转换为精美的可编辑 Excalidraw 白板图表。

### 🎯 功能介绍

这个 Claude Code 技能可以将你的 Markdown 文档、Word 文档或纯文本转换为专业的 `.excalidraw` 文件，你可以在 [excalidraw.com](https://excalidraw.com) 打开、编辑和分享。

**适用场景：**
- 📚 将文章和笔记转换为可视化知识地图
- 🎓 制作培训材料和演示文稿
- 🚀 可视化流程和工作流
- ✨ 制作可分享的信息图和概念图

### ✨ 特性

- **8种专业配色主题** - 加宁最爱、专业蓝、金融图表、极简路演、柔和粉彩、纸墨书香、复古编辑、深色模式
- **自定义品牌支持** - 使用你自己的 logo、颜色或品牌名
- **智能图表选择** - 自动选择最佳的可视化类型
- **完全可编辑** - Excalidraw 中的所有元素都可编辑
- **多语言支持** - 支持中文、英文、日文、韩文等
- **多种输入格式** - Markdown、Word、TXT 或直接粘贴文本

### 📦 安装

#### 方式1：下载 .skill 文件

1. 从 [Releases](https://github.com/YOUR_USERNAME/text-to-whiteboard/releases) 下载 `text-to-whiteboard-v2.skill`
2. 在 Claude Code 中运行：
   ```
   /skill install path/to/text-to-whiteboard-v2.skill
   ```

#### 方式2：手动安装

1. 克隆此仓库：
   ```bash
   git clone https://github.com/YOUR_USERNAME/text-to-whiteboard.git
   cd text-to-whiteboard
   ```

2. 复制到你的 Claude Code skills 目录：
   ```bash
   cp -r . ~/.claude/skills/text-to-whiteboard
   ```

### 🚀 快速开始

只需让 Claude 可视化你的内容：

```
用户: "把这篇文章做成白板"
用户: "将这个文档转为 Excalidraw"
用户: "用这个内容做一个知识图谱"
用户: "Visualize this process"
```

### 🎨 交互流程

创建白板时，Claude 会引导你：

**第一步：选择配色方案**
- **选项A**：浏览8种预设主题（打开预览页面）
- **选项B**：上传自定义配色（图片 / VI 文档）
- **选项C**：使用默认（加宁最爱）

**第二步：选择品牌露出**
- **选项A**：使用个人名字（输入名字）
- **选项B**：上传自定义品牌（logo / 颜色）
- **选项C**：跳过（无品牌）

### 📖 配色主题

| 主题 | 中文 | 适用场景 |
|------|------|----------|
| Jianing Fav | 加宁最爱 | 通用（默认）|
| Professional Blue | 专业蓝 | 商务、技术 |
| Finance Graph | 金融图表 | 数据分析 |
| Minimal Pitch | 极简路演 | 路演、产品发布 |
| Soft Pastel | 柔和粉彩 | 教育、教程 |
| Paper & Ink | 纸墨书香 | 文艺、读书笔记 |
| Vintage Editorial | 复古编辑 | 杂志风格 |
| Dark Mode | 深色模式 | 演示、正式场合 |

### 📊 支持的图表类型

- **流程图 & 步骤图** - 步骤、工作流、时间线
- **概念图** - 理论、分类、框架
- **对比图** - 优缺点、替代方案、前后对比
- **知识图谱** - 思维导图、概念网络

### 🛠️ 技术细节

- **输出格式：** `.excalidraw`（基于 JSON）
- **平台：** [excalidraw.com](https://excalidraw.com)
- **可编辑性：** 所有元素完全可编辑
- **分辨率：** 矢量格式，无限缩放
- **文件大小：** 通常 10-100KB

### 🤝 贡献

欢迎贡献：
- 报告 bug
- 提出新功能建议
- 添加新的配色主题
- 改进文档
- 提交 pull request

### 📝 许可证

MIT 许可证 - 可自由使用、修改和分发

---

## 📧 Contact | 联系方式

- GitHub Issues: [Submit an issue](https://github.com/YOUR_USERNAME/text-to-whiteboard/issues)
- Email: your.email@example.com

## 🙏 Acknowledgments | 致谢

Built with ❤️ using:
- [Claude Code](https://claude.ai/code)
- [Excalidraw](https://excalidraw.com)
- Python

---

**Star ⭐ this repo if you find it helpful! | 如果觉得有用，请给个星标 ⭐**