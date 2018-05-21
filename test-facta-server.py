#!/usr/bin/python
import sys
sys.path.append('../kendraio-api')
import kendraio_api_server, json, hashlib, sys, time, psycopg2, datetime
import jsonschema

if __name__ == '__main__':
    def assertion_handler(source_id, statements, context):
        # Hash a canonical representation of the JSON object
        hash = hashlib.sha256(json.dumps(statements, sort_keys=True)).hexdigest()

        # check that we are being sent something that looks like a statement list
        if type(statements) != list:
            raise Exception("invalid data, wrong type")
        if [1 for x in statements if (type(x) != dict) or ("@context" not in x)]:
            raise Exception("invalid data, missing attribute")

        jsonschema.validate(statements, context["json-ld-schema"])

        assertion_time = datetime.datetime.now().isoformat()
        assertion = {
            "@context": "https://kendra.io/schema/v1",
            "@type": "statement-container",
            "@id": "facta-statement-%s-%s" % (hash, assertion_time),
            "source_jwt_sub": source_id,
            "time_received": assertion_time,
            "statements": statements,
            "statement-hash": hash
        }

        # and write to database
        conn = context["db-connection"]
        cur = conn.cursor()
        cur.execute('INSERT INTO received_statements (time, subject, statement) VALUES (%s,%s,%s);',
                    (assertion_time, source_id, json.dumps(assertion, sort_keys=True)))
        conn.commit()
        cur.close()

        return {"received": assertion}

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

