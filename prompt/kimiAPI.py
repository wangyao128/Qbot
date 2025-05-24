# 对接kimi实现联网搜索大模型对话的代码
# 1. 准备工作
# 注册账号并获取API Key：访问Kimi API官网进行注册，并在“开发者中心”获取API Key。
# 安装必要的库：如果你使用Python进行调用，需要安装requests库或openai库。
# 3. 代码说明
# search_impl 函数：这是一个占位函数，用于模拟联网搜索工具的调用。在实际使用中，你可以根据需要替换为自己的搜索逻辑。
# chat 函数：用于发送消息给Kimi API并接收回复。通过tools参数声明了$web_search工具，Kimi会根据需要调用联网搜索。
# 主逻辑：在主逻辑中，程序会循环处理Kimi的回复，直到finish_reason为stop，表示聊天结束。
# 4. 注意事项
# 联网搜索功能可能会产生额外的费用，具体费用根据模型大小和使用的Tokens计算。
# 如果需要流式输出结果，可以在调用chat.completions.create时设置stream=True。
# 通过上述步骤，你可以成功调用Kimi的API并获得联网思考的结果。
import os
import json

import requests
from openai import OpenAI

# 初始化 Moonshot AI 客户端
api_key = "sk-5R32geupE2I8bWtN2MEITa4HERTX8A91fFlp292zTZd1mHrk"  # 替换为你的API Key
client = OpenAI(
  base_url="https://api.moonshot.cn/v1",
  api_key="sk-5R32geupE2I8bWtN2MEITa4HERTX8A91fFlp292zTZd1mHrk",  # 替换为你的API Key
)

# 定义调用Kimi API,计算 Token的函数
def call_kimi_api(messages):
    url = "https://api.moonshot.cn/v1/tokenizers/estimate-token-count"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    data = {
        "model": "moonshot-v1-128k",
        "messages": messages,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result['choices'][0]['message']['content']
    else:
        raise Exception(f"Error calling API: {response.text}")



# 定义联网搜索工具的占位函数
def search_impl(arguments: dict) -> dict:
  """
  在使用 Moonshot AI 提供的联网搜索工具时，只需原封不动地返回参数即可。
  """
  return arguments


# 定义聊天函数
def chat(messages: list,prompt_tokens) -> dict:
  """
  发送消息给 Moonshot AI 的 API 并获取回复。
  """
  completion = client.chat.completions.create(
    model="moonshot-v1-128k",  # 使用的模型名称
    messages=messages,  # 发送的消息列表
    temperature=0.3,  # 控制回复的随机性
    max_tokens=128*1024-prompt_tokens,  # 控制回复的长度
    tools=[  # 定义可以使用的工具
      {
        "type": "builtin_function",
        "function": {"name": "$web_search"},
      }
    ],
  )
  return completion.choices[0]


# 主逻辑
def main():
  messages = [
    {"role": "system", "content": "你是一名专业的股票分析师，擅长分析中国A股市场"},
    {"role": "user",
     "content": "请结合" + "2025年5月20日" + "的行情与市场新闻，分析出" + "2025年5月20日" + "中国A股股票市场的前十大热点领域，按领域热度从高到低排序，输出格式为JSON格式的字符串，包含以下字段："
                + "1.热点领域概念名称"
                + "2.热点理由"
                + "3.市场表现"
                + "4.驱动因素"
                + "5.核心股票 （核心股票不少于5个，并以JSON对象展示，包括股票代码，股票名称）"}
  ]
  prompt_tokens = call_kimi_api(messages)
  print(prompt_tokens)
  finish_reason = None
  while finish_reason is None or finish_reason == "tool_calls":
    choice = chat(messages,prompt_tokens)
    finish_reason = choice.finish_reason
    if finish_reason == "tool_calls":
      messages.append(choice.message)
      for tool_call in choice.message.tool_calls:
        tool_call_name = tool_call.function.name
        tool_call_arguments = json.loads(tool_call.function.arguments)
        if tool_call_name == "$web_search":
          tool_result = search_impl(tool_call_arguments)
        else:
          tool_result = f"Error: unable to find tool by name '{tool_call_name}'"
        messages.append({
          "role": "tool",
          "tool_call_id": tool_call.id,
          "name": tool_call_name,
          "content": json.dumps(tool_result),
        })
  print(finish_reason) # 输出结束原因
  print(choice.message.content)  # 输出最终结果


if __name__ == "__main__":
  main()
