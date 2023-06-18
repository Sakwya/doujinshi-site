import os.path

import requests
from core.scripts import request
from bs4 import BeautifulSoup


def get_info_from_dlsite(page):
    page = str(page)
    url = "https://www.dlsite.com/maniax/fsr/=/language/jp/sex_category[0]/male/ana_flg/all/age_category[" \
          "0]/general/work_category[0]/doujin/order[0]/trend/work_type_category[0]/comic/work_type_category[" \
          "1]/illust/work_type_category[2]/novel/work_type_category_name[0]/漫画/work_type_category_name[" \
          "1]/CG・插画/work_type_category_name[2]/小说/options_and_or/and/options[0]/JPN/options[1]/CHI/options[" \
          "2]/NM/per_page/30/page/"+page+"/show_type/3/lang_options[0]/日文/lang_options[1]/中文/lang_options[2]/不限语种"
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
        info_dic = {
            "标题": name,
            "社团": brand,
            "网址": urls[i],
            "封面": img_name,
        }
        for outline in outlines:
            if outline.text.split():
                info_pair = outline.text.split()
                info_dic.update({info_pair[0]: info_pair[1]})

        line = str(info_dic) + '\n'
        if line not in lines:
            f.write(line)
    f.close()


# get_info_from_dlsite(1)
# get_info_from_dlsite(2)
# get_info_from_dlsite(3)
# get_info_from_dlsite(4)
# get_info_from_dlsite(5)
