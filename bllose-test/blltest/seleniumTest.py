#coding=utf8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#1.创建Chrome浏览器对象，这会在电脑上在打开一个浏览器窗口
browser = webdriver.Chrome()
 
#通过浏览器向服务器发送URL请求
browser.get("http://baidu.com")