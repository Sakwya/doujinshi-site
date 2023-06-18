import requests
import random

headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/86.0.4240.75 Mobile Safari/537.36'
}


def request(url):
    with open("history\\index.txt", 'r+') as f:
        lines = f.readlines()
        if url + '\n' in lines:
            print("读取")
            f.close()
            filename = lines[lines.index(url + '\n') + 1][0:-1]
            with open("history\\" + filename, 'rb') as file:
                html = file.read()
                file.close()
        else:
            print("读取")
            filename = url[url.rindex('/') + 1:]
            while filename + '\n' in lines:
                filename = filename + str(random.randint(0, 9))
            try:
                html = requests.get(url, headers=headers).content
            except requests.exceptions.SSLError:
                return request(url)
            with open("history\\" + filename, 'xb') as file:
                file.write(html)
                file.close()
            f.write(url + '\n' + filename + '\n')
            f.close()
            print("写入")
        return html.decode("utf-8")
