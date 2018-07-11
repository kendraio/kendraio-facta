#!/usr/bin/python
import sys
sys.path.append('../kendraio-api')
import kendraio_api_server, json, hashlib, sys, time, psycopg2, datetime
import jsonschema
from StringIO import StringIO

# adapted from https://github.com/RDFLib/rdflib-sqlalchemy
from rdflib import plugin, Graph, Literal, URIRef, BNode, RDF
from rdflib.store import Store

from rdflib_sqlalchemy import registerplugins

# To use this, this code needs to be run as the user in question
# Note also that pip install is in general user-local
# Note that this DBURI does not specify host or username: instead, connection is 
# made via UNIX domain sockets, which are self-authenticating
DB_URI = Literal('postgresql+psycopg2:///kendraio_facta')

# This identifies the set of database tables used for storage
# Note that this does not directly correspond to the DB table name:
# not sure how the mapping is made...
semantic_store_id = "release_version_semantic_store"
DB_ident = URIRef(semantic_store_id)

# open a store with this ident
def setup_rdf_store(ident):
    registerplugins()
    store = plugin.get("SQLAlchemy", Store)(identifier=ident)
    return store

if __name__ == '__main__':
    def stub_handler(source_id, statements, context):
        # Attempt to canonicalize this object by round-tripping decoding and re-encoding
        statements = json.loads(json.dumps(statements, sort_keys=True))

        return {"received": statements, "comment": "this is a stub handler that only canonicalizes and echoes input"}

    def assertion_handler(source_id, statements, context):
        # Attempt to cnonicalize this object by round-tripping decoding and re-encoding
        statements = json.loads(json.dumps(statements, sort_keys=True))

        # check that we are being sent something that looks like a statement list
        if type(statements) != list:
            raise Exception("invalid data, should be a list of JSON-LD objects")

       # and now perform a trivial check on every object
        if [1 for x in statements if (type(x) != dict)]:
            raise Exception("invalid data, top-level list item is not an object")

        if [1 for x in statements if ("@context" not in x)]:
            raise Exception("invalid data, object in top-level list does not have an @context attribute")
        
        # And now validate that in more detail for every statement in the list
        for x in statements:
            jsonschema.validate(x, context["json-ld-schema"])

        assertion_time = datetime.datetime.now().isoformat()

        # and write to database
        conn = context["db-connection"]
        cur = conn.cursor()
        statements_text = json.dumps(statements, sort_keys=True)
        cur.execute('INSERT INTO received_statements (time, server_program_id, semantic_store_id, subject, statement, sha256_hash) VALUES (%s,%s,%s,%s,%s,%s);',
                    (assertion_time,
                     sys.argv[0],
                     semantic_store_id,
                     source_id,
                     statements_text,
                     hashlib.sha256(statements_text).hexdigest()
                    ))

        conn.commit()
        cur.close()

        store = setup_rdf_store(DB_ident)
        graph = Graph(store, identifier=URIRef(assertion_time+"_"+source_id))
        graph.open(DB_URI, create=True)

        for s in statements:
            graph.parse(StringIO(json.dumps(s)), format="json-ld")

        graph.close()

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
    server.add_handler('/revoke', stub_handler,
                       context={"db-connection": conn,
                                "json-ld-schema": json.loads(open("json-ld-schema.json").read())})
    server.add_handler('/query', stub_handler,
                       context={"db-connection": conn,
                                "json-ld-schema": json.loads(open("json-ld-schema.json").read())})
    server.run()

