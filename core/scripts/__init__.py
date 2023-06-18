import requests
import random
from urllib.parse import unquote

headers = {
    'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7,zh-TW;q=0.6',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/86.0.4240.75 Mobile Safari/537.36'
}
cookies = {
    'localesuggested': 'true',
    'locale': 'zh-cn',
    'adultchecked': '1'
}


def request(url):
    with open("index.info", 'r+', encoding="utf-8") as f:
        lines = f.readlines()
        if url + '\n' in lines:
            print("读取")
            f.close()
            filename = lines[lines.index(url + '\n') + 1][0:-1]
            with open("cache\\" + filename, 'rb') as file:
                html = file.read()
                file.close()
        else:
            print("读取")
            if url.split('.')[-1] == 'html':
                filename = url[url.rindex('/') + 1:]
            else:
                filename = url[url.index('/') + 2:]
                filename = filename.replace('/', ' ').replace('\\', ' ').replace('|', ' ').replace('*', ' ').replace(
                    '?', ' ').replace(':', ' ').replace('"', ' ').replace('<', ' ').replace('>', ' ')[:100]
            while filename + '\n' in lines:
                filename = filename + str(random.randint(0, 9))
            try:
                html = requests.get(url, headers=headers, cookies=cookies).content
            except requests.exceptions.SSLError:
                return request(url)
            with open("cache\\" + filename, 'xb') as file:
                file.write(html)
                file.close()
            f.write(url + '\n' + filename + '\n')
            f.close()
            print("写入")
        return html.decode("utf-8")
