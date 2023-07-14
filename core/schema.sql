--
-- SQLiteStudio v3.4.4 生成的文件，周四 6月 29 01:09:11 2023
--
-- 所用的文本编码：UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- 表：author
DROP TABLE IF EXISTS author;

CREATE TABLE author (
    author_id   INTEGER NOT NULL,
    author_name TEXT    UNIQUE
                        NOT NULL,
    PRIMARY KEY (
        author_id AUTOINCREMENT
    )
);


-- 表：author_url
DROP TABLE IF EXISTS author_url;

CREATE TABLE author_url (
    author_id   INTEGER NOT NULL,
    platform_id INTEGER NOT NULL,
    author_url  TEXT    NOT NULL,
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


-- 表：collection
DROP TABLE IF EXISTS collection;

CREATE TABLE collection (
    user_id      INTEGER NOT NULL,
    doujinshi_id INTEGER NOT NULL,
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


-- 表：comment
DROP TABLE IF EXISTS comment;

CREATE TABLE comment (
    comment_id   INTEGER NOT NULL,
    doujinshi_id INTEGER NOT NULL,
    user_id      INTEGER NOT NULL,
    comment      TEXT    NOT NULL,
    date         TEXT    DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime') ) 
                         NOT NULL,
    PRIMARY KEY (
        comment_id AUTOINCREMENT
    ),
    FOREIGN KEY (
        doujinshi_id
    )
    REFERENCES doujinshi (doujinshi_id),
    FOREIGN KEY (
        user_id
    )
    REFERENCES user (user_id) 
);


-- 表：doujinshi
DROP TABLE IF EXISTS doujinshi;

CREATE TABLE doujinshi (
    doujinshi_id    INTEGER NOT NULL,
    author_id       INTEGER,
    type_id         INTEGER NOT NULL,
    uploader_id     INTEGER NOT NULL,
    doujinshi_name  TEXT    NOT NULL
                            UNIQUE,
    doujinshi_cover TEXT,
    market          TEXT,
    pages           TEXT,
    class           INTEGER,
    PRIMARY KEY (
        doujinshi_id AUTOINCREMENT
    ),
    FOREIGN KEY (
        author_id
    )
    REFERENCES author (author_id),
    FOREIGN KEY (
        type_id
    )
    REFERENCES type (type_id),
    CONSTRAINT upload FOREIGN KEY (
        uploader_id
    )
    REFERENCES user (user_id) 
);


-- 表：doujinshi_backup
DROP TABLE IF EXISTS doujinshi_backup;

CREATE TABLE doujinshi_backup (
    recover_id      INTEGER NOT NULL,
    doujinshi_id    INTEGER UNIQUE
                            NOT NULL,
    author_id       INTEGER,
    type_id         INTEGER NOT NULL,
    uploader_id     INTEGER NOT NULL,
    doujinshi_name  TEXT    NOT NULL
                            UNIQUE,
    doujinshi_cover TEXT,
    market          TEXT,
    pages           TEXT,
    class           INTEGER,
    date            TEXT    NOT NULL
                            DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime') ),
    PRIMARY KEY (
        recover_id AUTOINCREMENT
    ),
    FOREIGN KEY (
        author_id
    )
    REFERENCES author (author_id),
    FOREIGN KEY (
        type_id
    )
    REFERENCES type (type_id),
    FOREIGN KEY (
        uploader_id
    )
    REFERENCES user (user_id) 
);


-- 表：doujinshi_tag
DROP TABLE IF EXISTS doujinshi_tag;

CREATE TABLE doujinshi_tag (
    doujinshi_id INTEGER NOT NULL,
    tag_id       INTEGER NOT NULL,
    PRIMARY KEY (
        doujinshi_id,
        tag_id
    ),
    FOREIGN KEY (
        doujinshi_id
    )
    REFERENCES doujinshi (doujinshi_id),
    FOREIGN KEY (
        tag_id
    )
    REFERENCES tag (tag_id) 
);


-- 表：doujinshi_url
DROP TABLE IF EXISTS doujinshi_url;

CREATE TABLE doujinshi_url (
    doujinshi_id  INTEGER NOT NULL,
    platform_id   INTEGER NOT NULL,
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
    platform_id   INTEGER NOT NULL,
    platform_name TEXT    NOT NULL,
    PRIMARY KEY (
        platform_id AUTOINCREMENT
    )
);


-- 表：tag
DROP TABLE IF EXISTS tag;

CREATE TABLE tag (
    tag_id   INTEGER NOT NULL,
    tag_name TEXT    NOT NULL,
    PRIMARY KEY (
        tag_id
    )
);


-- 表：tag_op_record
DROP TABLE IF EXISTS tag_op_record;

CREATE TABLE tag_op_record (
    op_id        INTEGER NOT NULL,
    doujinshi_id INTEGER NOT NULL,
    tag_id       INTEGER NOT NULL,
    editor_id    INTEGER NOT NULL,
    op_type      TEXT    NOT NULL
                         CHECK (op_type == "INSERT" OR 
                                op_type == "DELETE"),
    date         TEXT    DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime') ) 
                         NOT NULL,
    PRIMARY KEY (
        op_id AUTOINCREMENT
    ),
    FOREIGN KEY (
        doujinshi_id
    )
    REFERENCES doujinshi (doujinshi_id),
    FOREIGN KEY (
        tag_id
    )
    REFERENCES tag (tag_id),
    FOREIGN KEY (
        editor_id
    )
    REFERENCES user (user_id) 
);


-- 表：type
DROP TABLE IF EXISTS type;

CREATE TABLE type (
    type_id   INTEGER NOT NULL,
    type_name TEXT    NOT NULL
                      UNIQUE,
    PRIMARY KEY (
        type_id
    )
);


-- 表：unconfirmed
DROP TABLE IF EXISTS unconfirmed;

CREATE TABLE unconfirmed (
    review_id       INTEGER,
    author_name     TEXT,
    type_id         INTEGER REFERENCES type (type_id),
    uploader_id     INTEGER NOT NULL,
    doujinshi_name  TEXT    NOT NULL,
    doujinshi_cover TEXT    UNIQUE,
    market          TEXT,
    pages           INTEGER,
    tag_list        TEXT,
    class           INTEGER,
    condition       INTEGER DEFAULT (0) 
                            NOT NULL
                            CHECK (condition == 0 OR 
                                   condition == 1 OR 
                                   condition == -1),
    PRIMARY KEY (
        review_id AUTOINCREMENT
    ),
    FOREIGN KEY (
        type_id
    )
    REFERENCES type (type_id),
    CONSTRAINT upload FOREIGN KEY (
        uploader_id
    )
    REFERENCES user (user_id) 
);


-- 表：user
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    user_id   INTEGER PRIMARY KEY ASC AUTOINCREMENT,
    account   TEXT    NOT NULL
                      UNIQUE,
    user_name TEXT    UNIQUE
                      NOT NULL,
    password  TEXT    NOT NULL,
    email     TEXT    NOT NULL,
    head_img  TEXT    UNIQUE
);


-- 索引：
DROP INDEX IF EXISTS "";

CREATE UNIQUE INDEX "" ON comment (
    doujinshi_id COLLATE BINARY
);


-- 索引：tag_id
DROP INDEX IF EXISTS tag_id;

CREATE UNIQUE INDEX tag_id ON tag (
    tag_id COLLATE BINARY
);


-- 索引：user_id
DROP INDEX IF EXISTS user_id;

CREATE UNIQUE INDEX user_id ON user (
    user_id COLLATE BINARY
);


-- 触发器：add_backup
DROP TRIGGER IF EXISTS add_backup;
CREATE TRIGGER add_backup
        BEFORE DELETE
            ON doujinshi
BEGIN
    INSERT INTO doujinshi_backup (
                                     doujinshi_id,
                                     author_id,
                                     type_id,
                                     uploader_id,
                                     doujinshi_name,
                                     doujinshi_cover,
                                     market,
                                     pages,
                                     class
                                 )
                                 VALUES (
                                     old.doujinshi_id,
                                     old.author_id,
                                     old.type_id,
                                     old.uploader_id,
                                     old.doujinshi_name,
                                     old.doujinshi_cover,
                                     old.market,
                                     old.pages,
                                     old.class
                                 );
END;


-- 视图：doujinshi_in_order
DROP VIEW IF EXISTS doujinshi_in_order;
CREATE VIEW doujinshi_in_order AS
    SELECT row_number() OVER (ORDER BY doujinshi_id DESC) AS no,
           doujinshi_id,
           doujinshi_name,
           doujinshi_cover,
           type_id
      FROM doujinshi;


-- 视图：doujinshi_part
DROP VIEW IF EXISTS doujinshi_part;
CREATE VIEW doujinshi_part AS
    SELECT doujinshi_id,
           doujinshi_name,
           doujinshi_cover,
           type_id
      FROM doujinshi;


-- 视图：illustration_in_order
DROP VIEW IF EXISTS illustration_in_order;
CREATE VIEW illustration_in_order AS
    SELECT row_number() OVER (ORDER BY doujinshi_id DESC) AS no,
           doujinshi_id,
           doujinshi_name,
           doujinshi_cover,
           type_id
      FROM doujinshi
     WHERE type_id = 2;


-- 视图：manga_in_order
DROP VIEW IF EXISTS manga_in_order;
CREATE VIEW manga_in_order AS
    SELECT row_number() OVER (ORDER BY doujinshi_id DESC) AS no,
           doujinshi_id,
           doujinshi_name,
           doujinshi_cover,
           type_id
      FROM doujinshi
     WHERE type_id = 1;


-- 视图：novel_in_order
DROP VIEW IF EXISTS novel_in_order;
CREATE VIEW novel_in_order AS
    SELECT row_number() OVER (ORDER BY doujinshi_id DESC) AS no,
           doujinshi_id,
           doujinshi_name,
           doujinshi_cover,
           type_id
      FROM doujinshi
     WHERE type_id = 3;


-- 视图：tag_in_order
DROP VIEW IF EXISTS tag_in_order;
CREATE VIEW tag_in_order AS
    SELECT row_number() OVER (ORDER BY temp.num DESC) AS no,
           tag.tag_id,
           tag.tag_name,
           temp.num
      FROM (
               SELECT COUNT(tag_id) AS num,
                      tag_id
                 FROM doujinshi_tag
                GROUP BY tag_id
           )
           AS temp
           INNER JOIN
           tag ON temp.tag_id = tag.tag_id;


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
