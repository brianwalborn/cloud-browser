CREATE TABLE IF NOT EXISTS settings_exclude_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_key TEXT NOT NULL,
    tag_value TEXT NOT NULL,
    UNIQUE (tag_key, tag_value)
);

CREATE TABLE IF NOT EXISTS settings_putty_session_names (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region TEXT UNIQUE NOT NULL,
    session_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS settings_query_regions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    region TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS settings_query_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_key TEXT NOT NULL,
    tag_value TEXT NOT NULL,
    UNIQUE (tag_key, tag_value)
);

CREATE TABLE IF NOT EXISTS settings_selected_aws_profile (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aws_profile TEXT NOT NULL
);

INSERT OR IGNORE INTO settings_selected_aws_profile VALUES (1, 'default')
