# 数据结构规范 (DATA_SCHEMA.md)

本文档定义 `static/data.json` 的数据结构，这是核心导航数据库。

## 1. 完整数据结构

```json
{
  "version": "1.0.0",
  "last_updated": "2024-01-01",
  "categories": [
    {
      "id": "campus-services",
      "name": "校园服务",
      "icon": "fa-school",
      "description": "校园生活相关服务",
      "subcategories": [
        {
          "id": "campus-admin",
          "name": "教务服务",
          "items": [
            {
              "id": "jwc",
              "name": "教务处",
              "url": "https://jwc.sspu.edu.cn",
              "description": "课程安排、成绩查询",
              "keywords": ["教务", "课程", "成绩", "选课"],
              "icon": null
            }
          ]
        }
      ]
    }
  ]
}
```

## 2. 字段说明

### 2.1 根对象
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `version` | string | 是 | 数据版本号 |
| `last_updated` | string | 是 | 最后更新日期 (YYYY-MM-DD) |
| `categories` | array | 是 | 分类列表 |

### 2.2 分类对象 (Category)
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 是 | 分类唯一标识 (用于 AI 匹配) |
| `name` | string | 是 | 分类显示名称 |
| `icon` | string | 否 | Font Awesome 图标类名 |
| `description` | string | 否 | 分类描述 |
| `subcategories` | array | 是 | 子分类列表 |

### 2.3 子分类对象 (Subcategory)
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 是 | 子分类唯一标识 |
| `name` | string | 是 | 子分类显示名称 |
| `items` | array | 是 | 网站项列表 |

### 2.4 网站项对象 (Item)
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 是 | 网站唯一标识 (用于 AI 匹配和高亮) |
| `name` | string | 是 | 网站名称 |
| `url` | string | 是 | 网站 URL |
| `description` | string | 否 | 网站描述 |
| `keywords` | array | 是 | 关键词列表 (用于 AI 搜索匹配) |
| `icon` | string | 否 | 自定义图标 URL (null 则自动获取 Favicon) |

## 3. 示例数据

```json
{
  "version": "1.0.0",
  "last_updated": "2024-01-15",
  "categories": [
    {
      "id": "campus-services",
      "name": "校园服务",
      "icon": "fa-school",
      "description": "校园生活相关服务",
      "subcategories": [
        {
          "id": "campus-admin",
          "name": "教务服务",
          "items": [
            {
              "id": "jwc",
              "name": "教务处",
              "url": "https://jwc.sspu.edu.cn",
              "description": "课程安排、成绩查询、选课退课",
              "keywords": ["教务", "课程", "成绩", "选课", "课表"],
              "icon": null
            },
            {
              "id": "library",
              "name": "图书馆",
              "url": "https://library.sspu.edu.cn",
              "description": "图书借阅、座位预约",
              "keywords": ["图书馆", "借书", "座位", "自习"],
              "icon": null
            },
            {
              "id": "card-center",
              "name": "一卡通中心",
              "url": "https://card.sspu.edu.cn",
              "description": "校园卡充值、挂失、查询",
              "keywords": ["一卡通", "校园卡", "充值", "挂失"],
              "icon": null
            }
          ]
        },
        {
          "id": "campus-life",
          "name": "生活服务",
          "items": [
            {
              "id": "dormitory",
              "name": "宿舍管理",
              "url": "https://dorm.sspu.edu.cn",
              "description": "宿舍报修、水电查询",
              "keywords": ["宿舍", "报修", "水电", "住宿"],
              "icon": null
            },
            {
              "id": "canteen",
              "name": "食堂服务",
              "url": "https://canteen.sspu.edu.cn",
              "description": "食堂菜单、营业时间",
              "keywords": ["食堂", "菜单", "吃饭"],
              "icon": null
            }
          ]
        }
      ]
    },
    {
      "id": "learning-platforms",
      "name": "学习平台",
      "icon": "fa-book",
      "description": "在线学习与课程平台",
      "subcategories": [
        {
          "id": "online-courses",
          "name": "在线课程",
          "items": [
            {
              "id": "mooc",
              "name": "中国大学MOOC",
              "url": "https://www.icourse163.org",
              "description": "国家级在线课程平台",
              "keywords": ["MOOC", "慕课", "在线课程", "学习"],
              "icon": null
            },
            {
              "id": "xuexitong",
              "name": "学习通",
              "url": "https://i.chaoxing.com",
              "description": "超星学习平台",
              "keywords": ["学习通", "超星", "网课", "作业"],
              "icon": null
            },
            {
              "id": "zhihuishu",
              "name": "智慧树",
              "url": "https://www.zhihuishu.com",
              "description": "知到网课平台",
              "keywords": ["智慧树", "知到", "网课"],
              "icon": null
            }
          ]
        },
        {
          "id": "language-learning",
          "name": "语言学习",
          "items": [
            {
              "id": "duolingo",
              "name": "多邻国",
              "url": "https://www.duolingo.cn",
              "description": "免费语言学习平台",
              "keywords": ["英语", "语言", "学习", "多邻国"],
              "icon": null
            },
            {
              "id": "baicizhan",
              "name": "百词斩",
              "url": "https://www.baicizhan.com",
              "description": "英语单词学习",
              "keywords": ["英语", "单词", "背单词", "百词斩"],
              "icon": null
            }
          ]
        }
      ]
    },
    {
      "id": "academic-resources",
      "name": "学术资源",
      "icon": "fa-graduation-cap",
      "description": "论文、文献与研究资源",
      "subcategories": [
        {
          "id": "paper-databases",
          "name": "论文数据库",
          "items": [
            {
              "id": "cnki",
              "name": "中国知网",
              "url": "https://www.cnki.net",
              "description": "中文学术文献数据库",
              "keywords": ["知网", "论文", "文献", "学术", "CNKI"],
              "icon": null
            },
            {
              "id": "wanfang",
              "name": "万方数据",
              "url": "https://www.wanfangdata.com.cn",
              "description": "学术文献数据库",
              "keywords": ["万方", "论文", "文献"],
              "icon": null
            },
            {
              "id": "google-scholar",
              "name": "Google Scholar",
              "url": "https://scholar.google.com",
              "description": "谷歌学术搜索",
              "keywords": ["谷歌学术", "论文", "学术", "Scholar"],
              "icon": null
            }
          ]
        },
        {
          "id": "academic-tools",
          "name": "学术工具",
          "items": [
            {
              "id": "zhihu",
              "name": "知乎",
              "url": "https://www.zhihu.com",
              "description": "知识问答社区",
              "keywords": ["知乎", "问答", "知识", "经验"],
              "icon": null
            },
            {
              "id": "deepl",
              "name": "DeepL",
              "url": "https://www.deepl.com",
              "description": "高质量翻译工具",
              "keywords": ["翻译", "DeepL", "英文"],
              "icon": null
            }
          ]
        }
      ]
    },
    {
      "id": "common-tools",
      "name": "常用工具",
      "icon": "fa-tools",
      "description": "日常实用工具",
      "subcategories": [
        {
          "id": "office-tools",
          "name": "办公工具",
          "items": [
            {
              "id": "notion",
              "name": "Notion",
              "url": "https://www.notion.so",
              "description": "笔记与协作工具",
              "keywords": ["笔记", "协作", "Notion", "文档"],
              "icon": null
            },
            {
              "id": "canva",
              "name": "Canva",
              "url": "https://www.canva.com",
              "description": "在线设计工具",
              "keywords": ["设计", "海报", "Canva", "图片"],
              "icon": null
            }
          ]
        },
        {
          "id": "dev-tools",
          "name": "开发工具",
          "items": [
            {
              "id": "github",
              "name": "GitHub",
              "url": "https://github.com",
              "description": "代码托管平台",
              "keywords": ["GitHub", "代码", "开源", "Git"],
              "icon": null
            },
            {
              "id": "stackoverflow",
              "name": "Stack Overflow",
              "url": "https://stackoverflow.com",
              "description": "程序员问答社区",
              "keywords": ["Stack Overflow", "编程", "问答", "代码"],
              "icon": null
            }
          ]
        }
      ]
    }
  ]
}
```

## 4. ID 命名规范

- **分类 ID**: 使用小写字母和连字符，如 `campus-services`
- **子分类 ID**: 使用小写字母和连字符，如 `campus-admin`
- **网站项 ID**: 使用简短的小写字母或数字，如 `jwc`、`cnki`

## 5. 关键词规范

- 每个网站项应包含 3-5 个关键词
- 关键词应覆盖用户可能的搜索词
- 包括：网站名称、核心功能、常见别名
- 用于 AI 意图识别和匹配

## 6. 数据更新流程

1. 编辑 `static/data.json` 文件
2. 更新 `last_updated` 字段
3. 如有结构变更，更新 `version` 字段
4. 前端刷新页面即可获取最新数据
