import pytesseract
from PIL import Image

# 设置Tesseract OCR引擎的路径（根据实际情况修改）
pytesseract.pytesseract.tesseract_cmd = r'D:\Program Files\Tesseract-OCR\tesseract.exe'

def recognize_text_from_image(image_path):
    try:
        # 打开图片
        image = Image.open(image_path)
        # 使用pytesseract进行文字识别
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"发生错误: {e}")
        return None

# 替换为你的图片路径
image_path = r'D:\workplace\github\Bllools\captcha.jpg'
result = recognize_text_from_image(image_path)
if result:
    print("识别结果:")
    print(result)
    