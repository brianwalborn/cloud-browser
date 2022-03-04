DROP TABLE IF EXISTS settings_exclude_tags;
DROP TABLE IF EXISTS settings_query_regions;
DROP TABLE IF EXISTS settings_query_tags;

CREATE TABLE settings_exclude_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_key TEXT NOT NULL,
    tag_value TEXT NOT NULL,
    UNIQUE (tag_key, tag_value)
);

CREATE TABLE settings_query_regions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region TEXT UNIQUE NOT NULL
);

CREATE TABLE settings_query_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_key TEXT NOT NULL,
    tag_value TEXT NOT NULL,
    UNIQUE (tag_key, tag_value)
);
