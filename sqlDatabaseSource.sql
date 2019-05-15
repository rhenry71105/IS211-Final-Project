

-- - Setting up blogPosts Table.
CREATE TABLE `blogPosts` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`author`	TEXT NOT NULL,
	`title`	TEXT NOT NULL,
	`subHeading`	TEXT NOT NULL,
	`blogPost`	TEXT NOT NULL,
	`dateTime`	TEXT NOT NULL
);



-- - Setting Up users Table.
CREATE TABLE `users` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT NOT NULL,
	`username`	TEXT NOT NULL UNIQUE,
	`email`	TEXT NOT NULL UNIQUE,
	`password`	TEXT NOT NULL
);


-- - Setting up comments Table.
CREATE TABLE `comments` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`user_id`	INTEGER NOT NULL,
	`comment_text`	TEXT NOT NULL UNIQUE,
	`articale_id`	INTEGER NOT NULL,
	`comment_dateTime`	INTEGER NOT NULL
);


-- - Gets Current Time And Date.
SELECT datetime('now', 'localtime');