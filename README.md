# 二工大 AI 轻导航

> AI驱动的个性化导航起始页，为上海第二工业大学师生打造高度可定制、信息层级清晰的学习导航体验。

> 💡 **注意**：本项目由 AI 制作，作者仅在不断测试与优化。

## 🎯 核心特性

- 🤖 **AI 智能导航** - 自然语言查询，智谱 GLM-4.5-Air 智能匹配资源
- 🎨 **自适应布局** - 响应式网格设计，完美适配各种屏幕
- 🛠️ **高度定制化** - 添加自定义链接、生成 AI 壁纸、自定义快捷键
- 💾 **本地数据持久化** - LocalStorage 保存设置，无需登录
- ⌨️ **快捷键支持** - 数字键快速访问、键盘导航
- 🎭 **毛玻璃效果** - 现代美学设计

## 🚀 快速开始

### 前置要求
- Python 3.11+
- [智谱 AI API Key](https://open.bigmodel.cn/)

### 安装步骤

```bash
# 1. 进入项目目录
cd "ai-xuexitong - final"

# 2. 创建虚拟环境
python -m venv venv
venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置 .env 文件
# 创建 .env 并添加：
# ZHIPU_API_KEY=your_api_key_here
# FLASK_SECRET_KEY=your_flask_secret_key

# 5. 运行应用
python app.py
```

打开浏览器访问 `http://localhost:5000`

## 📁 项目结构

```
├── app.py                  # Flask 后端
├── requirements.txt        # 依赖列表
├── static/
│   ├── data.json          # 导航数据
│   └── images/            # 壁纸和图标
├── templates/
│   └── index.html         # 前端页面
└── .env                   # 环境配置
```

## 🔧 技术栈

- **后端**：Python + Flask + 智谱 AI
- **前端**：原生 JavaScript + Tailwind CSS + Font Awesome
- **存储**：LocalStorage + 本地文件

## 💡 主要功能

1. **AI 智能导航** - 自然语言查询，自动高亮匹配资源
2. **自定义导航** - 添加/删除链接，自动获取图标
3. **壁纸管理** - 上传本地或 AI 生成个性化壁纸
4. **快捷键** - 数字键快速访问、键盘操作
5. **设置面板** - 搜索引擎配置、快捷键设置

## 📚 更多文档

- [产品需求文档](PRD.md)
- [技术栈说明](TECH_STACK.md)
- [后端结构](BACKEND_STRUCTURE.md)
- [数据模型](DATA_SCHEMA.md)

---
