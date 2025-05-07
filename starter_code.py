import dashscope
from dashscope import Generation

dashscope.base_http_api_url = 'https://dashscope-intl.aliyuncs.com/api/v1'
dashscope.api_key = 'Your API Key!'

response = Generation.call(
    model='qwen-max',
    prompt='What is the capital of France?'
)

print("🤖 Response: ", response.output.text)