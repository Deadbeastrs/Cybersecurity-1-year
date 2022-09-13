PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE user (
	id INTEGER NOT NULL, 
	username VARCHAR(40),
	password BLOB,
	cmd_id BLOB,
	PRIMARY KEY (id), 
	UNIQUE (username)
);

CREATE TABLE oauth2_client (
	client_id VARCHAR(48), 
	client_secret VARCHAR(120), 
	client_id_issued_at INTEGER NOT NULL, 
	client_secret_expires_at INTEGER NOT NULL, 
	client_metadata TEXT, 
	id INTEGER NOT NULL, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(user_id) REFERENCES user (id) ON DELETE CASCADE
);

CREATE TABLE oauth2_code (
	code VARCHAR(120) NOT NULL, 
	client_id VARCHAR(48), 
	redirect_uri TEXT, 
	response_type TEXT, 
	scope TEXT, 
	auth_time INTEGER NOT NULL, 
	id INTEGER NOT NULL, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (code), 
	FOREIGN KEY(user_id) REFERENCES user (id) ON DELETE CASCADE
);

CREATE TABLE oauth2_token (
	client_id VARCHAR(48), 
	token_type VARCHAR(40), 
	access_token VARCHAR(255) NOT NULL, 
	refresh_token VARCHAR(255), 
	scope TEXT, 
	revoked BOOLEAN, 
	issued_at INTEGER NOT NULL, 
	expires_in INTEGER NOT NULL, 
	id INTEGER NOT NULL, 
	user_id INTEGER, 
	PRIMARY KEY (id), 
	UNIQUE (access_token), 
	FOREIGN KEY(user_id) REFERENCES user (id) ON DELETE CASCADE
);

CREATE TABLE Games (
	id INTEGER NOT NULL, 
	game VARCHAR(40), 
	skill INTEGER,
	behaviour INTEGER,
	user_id INTEGER,
	PRIMARY KEY (id),
	FOREIGN KEY(user_id) REFERENCES user (id) ON DELETE CASCADE
);


INSERT INTO user VALUES(1,'t1',X'9265282d959dded9600e7cfba5983fbe',NULL);
INSERT INTO user VALUES(2,'t2',X'9265282d959dded9600e7cfba5983fbe',NULL);
INSERT INTO user VALUES(3,'t3',X'9265282d959dded9600e7cfba5983fbe',NULL);
INSERT INTO user VALUES(4,'t4',X'9265282d959dded9600e7cfba5983fbe',NULL);
INSERT INTO user VALUES(5,'t5',X'9265282d959dded9600e7cfba5983fbe',NULL);
INSERT INTO user VALUES(6,'t6',X'9265282d959dded9600e7cfba5983fbe',NULL);


INSERT INTO Games VALUES(1,'chess',5,1,1);
INSERT INTO Games VALUES(2,'chess',10,4,2);
INSERT INTO Games VALUES(3,'chess',1,10,3);
INSERT INTO Games VALUES(4,'chess',2,3,4);
INSERT INTO Games VALUES(5,'chess',1,6,5);
INSERT INTO Games VALUES(6,'chess',2,3,6);

INSERT INTO Games VALUES(7,'sueca',9,2,1);
INSERT INTO Games VALUES(8,'sueca',1,5,2);
INSERT INTO Games VALUES(9,'sueca',15,14,3);
INSERT INTO Games VALUES(10,'sueca',3,9,4);
INSERT INTO Games VALUES(11,'sueca',0,6,5);
INSERT INTO Games VALUES(12,'sueca',5,10,6);

INSERT INTO Games VALUES(13,'checkers',1,10,1);
INSERT INTO Games VALUES(14,'checkers',15,4,2);
INSERT INTO Games VALUES(15,'checkers',3,8,3);
INSERT INTO Games VALUES(16,'checkers',7,9,4);
INSERT INTO Games VALUES(17,'checkers',3,12,5);
INSERT INTO Games VALUES(18,'checkers',2,2,6);

insert into oauth2_client values ("jOto33BdWpYlRO12Jy67S2Y9","FZ4oSVID2fTAqK1CPoixZSHQTZMlyV0ubK9FD9wQqU75Aqpj",1653581003,0,'{"client_name": "TM", "client_uri": "http://TM", "grant_types": ["authorization_code"], "redirect_uris": ["http://127.0.0.1:5000/tm/callback"], "response_types": ["code"], "scope": "indicators update_indicators", "token_endpoint_auth_method": "client_secret_basic"}',1,1);

COMMIT;