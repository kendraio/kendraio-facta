# adapted from https://github.com/RDFLib/rdflib-sqlalchemy
import unittest
from rdflib import plugin, Graph, Literal, URIRef, BNode, RDF
from rdflib.store import Store
import sys

from rdflib_sqlalchemy import registerplugins

def setup():
    ident = URIRef("rdflib_explorer")

    # Note that this DBURI does not specify host or username: instead, connection is 
    # made via UNIX domain sockets, which are self-authenticating
    
    # To use this, this code needs to be run as the user in question
    # Note also that pip install is in general user-local
    dburi = Literal('postgresql+psycopg2:///kendraio_facta')
    
    registerplugins()
    store = plugin.get("SQLAlchemy", Store)(identifier=ident)
    graph = Graph(store, identifier=URIRef("foobar"))
    graph.open(dburi, create=True)
    return graph, ident

def teardown(graph, ident):
    if ident:
        # this actually tears down the host database tables containing the graph
        graph.destroy(ident)
    try:
        graph.close()
    except:
        pass

if __name__ == '__main__':
    g, ident = setup()
    sid = BNode()
    g.add((sid, RDF.subject, URIRef("http://facta.kendra.io/")))
    teardown(g, None)
    
