import os
import json
import uuid
import re
import threading
from datetime import datetime
from urllib.parse import urlparse
from flask import Flask, render_template, request, jsonify, send_from_directory, Response
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import requests
from zai import ZhipuAiClient

load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_CONTENT_LENGTH', 5242880))
app.config['UPLOAD_FOLDER'] = os.getenv('UPLOAD_FOLDER', 'static/images/wallpapers')
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

DATA_FILE = 'static/data.json'

zhipu_client = None
try:
    zhipu_client = ZhipuAiClient(api_key=os.getenv('ZHIPU_API_KEY'))
except Exception as e:
    print(f"Warning: Failed to initialize Zhipu AI client: {e}")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"version": "1.0.0", "last_updated": datetime.now().strftime("%Y-%m-%d"), "categories": []}

def build_system_prompt(data):
    all_items = []
    
    for category in data.get('categories', []):
        cat_name = category.get('name', '')
        
        for subcategory in category.get('subcategories', []):
            subcat_name = subcategory.get('name', '')
            for item in subcategory.get('items', []):
                item_info = {
                    'id': item.get('id', ''),
                    'name': item.get('name', ''),
                    'description': item.get('description', ''),
                    'keywords': item.get('keywords', []),
                    'category': cat_name,
                    'subcategory': subcat_name
                }
                all_items.append(item_info)
    
    items_desc = "\n".join([
        f"- {item['name']} (id: {item['id']}, keywords: {', '.join(item['keywords'])})"
        for item in all_items
    ])
    
    return f"""你是一个导航助手，帮助用户快速找到有用的网站和资源。用户可以询问和导航相关的问题，你的工作是推荐相关的网站。

## 可用资源库：
{items_desc}

## 响应格式要求：
必须返回JSON格式，包含以下字段：
1. "response": 你的回答文本（友好、简洁）
2. "recommended_items": 推荐的网站ID列表（数组，最多5个，ID必须存在于上述资源库中）

示例：
{{"response": "根据你的需求，我推荐以下资源...", "recommended_items": ["id1", "id2", "id3"]}}

## 规则：
- 如果用户需求与某些资源匹配，在recommended_items中返回对应的ID
- 如果没有完全匹配，推荐最相关的3-5个资源
- 如果无法推荐任何资源，返回空数组 []
- 只返回有效的JSON，不要有其他内容
- 回答保持简洁，100字以内"""

def parse_ai_response(content):
    try:
        json_match = re.search(r'\{[\s\S]*\}', content)
        if json_match:
            parsed = json.loads(json_match.group())
            return parsed
        return {
            "response": content,
            "recommended_items": []
        }
    except json.JSONDecodeError:
        return {
            "response": content,
            "recommended_items": []
        }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/data')
def get_data():
    data = load_data()
    return jsonify(data)

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        if zhipu_client is None:
            return jsonify({
                "success": False,
                "response": "AI 服务未配置，请检查 API Key 设置。",
                "recommended_items": [],
                "error": "AI_NOT_CONFIGURED"
            }), 500
        
        data = request.get_json()
        messages = data.get('messages', [])
        
        if not messages:
            return jsonify({
                "success": False,
                "response": "请提供问题",
                "recommended_items": []
            }), 400
        
        nav_data = load_data()
        system_prompt = build_system_prompt(nav_data)
        
        # 构建消息列表
        api_messages = [{"role": "system", "content": system_prompt}]
        
        # 添加用户消息
        for msg in messages:
            api_messages.append({
                "role": msg.get('role', 'user'),
                "content": msg.get('content', '')
            })
        
        # 调用AI API
        response = zhipu_client.chat.completions.create(
            model="glm-4.5-air",
            messages=api_messages,
            max_tokens=1024,
            temperature=0.6
        )
        
        ai_content = response.choices[0].message.content
        result = parse_ai_response(ai_content)
        result['success'] = True
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "response": "AI 服务暂时不可用，请稍后重试。",
            "recommended_items": [],
            "error": str(e)
        }), 500

@app.route('/api/wallpaper/upload', methods=['POST'])
def upload_wallpaper():
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "error": "没有上传文件", "code": "INVALID_REQUEST"}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({"success": False, "error": "没有选择文件", "code": "INVALID_REQUEST"}), 400
        
        if not allowed_file(file.filename):
            return jsonify({"success": False, "error": "文件格式不支持，仅支持 jpg, png, webp", "code": "INVALID_FILE_TYPE"}), 400
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        random_str = uuid.uuid4().hex[:8]
        ext = file.filename.rsplit('.', 1)[1].lower()
        filename = f"{timestamp}_{random_str}.{ext}"
        
        upload_folder = app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)
        
        filepath = os.path.join(upload_folder, filename)
        file.save(filepath)
        
        return jsonify({
            "success": True,
            "url": f"/static/images/wallpapers/{filename}"
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e), "code": "INTERNAL_ERROR"}), 500

@app.route('/api/wallpaper/generate', methods=['POST'])
def generate_wallpaper():
    try:
        if zhipu_client is None:
            return jsonify({"success": False, "error": "AI 服务未配置，请检查 API Key 设置。", "code": "AI_ERROR"}), 500
        
        data = request.get_json()
        prompt = data.get('prompt', '')
        style = data.get('style', 'anime')
        
        style_prompts = {
            'anime': '动漫风格，色彩鲜艳，线条清晰，适合作为桌面壁纸',
            'realistic': '写实风格，照片级真实感，高清细节，适合作为桌面壁纸',
            'abstract': '抽象艺术风格，几何图形和色块，现代感强，适合作为桌面壁纸',
            'landscape': '自然风景，山川湖泊，唯美意境，适合作为桌面壁纸',
            'minimal': '极简主义风格，简洁线条，留白优雅，适合作为桌面壁纸'
        }
        
        full_prompt = f"{style_prompts.get(style, style_prompts['anime'])}，{prompt}"
        
        response = zhipu_client.images.generations(
            model="glm-image",
            prompt=full_prompt
        )
        
        if response.data and len(response.data) > 0:
            image_url = response.data[0].url
            
            img_response = requests.get(image_url)
            if img_response.status_code == 200:
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                random_str = uuid.uuid4().hex[:8]
                filename = f"generated_{timestamp}_{random_str}.png"
                
                upload_folder = app.config['UPLOAD_FOLDER']
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                
                filepath = os.path.join(upload_folder, filename)
                with open(filepath, 'wb') as f:
                    f.write(img_response.content)
                
                return jsonify({
                    "success": True,
                    "url": f"/static/images/wallpapers/{filename}"
                })
        
        return jsonify({"success": False, "error": "图片生成失败", "code": "AI_ERROR"}), 500
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e), "code": "AI_ERROR"}), 500

@app.route('/api/fetch_title')
def fetch_title():
    try:
        url = request.args.get('url', '')
        
        if not url:
            return jsonify({"success": False, "error": "URL 参数缺失", "code": "INVALID_REQUEST"}), 400
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        # 正确处理编码
        response.encoding = response.apparent_encoding or 'utf-8'
        
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', response.text, re.IGNORECASE)
        
        if title_match:
            title = title_match.group(1).strip()
            return jsonify({"success": True, "title": title})
        
        return jsonify({"success": False, "error": "无法获取网页标题", "code": "NETWORK_ERROR"}), 404
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e), "code": "NETWORK_ERROR"}), 500

# ── 图标获取配置 ──────────────────────────────────────────
FAVICON_TIMEOUT = 8
FAVICON_CACHE_DIR = os.path.join('static', 'images', 'icons')
FAVICON_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}


def _fetch_favicon_data(domain):
    """尝试多种方式获取 favicon 字节数据，优先直连，再用中国可用第三方 API"""
    # 方法1：HTTPS / HTTP 直接获取 /favicon.ico
    for scheme in ('https', 'http'):
        try:
            resp = requests.get(f'{scheme}://{domain}/favicon.ico',
                                headers=FAVICON_HEADERS, timeout=FAVICON_TIMEOUT)
            if resp.status_code == 200 and len(resp.content) > 100:
                ct = resp.headers.get('content-type', '')
                if any(t in ct for t in ('image', 'icon', 'octet-stream')) or ct == '':
                    return resp.content
        except Exception:
            pass

    # 方法2：解析首页 HTML 查找 <link rel="icon"> 标签
    for scheme in ('https', 'http'):
        try:
            resp = requests.get(f'{scheme}://{domain}',
                                headers=FAVICON_HEADERS, timeout=FAVICON_TIMEOUT)
            if resp.status_code == 200:
                icon_match = re.search(
                    r'<link[^>]*rel=["\'](?:shortcut\s+)?icon["\'][^>]*href=["\']([^"\']+)["\']',
                    resp.text, re.IGNORECASE
                )
                if not icon_match:
                    icon_match = re.search(
                        r'<link[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\'](?:shortcut\s+)?icon["\']',
                        resp.text, re.IGNORECASE
                    )
                if icon_match:
                    href = icon_match.group(1)
                    if href.startswith('//'):
                        href = 'https:' + href
                    elif href.startswith('/'):
                        href = f'{scheme}://{domain}{href}'
                    elif not href.startswith('http'):
                        href = f'{scheme}://{domain}/{href}'
                    icon_resp = requests.get(href, headers=FAVICON_HEADERS,
                                             timeout=FAVICON_TIMEOUT)
                    if icon_resp.status_code == 200 and len(icon_resp.content) > 100:
                        return icon_resp.content
            break  # HTTPS 能连通则不再尝试 HTTP
        except Exception:
            continue

    # 方法3：中国可访问的第三方 favicon API（直连失败时兜底）
    for api_url in (
        f'https://api.iowen.cn/favicon/{domain}.png',
        f'https://favicon.yandex.net/favicon/{domain}',
        f'https://icon.horse/icon/{domain}',
    ):
        try:
            resp = requests.get(api_url, headers=FAVICON_HEADERS, timeout=FAVICON_TIMEOUT)
            if resp.status_code == 200 and len(resp.content) > 200:
                return resp.content
        except Exception:
            pass

    return None


@app.route('/api/favicon')
def proxy_favicon():
    """代理获取网站 favicon，优先从服务器缓存返回，找不到时返回 404"""
    try:
        domain = request.args.get('domain', '')
        if not domain:
            return '', 404

        if domain.startswith(('http://', 'https://')):
            domain = urlparse(domain).netloc

        os.makedirs(FAVICON_CACHE_DIR, exist_ok=True)
        safe_name = domain.replace(':', '_').replace('/', '_')
        cache_path = os.path.join(FAVICON_CACHE_DIR, f'{safe_name}.png')

        # 优先返回服务器缓存
        if os.path.exists(cache_path):
            return send_from_directory(os.path.abspath(FAVICON_CACHE_DIR),
                                       f'{safe_name}.png')

        favicon_data = _fetch_favicon_data(domain)
        if favicon_data:
            with open(cache_path, 'wb') as f:
                f.write(favicon_data)
            return Response(favicon_data, mimetype='image/png')

        return '', 404

    except Exception:
        return '', 404


@app.route('/api/fetch_favicon')
def fetch_favicon():
    try:
        url = request.args.get('url', '')
        
        if not url:
            return jsonify({"success": False, "error": "URL 参数缺失", "code": "INVALID_REQUEST"}), 400
        
        from urllib.parse import urlparse
        parsed = urlparse(url if url.startswith(('http://', 'https://')) else 'https://' + url)
        domain = parsed.netloc
        
        favicon_url = f"/api/favicon?domain={domain}"
        
        return jsonify({
            "success": True,
            "favicon_url": favicon_url
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e), "code": "NETWORK_ERROR"}), 500

@app.route('/api/wallpaper/list')
def list_wallpapers():
    try:
        upload_folder = app.config['UPLOAD_FOLDER']
        if not os.path.exists(upload_folder):
            return jsonify({"success": True, "wallpapers": []})
        
        wallpapers = []
        for filename in os.listdir(upload_folder):
            if allowed_file(filename):
                wallpapers.append({
                    "url": f"/static/images/wallpapers/{filename}",
                    "name": filename
                })
        
        return jsonify({"success": True, "wallpapers": wallpapers})
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e), "code": "INTERNAL_ERROR"}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


def prefetch_all_icons():
    """启动时后台预获取 data.json 中所有网站的图标并缓存到服务器"""
    import time
    time.sleep(5)  # 等待 Flask 完全就绪
    os.makedirs(FAVICON_CACHE_DIR, exist_ok=True)
    data = load_data()
    for category in data.get('categories', []):
        for subcategory in category.get('subcategories', []):
            for item in subcategory.get('items', []):
                url = item.get('url', '')
                if not url:
                    continue
                try:
                    parsed = urlparse(url if url.startswith('http') else 'https://' + url)
                    domain = parsed.netloc
                    if not domain:
                        continue
                    safe_name = domain.replace(':', '_').replace('/', '_')
                    cache_path = os.path.join(FAVICON_CACHE_DIR, f'{safe_name}.png')
                    if os.path.exists(cache_path):
                        continue
                    favicon_data = _fetch_favicon_data(domain)
                    if favicon_data:
                        with open(cache_path, 'wb') as f:
                            f.write(favicon_data)
                        print(f'[Icon] 已缓存: {domain}')
                    else:
                        print(f'[Icon] 未找到: {domain}')
                    time.sleep(0.5)  # 避免请求过快
                except Exception as e:
                    print(f'[Icon] 出错 {url}: {e}')


# 启动后台线程，服务器就绪后自动预获取所有图标
threading.Thread(target=prefetch_all_icons, daemon=True).start()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
