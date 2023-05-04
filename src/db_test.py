import sqlite3
import db


def test_sqlite3_connection():
    with sqlite3.connect('warehouse.db') as con:
        cursor = con.cursor()
        assert list(cursor.execute('SELECT 1')) == [(1,)]


def test_connect_db():
    conn = db.connect_db('warehouse.db')
    assert conn is not None
    db.close_db(conn)


def test_close_db():
    conn = db.connect_db('warehouse.db')
    db.close_db(conn)
    try:
        conn.execute("SELECT 1")
    except sqlite3.ProgrammingError:
        assert True, "Connection is closed"


def test_insert_vote_data_with_db_error():
    # Create a mock database connection that raises an error
    class MockConnection:
        def cursor(self):
            raise sqlite3.Error("Mock DB error")

    # Create some test data
    vote_data_list = [(1, 1, 1, '2023-04-25'),
                      (2, 2, 1, '2023-04-25'),
                      (3, 3, 2, '2023-04-25')]
    try:
        # Call the function with the mock connection and vote data list
        db.insert_vote_data(MockConnection(), vote_data_list)
    except sqlite3.Error as e:
        # Assert that the error message is printed
        assert "Mock DB error" in str(e)


def test_insert_vote_data():
    conn = db.connect_db(':memory:')
    # Insert some test data
    vote_data_list = [(1, 1, 1, '2023-04-25'),
                      (2, 2, 1, '2023-04-25'),
                      (3, 3, 2, '2023-04-25')]
    db.insert_vote_data(conn, vote_data_list)

    # Check if the data was inserted correctly
    c = conn.cursor()
    c.execute("SELECT * FROM votes")
    result = c.fetchall()
    assert len(result) == 3
    assert result[0][0] == 1
    assert result[0][1] == 1
    assert result[0][2] == 1
    assert result[0][3] == '2023-04-25'


def test_insert_with_None_conn():
    try:
        # Insert some test data
        vote_data_list = [(1, 1, 1, '2023-04-25'),
                          (2, 2, 1, '2023-04-25'),
                          (3, 3, 2, '2023-04-25')]
        db.insert_vote_data(None, vote_data_list)
    except ValueError as e:
        assert "Database connection is not available" in str(e)


def test_insert_vote_data_with_existing_data():
    conn = db.connect_db(':memory:')
    # Insert some test data
    vote_data_list = [(1, 1, 1, '2023-04-25'),
                      (2, 2, 1, '2023-04-25'),
                      (3, 3, 2, '2023-04-25')]
    db.insert_vote_data(conn, vote_data_list)

    # Insert data with some existing ids
    vote_data_list_2 = [(1, 4, 1, '2023-04-25'),
                        (2, 5, 1, '2023-04-25'),
                        (3, 6, 2, '2023-04-25')]
    db.insert_vote_data(conn, vote_data_list_2)

    # Check if the data was inserted correctly and duplicates were filtered
    c = conn.cursor()
    c.execute("SELECT * FROM votes")
    result = c.fetchall()
    assert len(result) == 3
    assert result[0][1] == 1
    assert result[1][1] == 2
    assert result[2][1] == 3


def test_insert_vote_data_with_empty_data():
    conn = db.connect_db(':memory:')
    # Insert empty data
    vote_data_list = []
    db.insert_vote_data(conn, vote_data_list)

    # Check if no data was inserted
    c = conn.cursor()
    c.execute("SELECT * FROM votes")
    result = c.fetchall()
    assert len(result) == 0  # No new data should be inserted


def test_insert_vote_data_with_none_data():
    try:
        conn = db.connect_db(':memory:')
        # Insert None data
        vote_data_list = None
        db.insert_vote_data(conn, vote_data_list)
    except ValueError as e:
        assert "Input vote data list is None" in str(e)
