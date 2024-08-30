from http.server import HTTPServer, SimpleHTTPRequestHandler  
import os  
  
PORT = 8000  
  
# 指定你想要分享的目录  
os.chdir(r'C:\Users\bllos\Desktop\太平石化合同')  # 修改为你的实际目录路径  
  
# 创建一个HTTP服务器，监听在PORT端口  
Handler = SimpleHTTPRequestHandler  
httpd = HTTPServer(('', PORT), Handler)  
  
print(f"serving at port {PORT}...")  
httpd.serve_forever()