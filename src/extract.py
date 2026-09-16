import psycopg2
from config import parseConfig

def main():

    conn = None
    try:
        # read connection parameters
        params = parseConfig()

        # connect to the Postgre SQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create cursor
        cur = conn.cursor()

        # execute statement
        cur.execute('SELECT version()')

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print('Postgre SQL database version: ')
        print(db_version)

        # close the communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

if __name__ == "__main__":
    main()