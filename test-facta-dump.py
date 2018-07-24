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

    context = {
        "@context": {
                        "@vocab": "http://facta.kendra.io/vocab#",
                        "kendra": "http://kendra.io/types#",
                        "kuid": "http://kendra.io/uuid#",
                        "schema": "http://schema.org/"
                    }, 
    }
    for entry in cur.fetchall():
        statement, subject, timestamp = entry
#        rdf = jsonld.normalize(statement)
#        statement = jsonld.compact(jsonld.from_rdf(rdf), context)
#        statement = rdf
        print "STATEMENT:", timestamp.isoformat(), subject
        print json.dumps(statement, indent=4, sort_keys=True)
    cur.close()

main()
