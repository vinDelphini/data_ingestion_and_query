import sqlite3

from db import close_db
from outliers import calculate_outlier_weeks


# Test case 1: Normal database with outlier weeks
def test_normal_database_with_outliers():
    try:
        database_name = 'testing.db'
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        c.execute(
            'CREATE TABLE  IF NOT EXISTS votes (Id INTEGER PRIMARY KEY, PostId INTEGER, VoteTypeId INTEGER, CreationDate TEXT)')
        c.executemany("INSERT INTO votes (Id, PostId, VoteTypeId, CreationDate) VALUES (?, ?, ?, ?)",
                      [(1, 1, 1, "2022-01-01"),
                       (2, 2, 2, "2022-01-08"),
                          (7, 2, 2, "2022-01-09"),
                          (3, 3, 1, "2022-01-15"),
                          (4, 4, 2, "2022-01-22"),
                          (8, 4, 2, "2022-01-23"),
                          (5, 5, 2, "2022-01-29"),
                          (6, 6, 1, "2022-02-05")])
        conn.commit()
        outlier_week = calculate_outlier_weeks(database_name)
        print(outlier_week)
        expected_outliers = [('2022', '00', 1), ('2022', '01', 2), ('2022',
                                                                    '02', 1), ('2022', '03', 2), ('2022', '04', 1), ('2022', '05', 1)]
        assert expected_outliers == outlier_week
    finally:
        c.execute('DELETE FROM votes')
        conn.commit()
        close_db(conn)


# Test case 2: Normal database without outlier weeks
def test_normal_database_without_outliers():
    try:
        database_name = 'testing.db'
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        c.execute(
            'CREATE TABLE  IF NOT EXISTS votes (Id INTEGER PRIMARY KEY, PostId INTEGER, VoteTypeId INTEGER, CreationDate TEXT)')
        c.executemany("INSERT INTO votes (Id, PostId, VoteTypeId, CreationDate) VALUES (?, ?, ?, ?)",
                      [(1, 1, 1, "2022-01-01"),
                       (2, 2, 2, "2022-01-08"),
                       (3, 3, 1, "2022-01-15"),
                       (4, 4, 2, "2022-01-22"),
                       (5, 5, 2, "2022-01-29")])
        conn.commit()
        calculate_outlier_weeks(database_name)
        expected_outliers = []
        assert expected_outliers == []
    finally:
        c.execute('DELETE FROM votes')
        conn.commit()
        close_db(conn)


# Test case 3: Empty database
def test_empty_database():
    try:
        database_name = 'testing.db'
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        c.execute(
            'CREATE TABLE  IF NOT EXISTS votes (Id INTEGER PRIMARY KEY, PostId INTEGER, VoteTypeId INTEGER, CreationDate TEXT)')
        conn.commit()
        calculate_outlier_weeks(database_name)
        expected_outliers = []
        assert expected_outliers == []
    finally:
        c.execute('DELETE FROM votes')
        conn.commit()
        close_db(conn)


# Test case 4: Database with no votes data
def test_database_with_no_votes():
    try:
        database_name = 'testing.db'
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        c.execute(
            'CREATE TABLE IF NOT EXISTS  votes (Id INTEGER PRIMARY KEY, PostId INTEGER, VoteTypeId INTEGER, CreationDate TEXT)')
        conn.commit()
        calculate_outlier_weeks(database_name)
        expected_outliers = []
        assert expected_outliers == []

    finally:
        c.execute('DELETE FROM votes')
        conn.commit()
        close_db(conn)


# Test case 5: Database with votes of only one week
def test_database_with_single_week_votes():
    try:
        database_name = 'testing.db'
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        c.execute(
            'CREATE TABLE  IF NOT EXISTS  votes (Id INTEGER PRIMARY KEY, PostId INTEGER, VoteTypeId INTEGER, CreationDate TEXT)')
        c.executemany("INSERT INTO votes (Id, PostId, VoteTypeId, CreationDate) VALUES (?, ?, ?, ?)",
                      [(1, 1, 1, "2022-01-01"),
                       (2, 2, 2, "2022-01-02"),
                          (3, 3, 1, "2022-01-03"),
                          (4, 4, 2, "2022-01-04")])
        conn.commit()
        calculate_outlier_weeks(database_name)
        expected_outliers = []
        assert expected_outliers == []

    finally:
        c.execute('DELETE FROM votes')
        conn.commit()
        close_db(conn)


# Test case 6: Database with votes of multiple years
def test_database_with_multiple_years_votes():
    try:
        database_name = 'testing.db'
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        c.execute(
            'CREATE TABLE  IF NOT EXISTS votes (Id INTEGER PRIMARY KEY, PostId INTEGER, VoteTypeId INTEGER, CreationDate TEXT)')
        c.executemany("INSERT INTO votes (Id, PostId, VoteTypeId, CreationDate) VALUES (?, ?, ?, ?)",
                      [(1, 1, 1, "2020-12-28"),
                       (2, 2, 2, "2021-01-01"),
                          (3, 3, 1, "2021-01-02"),
                          (4, 4, 2, "2021-12-31"),
                          (5, 5, 2, "2022-01-01")])
        conn.commit()

        calculate_outlier_weeks(database_name)
        expected_outliers = []
        assert expected_outliers == []

    finally:
        c.execute('DELETE FROM votes')
        conn.commit()
        close_db(conn)


# Test case 7: Database with only one week of votes
def test_database_with_one_week_of_votes():
    try:
        database_name = 'testing.db'
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        c.execute(
            'CREATE TABLE  IF NOT EXISTS votes (Id INTEGER PRIMARY KEY, PostId INTEGER, VoteTypeId INTEGER, CreationDate TEXT)')
        c.executemany("INSERT INTO votes (Id,PostId, VoteTypeId, CreationDate) VALUES (?,?, ?, ?)",
                      [(1, 1, 2, "2022-01-01"), (2, 2, 1, "2022-01-02"), (3, 3, 2, "2022-01-03")])
        conn.commit()
        calculate_outlier_weeks(database_name)
        expected_outliers = []
        assert expected_outliers == []

    finally:
        c.execute('DELETE FROM votes')
        conn.commit()
        close_db(conn)


# Test case 8: Database with all votes as outliers
def test_database_with_all_outliers():
    try:
        database_name = 'testing.db'
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        c.execute(
            'CREATE TABLE IF NOT EXISTS votes(Id INTEGER PRIMARY KEY, PostId INTEGER, VoteTypeId INTEGER, CreationDate TEXT)')
        c.executemany("INSERT INTO votes (Id, PostId, VoteTypeId, CreationDate) VALUES (?,?, ?, ?)",
                      [(1, 1, 2, "2022-01-01"), (2, 2, 1, "2022-01-02"), (3, 3, 2, "2022-01-03")])
        conn.commit()
        outlier_week = calculate_outlier_weeks(database_name)
        print(outlier_week)
        expected_outliers = [('2022', '00', 2), ('2022', '01', 1)]
        assert expected_outliers == outlier_week
    finally:
        c.execute('DELETE FROM votes')
        conn.commit()
        close_db(conn)


# Test case 9: Test invalid connection
def test_calculate_outlier_weeks_exception():
    database_name = "xyz.db"
    outlier_weeks = calculate_outlier_weeks(database_name)
    assert outlier_weeks is None
