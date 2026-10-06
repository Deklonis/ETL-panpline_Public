-- Database schema generated from db.db
-- SQLite
PRAGMA foreign_keys = ON;

CREATE TABLE "data_company" (
	"comp_name"	TEXT,
	"comp_adress"	TEXT,
	"comp_tel"	TEXT,
	"comp_email"	TEXT,
	"comp_extra"	TEXT,
	"comp_post"	TEXT
);

CREATE TABLE file_draft (
        id INTEGER PRIMARY KEY,
        number INTEGER,
        fio TEXT,
        name_lastname TEXT,
        dat_lastname TEXT,
        company TEXT,
        post TEXT,
        dat_post TEXT,
        phone TEXT,
        email TEXT,
        in_base BOOL,
        in_conf TEXT,
        in_ban_list BOOL,
        last_modified TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

CREATE TABLE "framework" (
	"frame_work"	TEXT
);

CREATE TABLE "participation" (
	"participation_1"	TEXT
);

CREATE TABLE "peopledb" (
	"in_company"	TEXT,
	"FIO"	TEXT,
	"IO"	TEXT,
	"FIO_Dp"	TEXT,
	"post"	TEXT,
	"post_2"	TEXT,
	"tel_1"	TEXT,
	"tel_2"	TEXT,
	"email"	TEXT,
	"post_index"	TEXT,
	"extra"	TEXT,
	"in_conf"	TEXT
, "people_number"	INTEGER);

CREATE TABLE "position" (
	"position_1"	TEXT
);

CREATE TABLE "position_rod" (
	"position_2"	TEXT
);

CREATE TABLE "project" (
	"project_name"	TEXT,
	"Field1"	TEXT,
	"Field2"	TEXT,
	"Field3"	TEXT,
	"Field4"	TEXT,
	"Field5"	TEXT,
	"Field6"	TEXT,
	"Field7"	TEXT,
	"Field8"	TEXT,
	"Field9"	TEXT,
	"Field10"	TEXT,
	"Field11"	TEXT,
	"Field12"	TEXT
);

CREATE TABLE "project_filtres" (
	"pr_name"	TEXT,
	"pr_score"	TEXT,
	"pr_post_in"	TEXT,
	"Field4"	TEXT
);
