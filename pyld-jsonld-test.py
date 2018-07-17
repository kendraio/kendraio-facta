import json, pyaml

def fmt(x):
    return json.dumps(x, indent=4, sort_keys=True)


data = [
    {
        "@type": "kf:Gig",
        "@id": "kf:000001",
        "ical:summary": "Lady Gaga Concert",
        "ical:dtstart": "2011-04-09T20:00Z",
        "kf:venue": "kf:NYA"
    },
    {
        "@type": "kf:Gig",
        "ical:summary": "Hawkwind Concert",
        "ical:dtstart": "2011-04-09T20:00Z",
        "kf:venue": "kf:FPARK",
        "kf:testing": { "testing2:something": "that"},
        "@id": "http://dfgdsfgdfg.example/1"
    },
    {
        "@type": "kf:Gig",
        "ical:summary": "QOTSA Concert",
        "ical:dtstart": "2018-07-09T20:00Z",
        "kf:venue": "kf:FPARK",
        "@id": "http://dfgdsfgdfg.example/2"
    },
    {
        "@type": "kf:KLocation",
        "@id": "kf:NYA",
        "ical:location": "New Orleans Arena, New Orleans, Louisiana, USA",
    },
    {
        "@type": "kf:KLocation",
        "@id": "kf:FPARK",
        "ical:location": "Finsbury Park",
    }
]
    

context =   {
    "@context": {
        "ical": "http://www.w3.org/2002/12/cal/ical#",
        "xsd": "http://www.w3.org/2001/XMLSchema#",
        "kf": "http://facta.kendra.io/vocab#",
        "@vocab": "http://facta.kendra.io/vocab#",
        "kf:venue": {"@type": "@id"},
        "ical:dtstart": {
            "@type": "xsd:dateTime"
        }
    }
}


frame = {
    "@context": {"@vocab": "http://facta.kendra.io/vocab#",
                 "ical": "http://www.w3.org/2002/12/cal/ical#",
    },
    "@type": "Gig",
    "venue":{
        "@type": "KLocation"
        }
}

rev_frame = {
    "@context": {"@vocab": "http://facta.kendra.io/vocab#",
                 "ical": "http://www.w3.org/2002/12/cal/ical#",
                 "hosts": {"@reverse": "venue"}
    },
    "@type": "KLocation",
    "hosts":{
        "@type": "Gig"
        }
}

from pyld import jsonld

compacted = jsonld.compact(data, context)
print fmt(compacted)

doc = fmt(jsonld.expand(compacted))

rdf = jsonld.normalize(compacted)

print "Normalized"
print fmt(rdf)

print "Compacted"
print fmt(jsonld.compact(jsonld.from_rdf(rdf), context))

print "Framed"
print fmt(jsonld.frame(compacted, frame))

print "Reverse framed"
print fmt(jsonld.frame(compacted, rev_frame))

# usual caveats re YAML safety here..
print "YAML"
print pyaml.dump(jsonld.frame(compacted, frame), indent=4)

exit()

from rdflib import Graph, plugin
from rdflib.serializer import Serializer

g = Graph().parse(data=doc, format='json-ld')

print g

print(g.serialize(format='nt', indent=4))
