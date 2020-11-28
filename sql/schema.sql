BEGIN;

CREATE TABLE game (
	gid INTEGER auto_increment,
	gname VARCHAR(255),
	type VARCHAR(255),
	cid INTEGER,
	price INTEGER,
	release_date VARCHAR(255),
	gsystem VARCHAR(255),
	sizeG INTEGER,
	picture VARCHAR(255),
	PRIMARY KEY(gid)
);

CREATE TABLE company (
	cid INTEGER auto_increment,
	cname VARCHAR(255),
	passwd VARCHAR(255),
	cemail VARCHAR(255),
	PRIMARY KEY(cid)
);

CREATE TABLE user (
	uid INTEGER auto_increment,
	uname VARCHAR(255),
	age INTEGER,
	region VARCHAR(255),
	gender VARCHAR(255),
	passwd VARCHAR(255),
	reg_date VARCHAR(255),
	uemail VARCHAR(255),
	PRIMARY KEY(uid)
);

CREATE TABLE purchase (
	pid INTEGER auto_increment,
	uid INTEGER,
	gid INTEGER,
	score INTEGER,
	comment VARCHAR(255),
	pdate VARCHAR(255),
	PRIMARY KEY(pid),
	FOREIGN KEY(uid) REFERENCES user(uid),
	FOREIGN KEY(gid) REFERENCES game(gid)
);

CREATE TABLE likeGame (
	uid INTEGER,
	gid INTEGER,
	PRIMARY KEY(uid,gid),
	FOREIGN KEY(uid) REFERENCES user(uid),
	FOREIGN KEY(gid) REFERENCES game(gid)
);


COMMIT;
