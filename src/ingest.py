import json
import sys

from db import close_db, connect_db, insert_vote_data


def ingest_vote_data(dbConn, filename):
    try:
        message = ""
        with open(filename) as votes_in:
            vote_data_list = []
            unique_id_list = []
            for line in votes_in:
                vote_data = json.loads(line)
                if vote_data['Id'] not in unique_id_list:
                    # Check for null values in required fields
                    if vote_data['PostId'] and vote_data['VoteTypeId'] and vote_data['CreationDate']:
                        vote_data_list.append(
                            (vote_data['Id'], vote_data['PostId'], vote_data['VoteTypeId'], vote_data['CreationDate']))
                        unique_id_list.append(vote_data['Id'])
            insert_vote_data(dbConn, vote_data_list)
            message = "success"
    except FileNotFoundError:
        print("Please download the dataset using 'make fetch_data'")
        message = "FileNotFoundError"
    except json.JSONDecodeError as e:
        print(f"Error parsing vote data: {e}")
        message = "JSONDecodeError"
    except Exception as e:
        print(f"General Exception while executing ingest_vote_data: {e}")
        message = "GeneralException"

    return message


database = 'warehouse.db'
inputfile = sys.argv[1]
conn = connect_db(database)
ingest_vote_data(conn, inputfile)
close_db(conn)
# if set(vote_data.keys()) == {'Id', 'PostId', 'VoteTypeId', 'CreationDate'}:
