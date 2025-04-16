import requests
from bllonfig.Config import bConfig

@bConfig()
def get_phonological_features(config):
    url = "https://api.siliconflow.cn/v1/uploads/audio/voice"

    token = config['siliconflow']['token']

    payload = "-----011000010111000001101001\r\n \
        Content-Disposition: form-data; name=\"audio\"\r\n\r\ndata:audio/mpeg;base64,aGVsbG93b3JsZA==\r\n\
        -----011000010111000001101001\r\n\
        Content-Disposition: form-data; name=\"model\"\r\n\r\nFunAudioLLM/CosyVoice2-0.5B\r\n\
        -----011000010111000001101001\r\n\
        Content-Disposition: form-data; name=\"customName\"\r\n\r\nyour-voice-name\r\n\
        -----011000010111000001101001\r\n\
        Content-Disposition: form-data; name=\"text\"\r\n\r\n在一无所知中, 梦里的一天结束了，一个新的轮回便会开始\r\n\
        -----011000010111000001101001--\r\n\r\n"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "multipart/form-data"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response.text)

if __name__ == '__main__':
    get_phonological_features()