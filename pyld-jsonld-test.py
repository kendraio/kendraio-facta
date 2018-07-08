import json

def fmt(x):
    return json.dumps(x, indent=4, sort_keys=True)


data = [
    {
        "ical:summary": "Lady Gaga Concert",
        "ical:location": "New Orleans Arena, New Orleans, Louisiana, USA",
        "ical:dtstart": "2011-04-09T20:00Z"
    },
    {
        "ical:summary": "Hawkwind Concert",
        "ical:location": "Finsbury Park",
        "ical:dtstart": "2011-04-09T20:00Z",
        "@id": "http://dfgdsfgdfg"
    }
    ]
    

context =   { "@context": {
    "ical": "http://www.w3.org/2002/12/cal/ical#",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
    "ical:dtstart": {
      "@type": "xsd:dateTime"
    }
  }}


from pyld import jsonld

compacted = jsonld.compact(data, context)
print fmt(compacted)

doc = fmt(jsonld.expand(compacted))

rdf = jsonld.normalize(compacted)

print fmt(rdf)

print fmt(jsonld.compact(jsonld.from_rdf(rdf), context))

exit()

from rdflib import Graph, plugin
from rdflib.serializer import Serializer

g = Graph().parse(data=doc, format='json-ld')

print g

print(g.serialize(format='nt', indent=4))
