--
-- SQLiteStudio v3.4.4 生成的文件，周五 6月 16 14:58:52 2023
--
-- 所用的文本编码：UTF-8
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- 表：author
DROP TABLE IF EXISTS author;

CREATE TABLE author (
    author_id   INTEGER PRIMARY KEY ASC AUTOINCREMENT,
    author_name TEXT    UNIQUE
                        NOT NULL
);


-- 表：author_url
DROP TABLE IF EXISTS author_url;

CREATE TABLE author_url (
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


-- 表：collection
DROP TABLE IF EXISTS collection;

CREATE TABLE collection (
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
    type_id         INTEGER NOT NULL,
    uploader_id     INTEGER NOT NULL,
    doujinshi_name  TEXT    NOT NULL,
    doujinshi_cover TEXT    UNIQUE,
    market          TEXT,
    pages           INTEGER,
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
    doujinshi_id INTEGER,
    tag_id       INTEGER,
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


-- 表：tag
DROP TABLE IF EXISTS tag;

CREATE TABLE tag (
    tag_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_name TEXT    NOT NULL
);


-- 表：type
DROP TABLE IF EXISTS type;

CREATE TABLE type (
    type_id   INTEGER  PRIMARY KEY AUTOINCREMENT,
    type_name TEXT (6) UNIQUE
                       NOT NULL
);


-- 表：unconfirmed
DROP TABLE IF EXISTS unconfirmed;

CREATE TABLE unconfirmed (
    review_id       INTEGER     PRIMARY KEY AUTOINCREMENT,
    author_id       INTEGER,
    type_id         INTEGER,
    uploader_id     INTEGER     NOT NULL,
    doujinshi_name  TEXT        NOT NULL,
    doujinshi_cover TEXT        UNIQUE,
    market          TEXT,
    pages           INTEGER,
    condition       INTEGER (1) DEFAULT (0) 
                                NOT NULL,
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


-- 视图：doujinshi_part
DROP VIEW IF EXISTS doujinshi_part;
CREATE VIEW doujinshi_part AS
    SELECT doujinshi_id,
           doujinshi_name,
           doujinshi_cover,
           type_id
      FROM doujinshi;


-- 视图：illustration
DROP VIEW IF EXISTS illustration;
CREATE VIEW illustration AS
    SELECT doujinshi_id,
           doujinshi_name,
           doujinshi_cover,
           type_id
      FROM doujinshi
     WHERE type_id = 2;


-- 视图：magazine
DROP VIEW IF EXISTS magazine;
CREATE VIEW magazine AS
    SELECT doujinshi_id,
           doujinshi_name,
           doujinshi_cover,
           type_id
      FROM doujinshi
     WHERE type_id = 4;


-- 视图：manga
DROP VIEW IF EXISTS manga;
CREATE VIEW manga AS
    SELECT doujinshi_id,
           doujinshi_name,
           doujinshi_cover,
           type_id
      FROM doujinshi
     WHERE type_id = 1;


-- 视图：novel
DROP VIEW IF EXISTS novel;
CREATE VIEW novel AS
    SELECT doujinshi_id,
           doujinshi_name,
           doujinshi_cover,
           type_id
      FROM doujinshi
     WHERE type_id = 3;


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
