#!/usr/bin/python
import sys
sys.path.append('../kendraio-api')
import kendraio_api_server, json, hashlib, sys, time, psycopg2, datetime
import jsonschema

if __name__ == '__main__':
    def assertion_handler(source_id, statements, context):
        # Attempt to cnonicalize this object by round-tripping decoding and re-encoding
        statements = json.loads(json.dumps(statements, sort_keys=True))

        # check that we are being sent something that looks like a statement list
        if type(statements) != list:
            raise Exception("invalid data, wrong type")
        if [1 for x in statements if (type(x) != dict) or ("@context" not in x)]:
            raise Exception("invalid data, missing attribute")

        # And now validate that in more detail for every statement in the list
        for x in statements:
            jsonschema.validate(x, context["json-ld-schema"])

        assertion_time = datetime.datetime.now().isoformat()

        # and write to database
        conn = context["db-connection"]
        cur = conn.cursor()
        statements_text = json.dumps(statements, sort_keys=True)
        cur.execute('INSERT INTO received_statements (time, subject, statement, sha256_hash) VALUES (%s,%s,%s,%s);',
                    (assertion_time,
                     source_id,
                     statements_text,
                     hashlib.sha256(statements_text).hexdigest()
                    ))

        conn.commit()
        cur.close()

        return {"received": statements}

    # load credentials from stdin
    credentials = json.loads(sys.stdin.read())

    # passwordless login via UNIX sockets
    conn = psycopg2.connect(dbname=credentials["POSTGRES_DATABASE"],
                            user=credentials["POSTGRES_USERNAME"])
    print "created database connection"

    server = kendraio_api_server.api_server("localhost", int(sys.argv[1]))
    print "created http server"

    server.add_credentials(credentials)
    server.add_handler('/assert', assertion_handler,
                       context={"db-connection": conn,
                                "json-ld-schema": json.loads(open("json-ld-schema.json").read())})
    server.run()

