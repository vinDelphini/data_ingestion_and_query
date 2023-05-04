import sqlite3
from db import close_db, connect_db
from ingest import ingest_vote_data

database_name = ':memory:'


def test_ingest_vote_data_with_valid_file():

    conn = connect_db(database_name)
    sample_data = "src/test-resources/samples-votes.jsonl"
    ingest_vote_data(conn, sample_data)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM votes")
    result = c.fetchone()
    assert result[0] == 16
    close_db(conn)


def test_ingest_duplicate_vote_data():

    conn = connect_db(database_name)
    sample_data = "src/test-resources/samples-votes.jsonl"
    ingest_vote_data(conn, sample_data)
    ingest_vote_data(conn, sample_data)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM votes")
    result = c.fetchone()
    assert result[0] == 16
    close_db(conn)


def test_ingest_vote_data_with_missing_file():
    # Create an in-memory SQLite database
    try:
        conn = connect_db(database_name)
        status = ingest_vote_data(conn, 'nonexistent_file.json')
        print(status)
        assert status == "FileNotFoundError"
    finally:
        close_db(conn)

# def test_ingest_vote_data_with_missing_file():
#     # Create an in-memory SQLite database
#     conn = connect_db(database_name)
#
#     # Use pytest's `raises` context manager to assert that FileNotFoundError is raised
#     with pytest.raises(Exception) as e:
#         ingest_vote_data(conn, 'dummy.json')
#
#     # Assert on the error message or any other attributes of the exception
#     assert "Please download the dataset using 'make fetch_data'" in str(e.value)
#
#     close_db(conn)


def test_ingest_vote_data_with_invalid_file():
    try:
        conn = sqlite3.connect(':memory:')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS votes
                     (Id INTEGER PRIMARY KEY,
                     PostId INTEGER,
                     VoteTypeId INTEGER,
                     CreationDate TEXT)''')
        conn.commit()
        with open('test_vote_data.json', 'w') as f:
            f.write(
                '{"Id": 1, "PostId": 101, "VoteTypeId": "upvote", "CreationDate": "2022-01-01", "abc"}')

        status = ingest_vote_data(conn, 'test_vote_data.json')
        assert status == "JSONDecodeError"
    finally:
        close_db(conn)


def test_generic_exception_ingest_data():
    try:
        conn = connect_db(database_name)
        status = ingest_vote_data(conn, '.')
        assert status == "GeneralException"
    finally:
        close_db(conn)
