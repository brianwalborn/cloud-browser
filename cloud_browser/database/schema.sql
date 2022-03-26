DROP TABLE IF EXISTS settings_exclude_tags;
DROP TABLE IF EXISTS settings_putty_session_names;
DROP TABLE IF EXISTS settings_query_regions;
DROP TABLE IF EXISTS settings_query_tags;
DROP TABLE IF EXISTS settings_selected_aws_profile;

CREATE TABLE settings_exclude_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_key TEXT NOT NULL,
    tag_value TEXT NOT NULL,
    UNIQUE (tag_key, tag_value)
);

CREATE TABLE settings_putty_session_names (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region TEXT UNIQUE NOT NULL,
    session_name TEXT NOT NULL
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

CREATE TABLE settings_selected_aws_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aws_profile TEXT NOT NULL
);

INSERT INTO settings_selected_aws_profile VALUES (1, 'default')
