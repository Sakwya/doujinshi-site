import os.path

import requests

from request import request
from bs4 import BeautifulSoup


def get_info_from_dlsite(page):
    page = str(page)
    url = "https://www.dlsite.com/maniax/fsr/=/language/jp/sex_category%5B0%5D/male/ana_flg/all/age_category%5B0%5D" \
          "/general/work_category%5B0%5D/doujin/order%5B0%5D/trend/work_type_category%5B0%5D/comic/work_type_category" \
          "%5B1%5D/illust/work_type_category%5B2%5D/novel/work_type_category_name%5B0%5D/%E6%BC%AB%E7%94%BB" \
          "/work_type_category_name%5B1%5D/CG%E3%83%BB%E6%8F%92%E7%94%BB/work_type_category_name%5B2%5D/%E5%B0%8F%E8" \
          "%AF%B4/options_and_or/and/options%5B0%5D/JPN/options%5B1%5D/CHI/options%5B2%5D/NM/per_page/30/page/" + \
          page + "/show_type/3/lang_options%5B0%5D/%E6%97%A5%E6%96%87/lang_options%5B1%5D/%E4%B8%AD%E6%96%87" \
                 "/lang_options%5B2%5D/%E4%B8%8D%E9%99%90%E8%AF%AD%E7%A7%8D"
    html = request(url)
    print("获取第" + page + "页文档成功")
    document = BeautifulSoup(html, "html.parser")

    posts = document.select(".work_img_main")
    urls = []
    for post in posts:
        urls.append(post.select('a')[0]['href'])

    documents = []
    for i in range(len(urls)):
        html = request(urls[i])
        documents.append(BeautifulSoup(html, "html.parser"))
        print("获取内容[%d/%d]" % (i + 1, len(urls)))

    f = open("dlsite.info", mode="r+", encoding="utf-8")
    lines = f.readlines()
    for i in range(len(urls)):
        name = documents[i].find(id='work_name').text
        brand = documents[i].find(class_="maker_name").text.replace('\n', ' ')
        outlines = documents[i].find(id="work_outline").children
        picture = "http:" + documents[i].select("li>picture>img")[0]['srcset']
        img_name = picture[picture.rindex('/') + 1:]
        if os.path.exists("cover\\" + img_name):
            pass
        else:
            img_file = requests.get(picture).content
            with open("cover\\" + img_name, 'wb') as file:
                file.write(img_file)
            print("图片下载完成[%d/%d]" % (i + 1, len(urls)))
        info = []
        for outline in outlines:
            if outline.text.split():
                info.append(outline.text.split())

        info.insert(0, ["封面", img_name])
        info.insert(0, ["网址", urls[i]])
        info.insert(0, ["社团", brand])
        info.insert(0, ["标题", name])
        line = str(info) + '\n'
        if line not in lines:
            f.write(line)
    f.close()


# get_info_from_dlsite(1)
# get_info_from_dlsite(2)
# get_info_from_dlsite(3)
# get_info_from_dlsite(4)
# get_info_from_dlsite(5)
