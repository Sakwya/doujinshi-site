import ast
import os
from shutil import copyfile
from core.db import get_db


def read_dlsite():
    with open(os.getcwd() + "\\core\\scripts\\dlsite.info", mode='r', encoding="utf-8") as f:
        records = f.read().split('\n')
        records.remove('')

    info = []
    for record in records:
        dlsite = ast.literal_eval(record)
        type_dic = {
            'マンガ': 1,
            'マンガ音声あり': 1,
            'CG・イラスト': 2,
            'CG・イラスト音声あり': 2,
            'ノベル': 3,
            'ノベル音乐あり': 3,
            'ノベル音声あり': 3,
            '漫画': 1,
            '漫画有声音': 1,
            'CG・插画': 2,
            'CG・插画有声音': 2,
            '小说': 3,
            '小说有音乐': 3,
            '小说有声音': 3,
        }
        class_dic = {
            '全年龄': 0,
            '全年齢': 0,
            '18禁': 1,
        }
        try:
            type_name = dlsite['作品形式']
            class_ = class_dic[dlsite['年齢指定']]
        except KeyError:
            type_name = dlsite['作品类型']
            class_ = class_dic[dlsite['年龄指定']]
        type_id = type_dic[type_name]

        doujinshi_name = dlsite['标题']

        try:
            author = dlsite['作者']
            if len(author) > 1:
                author_name = dlsite['社团']
                author_url = dlsite['社团网址']
            else:
                author_name = author[0][0]
                author_url = author[0][1]
        except KeyError:
            author_name = dlsite['社团']
            author_url = dlsite['社团网址']

        try:
            market = dlsite['イベント']
        except KeyError:
            try:
                market = dlsite['活动']
            except KeyError:
                market = None

        try:
            pages = dlsite['ページ数']
        except KeyError:
            try:
                pages = dlsite['页数']
            except KeyError:
                pages = None
        doujinshi_cover = dlsite['封面']
        old_path = os.getcwd() + '\\core\\scripts\\cover\\' + doujinshi_cover
        new_path = os.getcwd() + '\\core\\static\\img\\cover\\' + doujinshi_cover

        if not os.path.exists(new_path):
            copyfile(old_path, new_path)

        if 'ジャンル' in dlsite:
            tag_list = dlsite['ジャンル']
        else:
            try:
                tag_list = dlsite['分类']
            except KeyError:
                tag_list = None

        if type(tag_list) == str:
            tag_list = [tag_list]
        info.append({
            'type_id': type_id,
            'platform_id': 1,

            'doujinshi_name': doujinshi_name,
            'doujinshi_url': dlsite['网址'],
            'author_name': author_name,
            'author_url': author_url,
            'market': market,
            'pages': pages,
            'class': class_,
            'doujinshi_cover': doujinshi_cover,
            'uploader_id': 0,
            'tag_list': tag_list,
        })
    return info


def read_melonbooks():
    with open(os.getcwd() + "\\core\\scripts\\melonbooks.info", mode='r', encoding="utf-8") as f:
        records = f.read().split('\n')
    records.remove('')

    info = []
    for record in records:
        melonbooks = ast.literal_eval(record)
        class_dic = {
            '一般向け': 0,
        }
        tags = melonbooks['标签']
        tag_list = []
        key_list = ['特集', '専売', 'ランキング', 'GWイベント', '作品', '発掘', '再入荷', 'さくっと注文不可', '同人', '売り尽くし',
                    '特典', 'サークル', '入荷', '応援', '通販', 'Vtuber保護者会', '再展開', '号掲載', '再販']
        while len(tags) > 0:
            tag = tags.pop(0)
            insert = True
            for key in key_list:
                if tag.find(key) != -1:
                    insert = False
                    break
            if insert:
                tag_list.append(tag)
        type_id = 1
        if 'イラスト集' in tag_list:
            type_id = 2
            tag_list.remove('イラスト集')
        elif '小説' in tag_list:
            type_id = 3
            tag_list.remove('小説')
        elif '写真集' in tag_list:
            type_id = 4
            tag_list.remove('写真集')
        elif 'コスプレ写真集' in tag_list:
            type_id = 4
            tag_list.remove('コスプレ写真集')
        elif '漫画' in tag_list:
            tag_list.remove('漫画')
        elif '4コマ' in tag_list:
            tag_list.remove('4コマ')
        elif '合同誌' in tag_list:
            tag_list.remove('合同誌')
        elif '総集編' in tag_list:
            tag_list.remove('総集編')
        else:
            pass

        if 'その別' in tag_list:
            tag_list.remove('その別')
        class_ = class_dic[melonbooks['作品種別']]
        try:
            pages = melonbooks['総ページ数・CG数・曲数']
        except KeyError:
            pages = None
        try:
            market = melonbooks['イベント']
        except KeyError:
            market = None

        doujinshi_cover = melonbooks['封面']
        old_path = os.getcwd() + '\\core\\scripts\\cover\\' + doujinshi_cover
        new_path = os.getcwd() + '\\core\\static\\img\\cover\\' + doujinshi_cover

        if not os.path.exists(new_path):
            copyfile(old_path, new_path)

        info.append({
            'type_id': type_id,
            'platform_id': 2,

            'doujinshi_name': melonbooks['标题'],
            'doujinshi_url': melonbooks['网址'],
            'author_name': melonbooks['作者'],
            'author_url': melonbooks['作者网址'],
            'pages': pages,
            'market': market,
            'class': class_,
            'doujinshi_cover': doujinshi_cover,
            'uploader_id': 0,
            'tag_list': tag_list,
        })
    return info


def read_toranoana():
    with open(os.getcwd() + "\\core\\scripts\\toranoana.info", mode='r', encoding="utf-8") as f:
        records = f.read().split('\n')
    records.remove('')

    info = []
    for record in records:
        toranoana = ast.literal_eval(record)
        class_dic = {
            '一般向け': 0,
        }
        tags = toranoana['标签']
        tag_list = []
        key_list = ['#']
        while len(tags) > 0:
            tag = tags.pop(0)
            insert = True
            for key in key_list:
                if tag.find(key) != -1:
                    insert = False
                    break
            if insert:
                tag_list.append(tag)

        if 'ジャンル/サブジャンル' in toranoana:
            series = toranoana['ジャンル/サブジャンル']
            if type(series) is list:
                for tag in series:
                    tag_list.append(tag)
            else:
                tag_list.append(series)

        if 'メインキャラ' in toranoana:
            mainchara = toranoana['メインキャラ']
            if type(mainchara) is list:
                for tag in mainchara:
                    tag_list.append(tag)

        if '種別/サイズ' in toranoana:
            type_ = toranoana['種別/サイズ']
            if type(type_) is list:
                type_name = type_[0]
                pages = type_[-1]
            else:
                type_name = type_
                pages = None
            if '漫画' in type_name:
                type_id = 1
            elif 'イラスト' in type_name:
                type_id = 2
            elif '小説' in type_name:
                type_id = 3
            else:
                # print(type_name,toranoana['网址'])
                continue
        else:
            continue

        class_ = 1

        try:
            market = toranoana['初出イベント']
            market = market.split(maxsplit=1)[-1]
            for day in ['（1日目）', '（2日目）', '（3日目）', '（4日目）', '（5日目）', '-day1-', '-day2-', '-day3-', '-day4-',
                        '-day5-']:
                market = market.replace(day, '').strip()
        except KeyError:
            market = None

        doujinshi_cover = toranoana['封面']
        old_path = os.getcwd() + '\\core\\scripts\\cover\\' + doujinshi_cover
        new_path = os.getcwd() + '\\core\\static\\img\\cover\\' + doujinshi_cover

        if not os.path.exists(new_path):
            copyfile(old_path, new_path)
        info.append({
            'type_id': type_id,
            'platform_id': 3,

            'doujinshi_name': toranoana['标题'],
            'doujinshi_url': toranoana['网址'],
            'author_name': toranoana['作者'],
            'author_url': toranoana['作者网址'],
            'pages': pages,
            'market': market,
            'class': class_,
            'doujinshi_cover': doujinshi_cover,
            'uploader_id': 0,
            'tag_list': tag_list,
        })
    return info


def not_exist(info):
    db = get_db()
    new_info = []
    for info_dic in info:
        doujinshi_name = info_dic['doujinshi_name']
        if db.execute(
                "SELECT * FROM doujinshi "
                "WHERE doujinshi_name = ? "
                "LIMIT 1",
                (doujinshi_name,)
        ).fetchone() is None:
            new_info.append(info_dic)
    return new_info
