# adapted from https://github.com/RDFLib/rdflib-sqlalchemy
import unittest
from rdflib import plugin, Graph, Literal, URIRef, BNode, RDF
from rdflib.store import Store
import sys

from rdflib_sqlalchemy import registerplugins

class SQLAGraphTestCase(unittest.TestCase):
    ident = URIRef("rdflib_test")

    # Note that this DBURI does not specify host or username: instead, connection is 
    # made via UNIX domain sockets, which are self-authenticating
    
    # To use this, this code needs to be run as the user in question
    # Note also that pip install is in general user-local
    dburi = Literal('postgresql+psycopg2:///kendraio_facta')
    
    def setUp(self):
        registerplugins()
        store = plugin.get("SQLAlchemy", Store)(identifier=self.ident)
        self.graph = Graph(store, identifier=self.ident)
        self.graph.open(self.dburi, create=True)
        g = self.graph
        sid = BNode()
        g.add((sid, RDF.subject, URIRef("http://www.google.com/")))

    def tearDown(self):
# don't destroy, so we can take a look at the persistent data
#        self.graph.destroy(self.uri)
        try:
            self.graph.close()
        except:
            pass

    def test01(self):
        self.assert_(self.graph is not None)
        print(self.graph)

if __name__ == '__main__':
    unittest.main()
