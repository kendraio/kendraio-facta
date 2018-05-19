import requests, sys, json

try:
    authtoken = sys.argv[1]
except:
    print >> sys.stderr, "Usage: python test-facta-client.py [JWT token]"
    exit(1)

statements = [
    {"@context": "https://kendra.io/schema/v1",
     "@id": "000001",
     "@type": "test-statement",
     "salutation": "hello",
     "subject": "world"
    }
]

print requests.post("http://localhost:8080/assert",
                    headers={'authorization': 'Bearer %s' % authtoken},
                    json=statements).json()
