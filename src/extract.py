import psycopg2
import os
import json
from config import parseConfig

def main():
    jsonObj = None
    path = os.path.join(os.path.dirname(__file__), '..\\json\\archive.json')
    print(path)
    with open(path, 'r') as file:
        content = file.read()
        jsonObj = json.loads(content)

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

        if(checkLocationExists(cur, jsonObj['latitude'],jsonObj['longitude'])):
            print('Location Exists')
        else:
            if(jsonObj is not None):
                print('Location does not exist')
                addLocation(conn, cur, float(jsonObj['latitude']), float(jsonObj['longitude']), float(jsonObj['elevation']), jsonObj['timezone'])

        # close the communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')

def checkLocationExists(dbCursor, latitude, longitude) -> bool:
    dbCursor.execute("SELECT LocationID, cityname FROM Locations WHERE Latitude = {0} AND Longitude = {1}".format(latitude, longitude))
    return dbCursor.fetchone() != None

def addLocation(dbConnection, dbCursor, latitude, longitude, elevation, timezone):
    dbCursor.execute('INSERT INTO locations (latitude, longitude, elevation, timezone) VALUES (%s, %s, %s, %s);', (latitude, longitude,elevation,timezone))
    dbConnection.commit()

if __name__ == "__main__":
    main()