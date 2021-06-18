import sqlite3
from sqlite3 import Error
from config import config

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    config_data = config(section='database')
    database = config_data['db_ref_loc']


    sql_create_requests_table = """ CREATE TABLE IF NOT EXISTS treedata (
                                        id integer PRIMARY KEY,
                                        species text NOT NULL,
                                        lat real NOT NULL,
                                        lng real NOT NULL,
                                        health text NOT NULL,
                                        height numeric,
                                        date text NOT NULL,
                                        personname text NOT NULL

                                    ); """

    # create a database connection
    conn = create_connection(database)

    with conn:
        # create tables
        if conn is not None:
            # create requests table
            conn.execute("DROP TABLE treedata")
            create_table(conn, sql_create_requests_table)

        else:
            print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()