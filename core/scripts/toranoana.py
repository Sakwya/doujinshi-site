import os.path
from core.scripts import request
from bs4 import BeautifulSoup
import requests


def get_info_from_toranoana(page):
    page = str(page)
    url = "https://ecs.toranoana.jp/tora/ec/app/catalog/list?commodityListCode=toracottoppush_u" \
          "&catalogListSortType=1&commodity_kind_name=%E5%90%8C%E4%BA%BA%E8%AA%8C&currentPage=" + page
    html = request(url, 0)
    print("获取第" + page + "页文档成功")
    document = BeautifulSoup(html, "html.parser")

    posts = document.select(".product-list-img")
    urls = []
    for post in posts:
        if post.select('a') is None:
            break
        urls.append("https://ecs.toranoana.jp" + post.select('a')[0]['href'])
        if len(urls) == 50:
            break

    documents = []
    for i in range(len(urls)):
        html = request(urls[i])
        documents.append(BeautifulSoup(html, "html.parser"))
        print("获取内容[%d/%d]" % (i + 1, len(urls)))

    f = open("toranoana.info", mode="r+", encoding="utf-8")
    lines = f.readlines()
    for i in range(len(urls)):
        document = documents[i]
        print("抓取数据[%d/%d]" % (i + 1, len(urls)))
        try:
            name = document.find(class_='product-detail-desc-title').text.replace('\n', ' ').strip()
            author = document.find_all(class_="sub-p")
            if len(author) > 2:
                author = author[0]
            else:
                author = author[1]
            author_name = author.text.replace('\n', ' ').strip()
            author_url = author.find("a")['href']
            outlines = document.select(".product-detail-spec-table > tbody > tr")
            tags = document.select(".pc > .product-detail-tag > a")
        except AttributeError:
            print("失败")
            continue
        tag_list = []
        for tag in tags:
            tag_list.append(tag.text[1:])

        pic = document.select("#preview > a > img")
        if len(pic) == 0:
            print(pic)
        else:
            pic = pic[0]['src']

        picture = pic
        img_name = picture.split('/')[-1].replace('-1p', '')
        if len(img_name.split('.')) < 2:
            img_name = "melonbooks_cover_" + img_name + ".jpg"
        if os.path.exists("cover\\" + img_name):
            pass
        else:
            img_file = requests.get(picture).content
            with open("cover\\" + img_name, 'wb') as file:
                file.write(img_file)
            print("图片下载完成[%d/%d]" % (i + 1, len(urls)))
        info_dic = {
            "标题": name,
            "网址": urls[i],
            "作者": author_name,
            "作者网址": "https://ecs.toranoana.jp" + author_url,
            "封面": img_name,
            "标签": tag_list
        }
        for outline in outlines:
            if outline.text.split():
                info_pair = outline.text.split(maxsplit=1)
                info = info_pair[1].replace('\u3000', ' ').replace('入荷アラートを設定', '')
                while '\r' in info:
                    info = info.replace('\r', '')
                while '  ' in info:
                    info = info.replace('  ', ' ')
                while ' \n' in info:
                    info = info.replace(' \n', '\n')
                while '\n ' in info:
                    info = info.replace('\n ', '\n')
                while '\n\n' in info:
                    info = info.replace('\n\n', '\n')
                if info[-1] == '\n':
                    info = info[:-1]
                info = info.split('\n')
                if len(info) == 1:
                    info = info[0]
                info_dic.update({info_pair[0]: info})

        print("成功")
        line = str(info_dic) + '\n'
        if line not in lines:
            print("写入",end='...')
            f.write(line)
            print("完成")
    f.close()


# get_info_from_toranoana(1)
# get_info_from_toranoana(2)
# get_info_from_toranoana(3)
# get_info_from_toranoana(4)