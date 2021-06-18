import sqlite3
import logging
from sqlite3 import Error
import sys
from setup.config import config

logger = logging.getLogger('MainAPI')

def create_connection():
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    logger.debug('::create_connection()..')

    config_data = config(filename='configurations.ini',section='database')
    db_file = config_data['db_loc']

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def insert_new_request(request):
    logger.debug('::insert_new_request()..')

    #database = r"C:\sqlite\db\rsarequestdb.db"
    # create a database connection
    conn = create_connection()
    with conn:
        # create a new request
        """
        Create a new request into the treedata table
        :param request:
        :return: request id
        """
        sql = ''' INSERT INTO treedata(species,lat,lng,health,height,date,personname)
                VALUES(?,?,?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, request)
        conn.commit()
        return cur.lastrowid
        

def update_request(request):
    logger.debug('::update_request()..')
    #database = r"C:\sqlite\db\rsarequestdb.db"
    # create a database connection
    conn = create_connection()
    with conn:
        # create a new request
        """
        Create a new request into the requests table
        :param request:
        :return: request id
        """        
        sql = ''' UPDATE treedata SET status =?, comment =? WHERE id = ?; '''

        cur = conn.cursor()
        cur.execute(sql, request)
        conn.commit()
        



def select_all_tasks():
    logger.debug('::select_all_tasks()..')
    """
    Query all rows in the tasks table
    :return: rows tuple
    """
    conn = create_connection()

    with conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM treedata")
        # cur.execute("SELECT * FROM treedata WHERE status='New'")
        rows = cur.fetchall()

        return rows

def delete_all_task():
    logger.debug('::delete_all_task()..')
    """
    Query delete rows in the treedata table
    """
    conn = create_connection()
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM treedata")


