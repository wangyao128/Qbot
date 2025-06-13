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
import json
from typing import Dict, Any



from prompt.data2mysql.DatabaseManager import DatabaseManager
import pandas as pd
import requests
from openai import OpenAI
from openai.types.chat.chat_completion import Choice
from datetime import datetime


class KimiAPI:

  def __init__(self):
    # 初始化 Moonshot AI 客户端
    self.api_key = "sk-5R32geupE2I8bWtN2MEITa4HERTX8A91fFlp292zTZd1mHrk"  # 替换为你的API Key
    self.client = OpenAI(
              base_url="https://api.moonshot.cn/v1",
              api_key= self.api_key,  # 替换为你的API Key
            )

  # 定义调用Kimi API,计算 Token的函数
  def call_kimi_api(self,messages):
    url = "https://api.moonshot.cn/v1/tokenizers/estimate-token-count"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {self.api_key}'
    }
    data = {
        "model": "moonshot-v1-128k",#"moonshot-v1-128k",
        "messages": messages,
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        result = response.json()
        return result['data']['total_tokens']
    else:
        raise Exception(f"Error calling API: {response.text}")



# 定义联网搜索工具的占位函数
  def search_impl(self,arguments: Dict[str, Any]) -> Any:
    """
    在使用 Moonshot AI 提供的联网搜索工具时，只需原封不动地返回参数即可。
    """
    return arguments


  # 定义聊天函数
  def chat(self,messages: list,prompt_tokens) -> Choice:
    """
    发送消息给 Moonshot AI 的 API 并获取回复。
    """
    completion = self.client.chat.completions.create(
      model="moonshot-v1-128k",  # 使用的模型名称
      messages=messages,  # 发送的消息列表
      temperature=0.3,  # 控制回复的随机性
      max_tokens=8192,
      # max_tokens=128*1024-prompt_tokens,  # 控制回复的长度
      response_format = {"type": "json_object"}, # 指定回复的格式
      tools=[  # 定义可以使用的工具
          {
            "type": "builtin_function",
            "function": {"name": "$web_search"},
          }
        ],
      )
    usage = completion.usage
    choice = completion.choices[0]
    # =========================================================================
    # 通过判断 finish_reason = stop，我们将完成联网搜索流程后，消耗的 Tokens 打印出来
    if choice.finish_reason == "stop":
      print(f"消耗的 Tokens:")
      print(f"chat_prompt_tokens:          {usage.prompt_tokens}")
      print(f"chat_completion_tokens:      {usage.completion_tokens}")
      print(f"chat_total_tokens:           {usage.total_tokens}")
    # =========================================================================
    return choice

  def messagesAssemble(self,content:dict):
    jsoncontent = ("输出JSON格式："
                   + ' { '
                   + '"domain_name": "热点领域概念名称",'
                   + '"hotspot_reson": "热点理由",'
                   + '"market_performance": "市场表现",'
                   + '"driving_factor": "驱动因素",'
                   + '"core_stock": "核心股票 （核心股票不少于5个，并以JSON对象展示，包括股票代码，股票名称，是否推荐买入，推荐买入价格，推荐买入理由）"'
                   + '}'
                   + '核心股票JSON格式：'
                   + '{'
                   + '"code": "证券代码(例如:sh.600030 或者 sz.301187)",'
                   + '"code_name": "证券名称"，'
                   + '"recommend_type":"是否推荐买入",'
                   + '"recommend_price":"推荐价格", '
                   + '"recommend_reason":"推荐理由"'
                   + '}')

    messages = [
      {"role": "system", "content": "你是一名专业的股票分析师，擅长分析中国A股市场行情"},
      {"role": "user",
       "content": "请结合" + content['date'] + "的行情与市场新闻，分析出" + content['date'] + "中国A股股票市场的前十大热点领域，按领域热度从高到低排序，输出格式为JSON格式的字符串，包含以下字段："
                  + "1.热点领域概念名称"
                  + "2.热点理由"
                  + "3.市场表现"
                  + "4.驱动因素"
                  + "5.核心股票（核心股票不少于5个，并以JSON对象展示，包括股票代码，股票名称）"
                  + jsoncontent
       }
    ]
    print(f"送给kimi提问的提示词：{messages}\n")
    return messages

  def getKimistockAnalysis(self,content:dict):
    #获取指定日期 kimi的股票热点分析数据
    messages = self.messagesAssemble(content)
    prompt_tokens = self.call_kimi_api(messages)
    print(f"送给kimi提问的提示词token数：{prompt_tokens}\n")
    finish_reason = None
    while finish_reason is None or finish_reason == "tool_calls":
      choice = self.chat(messages, prompt_tokens)
      finish_reason = choice.finish_reason
      if finish_reason == "tool_calls":
        messages.append(choice.message)
        for tool_call in choice.message.tool_calls:
          tool_call_name = tool_call.function.name
          tool_call_arguments = json.loads(tool_call.function.arguments)
          if tool_call_name == "$web_search":
            tool_result = self.search_impl(tool_call_arguments)
          else:
            tool_result = f"Error: unable to find tool by name '{tool_call_name}'"
          # 使用函数执行结果构造一个 role=tool 的 message，以此来向模型展示工具调用的结果；
          # 注意，我们需要在 message 中提供 tool_call_id 和 name 字段，以便 Kimi 大模型
          # 能正确匹配到对应的 tool_call。
          messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": tool_call_name,
            "content": json.dumps(tool_result),
          })
    # print(finish_reason)  # 输出结束原因
    # print(choice.message.content)  # 输出最终结果
    return choice.message.content

  def syncKimistockAnalysis2DB(self,json_str,content:dict):
    #同步热点领域股票数据入数据库 包含 json数据转换与数据库写入
    #将json数据转换成dataframe
    print("json数据:",json_str)
    data = json.loads(json_str)

    photspot,pstock =self.process_nested_json(data,content)
    db_manager = DatabaseManager()
    exception_occurred = False
    try :
      # 创建数据库管理器实例

      engine_ts = db_manager.connect()
      # print("将热点领域数据写入数据库：",photspot.to_string())
      db_manager.delete_data("hotstockinfo", "hot_date = '" + content['date'] + "'")
      db_manager.insert_data("hotstockinfo",photspot)
      # print("将热点领域对应的股票数据写入数据库：",pstock.to_string())
      #处理热点领域推荐的核心股票，增加hotstockinfo_id 列并赋值，使其可以与hotstockinfo表关联
      domain_id = db_manager.read_data(f"select id,domain_name from hotstockinfo where hot_date = '" + content['date'] + "'")
      for index, row in domain_id.iterrows():
        pstock.loc[pstock['domain_name'] == row['domain_name'], 'hotstockinfo_id'] = row['id']
      # db_manager.bulk_delete_from_dataframe(pstock, "hotcorestock", ["hotstockinfo_id"])
      db_manager.insert_data("hotcorestock",pstock)


    # df = pd.json_normalize(json_str)
    except   Exception as e:
      print(f"同步热点领域股票数据失败: {e}")
      exception_occurred = True
    finally:
      db_manager.disconnect()
      if exception_occurred:
        return False
      else:
        return True

  # def process_pstock(self,data:pd.DataFrame):
  #   #处理热点领域推荐的核心股票，增加hotstockinfo_id 列并赋值，使其可以与hotstockinfo表关联
  #   data

  def process_nested_json(self,data,content:dict):
    #  处理嵌套的JSON数据
    dfhotspot = pd.DataFrame()
    dfstock = pd.DataFrame()
    if isinstance(data, dict):
      for key, value in data.items():
        if isinstance(value, dict):
          new_row = {
            "hot_date": content['date'],
            "domain_name": value["domain_name"],
            "hotspot_reson": value["hotspot_reson"],
            "market_performance": value["market_performance"],
            "driving_factors": value["driving_factor"],
            "create_time": datetime.now()
          }
          dfhotspot = pd.concat([dfhotspot, pd.DataFrame([new_row])], ignore_index=True)
          if isinstance(value["core_stock"],dict):
            for key,stock in value["core_stock"].items():
              new_row = {
                "domain_name": value['domain_name'],
                "code": stock["code"],
                "code_name": stock["code_name"],
                "recommend_type": stock["recommend_type"],
                "recommend_price": stock["recommend_price"],
                "recommend_reason": stock["recommend_reason"],
                "create_time": datetime.now()
             }
              dfstock = pd.concat([dfstock, pd.DataFrame([new_row])], ignore_index=True)
          elif isinstance(value["core_stock"],list):
            for stock in value["core_stock"]:
              new_row = {
                "domain_name": value['domain_name'],
                "code": stock["code"],
                "code_name": stock["code_name"],
                "recommend_type": stock["recommend_type"],
                "recommend_price": stock["recommend_price"],
                "recommend_reason": stock["recommend_reason"],
                "create_time": datetime.now()
              }
              dfstock = pd.concat([dfstock, pd.DataFrame([new_row])], ignore_index=True)
        elif isinstance(value, list):
          for item in value:
            if isinstance(item, dict):
              new_row = {
                "hot_date": content['date'],
                "domain_name": item["domain_name"],
                "hotspot_reson": item["hotspot_reson"],
                "market_performance": item["market_performance"],
                "driving_factors": item["driving_factor"],
                "create_time": datetime.now()
              }
              dfhotspot = pd.concat([dfhotspot, pd.DataFrame([new_row])], ignore_index=True)
              if isinstance(item["core_stock"], dict):
                for key, stock in item["core_stock"].items():
                  new_row = {
                      "domain_name": value['domain_name'],
                      "code": stock["code"],
                      "code_name": stock["code_name"],
                      "recommend_type": stock["recommend_type"],
                      "recommend_price": stock["recommend_price"],
                      "recommend_reason": stock["recommend_reason"],
                      "create_time": datetime.now()
                      }
                  dfstock = pd.concat([dfstock, pd.DataFrame([new_row])], ignore_index=True)
              elif isinstance(item["core_stock"], list):
                for stock in item["core_stock"]:
                  new_row = {
                      "domain_name": item['domain_name'],
                      "code": stock["code"],
                      "code_name": stock["code_name"],
                      "recommend_type": stock["recommend_type"],
                      "recommend_price": stock["recommend_price"],
                      "recommend_reason": stock["recommend_reason"],
                      "create_time": datetime.now()
                      }
                  dfstock = pd.concat([dfstock, pd.DataFrame([new_row])], ignore_index=True)
    else:
      print(f"kimi大模型返回的json格式不正确，请重试。Value: {data}")
    return dfhotspot,dfstock
  # 主逻辑
# def main():
#   kimiapi = KimiAPI()
#
#   content = {"date": "2025-06-09","role":"专业的股票分析师"}
#   messages = kimiapi.messagesAssemble(content)
#   prompt_tokens = kimiapi.call_kimi_api(messages)
#   print(f"1.送给kimi提问的提示词token数：{prompt_tokens}")
#   finish_reason = None
#   while finish_reason is None or finish_reason == "tool_calls":
#     choice = kimiapi.chat(messages,prompt_tokens)
#     finish_reason = choice.finish_reason
#     if finish_reason == "tool_calls":
#       messages.append(choice.message)
#       for tool_call in choice.message.tool_calls:
#         tool_call_name = tool_call.function.name
#         tool_call_arguments = json.loads(tool_call.function.arguments)
#         if tool_call_name == "$web_search":
#           tool_result = kimiapi.search_impl(tool_call_arguments)
#         else:
#           tool_result = f"Error: unable to find tool by name '{tool_call_name}'"
#         # 使用函数执行结果构造一个 role=tool 的 message，以此来向模型展示工具调用的结果；
#         # 注意，我们需要在 message 中提供 tool_call_id 和 name 字段，以便 Kimi 大模型
#         # 能正确匹配到对应的 tool_call。
#         messages.append({
#           "role": "tool",
#           "tool_call_id": tool_call.id,
#           "name": tool_call_name,
#           "content": json.dumps(tool_result),
#         })
#   print(finish_reason) # 输出结束原因
#   print(choice.message.content)  # 输出最终结果

if __name__ == "__main__":
    kimiAPI = KimiAPI()
    content = {"date": "2025-06-13", "role": "专业的股票分析师","sync_time":"16：00"}
    json_str = kimiAPI.getKimistockAnalysis(content)
    FLG = kimiAPI.syncKimistockAnalysis2DB(json_str,content)
    print(FLG)
    # 每天下午 四点钟同步会比较好
    # data = json.loads(json_str)
    # df = pd.json_normalize(json_str)
    # print(data)
