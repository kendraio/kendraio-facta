# adapted from https://github.com/RDFLib/rdflib-sqlalchemy
import unittest
from rdflib import plugin, Graph, Literal, URIRef, BNode, RDF
from rdflib.store import Store

from rdflib_sqlalchemy import registerplugins

class SQLASQLiteGraphTestCase(unittest.TestCase):
    ident = URIRef("rdflib_test")
    uri = Literal("sqlite:////tmp/sqlite-test-db")

    def setUp(self):
        registerplugins()
        store = plugin.get("SQLAlchemy", Store)(identifier=self.ident)
        self.graph = Graph(store, identifier=self.ident)
        self.graph.open(self.uri, create=True)
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
