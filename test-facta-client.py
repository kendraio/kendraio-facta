#!/usr/bin/python
import requests, sys, json

try:
    target_uri = sys.argv[1]
    authtoken = sys.argv[2]
except:
    print >> sys.stderr, "Usage: python test-facta-client.py [target URI] [JWT token]"
    exit(1)

statements = [
    {"@context": "https://kendra.io/schema/v1",
     "@id": "000001",
     "@type": "test-statement",
     "salutation": "hello",
     "subject": "world"
    }
]

print requests.post(target_uri,
                    headers={'authorization': 'Bearer %s' % authtoken},
                    json=statements).json()
