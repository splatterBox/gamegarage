DROP DATABASE IF EXISTS garage;
CREATE DATABASE garage;
\c garage

DROP TABLE IF EXISTS users;
CREATE TABLE users (
  userid BIGSERIAL PRIMARY KEY NOT NULL,
  username text NOT NULL,
  firstname text NOT NULL,
  lastname text NOT NULL,
  password text NOT NULL,
  avatarpath text NOT NULL);

CREATE EXTENSION pgcrypto;
INSERT INTO users (username, firstname, lastname, password, avatarpath) VALUES ('Bot', 'system', 'system', crypt('bot', gen_salt('bf')), 'none');
INSERT INTO users (username, firstname, lastname, password, avatarpath) VALUES ('raz', 'Ron', 'Zacharski', crypt('p00d13', gen_salt('bf')), 'none');
INSERT INTO users (username, firstname, lastname, password, avatarpath) VALUES ('ann', 'Ann', 'Hedberg', crypt('changeme', gen_salt('bf')), 'none');
INSERT INTO users (username, firstname, lastname, password, avatarpath) VALUES ('lazy', 'Big', 'Easy', crypt('querty', gen_salt('bf')), 'none');

DROP TABLE IF EXISTS creditcards;
CREATE TABLE creditcards (
  ccid BIGSERIAL PRIMARY KEY NOT NULL,
  userid int REFERENCES users(userid) NOT NULL,
  ccnumber text NOT NULL,
  cccode text NOT NULL,
  expmonth text NOT NULL,
  expyear int NOT NULL);
  

INSERT INTO creditcards (userid, ccnumber, cccode, expmonth, expyear) VALUES (1, crypt('1234567890123456', gen_salt('bf')), crypt('1234', gen_salt('bf')), 'june', 2050); 

DROP TABLE IF EXISTS games;
CREATE TABLE games (
  gid BIGSERIAL PRIMARY KEY NOT NULL,
  title text NOT NULL,
  price decimal(10,2) NOT NULL,
  discountprice decimal(10,2) NOT NULL DEFAULT 0.00,
  onsale  boolean  NOT NULL DEFAULT FALSE);
  
INSERT INTO games (title, price, discountprice) VALUES ('FEAR2', 19.99, 19.99);
INSERT INTO games (title, price, discountprice) VALUES ('Juniper''s Knot', 0, 0);
INSERT INTO games (title, price, discountprice) VALUES ('140', 4.99, 4.99);
INSERT INTO games (title, price, discountprice) VALUES ('Analogue: A Hate Story', 9.99, 9.99);
INSERT INTO games (title, price, discountprice) VALUES ('Antichamber', 19.99, 19.99);
INSERT INTO games (title, price, discountprice) VALUES ('Cave Story', 14.99, 14.99);
INSERT INTO games (title, price, discountprice) VALUES ('Hotline Miami', 9.99, 9.99);
INSERT INTO games (title, price, discountprice) VALUES ('LIMBO', 9.99, 9.99);
INSERT INTO games (title, price, discountprice) VALUES ('Touhou Gensoukyou ~ Lotus Land Story', 29.99, 29.99);
INSERT INTO games (title, price, discountprice) VALUES ('Long Live the Queen', 9.99, 9.99);
INSERT INTO games (title, price, discountprice) VALUES ('Portal', 9.99, 9.99);
INSERT INTO games (title, price, discountprice) VALUES ('Space Pirates and Zombies (S.P.A.Z.)', 9.99, 9.99);
INSERT INTO games (title, price, discountprice) VALUES ('Superbrothers: Sword & Sworcery EP', 7.99, 7.99);
INSERT INTO games (title, price, discountprice) VALUES ('Thomas Was Alone', 9.99, 9.99);
 
DROP TABLE IF EXISTS gamedetails;
CREATE TABLE gamedetails (
  gid int PRIMARY KEY REFERENCES games(gid) NOT NULL,
  gdesc text NOT NULL,
  votes int NOT NULL DEFAULT 0,
  artpath text NOT NULL); 

INSERT INTO gamedetails (gid, gdesc, artpath) VALUES (1, 'Confront terrors both known and unknown in a explosive battle for survival with F.E.A.R 2: Project Origin for PC. This action-packed follow-up to Monolith Productions''s award-winning supernatural shooter F.E.A.R. begins where the previous game left off. This time, you''ll come up against Alma''s powers from the perspective of special forces operator Michael Becket. After an enormous explosion has devastated the city of Auburn, you''ll quickly discover that what seemed like an ordinary mission to retrieve and interrogate Genevieve Aristide is anything but.', 'css/images/img7.jpg');
INSERT INTO gamedetails (gid, gdesc, artpath) VALUES (2, 'Juniper''s Knot is a short kinetic visual novel developed by Dischan Media. Created in under a month, Juniper''s Knot revolves around a lost boy and an imprisoned demon, as they help overcome each other''s obstacles through wit and memory, respectively.  Price: Free Release Date: April 13, 2012 Developer: Dischan Media Platform: Microsoft Windows / Mac OS / Linux', 'url');
INSERT INTO gamedetails (gid, gdesc, artpath) VALUES (3, '140 is a platform game independently developed by Jeppe Carlsen, known for his gameplay direction for Playdead''s Limbo. The game is described as a "minimalistic platformer", using electronic music to create synesthesia as the player manipulates their avatar, a character that can take on several basic geometric shapes, through levels in time to the music. The gameplay has been compared to other similar games which involve music synchronization like Sound Shapes and the Bit.Trip series, though with difficult platforming elements comparable to games in the Mega Man series. The game was released in October 2013.  Price: $4.99 Release Date: October 16, 2013 Developer: Jeppe Carlsen Platform: Microsoft Windows / Mac OS / Linux', 'url');
INSERT INTO gamedetails (gid, gdesc, artpath) VALUES (4, 'Analogue: A Hate Story is a visual novel created by independent designer and visual novelist Christine Love. It was created with the Ren''Py engine, and was first released for download on the author''s website in February 2012. A sequel set centuries after Love''s earlier work, Digital: A Love Story (2010), Analogue revolves around an unnamed investigator, who is tasked with discovering the reason for an interstellar ship''s disappearance once it reappears after 600 years. The game''s themes focus similarly around human/computer interaction, interpersonal relationships, and LGBT issues; but focus primarily on "transhumanism, traditional marriage, loneliness and cosplay." Price: $9.99 Release Date: February 1, 2012 Developer: Christine Love Platform: Microsoft Windows / Mac OS / Linux', 'url');
INSERT INTO gamedetails (gid, gdesc, artpath) VALUES (5, 'Antichamber is a single-player first-person puzzle-platform video game created by Alexander Bruce. Many of the puzzles are based on phenomena that occur within impossible objects created by the game engine, such as passages that lead the player to different locations depending on which way they face, and structures that seem otherwise impossible within normal three-dimensional space. The game includes elements of psychological exploration through brief messages of advice to help the player figure out solutions to the puzzles as well as adages for real life. The game was released on Steam for Microsoft Windows on January 31, 2013, a version sold with the Humble Indie Bundle 11 in February 2014 added support for Linux and Mac OS X.  Price: $19.99 Release Date: January 31, 2013 Developer: Alexander Bruce Platform: Microsoft Windows / Mac OS / Linux', 'url');
INSERT INTO gamedetails (gid, gdesc, artpath) VALUES (6, 'The game focuses on an amnesiac protagonist who awakens in a cave. Through his explorations, he discovers a plot by the Doctor, a megalomaniac who intends to force the inhabitants of the cave to fight for him in his bid to conquer the world. The protagonist is thrust into the position of savior as he endeavors to defeat the Doctor.  Price: $14.99 Release Date: December 20, 2004 Developer: Studio Pixel Platform: Microsoft Windows / Mac OS / Linux / Wii / DSi / 3DS', 'url');
INSERT INTO gamedetails (gid, gdesc, artpath) VALUES (7, 'Hotline Miami is divided into several chapters, each of which is further broken down into several stages. At the start of most chapters, the unnamed protagonist wakes up in his apartment and listens to cryptic messages on his answering machine. These messages tell him to perform an arbitrary task at a certain location, which in each case is inferred as a metaphor for killing every person at that location, such as giving VIPs at a hotel a ''great stay'', or taking care of a ''pest infestation''. Prior to commencing a mission, the player is asked to select an animal mask to wear, each of which provides unique advantages or handicaps.  Price: $9.99 Release Date: October 23, 2012 Developer: Dennaton Games, Abstraction Games Platform: Microsoft Windows / Mac OS / Linux / PlayStation 3 / PlayStation 4 / PlayStation Vita / Android', 'url');
INSERT INTO gamedetails (gid, gdesc, artpath) VALUES (8, 'Limbo is a 2D sidescroller, incorporating the physics system Box2D to govern environmental objects and the player character. The player guides an unnamed boy through dangerous environments and traps as he searches for his sister. The developer built the game''s puzzles expecting the player to fail before finding the correct solution. Playdead called the style of play "trial and death", and used gruesome imagery for the boy''s deaths to steer the player from unworkable solutions.  Price: $9.99 Release Date: October 23, 2012 Developer: Dennaton Games, Abstraction Games Platform: Microsoft Windows / Mac OS / Linux / PlayStation 3 / PlayStation 4 / PlayStation Vita / Android', 'url');
INSERT INTO gamedetails (gid, gdesc, artpath) VALUES (9, 'Following the events of the previous games, youkai soon begin to swarm the Hakurei Shrine, prompting Reimu Hakurei and Marisa Kirisame to separately head for a lake in the mountains, which appears to be the source of a tremendous power surge. The two reach the gateway underneath the lake, which teleports them to a strange Fantasy World, in which the mansion Mugenkan exists, where the mastermind supposedly is.  Price: $29.99 Release Date: August 14, 1998 Developer: ZUN Soft Platform: NEC PC-9800 / EPSON PC-486/586', 'url');
INSERT INTO gamedetails (gid, gdesc, artpath) VALUES (10, 'Being a Queen is no easy job. Especially when you''re only fourteen, your mother has just died, and everyone and their pet snake is out to marry you, kill you, or worse. You must frantically learn the skills necessary to manage a country while fending off invasions, civil war, assassins, manipulative suitors, and eldritch abominations. Rule the world or die trying. Price: $9.99 Release Date: June 2, 2012 Developer: Hanako Games and Spiky Caterpillar Platform: Microsoft Windows / Mac OS / Linux', 'url');
INSERT INTO gamedetails (gid, gdesc, artpath) VALUES (11, 'The game primarily comprises a series of puzzles that must be solved by teleporting the player''s character and simple objects using "the Aperture Science Handheld Portal Device", a device that can create inter-spatial portals between two flat planes. The player-character, Chell, is challenged by an artificial intelligence named GLaDOS (Genetic Lifeform and Disk Operating System) to complete each puzzle in the Aperture Science Enrichment Center using the portal gun with the promise of receiving cake when all the puzzles are completed. The game''s unique physics allows momentum to be retained through portals, requiring creative use of portals to maneuver through the test chambers.  Price: $9.99 Release Date: October 9, 2007 Developer: Valve Corporation Platform: Microsoft Windows / Mac OS / Linux / PlayStation 3 / Xbox 360  / Shield Portable / Shield Tablet', 'url');
INSERT INTO gamedetails (gid, gdesc, artpath) VALUES (12, 'Explore a randomly generated Galaxy populated with factions, enemies, missions, and items providing you with a unique experience each time you play.  Price: $9.99 Release Date: August 15, 2011 Developer: MinMax Games Platform: Microsoft Windows / Mac OS / Linux', 'url');
INSERT INTO gamedetails (gid, gdesc, artpath) VALUES (13, 'Explore a randomly generated Galaxy populated with factions, enemies, missions, and items providing you with a unique experience each time you play.  Price: $7.99 Release Date: August 15, 2011 Developer: Capybara and Superbrothers and Jim Guthrie Platform: Microsoft Windows / Mac OS / Linux / Android / iOS', 'url');
INSERT INTO gamedetails (gid, gdesc, artpath) VALUES (14, 'In the game, the player controls one or more simple polygon shapes representing several out-of-control artificial intelligence entities, working with the shapes to get each to their individual end points on each level. Each shape is characterized with a unique name and personality, including the eponymous Thomas, which are conveyed to the player through the use of a narrator, voiced by Danny Wallace and whose performance earned the game a BAFTA Games Award.  Price: $9.99 Release Date: June 30, 2012 Platform: Microsoft Windows / Mac OS / Linux / PlayStation 3 / PlayStation 4 / PlayStation Vita / iOS / Android / Xbox One / WiiU', 'url');
 
DROP TABLE IF EXISTS userlibrary;
CREATE TABLE userlibrary (
  gid int REFERENCES games(gid) NOT NULL,
  userid int REFERENCES users(userid) NOT NULL,
  purchasedstatus boolean NOT NULL DEFAULT FALSE,
  PRIMARY KEY (gid, userid));
  
INSERT INTO userlibrary (gid, userid) VALUES (1, 1);
INSERT INTO userlibrary (gid, userid) VALUES (2, 3);
INSERT INTO userlibrary (gid, userid) VALUES (5, 3);
INSERT INTO userlibrary (gid, userid) VALUES (7, 3);
  
GRANT SELECT ON creditcards TO limited;
GRANT INSERT ON creditcards TO limited;
GRANT UPDATE ON creditcards TO limited;
GRANT USAGE ON creditcards_ccid_seq TO limited;

GRANT SELECT ON users TO limited;
GRANT INSERT ON users TO limited;
GRANT UPDATE ON users TO limited;
GRANT USAGE ON users_userid_seq TO limited;

GRANT SELECT ON games TO limited;
GRANT INSERT ON games TO limited;
GRANT UPDATE ON games TO limited;
GRANT USAGE ON games_gid_seq TO limited;

GRANT SELECT ON gamedetails TO limited;
GRANT INSERT ON gamedetails TO limited;
GRANT UPDATE ON gamedetails TO limited;

GRANT SELECT ON userlibrary TO limited;
GRANT INSERT ON userlibrary TO limited;
GRANT UPDATE ON userlibrary TO limited;

GRANT CONNECT ON DATABASE garage TO limited;
