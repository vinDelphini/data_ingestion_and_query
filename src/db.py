import sqlite3


def connect_db(dbName):
    conn = sqlite3.connect(dbName)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS votes
                     (Id INTEGER PRIMARY KEY,
                     PostId INTEGER,
                     VoteTypeId INTEGER,
                     CreationDate TEXT)''')
    conn.commit()
    return conn


def close_db(conn):
    if conn:
        conn.commit()  # Commit any pending transactions
        conn.close()  # Close the connection


def insert_vote_data(dbConn, vote_data_list):
    try:
        if dbConn is None:
            raise ValueError("Database connection is not available")

        if vote_data_list is None:
            raise ValueError("Input vote data list is None")

        # for vote_data in vote_data_list:
        #     if not isinstance(vote_data, tuple) or len(vote_data) != 4:
        #         raise ValueError("Input vote data is not in the correct format")
        #     id, postId, voteTypeId, creationDate = vote_data
        #     if not isinstance(id, int) or not isinstance(postId, int) or not isinstance(voteTypeId,
        #                                                                                 int) or not isinstance(
        #         creationDate, str):
        #         raise ValueError("Input vote data has incorrect data types")
        #     # Add additional schema validation checks as needed

        c = dbConn.cursor()
        c.execute("SELECT id FROM votes")
        existing_ids = [int(row[0])
                        for row in c.fetchall()]
        vote_count = len(vote_data_list)
        filtered_vote_data_list = [(id, postId, voteTypeId, creationDate) for id, postId, voteTypeId, creationDate in
                                   vote_data_list if int(id) not in existing_ids]
        filtered_count = len(filtered_vote_data_list)
        c.executemany("INSERT INTO votes (Id, PostId, VoteTypeId, CreationDate) VALUES (?, ?, ?, ?)",
                      filtered_vote_data_list)
        dbConn.commit()
        print(
            f"Total {filtered_count} records inserted in warehouse.db out of input {vote_count} records")
    except sqlite3.Error as e:
        print(f"Error inserting vote data into the database: {e}")
        raise e
    except ValueError as ve:
        print(ve)
        raise ve
