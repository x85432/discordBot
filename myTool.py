from datetime import datetime, timedelta
import pytz

# Few-shot prompt 建立
def get_prompt_for_todo(text: str) -> str:
    tz = pytz.timezone('Asia/Taipei')
    now = datetime.now(tz)
    next_wed = now + timedelta(days=((2 - now.weekday() + 7) % 7 or 7))
    next_wed = next_wed.strftime('%Y-%m-%d')
    tomorrow = (now + timedelta(days=1)).strftime('%Y-%m-%d')
    today_2pm = now.replace(hour=14, minute=30, second=0, microsecond=0).strftime('%Y-%m-%d %H:%M')
    current_time = now.strftime('%Y-%m-%d %H:%M:%S')

    prompt = f"""
你現在是時間與事件的格式標準化助理。請將輸入的句子轉換為 JSON 陣列，格式如下：

[
  {{"title": "事件內容", "start_date": null 或 yyyy-mm-ddTHH:mm, "due_date": null 或 yyyy-mm-ddTHH:mm, "description": "備註"}}
]

已知現在時間是 {current_time}。

一些範例：
- 「下禮拜三考C++期末考」 → 考C++期末考: {next_wed}
- 「明天交線性代數作業，打大資盃12/18」 → 交線性代數作業: {tomorrow}, 打大資盃: 2024-12-18
- 「今天下午2點30分要跟同學聚餐」 → 跟同學聚餐: {today_2pm}
- 沒有時間的就標註為 null → 「把數學作業寫完」 → due_date: null
- 看不懂或無法對應 → 「今朝有酒今朝醉」 → 說明「沒有特定時間」

請幫我分析：
{text}
"""
    return prompt

# 將 Gemini 回傳的 JSON 從文字中擷取出來
def extract_json_from_text(text: str) -> str:
    import re, json
    match = re.search(r'\[[\s\S]*?\]', text)
    if match:
        try:
            return json.dumps(json.loads(match.group(0)), ensure_ascii=False, indent=2)
        except Exception:
            return f"⚠️ 解析失敗：\n```\n{text}\n```"
    return f"⚠️ 沒找到合法 JSON 區段：\n```\n{text}\n```"
