#!/usr/bin/python
import requests, sys, json

try:
    target_uri = sys.argv[1]
    authtoken = sys.argv[2]
except:
    print >> sys.stderr, "Usage: python test-facta-client.py [target URI] [JWT token]"
    exit(1)

statements = [
        {# "@context": "https://kendra.io/schema/v1",
                 "@id": "http://kendra.io/000001",
                 "@type": "http://kendra.io/test-statement",
                 "http://kendra.io/name": "hello",
                 "http://kendra.io/description": "world"
                }
    ]

print json.dumps(requests.post(target_uri,
                    headers={'authorization': 'Bearer %s' % authtoken},
                              json=statements).json(), sort_keys=True)
