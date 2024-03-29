CREATE TABLE users (
    avatar      VARCHAR(80),
    followers   INTEGER NOT NULL,
    following   INTEGER NOT NULL,
    id          INTEGER PRIMARY KEY,
    name        VARCHAR(50) NOT NULL,
    uname       VARCHAR(32) NOT NULL,
    about       VARCHAR(150),
    likes       INTEGER NOT NULL,
    answers     INTEGER NOT NULL,
    tells       INTEGER NOT NULL,
    verified    BOOLEAN NOT NULL
);

CREATE TABLE answers (
    id          INTEGER PRIMARY KEY,
    answer      VARCHAR(2048) NOT NULL,
    likes       INTEGER NOT NULL,
    created     DATETIME NOT NULL,
    tell        VARCHAR(1024),
    user        INTEGER NOT NULL,
    parent_id   INTEGER,
    FOREIGN KEY (user) REFERENCES users(id),
    FOREIGN KEY (parent_id) REFERENCES answers(id)
);