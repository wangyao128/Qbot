import json
import os
import re

from openai import OpenAI
from openai.types.chat.chat_completion import Choice
import pandas as pd


class QwenAPI:
  def __init__(self):
    self.api_key = "sk-17ff6bd821ae4220be6ec72cefb4a7e9"
    self.base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1" # 填写DashScope服务的base_url
    self.client = OpenAI(
              base_url=self.base_url,
              api_key= self.api_key,
            )

  def chat(self,messages: list,prompt_tokens) -> str:
    completion = self.client.chat.completions.create(
      model="qwen-max-latest",  # 此处以qwen-plus为例，可按需更换模型名称。模型列表：https://help.aliyun.com/zh/model-studio/getting-started/models
      messages=messages,
      stream=True,
      temperature=0.3,
      extra_body={
        "enable_search": True,
        "search_options":{
            "forced_search": True,
            "search_strategy": "pro"}
      }
    )
    full_content = ""
    for chunk in completion:
      if chunk.choices:
        full_content += chunk.choices[0].delta.content
        print(chunk.choices[0].delta.content)
    print("大模型完整输出:",full_content)
    # choice = completion.choices[0]
    # print(completion.model_dump_json())
    return full_content


  def  messagesAssemble(self,content:dict) -> list:
    jsoncontent = ("请使用如下 JSON 格式输出你的回复："
                      +   ' { '
                      + '  "domain_name": "热点领域概念名称",'
                      + ' "hotspot_reson": "热点理由",'
                      + '  "market_performance": "市场表现",'
                      + '  "driving_factor": "驱动因素",'
                      + '  "core_stock": "核心股票 （核心股票不少于5个，并以JSON对象展示，包括股票代码，股票名称，是否推荐买入，推荐买入价格，推荐买入理由）"'
                      + '  }'
                      + '  核心股票以如下json格式输入：'
                      + '   {'
                      + '  "code": "证券代码",'
                      + '  "code_name": "证券名称"，'
                      + '  "recommend_type":"是否推荐买入",'
                      + ' "recommend_price":"推荐价格", '
                      + ' "recommend_reason":"推荐理由" '
                      + '                    }  ')
    messages = [
      {"role": "system", "content": "你是一名专业的股票分析师，擅长分析中国A股市场行情"},
      {"role": "user",
       "content": "请结合" + content["date"] + "的行情与市场新闻，分析出" + content["date"]
                  + "中国A股股票市场的前十大热点领域，按领域热度从高到低排序，输出格式为JSON格式的字符串，包含以下字段："
                  + "1.热点领域概念名称"
                  + "2.热点理由"
                  + "3.市场表现"
                  + "4.驱动因素"
                  + "5.核心股票 （核心股票不少于5个，并以JSON对象展示，包括股票代码，股票名称）"
                  + jsoncontent}
    ]
    print("大模型输入提示词：",messages)
    return messages

  def recommendHotspotData2DB(self,content:dict):
    #### 同步指定日期的热点领域股票数据入数据库 ####
    try:
      messages  = self.messagesAssemble(content)
      result = self.chat(messages,prompt_tokens=0)
      # json_str  = result.message.content.strip()
      json_str  = self.remove_json_chars(result)
      print("前后多余字符，生成标准json字符串的结果：", json_str)
      # print("大模型的输出结果：",json_str)
      # 将json转换为dataframe
      data = json.loads(json_str)
      df = pd.json_normalize(data)
      print(df)
    except Exception as e:
      print(f"同步指定日期的热点领域股票数据入数据库失败: {str(e)}")
      return e
      # return f"同步指定日期的热点领域股票数据入数据库失败: {str(e)}"

  def remove_json_chars(self,text):
    # 去掉开头到 [ 和结尾到 ] 的内容
    start_index = text.find('[')
    end_index = text.rfind(']')
    if start_index != -1 and end_index != -1:
      return text[start_index - 1:end_index+1]
    return text




if __name__ == "__main__":
    qwenAPI = QwenAPI()
    # messages = [
    #   {'role': 'system', 'content': 'You are a helpful assistant.'},
    #   {'role': 'user', 'content': '中国队在巴黎奥运会获得了多少枚金牌'}]
    # messages  = qwenAPI.messagesAssemble({"date":"2025-06-05"})
    # result = qwenAPI.chat(messages,0)
    # print(result.model_dump_json())
    # print("大模型的输出结果：",result.message.content)
    # print("\n大模型的输出结果(按行输出)：\n")
    # # 将JSON数据转换为字符串，并按行输出
    # json_str = json.dumps(result.message.content, ensure_ascii=False, indent=4)
    # for line in json_str.splitlines():
    #   print(line)
    content = {"date":"2025-06-05"}
    # print(content['date'])
    qwenAPI.recommendHotspotData2DB(content)

