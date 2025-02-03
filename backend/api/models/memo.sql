DROP TABLE IF EXISTS followlist;
DROP TABLE IF EXISTS good;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS report;
DROP TABLE IF EXISTS corpinfo;
DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS user;

-- User テーブル
CREATE TABLE user (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(10),
    email VARCHAR(30),
    password VARCHAR(64),
    comment VARCHAR(100),
    image VARCHAR(255)
);


-- Followlist テーブル
CREATE TABLE followlist (
    following CHAR(36) NOT NULL,
    followed CHAR(36) NOT NULL,
    flag BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (following, followed),
    FOREIGN KEY (following) REFERENCES user(id) ON DELETE CASCADE,
    FOREIGN KEY (followed) REFERENCES user(id) ON DELETE CASCADE
);

-- Post テーブル
CREATE TABLE post (
    id CHAR(36) PRIMARY KEY,
    title VARCHAR(17),
    caption VARCHAR(50),
    create_date_time DATETIME,
    goodcount INT DEFAULT 0,
    image VARCHAR(255),
    user_id CHAR(36),
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE good (
    id CHAR(36) PRIMARY KEY,
    user_id CHAR(36) NOT NULL,
    post_id CHAR(36) NOT NULL,
    flag BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (user_id) REFERENCES user(id),
    FOREIGN KEY (post_id) REFERENCES post(id)
);

-- Report テーブル
CREATE TABLE report (
    id CHAR(36) PRIMARY KEY,
    times INT DEFAULT 0,
    update_date_time DATETIME,
    user_id CHAR(36),
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
);

-- Admin テーブル
CREATE TABLE admin (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(10),
    email VARCHAR(30),
    password VARCHAR(64)
);

-- CorpInfo テーブル
CREATE TABLE corpinfo (
    id CHAR(36) PRIMARY KEY,
    corpname VARCHAR(30),
    email VARCHAR(30),
    manager VARCHAR(30),
    image VARCHAR(255)
);
