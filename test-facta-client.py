import requests, sys

try:
    authtoken = sys.argv[1]
except:
    print >> sys.stderr, "Usage: python test-facta-client.py [JWT token]"
    exit(1)

print requests.post("http://localhost:8080/assert", headers={'authorization': 'Bearer %s' % authtoken}, json={'input': 'data'}).json()
