import json

def fmt(x):
    return json.dumps(x, indent=4, sort_keys=True)


data = {
    "@context": {
        "@vocab": "http://example.org/",
        "contains": {"@type": "@id"}
    },
    "@graph": [{
        "@id": "http://example.org/library",
        "@type": "Library",
        "contains": "http://example.org/library/the-republic"
    }, {
        "@id": "http://example.org/library/the-republic",
        "@type": "Book",
        "creator": "Plato",
        "title": "The Republic",
        "contains": "http://example.org/library/the-republic#introduction"
    }, {
        "@id": "http://example.org/library/the-republic#introduction",
        "@type": "Chapter",
        "description": "An introductory chapter on The Republic.",
        "title": "The Introduction"
    }]
}

from pyld import jsonld

rdf = jsonld.normalize(data)

print "Normalized"
print fmt(rdf)

frame = {
    "@context": {"@vocab": "http://example.org/"},
    "@type": "Library",
    "contains": {
          "@type": "Book",
          "contains": {
                  "@type": "Chapter"
              }
      }
}

print "Framed"
print fmt(jsonld.frame(jsonld.from_rdf(rdf), frame))

