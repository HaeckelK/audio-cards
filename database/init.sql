CREATE TABLE IF NOT EXISTS words (
    id SERIAL PRIMARY KEY,
    language text,
    word text,
    known boolean,
    date_known int,
    added int,
    UNIQUE (language, word)
);
