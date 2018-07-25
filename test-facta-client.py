#!/usr/bin/python
import requests, sys, json

try:
    target_uri = sys.argv[1]
    authtoken = sys.argv[2]
except:
    print >> sys.stderr, "Usage: python test-facta-client.py [target URI] [JWT token]"
    exit(1)

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

if "--stdin" in sys.argv[1:]:
    statements = json.loads(sys.stdin.read())
    
print json.dumps(requests.post(target_uri,
                    headers={'authorization': 'Bearer %s' % authtoken},
                              json=statements).json(), sort_keys=True)
