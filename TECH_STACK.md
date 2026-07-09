# 技术栈规范

## 1. 后端
- **框架**：Python 3.11 + Flask
- **核心依赖**：
  - `flask>=3.0.0`: Web 框架
  - `zhipuai>=2.0.0`: 智谱 AI SDK
  - `python-dotenv>=1.0.0`: 环境变量管理
  - `flask-cors>=4.0.0`: 处理跨域（如果前后端分离开发）
  - `werkzeug>=3.0.0`: 文件上传处理

## 2. 前端
- **架构**：单页应用 (SPA)
- **布局**: CSS Grid (用于自适应网格) + Flexbox (用于组件内部)。
- **HTML**: HTML5
- **CSS**:
  - Tailwind CSS (via CDN 用于快速布局，自定义 CSS 处理特殊动画)
  - 原生 CSS (用于特定动画：抖动、上浮、毛玻璃效果)
- **JS**:
  - 原生 JavaScript (Vanilla JS)
  - 无需引入 React/Vue 等框架，保持轻量。
- **图标库**: Font Awesome 6.0 (CDN)

## 3. 数据存储
- **静态数据**: `/static/data.json`
  - 存储所有预置的导航分类、链接信息。
- **用户上传文件**: 
  - `/static/images/wallpapers/`: 存放用户上传的壁纸
  - `/static/images/icons/`: 存放用户自定义图标（可选）
- **用户数据**: LocalStorage
  - `user_settings`: 用户设置数据
    ```json
    {
      "show_tags_area": true,
      "enabled_engines": ["baidu", "bing", "google", "ai"],
      "hotkeys_enabled": true,
      "wallpaper_url": "/static/images/wallpapers/xxx.jpg"
    }
    ```
  - `user_dock`: 用户自定义的 Dock 图标
    ```json
    [
      {
        "id": "unique-id-1",
        "name": "网站名称",
        "url": "https://example.com",
        "icon": "https://... 或 emoji 或 首字母",
        "icon_type": "favicon|emoji|letter",
        "added_at": 1234567890
      }
    ]
    ```
  - `user_nav_items`: 用户添加到中部导航区的图标
    ```json
    [
      {
        "id": "unique-id-2",
        "name": "网站名称",
        "url": "https://example.com",
        "icon": "...",
        "icon_type": "favicon|emoji|letter",
        "category": "校园服务",
        "added_at": 1234567890
      }
    ]
    ```

## 4. API 集成
- **智谱 AI API**:
  - SDK: `zai-sdk` (智谱 AI 官方 SDK)
  - 对话模型: `glm-4.5-air` (GLM-4.5 Air)
  - 图像生成: `cogview-3-plus` (壁纸生成)
  - 认证: API Key (存储在后端 `.env` 文件中，切勿暴露在前端)

## 5. 环境变量 (.env)
```env
ZHIPU_API_KEY=your_api_key_here
FLASK_SECRET_KEY=your_flask_secret_key
UPLOAD_FOLDER=static/images/wallpapers
MAX_CONTENT_LENGTH=5242880
```
