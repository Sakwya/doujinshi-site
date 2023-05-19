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
    doujinshi_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id      INTEGER,
    class_id       INTEGER,
    market_id      INTEGER,
    user_id        INTEGER NOT NULL,
    doujinshi_name TEXT    NOT NULL,
    pages          INTEGER,
    FOREIGN KEY (
        author_id
    )
    REFERENCES author (author_id),
    FOREIGN KEY (
        class_id
    )
    REFERENCES class (class_id),
    FOREIGN KEY (
        market_id
    )
    REFERENCES market (market_id),
    FOREIGN KEY (
        user_id
    )
    REFERENCES user (user_id) 
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


-- 表：market
DROP TABLE IF EXISTS market;

CREATE TABLE market (
    market_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    market_name TEXT    NOT NULL
);


-- 表：platform
DROP TABLE IF EXISTS platform;

CREATE TABLE platform (
    platform_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    platform_name TEXT    NOT NULL
);


-- 表：review
DROP TABLE IF EXISTS review;

CREATE TABLE review (
    review_id      INTEGER PRIMARY KEY AUTOINCREMENT,
    author_id      INTEGER,
    class_id       INTEGER,
    market_id      INTEGER,
    user_id        INTEGER NOT NULL,
    doujinshi_name TEXT    NOT NULL,
    pages          INTEGER,
    FOREIGN KEY (
        author_id
    )
    REFERENCES author (author_id),
    FOREIGN KEY (
        class_id
    )
    REFERENCES class (class_id),
    FOREIGN KEY (
        market_id
    )
    REFERENCES market (market_id),
    FOREIGN KEY (
        user_id
    )
    REFERENCES user (user_id) 
);


-- 表：topic
DROP TABLE IF EXISTS topic;

CREATE TABLE topic (
    topic_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_name TEXT    NOT NULL
);


-- 表：user
DROP TABLE IF EXISTS user;

CREATE TABLE user (
    user_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT    NOT NULL,
    password  TEXT    NOT NULL,
    email     TEXT    NOT NULL
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


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
