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
            'CG・イラスト': 2,
            'ノベル': 3,
            'マンガ音声あり': 1,
            '漫画': 1,
            'CG・插画': 2,
            '小说': 3,
            '漫画有声音': 1,
        }
        class_dic = {
            '全年龄': 0,
            '全年齢': 0,
            '18禁': 1,
        }
        try:
            type_name = dlsite['作品形式']
            adult = class_dic[dlsite['年齢指定']]
        except KeyError:
            type_name = dlsite['作品类型']
            adult = class_dic[dlsite['年龄指定']]
        type_id = type_dic[type_name]

        doujinshi_name = dlsite['标题']

        try:
            author_name = dlsite['作者']
        except KeyError:
            author_name = dlsite['社团']

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
        info.append({
            'type_id': type_id,
            'doujinshi_name': doujinshi_name,
            'author_name': author_name,
            'pages': pages,
            'class': adult,
            'doujinshi_cover': doujinshi_cover,
            'upload_id': 0,
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
