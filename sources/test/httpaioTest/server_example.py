from aiohttp import web
from rich import inspect
from rich.console import Console
import requests


console = Console()

async def handle(request):
    message = request.message
    inspect(message)
    
    url = message.url
    headers = message.raw_headers
    hDict = {}
    for index in range(len(headers)):
        hDict[headers[index][0].decode()] = headers[index][1].decode()
    console.print('headers ->')
    console.print_json(data=hDict)

    type = message.method
    if 'GET' == type:
        response = requests.get(url=url, headers=message.headers)
    elif 'POST' == type:
        response = requests.post(url=url, headers=message.headers, data=message.compression)
    console.print(str(response))

    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)




app = web.Application()
app.add_routes([web.get('/', handle),
                web.get('/{name}', handle),
                web.post('/{root}/{path1}/{path2}/{path3}', handle),
                web.post('/{root}/{path1}/{path2}', handle)])

if __name__ == '__main__':
    web.run_app(app)