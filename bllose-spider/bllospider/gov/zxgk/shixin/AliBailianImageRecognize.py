import os
import json
import base64
import requests
from datetime import datetime
class AliBailianImageService:
    def __init__(self, configuration):
         self.configuration = configuration
    def get_api_key(self):
         # 根据环境变量决定从哪里读取 API Key
        dev_environment_variable = os.getenv("ENVIRONMENT")
        is_development = not dev_environment_variable or dev_environment_variable.lower() == "development"
        if is_development:
             # 开发环境从配置中读取
             api_key = self.configuration.get("DASHSCOPE_API_KEY")
        else:
             # 生产环境从环境变量读取
             api_key = os.getenv("DASHSCOPE_API_KEY")
        # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key = "sk-xxx"
        if not api_key:
             print("API Key 未设置。请确保环境变量 'DASHSCOPE_API_KEY' 已设置。")
             return None
        return api_key
    def get_image_base64_string_and_save(self, image_url):
        response = requests.get(image_url)
        if response.status_code != 200:
             raise Exception(f"Failed to download image: {response.status_code}")
        image_data = response.content
        encoded_image = base64.b64encode(image_data).decode('utf-8')
        # 可选步骤：保存图片到文件
         # filename = f"{uuid.uuid4()}.jpg"
         # with open(filename, 'wb') as f:
         #     f.write(image_data)
        return encoded_image
    def send_post_request(self, url, json_content, api_key):
        headers = {
             "Authorization": f"Bearer {api_key}",
             "Content-Type": "application/json",
             "Accept": "application/json"
        }
        response = requests.post(url, data=json_content, headers=headers)
        response_body = response.text
        self.write_response_to_log(response_body)
        if response.status_code >= 200 and response.status_code < 300:
            return response_body
        else:
            return f"请求失败: {response.status_code}"
    def write_response_to_log(self, response_body):
        log_file_path = "Logs/response.log"
        log_dir = os.path.dirname(log_file_path)
        if not os.path.exists(log_dir):
             os.makedirs(log_dir)
        with open(log_file_path, 'a') as f:
             f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Response Body: {response_body}\n")
    def get_results(self, image_base64_string):
        api_key = self.get_api_key()
        if not api_key or not image_base64_string.strip():
             return None

        url = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions"
        json_content = {
             "model": "qwen2-vl-7b-instruct",
             "messages": [
                 {
                     "role": "user",
                     "content": [
                         {"type": "text", "text": "请对这张图片进行OCR识别，并输出最准确的验证码，直接输出识别出的结果字符，不要输出其他内容。"},
                         {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{image_base64_string}"}}
                     ]
                 }
             ]
         }
        json_content_str = json.dumps(json_content)
        result = self.send_post_request(url, json_content_str, api_key)
        print(result)
        return result

    def get_image_base64_string(self, image_path):
        with open(image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_string


def recognize_text_from_image(image_path, image_base64_string) -> str:
    captcha = None
    config = {
         "DASHSCOPE_API_KEY": "sk-ef6de807f9474434aae7d8efaa9d6ad9"
    }
    service = AliBailianImageService(config)
    if not image_base64_string:
        image_base64_string = service.get_image_base64_string(image_path)
    resultStr = service.get_results(image_base64_string)
    if resultStr:
        result = json.loads(resultStr)
        choices = result['choices']
        captcha = choices[0]['message']['content']
        print("Result:", result)
    return captcha

if __name__ == "__main__":
     # 示例配置
    config = {
         "DASHSCOPE_API_KEY": "sk-ef6de807f9474434aae7d8efaa9d6ad9"
    }
    service = AliBailianImageService(config)
    result = service.get_results(service.get_image_base64_string(r'captcha.jpg'))
    if result:
        choices = result['choices']
        captcha = choices[0]['message']['content']
        print("Result:", result)
    # service = AliBailianImageService(None)
    # print(service.get_image_base64_string(r'captcha.jpg'))