# adapted from https://github.com/RDFLib/rdflib-sqlalchemy
import unittest
from rdflib import plugin, Graph, Literal, URIRef, BNode, RDF, ConjunctiveGraph
from rdflib.store import Store
import sys

from rdflib_sqlalchemy import registerplugins

def setup(graph_id):
    rdf_store_ident = URIRef("rdflib_explorer")

    # Note that this DBURI does not specify host or username: instead, connection is 
    # made via UNIX domain sockets, which are self-authenticating
    
    # To use this, this code needs to be run as the user in question
    # Note also that pip install is in general user-local
    dburi = Literal('postgresql+psycopg2:///kendraio_facta')
    
    registerplugins()
    store = plugin.get("SQLAlchemy", Store)(identifier=rdf_store_ident)
    graph = Graph(store, identifier=URIRef(graph_id))
    graph.open(dburi, create=True)
    return graph, rdf_store_ident

def setup_conjunctive():
    rdf_store_ident = URIRef("rdflib_explorer")

    # Note that this DBURI does not specify host or username: instead, connection is 
    # made via UNIX domain sockets, which are self-authenticating
    
    # To use this, this code needs to be run as the user in question
    # Note also that pip install is in general user-local
    dburi = Literal('postgresql+psycopg2:///kendraio_facta')
    
    registerplugins()
    store = plugin.get("SQLAlchemy", Store)(identifier=rdf_store_ident)
    graph = ConjunctiveGraph(store)
    graph.open(dburi, create=True)
    return graph, rdf_store_ident

def teardown(graph, ident):
    if ident:
        # this actually tears down the host database tables containing the graph
        graph.destroy(ident)
    try:
        graph.close()
    except:
        pass

if __name__ == '__main__':
    g, rdf_store_ident = setup("foo")
    g.add((BNode(), RDF.subject, URIRef("http://facta.kendra.io/foo")))
    g, rdf_store_ident = setup("bar")
    g.add((BNode(), RDF.subject, URIRef("http://facta.kendra.io/bar")))
    g, rdf_store_ident = setup_conjunctive()
    results = g.query("select ?s ?p ?o where {?s ?p ?o} limit 100")
    # Turn the whole thing into a JSON string...
    print repr(results.serialize(format="json"))
    teardown(g, None)
    
