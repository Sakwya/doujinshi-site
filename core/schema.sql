--
-- SQLiteStudio v3.4.4 生成的文件，周四 5月 25 19:36:30 2023
--
-- 所用的文本编码：UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- 表：author
DROP TABLE IF EXISTS author;

CREATE TABLE author (
    author_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    author_name TEXT    UNIQUE
                        NOT NULL
);

INSERT INTO author (
                       author_id,
                       author_name
                   )
                   VALUES (
                       1,
                       '王占全'
                   );

INSERT INTO author (
                       author_id,
                       author_name
                   )
                   VALUES (
                       2,
                       '梁建宁'
                   );


-- 表：authorURL
DROP TABLE IF EXISTS authorURL;

CREATE TABLE authorURL (
    author_id   INTEGER,
    platform_id INTEGER,
    author_url  TEXT    UNIQUE
                        NOT NULL,
    PRIMARY KEY (
        author_id,
        platform_id
    ),
    FOREIGN KEY (
        author_id
    )
    REFERENCES author (author_id),
    FOREIGN KEY (
        platform_id
    )
    REFERENCES platform (platform_id) 
);


-- 表：class
DROP TABLE IF EXISTS class;

CREATE TABLE class (
    class_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    class_name TEXT    UNIQUE
                       NOT NULL
);

INSERT INTO class (
                      class_id,
                      class_name
                  )
                  VALUES (
                      1,
                      '漫画'
                  );

INSERT INTO class (
                      class_id,
                      class_name
                  )
                  VALUES (
                      2,
                      '画集'
                  );

INSERT INTO class (
                      class_id,
                      class_name
                  )
                  VALUES (
                      3,
                      '公式本'
                  );

INSERT INTO class (
                      class_id,
                      class_name
                  )
                  VALUES (
                      4,
                      '同人文'
                  );


-- 表：comment
DROP TABLE IF EXISTS comment;

CREATE TABLE comment (
    comment_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id      INTEGER NOT NULL,
    comment_text TEXT    NOT NULL,
    comment_date TEXT    NOT NULL,
    FOREIGN KEY (
        user_id
    )
    REFERENCES user (user_id) 
);


-- 表：doujinshi
DROP TABLE IF EXISTS doujinshi;

CREATE TABLE doujinshi (
    doujinshi_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id       INTEGER,
    class_id        INTEGER,
    user_id         INTEGER NOT NULL,
    doujinshi_name  TEXT    NOT NULL,
    doujinshi_cover TEXT    UNIQUE,
    market          TEXT,
    pages           INTEGER,
    FOREIGN KEY (
        author_id
    )
    REFERENCES author (author_id),
    FOREIGN KEY (
        class_id
    )
    REFERENCES class (class_id),
    FOREIGN KEY (
        user_id
    )
    REFERENCES user (user_id) 
);

INSERT INTO doujinshi (
                          doujinshi_id,
                          author_id,
                          class_id,
                          user_id,
                          doujinshi_name,
                          doujinshi_cover,
                          market,
                          pages
                      )
                      VALUES (
                          1,
                          NULL,
                          NULL,
                          1,
                          '性爱',
                          NULL,
                          NULL,
                          NULL
                      );

INSERT INTO doujinshi (
                          doujinshi_id,
                          author_id,
                          class_id,
                          user_id,
                          doujinshi_name,
                          doujinshi_cover,
                          market,
                          pages
                      )
                      VALUES (
                          2,
                          NULL,
                          NULL,
                          1,
                          '牛魔',
                          NULL,
                          NULL,
                          NULL
                      );

INSERT INTO doujinshi (
                          doujinshi_id,
                          author_id,
                          class_id,
                          user_id,
                          doujinshi_name,
                          doujinshi_cover,
                          market,
                          pages
                      )
                      VALUES (
                          3,
                          NULL,
                          NULL,
                          1,
                          '王占全写真',
                          NULL,
                          NULL,
                          NULL
                      );


-- 表：doujinshiTopic
DROP TABLE IF EXISTS doujinshiTopic;

CREATE TABLE doujinshiTopic (
    doujinshi_id INTEGER,
    topic_id     INTEGER,
    PRIMARY KEY (
        doujinshi_id,
        topic_id
    ),
    FOREIGN KEY (
        doujinshi_id
    )
    REFERENCES doujinshi (doujinshi_id),
    FOREIGN KEY (
        topic_id
    )
    REFERENCES topic (topic_id) 
);


-- 表：doujinshiURL
DROP TABLE IF EXISTS doujinshiURL;

CREATE TABLE doujinshiURL (
    doujinshi_id  INTEGER,
    platform_id   INTEGER,
    doujinshi_url TEXT    NOT NULL,
    PRIMARY KEY (
        doujinshi_id,
        platform_id
    ),
    FOREIGN KEY (
        doujinshi_id
    )
    REFERENCES doujinshi (doujinshi_id),
    FOREIGN KEY (
        platform_id
    )
    REFERENCES platform (platform_id) 
);


-- 表：platform
DROP TABLE IF EXISTS platform;

CREATE TABLE platform (
    platform_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    platform_name TEXT    NOT NULL
);


-- 表：topic
DROP TABLE IF EXISTS topic;

CREATE TABLE topic (
    topic_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_name TEXT    NOT NULL
);


-- 表：unconfirmed
DROP TABLE IF EXISTS unconfirmed;

CREATE TABLE unconfirmed (
    doujinshi_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id       INTEGER,
    class_id        INTEGER,
    user_id         INTEGER NOT NULL,
    doujinshi_name  TEXT    NOT NULL,
    doujinshi_cover TEXT    UNIQUE,
    market          TEXT,
    pages           INTEGER,
    FOREIGN KEY (
        author_id
    )
    REFERENCES author (author_id),
    FOREIGN KEY (
        class_id
    )
    REFERENCES class (class_id),
    FOREIGN KEY (
        user_id
    )
    REFERENCES user (user_id) 
);

INSERT INTO unconfirmed (
                            doujinshi_id,
                            author_id,
                            class_id,
                            user_id,
                            doujinshi_name,
                            doujinshi_cover,
                            market,
                            pages
                        )
                        VALUES (
                            1,
                            1,
                            3,
                            1,
                            '数据库原理',
                            '数据库原理.png',
                            'ww',
                            114
                        );

INSERT INTO unconfirmed (
                            doujinshi_id,
                            author_id,
                            class_id,
                            user_id,
                            doujinshi_name,
                            doujinshi_cover,
                            market,
                            pages
                        )
                        VALUES (
                            2,
                            1,
                            3,
                            1,
                            '数据库原理',
                            '数据库原理.jpg',
                            'ww',
                            114
                        );

INSERT INTO unconfirmed (
                            doujinshi_id,
                            author_id,
                            class_id,
                            user_id,
                            doujinshi_name,
                            doujinshi_cover,
                            market,
                            pages
                        )
                        VALUES (
                            3,
                            1,
                            3,
                            1,
                            '数据库原理',
                            '数据库原理531.jpg',
                            'ww',
                            114
                        );

INSERT INTO unconfirmed (
                            doujinshi_id,
                            author_id,
                            class_id,
                            user_id,
                            doujinshi_name,
                            doujinshi_cover,
                            market,
                            pages
                        )
                        VALUES (
                            4,
                            1,
                            3,
                            1,
                            '数据库原理',
                            '数据库原理358.jpg',
                            'ww',
                            114
                        );

INSERT INTO unconfirmed (
                            doujinshi_id,
                            author_id,
                            class_id,
                            user_id,
                            doujinshi_name,
                            doujinshi_cover,
                            market,
                            pages
                        )
                        VALUES (
                            5,
                            1,
                            3,
                            1,
                            '数据库原理',
                            '数据库原理48922.jpg',
                            'ww',
                            114
                        );


-- 表：user
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    user_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT    NOT NULL
                      UNIQUE,
    password  TEXT    NOT NULL,
    email     TEXT    NOT NULL
);

INSERT INTO user (
                     user_id,
                     user_name,
                     password,
                     email
                 )
                 VALUES (
                     1,
                     '王予嘉',
                     'pbkdf2:sha256:260000$rTia2vvfeo9VXWef$f871d8dad6d41810e8a4def6cd98f0846ed361f791fea774a8dcc35ef7dd77b9',
                     '1041173672@qq.com'
                 );

INSERT INTO user (
                     user_id,
                     user_name,
                     password,
                     email
                 )
                 VALUES (
                     2,
                     '司盛鑫',
                     'pbkdf2:sha256:260000$neYmo2CbSJ3V9iwx$50da7ebd8c3d31873ca5b970800f1ca8cd497a63ba829e0bcaf826fbe7144ead',
                     '995514826@qq.com'
                 );


-- 表：usercollection
DROP TABLE IF EXISTS usercollection;

CREATE TABLE usercollection (
    user_id      INTEGER,
    doujinshi_id INTEGER,
    PRIMARY KEY (
        user_id,
        doujinshi_id
    ),
    FOREIGN KEY (
        user_id
    )
    REFERENCES user (user_id),
    FOREIGN KEY (
        doujinshi_id
    )
    REFERENCES doujinshi (doujinshi_id) 
);

INSERT INTO usercollection (
                               user_id,
                               doujinshi_id
                           )
                           VALUES (
                               1,
                               3
                           );

INSERT INTO usercollection (
                               user_id,
                               doujinshi_id
                           )
                           VALUES (
                               1,
                               1
                           );

INSERT INTO usercollection (
                               user_id,
                               doujinshi_id
                           )
                           VALUES (
                               1,
                               2
                           );


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
