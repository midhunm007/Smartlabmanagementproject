CREATE TABLE admin (
    aid VARCHAR(255) NOT NULL,
    apd VARCHAR(255) NOT NULL,
    PRIMARY KEY (aid)
);

INSERT INTO admin (aid, apd) VALUES ('admin', '123456');
select * from admin;
CREATE TABLE department (
    depid VARCHAR(255) NOT NULL,
    depname VARCHAR(255) NOT NULL,
    PRIMARY KEY (depid)
);
CREATE TABLE teacher (
    tid VARCHAR(255) NOT NULL,
    tpd VARCHAR(255) NOT NULL,
    tname VARCHAR(255) NOT NULL,
    depid VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY (tid),
    FOREIGN KEY (depid) REFERENCES department(depid)
);
CREATE TABLE year (
    yid integer(255) NOT NULL,
    PRIMARY KEY (yid)
);


CREATE TABLE class (
    cid VARCHAR(255) NOT NULL,
    depid VARCHAR(255) NOT NULL,
    yid INTEGER NOT NULL,
    section VARCHAR(255) NOT NULL,
    PRIMARY KEY (cid),
    FOREIGN KEY (depid) REFERENCES department(depid),
    FOREIGN KEY (yid) REFERENCES year(yid),
    FOREIGN KEY (section) REFERENCES sect(section)
);

CREATE TABLE sect (
    section VARCHAR(255) NOT NULL,
    PRIMARY KEY (section)
);
CREATE TABLE student (
    sid VARCHAR(255) NOT NULL,
    spd VARCHAR(255) NOT NULL,
    sname VARCHAR(255) NOT NULL,
    rollno VARCHAR(255) NOT NULL,
    depid VARCHAR(255) NOT NULL,
    yid INTEGER NOT NULL,
    section VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    PRIMARY KEY (sid),
    FOREIGN KEY (depid) REFERENCES department(depid),
    FOREIGN KEY (yid) REFERENCES year(yid),
    FOREIGN KEY (section) REFERENCES sect(section)
);
USE mydb;

SELECT * FROM admin;
SELECT * FROM class;
INSERT INTO department (depid, depname) VALUES 
('D1', 'CS'),
('D2', 'EC'),
('D3', 'EE');
INSERT INTO sect (section) VALUES 
('A'),
('B'),
('C'),
('D');
INSERT INTO year (yid) VALUES 
(1),
(2),
(3),
(4);
INSERT INTO class (cid, depid, yid, section) VALUES ('C1', 'D1', 1, 'B');
CREATE TABLE USER (
    username VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    PRIMARY KEY (username)
);
INSERT INTO user (username,password) VALUES ('user1', '12345');
use mydb;
INSERT INTO teacher (tid, tpd, tname, depid, email) VALUES
('T2', 'password2', 'Jane Smith', 'D2', 'jane.smith@example.com'),
('T3', 'password3', 'Michael Johnson', 'D1', 'michael.johnson@example.com');
use mydb;
use mydb;
select * from class;
INSERT INTO class (cid, depid, yid, section) VALUES ('C1', 'D1', 1, 'B');


INSERT INTO student (sid, spd, sname, rollno, depid, yid, section, email) VALUES
    ('s1', 'password_1', 'Student 1', '1', 'D1', 1, 'A', 'email1@example.com'),
    ('s2', 'password_2', 'Student 2', '2', 'D2', 2, 'B', 'email2@example.com'),
    ('s3', 'password_3', 'Student 3', '3', 'D3', 3, 'C', 'email3@example.com'),
    ('s4', 'password_4', 'Student 4', '4', 'D1', 4, 'D', 'email4@example.com');

UPDATE class SET depid = 'D1', yid = 2, section = 'B' WHERE cid = 'C1';
desc class;

select * from student;

use mydb;

CREATE TABLE lab (
    lid VARCHAR(255) NOT NULL,
    lname VARCHAR(255) NOT NULL,
    cid VARCHAR(255) NOT NULL,
    tid VARCHAR(255) NOT NULL,
    PRIMARY KEY (lid),
    FOREIGN KEY (cid) REFERENCES class(cid),
    FOREIGN KEY (tid) REFERENCES teacher(tid)
);

INSERT INTO lab (lid, lname, cid, tid) VALUES
('L1', 'Lab 1', 'C2', 'T1'),
('L2', 'Lab 2', 'C2', 'T2'),
('L3', 'Lab 3', 'C2', 'T3');









