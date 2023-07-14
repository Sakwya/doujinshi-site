from core.db import get_db


def create_doujinshi_url(doujinshi_id, platform_id, url):
    db = get_db()
    if db.execute(
            "SELECT * FROM doujinshi_url "
            "WHERE doujinshi_id = ? and platform_id = ? "
            "LIMIT 1",
            (doujinshi_id, platform_id)
    ).fetchone() is None:
        db.execute(
            "INSERT INTO doujinshi_url (doujinshi_id,platform_id,doujinshi_url) "
            "VALUES(?,?,?)",
            (doujinshi_id, platform_id, url)
        )
        db.commit()


def get_doujinshi_id(doujinshi_name):
    db = get_db()
    doujinshi_id = db.execute(
        "SELECT doujinshi_id FROM doujinshi "
        "WHERE doujinshi_name = ? "
        "LIMIT 1",
        (doujinshi_name,)
    ).fetchone()
    if doujinshi_id is None:
        return -1
    else:
        return doujinshi_id[0]


def get_author_id(author_name):
    db = get_db()
    author_id = db.execute(
        "SELECT author_id FROM author "
        "WHERE author_name = ? "
        "LIMIT 1",
        (author_name,)
    ).fetchone()
    if author_id is None:
        return -1
    else:
        return author_id[0]


def get_tag_id(tag_name):
    db = get_db()
    tag_id = db.execute(
        "SELECT tag_id FROM tag "
        "WHERE tag_name =? "
        "LIMIT 1",
        (tag_name,)
    ).fetchone()
    if tag_id is None:
        db.execute(
            "INSERT INTO tag (tag_name) "
            "VALUES(?)",
            (tag_name,)
        )
        db.commit()
        return db.execute(
            "SELECT tag_id FROM tag "
            "WHERE tag_name =? "
            "LIMIT 1",
            (tag_name,)
        ).fetchone()[0]
    return tag_id[0]


def add_tag(doujinshi_id, tag_name):
    db = get_db()
    tag_id = get_tag_id(tag_name)
    result = db.execute(
        "SELECT * FROM doujinshi_tag "
        "WHERE doujinshi_id = ? AND tag_id = ? "
        "LIMIT 1",
        (doujinshi_id, tag_id)
    ).fetchone()
    if result is not None:
        return -1
    else:
        db.execute(
            "INSERT INTO doujinshi_tag (doujinshi_id,tag_id) "
            "VAlUES(?,?)",
            (doujinshi_id, tag_id)
        )
        db.commit()
        return 0


def insert_doujinshi(info_dic):
    sql = 'INSERT INTO doujinshi (type_id,uploader_id,doujinshi_name,author_id,doujinshi_cover,market,pages,' \
          'class) VALUES (\\replace\\,\\replace\\,\'\\replace\\\',\\replace\\,\\replace\\,' \
          '\\replace\\,\\replace\\,\\replace\\)'
    db = get_db()

    if 'type_id' in info_dic and 'uploader_id' in info_dic and 'doujinshi_name' in info_dic:
        type_id = info_dic['type_id']
        uploader_id = info_dic['uploader_id']
        doujinshi_name = info_dic['doujinshi_name'].replace('\'', '\'\'')
    else:
        return -1

    sql = sql.replace('\\replace\\', str(type_id), 1)
    sql = sql.replace('\\replace\\', str(uploader_id), 1)
    sql = sql.replace('\\replace\\', doujinshi_name, 1)

    if 'author_name' in info_dic:
        author_name = info_dic['author_name']
        if author_name is None:
            sql = sql.replace('author_id,', '').replace(',\\replace\\', '', 1)
        else:
            author_id = get_author_id(author_name)

            if author_id == -1:
                db.execute("INSERT INTO author(author_name) VALUES (?)", (author_name,))
                db.commit()
                author_id = db.execute(
                    "SELECT author_id FROM author "
                    "WHERE author_name =?",
                    (author_name,)
                ).fetchone()[0]

            if 'author_url' in info_dic:
                author_url = info_dic['author_url']
                platform_id = info_dic['platform_id']
                if db.execute(
                        "SELECT * FROM author_url "
                        "WHERE author_id = ? and platform_id = ? "
                        "LIMIT 1",
                        (author_id, platform_id)
                ).fetchone() is None:
                    db.execute(
                        "INSERT INTO author_url (author_id,platform_id,author_url) "
                        "VALUES(?,?,?)",
                        (str(author_id), str(platform_id), author_url)
                    )
                    db.commit()

            sql = sql.replace('\\replace\\', str(author_id), 1)
    else:
        sql = sql.replace('author_id,', '').replace(',\\replace\\', '', 1)

    if 'doujinshi_cover' in info_dic:
        doujinshi_cover = info_dic['doujinshi_cover']
        if doujinshi_cover is None:
            sql = sql.replace(',doujinshi_cover', '').replace(',\\replace\\', '', 1)
        else:
            sql = sql.replace('\\replace\\', "'" + doujinshi_cover + "'", 1)
    else:
        sql = sql.replace(',doujinshi_cover', '').replace(',\\replace\\', '', 1)

    if 'market' in info_dic:
        market = info_dic['market']
        if market is None:
            sql = sql.replace(',market', '').replace(',\\replace\\', '', 1)
        else:
            sql = sql.replace('\\replace\\', "'" + market + "'", 1)
    else:
        sql = sql.replace(',market', '').replace(',\\replace\\', '', 1)

    if 'pages' in info_dic:
        pages = info_dic['pages']
        if pages is None:
            sql = sql.replace(',pages', '').replace(',\\replace\\', '', 1)
        else:
            sql = sql.replace('\\replace\\', "'" + pages + "'", 1)
    else:
        sql = sql.replace(',pages', '').replace(',\\replace\\', '', 1)

    if 'class' in info_dic:
        adult = info_dic['class']
        if adult is None:
            sql = sql.replace(',class', '').replace(',\\replace\\', '', 1)
        else:
            sql = sql.replace('\\replace\\', str(adult), 1)
    else:
        sql = sql.replace(',class', '').replace(',\\replace\\', '', 1)

    print(sql)
    try:
        db.execute(sql)
        db.commit()
    except ValueError:
        return -2
    if 'tag_list' in info_dic:
        doujinshi_id = get_doujinshi_id(doujinshi_name)
        tag_list = info_dic['tag_list']
        if tag_list is None:
            return 0
        for tag in tag_list:
            add_tag(doujinshi_id, tag)
    return 0


def insert_unconfirmed(info_dic):
    sql = 'INSERT INTO unconfirmed (type_id,uploader_id,doujinshi_name,author_name,doujinshi_cover,market,pages,' \
          'tag_list,class) VALUES (\\replace\\,\\replace\\,\'\\replace\\\',\\replace\\,\\replace\\,\\replace\\,' \
          '\\replace\\,\\replace\\,\\replace\\)'
    db = get_db()

    if 'type_id' in info_dic and 'uploader_id' in info_dic and 'doujinshi_name' in info_dic:
        type_id = info_dic['type_id']
        uploader_id = info_dic['uploader_id']
        doujinshi_name = info_dic['doujinshi_name'].replace('\'', '\'\'')
    else:
        return -1

    sql = sql.replace('\\replace\\', str(type_id), 1)
    sql = sql.replace('\\replace\\', str(uploader_id), 1)
    sql = sql.replace('\\replace\\', doujinshi_name, 1)

    if 'author_name' in info_dic:
        author_name = info_dic['author_name']
        if author_name is None:
            sql = sql.replace('author_name,', '').replace(',\\replace\\', '', 1)
        else:
            sql = sql.replace('\\replace\\', "'" + author_name + "'", 1)
    else:
        sql = sql.replace('author_name,', '').replace(',\\replace\\', '', 1)

    if 'doujinshi_cover' in info_dic:
        doujinshi_cover = info_dic['doujinshi_cover']
        if doujinshi_cover is None:
            sql = sql.replace(',doujinshi_cover', '').replace(',\\replace\\', '', 1)
        else:
            sql = sql.replace('\\replace\\', "'" + doujinshi_cover + "'", 1)
    else:
        sql = sql.replace(',doujinshi_cover', '').replace(',\\replace\\', '', 1)

    if 'market' in info_dic:
        market = info_dic['market']
        if market is None:
            sql = sql.replace(',market', '').replace(',\\replace\\', '', 1)
        else:
            sql = sql.replace('\\replace\\', "'" + market + "'", 1)
    else:
        sql = sql.replace(',market', '').replace(',\\replace\\', '', 1)

    if 'pages' in info_dic:
        pages = info_dic['pages']
        if pages is None:
            sql = sql.replace(',pages', '').replace(',\\replace\\', '', 1)
        else:
            sql = sql.replace('\\replace\\', "'" + pages + "'", 1)
    else:
        sql = sql.replace(',pages', '').replace(',\\replace\\', '', 1)

    if 'tag_list' in info_dic:
        tag_list = info_dic['tag_list']
        if tag_list is None:
            sql = sql.replace(',tag_list', '').replace(',\\replace\\', '', 1)
        else:
            sql = sql.replace('\\replace\\', "'" + tag_list + "'", 1)
    else:
        sql = sql.replace(',tag_list', '').replace(',\\replace\\', '', 1)

    if 'class' in info_dic:
        class_ = info_dic['class']
        if class_ is None:
            sql = sql.replace(',class', '').replace(',\\replace\\', '', 1)
        else:
            sql = sql.replace('\\replace\\', "'" + class_ + "'", 1)
    else:
        sql = sql.replace(',class', '').replace(',\\replace\\', '', 1)

    print(sql)
    try:
        db.execute(sql)
        db.commit()
    except ValueError:
        return -2
    return 0

def remove_doujinshi(doujinshi_id):
    db = get_db()
    if db.execute(
            "SELECT * FROM doujinshi "
            "WHERE doujinshi_id = ? "
            "LIMIT 1",
            (doujinshi_id,)
    ).fetchone() is None:
        return -2

    db.execute(
        "DELETE FROM doujinshi_tag "
        "WHERE doujinshi_id = ?",
        (doujinshi_id,)
    )
    try:
        db.commit()
    except ValueError:
        return -1

    db.execute(
        "DELETE FROM doujinshi_url "
        "WHERE doujinshi_id = ?",
        (doujinshi_id,)
    )
    try:
        db.commit()
    except ValueError:
        return -1

    db.execute(
        "DELETE FROM collection "
        "WHERE doujinshi_id = ?",
        (doujinshi_id,)
    )
    try:
        db.commit()
    except ValueError:
        return -1

    db.execute(
        "DELETE FROM comment "
        "WHERE doujinshi_id = ?",
        (doujinshi_id,)
    )
    try:
        db.commit()
    except ValueError:
        return -1

    db.execute(
        "DELETE FROM doujinshi "
        "WHERE doujinshi_id = ?",
        (doujinshi_id,)
    )
    try:
        db.commit()
    except ValueError:
        return -1

    return 0


def get_recover_id(doujinshi_id):
    db = get_db()
    recover_id = db.execute(
        "SELECT recover_id FROM doujinshi_backup "
        "WHERE doujinshi_id = ? "
        "LIMIT 1",
        (doujinshi_id,)
    ).fetchone()
    if recover_id is None:
        return -1
    return recover_id[0]


def recover_doujinshi(recover_id):
    db = get_db()
    db.execute(
        "INSERT INTO doujinshi "
        "(doujinshi_id,author_id,type_id,uploader_id,doujinshi_name,doujinshi_cover,market,pages,class) "
        "SELECT doujinshi_id,author_id,type_id,uploader_id,doujinshi_name,doujinshi_cover,market,pages,class "
        "FROM doujinshi_backup "
        "WHERE recover_id = ?",
        (recover_id,)
    )
    try:
        db.commit()
        db.execute(
            "DELETE FROM doujinshi_backup "
            "WHERE recover_id = ?",
            (recover_id,)
        )
        db.commit()
        return 0
    except ValueError:
        return -1
