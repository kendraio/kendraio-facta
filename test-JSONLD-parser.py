#!/usr/bin/python
import requests, sys, json

# adapted from https://github.com/RDFLib/rdflib-sqlalchemy
from rdflib import plugin, Graph, Literal, URIRef, BNode, RDF
from rdflib.store import Store

from rdflib_sqlalchemy import registerplugins

from StringIO import StringIO

statements = [
        {    "@context": {
                    "@language": "en",
                    "@vocab": "http://kendra.io/terms/"
                },
                 "@id": "http://kendra.io/000001",
                 "@type": "http://kendra.io/test-statement",
                 "name": "hello",
                 "description": "world"
                }
    ]

statements2 = [{
    "@id": "http://example.org/0000001",
    "http://purl.org/dc/terms/title": [
        {
            "@language": "en",
            "@value": "Someone's Homepage"
        }
    ]
}
]

statements3 = [{
    "@id": "http://example.org/0000001",
    "http://example.org/salutation": "hello"
}
]

def test():
    graph = Graph()
    
    for s in statements:
        print "parsing", json.dumps(s)
        graph.parse(StringIO(json.dumps(s)), format="json-ld")
        
    print graph.serialize(format="json-ld")
    print graph.serialize(format="n3")
    graph.close()

    
test()
