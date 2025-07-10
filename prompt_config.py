# prompt_config.py

# 使用者狀態 (建議由主程式載入並管理)
user_topic = {}

# 語氣樣板
topic_prompts = {
    "台語": """
User: 你會說台語嗎？
AI: 我會啊，你欲講啥？
User: 今天天氣如何？
AI: 今仔日攏無落雨，感覺真舒適。
""",
    "英文": """
User: Do you speak English?
AI: Sure! How can I help you today?
User: What's the weather like?
AI: It's sunny and calm today. Perfect for a walk!
""",
    "默認": ""  # 無引導
}
