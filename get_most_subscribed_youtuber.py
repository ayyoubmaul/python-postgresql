import psycopg2
import pandas as pd
from sqlalchemy import create_engine


# create database connection
def connect_db(database):
    user = 'postgres'
    passwd = 'postgres'
    hostname = 'localhost'

    conn_string = f'postgresql://{user}:{passwd}@{hostname}:5432/{database}'

    db = create_engine(conn_string)
    conn = db.connect()

    return conn

def most_subscribed(sql):
    # connect to raw database
    conn = connect_db('youtube')

    # read sql table
    data = pd.read_sql(sql, con=conn)

    # connect to datawarehouse
    conn = connect_db('youtube_dw')

    # load dataframe to warehouse
    data.to_sql('youtuber_by_year', con=conn, if_exists='replace', index=False)

    # load to bigquery
    # define bigquery loader function


    print('success')

    return data

if __name__ == '__main__':
    sql = '''
    SELECT
        ytb."Youtuber",
        ytb.subscribers
    FROM global_youtube_stat AS ytb
    ORDER BY subscribers DESC
    LIMIT 100;
    '''

    sql_filtered_year = '''
    SELECT
        ytb."Youtuber",
        ytb.subscribers,
        ytb.created_year
    FROM global_youtube_stat AS ytb
    WHERE created_year BETWEEN 2011 AND 2013;
    '''

    most_subscribed(sql_filtered_year)
