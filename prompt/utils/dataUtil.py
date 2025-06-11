
def process_nested_json(data):
  """递归解析多层嵌套的JSON数据"""
  if isinstance(data, dict):
    for key, value in data.items():
      process_nested_json(value)
  elif isinstance(data, list):
    for item in data:
      process_nested_json(item)
  else:
    print(f"Value: {data}")
