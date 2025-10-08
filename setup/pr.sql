CREATE TABLE IF NOT EXISTS Groups (
    name TEXT PRIMARY KEY CHECK (LENGTH(name) >= 3)
);

CREATE TABLE IF NOT EXISTS Posts (
    id SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    file_name TEXT NOT NULL,
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
