#!/usr/bin/python
import sys
sys.path.append('../kendraio-api')
import kendraio_api_server, json, hashlib, sys, time, psycopg2, datetime
import jsonschema
from StringIO import StringIO
import sparql_to_jsonld as s2j

# adapted from https://github.com/RDFLib/rdflib-sqlalchemy
from rdflib import plugin, Graph, Literal, URIRef, BNode, RDF, ConjunctiveGraph
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

        return {"comment": "this is a stub handler for an unimplemented API method"}

    def assertion_handler(source_id, statements, context):
        # Attempt to canonicalize this object by round-tripping decoding and re-encoding
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

        rdf_store = context["rdf_store"]
        graph = Graph(rdf_store, identifier=URIRef(assertion_time+"_"+source_id))
        graph.open(DB_URI, create=True)

        for s in statements:
            graph.parse(StringIO(json.dumps(s)), format="json-ld")

        graph.close()

        return {"received": statements}

    def query_handler(source_id, query, context):
        # Attempt to cnonicalize this object by round-tripping decoding and re-encoding
        query = json.loads(json.dumps(query, sort_keys=True))

        rdf_store = context["rdf_store"]
        graph = ConjunctiveGraph(rdf_store)
        graph.open(DB_URI)
        results = graph.query("select ?subject ?predicate ?object where {?subject ?predicate ?object}")
        # Inelegant, but works: serialize to JSON string, then re-parse
        statements = json.loads(results.serialize(format="json"))
        graph.close()
        
        context =  {
            "@context": {
                "@vocab": "http://facta.kendra.io/vocab#",
                "kv": "http://facta.kendra.io/vocab#",
                "kendra": "http://kendra.io/types#",
                "kuid": "http://kendra.io/uuid#",
                "schema": "http://schema.org/",
                "xsd": "http://www.w3.org/2001/XMLSchema#"
            }
        }

        compacted_graph, contained = s2j.result_data_to_jsonld(statements, context)
        result = s2j.extract_salient_results(
            compacted_graph,
            contained,
            ["kendra:InclusionRelationship", "kendra:TextSelection"])

        result = s2j.quicksearch(result, query)

        return {"result": 
                result}
        
    # load credentials from stdin
    credentials = json.loads(sys.stdin.read())

    # passwordless login via UNIX sockets
    conn = psycopg2.connect(dbname=credentials["POSTGRES_DATABASE"],
                            user=credentials["POSTGRES_USERNAME"])
    print "created database connection"

    http_server = kendraio_api_server.api_server("localhost", int(sys.argv[1]))
    print "created http server"

    context={"db-connection": conn,
             "json-ld-schema": json.loads(open("json-ld-schema.json").read()),
             "rdf_store": setup_rdf_store(DB_ident)}

    http_server.add_credentials(credentials)
    http_server.add_handler('/assert', assertion_handler,
                            context=context)
    http_server.add_handler('/revoke', stub_handler,
                            context=context)
    http_server.add_handler('/query', query_handler,
                            context=context)
    http_server.run()

