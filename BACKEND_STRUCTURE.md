# 后端结构文档

## 1. 项目目录树
```
/project_root
  /static
    /images
      /wallpapers (存放用户上传的壁纸)
      /icons (存放用户自定义图标，可选)
    data.json (核心导航数据库)
  /templates
    index.html
  app.py
  requirements.txt
  .env (存储 API Key 和配置)
```

## 2. API 端点定义

### `GET /`
- 描述: 渲染主页 index.html。

### `GET /api/data`
- 描述: 获取导航数据 (data.json)。
- 响应体:
  ```json
  {
    "categories": [...]
  }
  ```

### `POST /api/chat`
- 描述: 处理 AI 对话请求。
- 请求体:
  ```json
  {
    "message": "我想找论文网站",
    "context": [] // 可选，历史对话
  }
  ```
- 响应体:
  ```json
  {
    "type": "action|text",
    "action": {
      "type": "highlight|open_category",
      "ids": ["id1", "id2"],  // highlight 时使用
      "target": "学术资源"     // open_category 时使用
    },
    "text": "为您找到了以下资源...",  // text 类型时使用
    "need_confirm": false
  }
  ```

### `POST /api/wallpaper/upload`
- 描述: 上传自定义壁纸。
- 请求体: `multipart/form-data`
  - `file`: 图片文件 (jpg, png, webp)
- 响应体:
  ```json
  {
    "success": true,
    "url": "/static/images/wallpapers/xxx.jpg"
  }
  ```
- 错误响应:
  ```json
  {
    "success": false,
    "error": "文件格式不支持"
  }
  ```

### `POST /api/wallpaper/generate`
- 描述: AI 生成壁纸。
- 请求体:
  ```json
  {
    "prompt": "赛博朋克风格的校园",
    "style": "anime" // "anime" | "realistic" | "abstract"
  }
  ```
- 响应体:
  ```json
  {
    "success": true,
    "url": "/static/images/wallpapers/generated_xxx.jpg"
  }
  ```

### `GET /api/fetch_title`
- 描述: 用户添加链接时，自动获取网页标题。
- 参数: `?url=http://example.com`
- 响应:
  ```json
  {
    "success": true,
    "title": "Example Domain"
  }
  ```
- 错误响应:
  ```json
  {
    "success": false,
    "error": "无法获取网页标题"
  }
  ```

### `GET /api/fetch_favicon`
- 描述: 获取网站 Favicon。
- 参数: `?url=http://example.com`
- 响应:
  ```json
  {
    "success": true,
    "favicon_url": "https://www.google.com/s2/favicons?domain=example.com"
  }
  ```

## 3. AI 响应格式规范

### 3.1 响应类型

#### 高亮类型 (highlight)
当 AI 匹配到已有资源时返回：
```json
{
  "type": "action",
  "action": {
    "type": "highlight",
    "ids": ["zhihu", "google-scholar"]
  },
  "text": "为您找到了以下相关资源：",
  "need_confirm": false
}
```

#### 打开分类类型 (open_category)
当 AI 建议打开某个分类时返回：
```json
{
  "type": "action",
  "action": {
    "type": "open_category",
    "target": "学术资源"
  },
  "text": "建议您查看学术资源分类",
  "need_confirm": true
}
```

#### 纯文本类型 (text)
当 AI 无法匹配资源，返回纯文本回答：
```json
{
  "type": "text",
  "text": "抱歉，没有找到相关资源。您可以尝试...",
  "need_confirm": false
}
```

### 3.2 AI System Prompt
```
你是一个导航助手，帮助用户找到他们需要的网站或资源。
你的职责是：
1. 识别用户的意图，判断他们想找什么类型的网站或资源
2. 如果用户想找的资源在已有数据中存在，返回 highlight 动作
3. 如果用户想找的资源可能在某个分类中，返回 open_category 动作
4. 如果无法匹配，返回友好的文本提示

响应格式必须是 JSON：
- type: "action" 或 "text"
- action: 仅当 type 为 "action" 时存在
  - type: "highlight" 或 "open_category"
  - ids: 高亮时匹配的图标 ID 列表
  - target: 打开分类时的分类名称
- text: 给用户的提示文本
- need_confirm: 是否需要用户确认

保持回答简洁，不要过度解释。
```

## 4. 错误响应格式

所有 API 在发生错误时统一返回：
```json
{
  "success": false,
  "error": "错误描述信息",
  "code": "ERROR_CODE"
}
```

### 错误码定义
| 错误码 | 描述 |
|--------|------|
| `INVALID_REQUEST` | 请求参数无效 |
| `FILE_TOO_LARGE` | 上传文件超过限制 |
| `INVALID_FILE_TYPE` | 文件类型不支持 |
| `AI_ERROR` | AI 服务调用失败 |
| `NETWORK_ERROR` | 网络请求失败 |
| `INTERNAL_ERROR` | 服务器内部错误 |

## 5. 文件上传限制
- 最大文件大小: 5MB
- 支持的图片格式: jpg, jpeg, png, webp
- 壁纸存储路径: `/static/images/wallpapers/`
- 文件命名规则: `{timestamp}_{random_string}.{ext}`

## 6. 后端核心模块

### 6.1 app.py 结构
```python
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os

# 加载环境变量
load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB
app.config['UPLOAD_FOLDER'] = 'static/images/wallpapers'

# 路由定义
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    # 返回 data.json
    pass

@app.route('/api/chat', methods=['POST'])
def chat():
    # 处理 AI 对话
    pass

@app.route('/api/wallpaper/upload', methods=['POST'])
def upload_wallpaper():
    # 处理壁纸上传
    pass

@app.route('/api/wallpaper/generate', methods=['POST'])
def generate_wallpaper():
    # AI 生成壁纸
    pass

@app.route('/api/fetch_title')
def fetch_title():
    # 获取网页标题
    pass

if __name__ == '__main__':
    app.run(debug=True)
```

### 6.2 AI 服务模块
```python
from zhipuai import ZhipuAI

def get_ai_response(message, context=None, data=None):
    """
    调用智谱 AI 获取响应
    
    Args:
        message: 用户消息
        context: 历史对话上下文
        data: 导航数据（用于构建 system prompt）
    
    Returns:
        dict: AI 响应结果
    """
    client = ZhipuAI(api_key=os.getenv('ZHIPU_API_KEY'))
    
    # 构建包含导航数据的 system prompt
    system_prompt = build_system_prompt(data)
    
    response = client.chat.completions.create(
        model="glm-4-plus",
        messages=[
            {"role": "system", "content": system_prompt},
            *context if context else [],
            {"role": "user", "content": message}
        ]
    )
    
    return parse_ai_response(response.choices[0].message.content)
```
