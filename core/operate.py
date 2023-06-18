from core.db import get_db


def insert_doujinshi(info_dic):
    sql = 'INSERT INTO doujinshi (type_id,uploader_id,doujinshi_name,author_id,doujinshi_cover,market,pages,class' \
          ') VALUES (?,?,"?",?,?,?,?,?)'
    db = get_db()
    print(info_dic)

    if 'type_id' in info_dic and 'uploader_id' in info_dic and 'doujinshi_name' in info_dic:
        type_id = info_dic['type_id']
        uploader_id = info_dic['uploader_id']
        doujinshi_name = info_dic['doujinshi_name']
    else:
        return -1

    sql = sql.replace('?', type_id, 1)
    sql = sql.replace('?', str(uploader_id), 1)
    sql = sql.replace('?', doujinshi_name, 1)

    if 'author_name' in info_dic:
        author_name = info_dic['author_name']
        if author_name is None:
            sql = sql.replace('author_id,', '').replace(',?', '', 1)
        else:
            author_id = db.execute(
                "SELECT author_id FROM author "
                "WHERE author_name =?",
                (author_name,)
            ).fetchone()
            if author_id is None:
                db.execute("INSERT INTO author(author_name) VALUES (?)", (author_name,))
                db.commit()
                author_id = db.execute(
                    "SELECT author_id FROM author "
                    "WHERE author_name =?",
                    (author_name,)
                ).fetchone()
            sql = sql.replace('?', str(author_id[0]), 1)
    else:
        sql = sql.replace('author_id,', '').replace(',?', '', 1)

    if 'doujinshi_cover' in info_dic:
        doujinshi_cover = info_dic['doujinshi_cover']
        if doujinshi_cover is None:
            sql = sql.replace(',doujinshi_cover', '').replace(',?', '', 1)
        else:
            sql = sql.replace('?', '"' + doujinshi_cover + '"', 1)
    else:
        sql = sql.replace(',doujinshi_cover', '').replace(',?', '', 1)

    if 'market' in info_dic:
        market = info_dic['market']
        if market is None:
            sql = sql.replace(',market', '').replace(',?', '', 1)
        else:
            sql = sql.replace('?', market, 1)
    else:
        sql = sql.replace(',market', '').replace(',?', '', 1)

    if 'pages' in info_dic:
        pages = info_dic['pages']
        if pages is None:
            sql = sql.replace(',pages', '').replace(',?', '', 1)
        else:
            sql = sql.replace('?', pages, 1)
    else:
        sql = sql.replace(',pages', '').replace(',?', '', 1)

    if 'class' in info_dic:
        adult = info_dic['class']
        if adult is None:
            sql = sql.replace(',class', '').replace(',?', '', 1)
        else:
            sql = sql.replace('?', adult, 1)
    else:
        sql = sql.replace(',class', '').replace(',?', '', 1)

    print(sql)
    try:
        db.execute(sql)
        db.commit()
    except ValueError:
        return -2
    return 0


def insert_unconfirmed(info_dic):
    sql = 'INSERT INTO unconfirmed (type_id,uploader_id,doujinshi_name,author_name,doujinshi_cover,market,pages,class' \
          ') VALUES (?,?,"?",?,?,?,?,?)'
    db = get_db()

    if 'type_id' in info_dic and 'uploader_id' in info_dic and 'doujinshi_name' in info_dic:
        type_id = info_dic['type_id']
        uploader_id = info_dic['uploader_id']
        doujinshi_name = info_dic['doujinshi_name']
    else:
        return -1

    sql = sql.replace('?', type_id, 1)
    sql = sql.replace('?', str(uploader_id), 1)
    sql = sql.replace('?', doujinshi_name, 1)

    if 'author_name' in info_dic:
        author_name = info_dic['author_name']
        if author_name is None:
            sql = sql.replace('author_name,', '').replace(',?', '', 1)
        else:
            sql = sql.replace('?', '"'+author_name+'"', 1)
    else:
        sql = sql.replace('author_name,', '').replace(',?', '', 1)

    if 'doujinshi_cover' in info_dic:
        doujinshi_cover = info_dic['doujinshi_cover']
        if doujinshi_cover is None:
            sql = sql.replace(',doujinshi_cover', '').replace(',?', '', 1)
        else:
            sql = sql.replace('?', '"' + doujinshi_cover + '"', 1)
    else:
        sql = sql.replace(',doujinshi_cover', '').replace(',?', '', 1)

    if 'market' in info_dic:
        market = info_dic['market']
        if market is None:
            sql = sql.replace(',market', '').replace(',?', '', 1)
        else:
            sql = sql.replace('?', market, 1)
    else:
        sql = sql.replace(',market', '').replace(',?', '', 1)

    if 'pages' in info_dic:
        pages = info_dic['pages']
        if pages is None:
            sql = sql.replace(',pages', '').replace(',?', '', 1)
        else:
            sql = sql.replace('?', pages, 1)
    else:
        sql = sql.replace(',pages', '').replace(',?', '', 1)

    if 'class' in info_dic:
        adult = info_dic['class']
        if adult is None:
            sql = sql.replace(',class', '').replace(',?', '', 1)
        else:
            sql = sql.replace('?', adult, 1)
    else:
        sql = sql.replace(',class', '').replace(',?', '', 1)

    print(sql)
    try:
        db.execute(sql)
        db.commit()
    except ValueError:
        return -2
    return 0
