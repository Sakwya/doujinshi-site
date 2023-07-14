import requests
import random
from urllib.parse import unquote


# python (version<=3.9)
requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':HIGH:!DH:!aNULL'
headers = {
    'Accept-Language': 'zh-CN,zh;q=0.9,ja;q=0.8,en;q=0.7,zh-TW;q=0.6',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/86.0.4240.75 Mobile Safari/537.36'
}
cookies = {
    'localesuggested': 'true',
    'locale': 'zh-cn',
    'adultchecked': '1',


    'MELONBOOKS_CHECK_NEWS' :'1',
    'MELONBOOKS_CHECK_NEWS_SP':'1',
    'MELONBOOKS_CHECK_SHOP':'1',
    'MELONBOOKS_CS_CHECK_NEWS':'1',
    'COAG_MELONBOOKS':'2',
    'AUTH_ADULT':'1',

    'fsfew':'0',
    'cexists':'0',
    'csfew':'0',
}

def request(url, cache = 1):
    if cache == 0:
        print("获取",end="...")
        try:
            html = requests.get(url, headers=headers, cookies=cookies).content
            print("成功")
        except requests.exceptions.SSLError:
            print("失败")
            return request(url)
        return html.decode("utf-8")

    with open("index.info", 'r+', encoding="utf-8") as f:
        lines = f.readlines()
        if url + '\n' in lines:
            f.close()
            filename = lines[lines.index(url + '\n') + 1][0:-1]
            with open("cache\\" + filename, 'rb') as file:
                html = file.read()
                file.close()
        else:
            print("获取",end="...")
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
                print("成功")
            except requests.exceptions.SSLError:
                print("失败")
                return request(url)
            with open("cache\\" + filename, 'xb') as file:
                file.write(html)
                file.close()
            f.write(url + '\n' + filename + '\n')
            f.close()
            print("写入cache")
        return html.decode("utf-8")

