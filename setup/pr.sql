CREATE TABLE IF NOT EXISTS Groups (
    name TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Posts (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    file_name TEXT NOT NULL,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    owner TEXT REFERENCES Groups(name)
);

CREATE TABLE IF NOT EXISTS PostViews (
    route TEXT PRIMARY KEY CHECK (route ~ '^[a-z0-9_-]+$'), -- case sensative, only allow lower-cased letters, numbers, underscores, and dashes
    owner TEXT REFERENCES Groups(name)
);

CREATE TABLE IF NOT EXISTS ViewContents (
    view_route TEXT REFERENCES PostViews(route) ON DELETE CASCADE,
    post_id INT REFERENCES Posts(id) ON DELETE CASCADE  
);