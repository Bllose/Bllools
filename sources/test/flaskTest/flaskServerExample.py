from flask import Flask, request, make_response
import requests
from rich.console import Console
import gzip
import zlib

app = Flask(__name__)
console = Console()

@app.route('/')
@app.route('/<path:path>', methods=['GET', 'POST'])
def query_example():
    url = request.url
    type = request.method
    headers = {h[0]: h[1] for h in request.headers}

    console.print(type + ' -> '+ url)
    console.print_json(data=headers)

    if type == 'GET':
        response = requests.get(url=url, headers=headers)
    elif type == 'POST':
        data = request.data
        response = requests.post(url=url, headers=headers, data= data)
    return response_maker(response)


@app.route('/static/bootstrap/css/bootstrap.min.css', methods=['GET'])
@app.route('/static/style.css', methods=['GET'])
@app.route('/static/jquery/jquery.min.js', methods=['GET'])
@app.route('/static/bootstrap/js/bootstrap.min.js', methods=['GET'])
def static_request_handler():
    url = request.url
    headers = {h[0]: h[1] for h in request.headers}
    console.print('资源加载 -> '+ url)
    console.print_json(data=headers)
    response = requests.get(url=url, headers=headers)
    
    return response_maker(response)


def response_maker(response):
    if 'Content-Encoding' in response.headers:
        encoding = response.headers['Content-Encoding'].lower()
        if encoding == 'gzip':
            content = gzip.compress(response.content)
        elif encoding == 'deflate':
            content = zlib.compress(response.content)
        else:
            content = response.content
    else:
        content = response.content

    flask_response = make_response(content)
    flask_response.status_code = response.status_code
    for key, value in response.headers.items():
        flask_response.headers[key] = value
    return flask_response

if __name__ == '__main__':
    app.run(debug=True)