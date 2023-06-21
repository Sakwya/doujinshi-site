import os.path
import requests
from core.scripts import request
from bs4 import BeautifulSoup


def get_info_from_dlsite(type_id, page):
    page = str(page)
    if type_id == 1:
        url = "https://www.dlsite.com/maniax/fsr/=/language/jp/sex_category[0]/male/ana_flg/all/age_category[0]/" \
              "general/work_category[0]/doujin/order[0]/trend/work_type_category[0]/comic/work_type_category_name[0]" \
              "/漫画/options_and_or/and/options[0]/JPN/options[1]/CHI/options[2]/NM/per_page/30/page/" + page + \
              "/show_type/3/lang_options[0]/日文/lang_options[1]/中文/lang_options[2]/不限语种"
    elif type_id == 2:
        url = "https://www.dlsite.com/maniax/fsr/=/language/jp/sex_category[0]/male/ana_flg/all/age_category[0]/" \
              "general/work_category[0]/doujin/order[0]/trend/work_type_category[0]/illust/work_type_category_name[0]" \
              "/CG・插画/options_and_or/and/options[0]/JPN/options[1]/CHI/options[2]/NM/per_page/30/page/" + page + \
              "/show_type/3/lang_options[0]/日文/lang_options[1]/中文/lang_options[2]/不限语种"
    elif type_id == 3:
        url = "https://www.dlsite.com/maniax/fsr/=/language/jp/sex_category[0]/male/ana_flg/all/age_category[0]/" \
              "general/work_category[0]/doujin/order[0]/trend/work_type_category[0]/novel/work_type_category_name[0]" \
              "/小说/options_and_or/and/options[0]/JPN/options[1]/CHI/options[2]/NM/per_page/30/page/" + page + \
              "/show_type/3/lang_options[0]/日文/lang_options[1]/中文/lang_options[2]/不限语种"
    else:
        url = "https://www.dlsite.com/maniax/fsr/=/language/jp/sex_category[0]/male/ana_flg/all/age_category[0]/" \
              "general/work_category[0]/doujin/order[0]/trend/work_type_category[0]/comic/work_type_category[1]/" \
              "illust/work_type_category[2]/novel/work_type_category_name[0]/漫画/work_type_category_name[1]/CG・插画/" \
              "work_type_category_name[2]/小说/options_and_or/and/options[0]/JPN/options[1]/CHI/options[2]/NM/" \
              "per_page/30/page/" + page + "/show_type/3/lang_options[0]/日文/lang_options[1]/中文/lang_options[2]/不限语种"
    html = request(url, 0)
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
        document = documents[i]
        print("抓取数据[%d/%d]" % (i + 1, len(urls)))
        name = document.find(id='work_name').text
        brand = document.find(class_="maker_name")
        outlines = document.find(id="work_outline").find_all("tr")
        picture = "https:" + document.select("li>picture>img")[0]['srcset']
        img_name = picture.split('/')[-1]
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
            "社团": brand.text.replace('\n', ' '),
            "社团网址": brand.find("a")['href'],
            "封面": img_name,
        }
        for outline in outlines:
            info = list(map(str.strip, outline.text.split('\n')))
            while '' in info:
                info.remove('')
            if outline.text.split():
                info_pair = outline.text.split()
                if len(info_pair) > 2:
                    info_dic.update({info_pair[0]: info_pair[1:]})
                else:
                    info_dic.update({info_pair[0]: info_pair[1]})
        if '作者' in info_dic:
            author = info_dic['作者']
            if type(author) is list:
                author_name = ""
                for _ in author:
                    author_name = author_name + _ + " "
                author_name = list(map(str.strip, author_name.split('/')))
                author = []
                for i in range(len(author_name)):
                    author.append([author_name[i], info_dic['社团网址']])
                info_dic['作者'] = author
            else:
                info_dic['作者'] = [[author, info_dic['社团网址']]]
        print("成功")
        line = str(info_dic) + '\n'
        if line not in lines:
            print("写入", end='...')
            f.write(line)
            print("完成")
    f.close()


# get_info_from_dlsite(0, 1)
# get_info_from_dlsite(0, 2)
# get_info_from_dlsite(0, 3)
# get_info_from_dlsite(0, 4)
# get_info_from_dlsite(0, 5)

# get_info_from_dlsite(1, 1)
# get_info_from_dlsite(1, 2)
# get_info_from_dlsite(1, 3)
# get_info_from_dlsite(2, 1)
# get_info_from_dlsite(2, 2)
# # get_info_from_dlsite(2, 3)
# for i in range(3,5):
#     get_info_from_dlsite(3, i)
