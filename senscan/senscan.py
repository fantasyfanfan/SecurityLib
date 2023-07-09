from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from bs4 import BeautifulSoup
import urllib.parse
import requests
import re

# 替换为Firefox浏览器的实际路径和你的GeckoDriver的实际路径
firefox_path = 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'  
geckodriver_path = 'C:\\Program Files\\geckodriver.exe'

# 网站url
url = 'https://www.example.com'

# 设置 Firefox 选项
options = Options()
options.binary_location = firefox_path

# 设定 GeckoDriver 服务
service = Service(executable_path=geckodriver_path)

# 正则表达式
regexes = {
    'IP地址': r"(?<![0-9.])((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9])\.(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9]?[0-9]))(?![0-9.])",
    '邮箱': r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
    #'手机号': r"^1[3-9]\d{9}$",#不准确

}

# 启动 Selenium，获取动态生成的 HTML
driver = webdriver.Firefox(service=service, options=options)
driver.get(url)

# 使用 BeautifulSoup 解析 HTML
soup = BeautifulSoup(driver.page_source, 'html.parser')

# 查找所有的 <script> 标签，只要有 src 属性即可
scripts = soup.find_all('script', attrs={'src': True})

# 提取 JS 文件的 url
js_files = [script['src'] for script in scripts]

# 对于相对 URL，使用 urllib.parse.urljoin 进行解析
js_files = [urllib.parse.urljoin(url, js_file) for js_file in js_files]

# 打印所有 JS 文件的 URL 并检查是否包含敏感信息
for js_file in js_files:
    print("Checking file: ", js_file)
    
    # 下载JS文件
    response = requests.get(js_file)
    
    if response.status_code == 200:
        js_content = response.text
        # 使用正则表达式查找匹配项
        for name, regex in regexes.items():
            matches = re.finditer(regex, js_content)
            for match in matches:
                print(f"Sensitive information found ({name}): ", match.group())

# 关闭 Selenium
driver.quit()
