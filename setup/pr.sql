CREATE TABLE IF NOT EXISTS Groups (
    name TEXT PRIMARY KEY CHECK (LENGTH(name) >= 3)
);

CREATE TABLE IF NOT EXISTS Posts (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    owner TEXT NOT NULL REFERENCES Groups(name) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS TimedPosts (
    id INT PRIMARY KEY REFERENCES Posts(id) ON DELETE CASCADE,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS Slideshows (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    owner TEXT NOT NULL REFERENCES Groups(name) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS inSlideshow (
    slideshow_id INT NOT NULL REFERENCES Slideshows(id) ON DELETE CASCADE,
    post_id INT NOT NULL REFERENCES Posts(id) ON DELETE CASCADE,
    PRIMARY KEY (slideshow_id, post_id) 
);

CREATE OR REPLACE VIEW ActivePosts AS
SELECT posts.id, posts.description, posts.owner, timedposts.start_time, timedposts.end_time
FROM posts
LEFT JOIN timedposts ON posts.id = timedposts.id
AND NOW() BETWEEN timedposts.start_time AND timedposts.end_time;

CREATE OR REPLACE VIEW NonExpiredPosts AS
SELECT posts.id, posts.description, posts.owner, timedposts.start_time,timedposts.end_time
FROM posts
LEFT JOIN timedposts ON posts.id = timedposts.id
AND timedposts.end_time > NOW();