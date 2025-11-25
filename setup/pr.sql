CREATE TABLE IF NOT EXISTS Actors (
    id SERIAL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS CoOwners (
    actor_id INT NOT NULL REFERENCES Actors(id) ON DELETE CASCADE,
    slideshow_id INT NOT NULL REFERENCES Slideshows(id) ON DELETE CASCADE,
    delete_permission ENUM('all', 'own') NOT NULL,
    PRIMARY KEY (actor_id, slideshow_id)
);

CREATE TABLE IF NOT EXISTS Groups (
    actor_id INT PRIMARY KEY REFERENCES Actors(id) ON DELETE CASCADE,
    group_id TEXT NOT NULL 
);

CREATE TABLE IF NOT EXISTS Users (
    actor_id INT PRIMARY KEY REFERENCES Actors(id) ON DELETE CASCADE,
    user_id TEXT NOT NULL
)

CREATE TABLE IF NOT EXISTS Posts (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
    description TEXT,
    owner INT NOT NULL REFERENCES Actors(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS TimedPosts (
    id INT PRIMARY KEY REFERENCES Posts(id) ON DELETE CASCADE,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS Slideshows (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    visibility ENUM('all', 'gamma', 'specific', 'owner') NOT NULL,
    owner TEXT NOT NULL REFERENCES Actors(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS SlideshowContents (
    slideshow_id INT NOT NULL REFERENCES Slideshows(id) ON DELETE CASCADE,
    post_id INT NOT NULL REFERENCES Posts(id) ON DELETE CASCADE,
    PRIMARY KEY (slideshow_id, post_id) 
);

CREATE TABLE IF NOT EXISTS SpecificVisibility (
    actor_id INT NOT NULL REFERENCES Actors(id) ON DELETE CASCADE,
    slideshow_id INT NOT NULL REFERENCES Slideshows(id) ON DELETE CASCADE,
)



-- Ta bort SpecificVisibility och lägga till en till delete_permission som är typ "view"



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