CREATE TABLE IF NOT EXISTS Groups (
    name TEXT PRIMARY KEY CHECK (LENGTH(name) >= 3)
);

CREATE TABLE IF NOT EXISTS Posts (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    file_name TEXT NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    owner TEXT NOT NULL REFERENCES Groups(name) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS PostViews (
    id SERIAL PRIMARY KEY,
    route TEXT NOT NULL UNIQUE CHECK (route ~ '^[a-z0-9_-]+$'), -- only lowercase letters, numbers, underscores, and dashes
    name TEXT NOT NULL,
    owner TEXT NOT NULL REFERENCES Groups(name) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS PostViewContents (
    view_id INT NOT NULL REFERENCES PostViews(id) ON DELETE CASCADE,
    post_id INT NOT NULL REFERENCES Posts(id) ON DELETE CASCADE,
    PRIMARY KEY (view_id, post_id) 
);