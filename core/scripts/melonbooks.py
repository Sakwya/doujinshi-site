import os.path
from core.scripts import request
from bs4 import BeautifulSoup
import requests


def get_info_from_melonbooks(order_id, page):
    page = str(page)
    if order_id == 1:
        url = "https://www.melonbooks.co.jp/tags/index.php?genre=&chara=&tag=&fromagee_flg=0&orderby=&disp_number=30" \
              "&pageno=" + page + "&text_type=all&name=&category_ids=1&child_category_ids=9&product_type=st" \
                                       "&is_end_of_sale%5B%5D=1&is_end_of_sale2=1&sale_date_before=&sale_date_after=" \
                                       "&publication_date_before=&publication_date_after="

    else:
        url = "https://www.melonbooks.co.jp/tags/index.php?genre=&chara=&tag=&fromagee_flg=0&orderby=popular" \
              "&disp_number=30&pageno=" + page + "&text_type=all&name=&category_ids=1&child_category_ids=9" \
                                                      "&product_type=all&is_end_of_sale%5B%5D=1&is_end_of_sale2=1" \
                                                      "&sale_date_before=&sale_date_after=&publication_date_before=" \
                                                      "&publication_date_after="
    html = request(url, 0)
    print("获取第" + page + "页文档成功")
    document = BeautifulSoup(html, "html.parser")
    print(url)
    posts = document.select(".item-image")
    urls = []
    for post in posts:
        if post.select('a') is None:
            break
        urls.append("https://www.melonbooks.co.jp" + post.select('a')[0]['href'])
        if len(urls) == 30:
            break

    documents = []
    for i in range(len(urls)):
        html = request(urls[i])
        documents.append(BeautifulSoup(html, "html.parser"))
        print("获取内容[%d/%d]" % (i + 1, len(urls)))

    f = open("melonbooks.info", mode="r+", encoding="utf-8")
    lines = f.readlines()
    for i in range(len(urls)):
        document = documents[i]
        print("抓取数据[%d/%d]" % (i + 1, len(urls)))
        try:
            name = document.find(class_='page-header').text
            author = document.find(class_="author-name")
            author_name = author.text.replace('\n', ' ')
            author_url = author.find("a")['href']
            outlines = document.find('table').children
            tags = document.select("div.item-detail2 > p > a")
        except AttributeError:
            print("失败")
            continue
        tag_list = []
        for tag in tags:
            tag_list.append(tag.text[1:])

        pic = document.select("figure>a")
        if len(pic) == 0:
            pic = document.select("figure>img")[0]['src']
        else:
            pic = pic[0]['href']

        picture = "https:" + pic
        img_name = picture.split('=')[-1]
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
            "作者网址": author_url,
            "封面": img_name,
            "标签": tag_list
        }
        for outline in outlines:
            if outline.text.split():
                info_pair = outline.text.split()
                info_dic.update({info_pair[0]: info_pair[1]})

        print("成功")
        line = str(info_dic) + '\n'
        if line not in lines:
            print("写入",end='...')
            f.write(line)
            print("完成")
    f.close()


# get_info_from_melonbooks(0, 1)
# get_info_from_melonbooks(0, 2)
# get_info_from_melonbooks(0, 3)
# get_info_from_melonbooks(0, 4)
# get_info_from_melonbooks(0, 5)
#
# get_info_from_melonbooks(1, 1)
# get_info_from_melonbooks(1, 2)
# get_info_from_melonbooks(1, 3)
# get_info_from_melonbooks(1, 4)
# get_info_from_melonbooks(1, 5)
