CREATE database telebot;

CREATE SEQUENCE voice_ids;

CREATE TABLE users(
    uid INTEGER PRIMARY KEY,
    username VARCHAR (50) NOT NULL);

CREATE TABLE voices(
    voice_id INTEGER DEFAULT nextval('voice_ids'),
    path_to_voice_message VARCHAR(255) NOT NULL,
    user_id INTEGER NOT NULL,
    PRIMARY KEY (voice_id, user_id),
    FOREIGN KEY (user_id ) REFERENCES users(uid)
);