import requests
import os
from dotenv import load_dotenv

load_dotenv()  # 加载 .env 文件
api_key = os.getenv("NotionAPIKey")  
database_id = os.getenv("NotionDatabaseID")  

headers = {
    "Authorization": f"Bearer {api_key}",  # 添加 Bearer 前缀
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def get_database_properties():
    """获取数据库的属性"""
    url = f"https://api.notion.com/v1/databases/{database_id}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()["properties"]
    else:
        print(f"获取数据库属性失败，状态码：{response.status_code}, 错误信息：{response.text}")
        return None

def create_notion_page(data, properties):
    """将数据插入到 Notion 数据库中"""
    create_url = "https://api.notion.com/v1/pages"

    new_page_data = {
        "parent": {"database_id": database_id},
        "properties": {}
    }

    for prop_name, prop_schema in properties.items():
        if prop_schema["type"] == "title":
            new_page_data["properties"][prop_name] = {
                "title": [
                    {
                        "text": {
                            "content": data.get("Title", "")  # 假设 "Title" 对应 title 属性
                        }
                    }
                ]
            }
        elif prop_schema["type"] == "rich_text":
            new_page_data["properties"][prop_name] = {
                "rich_text": [
                    {
                        "text": {
                            "content": data.get("Content", "")  # 假设 "Content" 对应 rich_text 属性
                        }
                    }
                ]
            }
        elif prop_schema["type"] == "select":
            new_page_data["properties"][prop_name] = {
                "select": {
                    "name": data.get("Type", "")  # 假设 "Type" 对应 select 属性
                }
            }
        elif prop_schema["type"] == "date":
            # 处理日期类型，假设你有一个 `Date` 字段在 `data` 中
            new_page_data["properties"][prop_name] = {
                "date": {
                    "start": data.get("Date", "")  # 假设 "Date" 对应日期属性，格式为 "YYYY-MM-DD"
                }
            }
        else:
            print(f"不支持的属性类型：{prop_schema['type']}")

    response = requests.post(create_url, headers=headers, json=new_page_data)

    if response.status_code == 200:
        print("页面创建成功")
    else:
        print(f"页面创建失败，状态码：{response.status_code}, 错误信息：{response.text}")

def Notion_upload(calendar_datas):
    properties = get_database_properties()

    # 遍历 JSON 数据并创建 Notion 页面
    if properties:
        for item in calendar_datas["data"]:
            create_notion_page(item, properties)

    print("all pages created successfully")