# Ferdinand Kamuzora
# Python 2.7

import sqlite3
# from app import app
import json
with open('config.json') as data_file:
    config = json.load(data_file)

conn = sqlite3.connect(config['database'], check_same_thread=False)

conn.execute('pragma foreign_keys=ON')


def dict_factory(cursor, row):
    """This is an function use to fonmat the json when retirve from the  myswl database"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


conn.row_factory = dict_factory

conn.execute(
    ''' 
        CREATE TABLE IF NOT EXISTS `admin` (
        `ad_id`INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        `ad_first_name`TEXT NOT NULL,
        `ad_last_name`TEXT NOT NULL)
    '''
)

conn.execute(
    '''
        CREATE TABLE IF NOT EXISTS "patient"
        (pat_id INTEGER PRIMARY KEY AUTOINCREMENT,
        pat_first_name TEXT NOT NULL,
        pat_last_name TEXT NOT NULL,
        pat_insurance_no TEXT NOT NULL,
        pat_ph_no TEXT NOT NULL,
        pat_date DATE DEFAULT (datetime('now','localtime')),
        pat_address TEXT NOT NULL, pat_gender INTEGER)
    '''
)

conn.execute(
    '''
        CREATE TABLE IF NOT EXISTS "doctor"
        (doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
        doc_first_name TEXT NOT NULL,
        doc_last_name TEXT NOT NULL,
        doc_ph_no TEXT NOT NULL,
        doc_date DATE DEFAULT (datetime('now','localtime')),
        doc_address TEXT NOT NULL, doc_gender INTEGER);

    '''
)

conn.execute(
    '''
        CREATE TABLE IF NOT EXISTS appointment
        (app_id INTEGER PRIMARY KEY AUTOINCREMENT,
        pat_id INTEGER NOT NULL,
        doc_id INTEGER NOT NULL,
        appointment_date DATE NOT NULL,
        state INTEGER DEFAULT 0,
        FOREIGN KEY(pat_id) REFERENCES "_patient"(pat_id),
        FOREIGN KEY(doc_id) REFERENCES doctor(doc_id));
    '''
)

conn.execute(
    '''
        CREATE TABLE IF NOT EXISTS user (
        id INTEGER NOT NULL,
        email TEXT PRIMARY KEY,
        password TEXT,
        role_id INTEGER NOT NULL,
        last_login DATE DEFAULT (datetime('now','localtime')));
    '''
)
