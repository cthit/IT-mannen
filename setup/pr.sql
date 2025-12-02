DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'permission_type') THEN
        CREATE TYPE permission_type AS ENUM ('all', 'own', 'view'); -- all: can remove all posts in slideshow, own: can remove their own posts, view: can neither add or remove posts, only for specific visibility
    END IF;
END$$;

DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'visibility_type') THEN
        CREATE TYPE visibility_type AS ENUM ('all', 'gamma', 'specific', 'owner');
    END IF;
END$$;

CREATE TABLE IF NOT EXISTS Actors (
    id SERIAL PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS Slideshows (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    visibility visibility_type NOT NULL,
    owner INT NOT NULL REFERENCES Actors(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS CoOwners (
    actor_id INT NOT NULL REFERENCES Actors(id) ON DELETE CASCADE,
    slideshow_id INT NOT NULL REFERENCES Slideshows(id) ON DELETE CASCADE,
    permission permission_type NOT NULL,      
    PRIMARY KEY (actor_id, slideshow_id)
);

CREATE TABLE IF NOT EXISTS Groups (
    actor_id INT PRIMARY KEY REFERENCES Actors(id) ON DELETE CASCADE,
    group_id TEXT NOT NULL 
);
-- Example usrId and grpId 8bd1329b-01e6-444e-852b-eed58659d717
CREATE TABLE IF NOT EXISTS Users (
    actor_id INT PRIMARY KEY REFERENCES Actors(id) ON DELETE CASCADE,
    user_id TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Posts (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL, 
    description TEXT,
    owner INT NOT NULL REFERENCES Actors(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS TimedPosts (
    id INT PRIMARY KEY REFERENCES Posts(id) ON DELETE CASCADE,
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL
);


CREATE TABLE IF NOT EXISTS SlideshowContents (
    slideshow_id INT NOT NULL REFERENCES Slideshows(id) ON DELETE CASCADE,
    post_id INT NOT NULL REFERENCES Posts(id) ON DELETE CASCADE,
    PRIMARY KEY (slideshow_id, post_id) 
);






/*
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
*/
