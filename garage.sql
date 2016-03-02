DROP DATABASE IF EXISTS garage;
CREATE DATABASE garage;
\c garage

DROP TABLE IF EXISTS users;
CREATE TABLE users (
  user_id BIGSERIAL PRIMARY KEY NOT NULL,
  username text NOT NULL,
  firstname text NOT NULL,
  lastname text NOT NULL,
  password text NOT NULL);

CREATE EXTENSION pgcrypto;
INSERT INTO users (username, firstname, lastname, password) VALUES ('Bot', 'system', 'system', crypt('bot', gen_salt('bf')));
INSERT INTO users (username, firstname, lastname, password) VALUES ('raz', 'Ron', 'Zacharski', crypt('p00d13', gen_salt('bf')));
INSERT INTO users (username, firstname, lastname, password) VALUES ('ann', 'Ann', 'Hedberg', crypt('changeme', gen_salt('bf')));
INSERT INTO users (username, firstname, lastname, password) VALUES ('lazy', 'Big', 'Easy', crypt('querty', gen_salt('bf')));

DROP TABLE IF EXISTS creditcards;
CREATE TABLE creditcards (
  cc_id BIGSERIAL PRIMARY KEY NOT NULL,
  user_id int REFERENCES users(user_id) NOT NULL,
  cc_number text NOT NULL,
  cc_code text NOT NULL,
  exp_month text NOT NULL,
  exp_year int NOT NULL);
  

INSERT INTO creditcards (user_id, cc_number, cc_code, exp_month, exp_year) VALUES (1, crypt('1234567890123456', gen_salt('bf')), crypt('1234', gen_salt('bf')), 'june', 2050); 

DROP TABLE IF EXISTS games;
CREATE TABLE games (
  g_id BIGSERIAL PRIMARY KEY NOT NULL,
  title text NOT NULL,
  price decimal NOT NULL,
  discount_price decimal NOT NULL DEFAULT 0.00);
  
INSERT INTO games (title, price, discount_price) VALUES ('FEAR2', 19.99, 8.99);
  
DROP TABLE IF EXISTS gamedetails;
CREATE TABLE gamedetails (
  g_id int PRIMARY KEY REFERENCES games(g_id) NOT NULL,
  g_desc text NOT NULL,
  votes int NOT NULL DEFAULT 0,
  art_name text NOT NULL); 

INSERT INTO gamedetails (g_id, g_desc, art_name) VALUES (1, 'Confront terrors both known and unknown in a explosive battle for survival with F.E.A.R 2: Project Origin for PC. This action-packed follow-up to Monolith Productions''s award-winning supernatural shooter F.E.A.R. begins where the previous game left off. This time, you''ll come up against Alma''s powers from the perspective of special forces operator Michael Becket. After an enormous explosion has devastated the city of Auburn, you''ll quickly discover that what seemed like an ordinary mission to retrieve and interrogate Genevieve Aristide is anything but.', 'css/images/img7.jpg');
  
DROP TABLE IF EXISTS userlibrary;
CREATE TABLE userlibrary (
  g_id int REFERENCES games(g_id) NOT NULL,
  user_id int REFERENCES users(user_id) NOT NULL,
  purchasedstatus boolean NOT NULL DEFAULT FALSE,
  PRIMARY KEY (g_id, user_id));
  
INSERT INTO userlibrary (g_id, user_id) VALUES (1, 1);
  
GRANT SELECT ON creditcards TO limited;
GRANT INSERT ON creditcards TO limited;
GRANT UPDATE ON creditcards TO limited;
GRANT USAGE ON creditcards_cc_id_seq TO limited;

GRANT SELECT ON users TO limited;
GRANT INSERT ON users TO limited;
GRANT UPDATE ON users TO limited;
GRANT USAGE ON users_user_id_seq TO limited;

GRANT SELECT ON games TO limited;
GRANT INSERT ON games TO limited;
GRANT UPDATE ON games TO limited;
GRANT USAGE ON games_g_id_seq TO limited;

GRANT SELECT ON gamedetails TO limited;
GRANT INSERT ON gamedetails TO limited;
GRANT UPDATE ON gamedetails TO limited;

GRANT SELECT ON userlibrary TO limited;
GRANT INSERT ON userlibrary TO limited;
GRANT UPDATE ON userlibrary TO limited;

GRANT CONNECT ON DATABASE garage TO limited;