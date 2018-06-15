#!/usr/bin/python
import sys
import json, hashlib, sys, time, psycopg2, datetime
import jsonschema
import psycopg2.extras
from pyld import jsonld

def main():

    credentials = json.loads(sys.stdin.read())
    
    # passwordless login via UNIX sockets
    conn = psycopg2.connect(dbname=credentials["POSTGRES_DATABASE"],
                            user=credentials["POSTGRES_USERNAME"])

    print "created database connection"
    # and read from database
    cur = conn.cursor()
    cur.execute('SELECT statement, subject, time FROM received_statements;', ())

    for entry in cur.fetchall():
        statement, subject, timestamp = entry
        print timestamp.isoformat(), subject
        print json.dumps(statement, indent=4, sort_keys=True)
    cur.close()

main()
