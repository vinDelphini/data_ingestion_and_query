import sqlite3
from db import close_db


def calculate_outlier_weeks(database_name):
    try:
        conn = sqlite3.connect(database_name)
        c = conn.cursor()
        # SQL query to calculate outlier weeks
        sql_query = '''WITH weekly_votes AS (
                        SELECT strftime('%Y', CreationDate) AS Year,
                        strftime('%W', CreationDate) AS Week,
                        COUNT(*) AS Votes
                        FROM votes
                        GROUP BY Year, Week)
                            SELECT Year, Week, Votes
                            FROM weekly_votes
                            WHERE ABS(1 - (Votes * 1.0 / (SELECT AVG(Votes) FROM weekly_votes))) > 0.2
                            ORDER BY Year, Week;
                            '''
        c.execute(sql_query)
        outlier_weeks = c.fetchall()

        # Print the outlier weeks
        print("Year | Week | Votes")
        for row in outlier_weeks:
            print(f"{row[0]} | {row[1]} | {row[2]}")

        return outlier_weeks
    except sqlite3.Error as e:
        print("Error: ", e)
    finally:
        close_db(conn)


database_name = 'warehouse.db'
calculate_outlier_weeks(database_name)
