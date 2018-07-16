# kendraio-facta
Assertion repository

Schema for raw storage for statements:

  create table received_statements (
      id bigserial primary key,
      time timestamp with time zone,
      subject varchar,
      statement json,
      sha256_hash varchar);

To run the listener, run as

  cat [credentials-file] | nohup sudo -u [facta-daemon-username] ./test-facta-server.py [internal-port#]

to run the client test program run:

  python test-facta-client.py [API URI] [authorization-token]

To remove the entire contents of the semantic store:

  cat [credentials-file] | sudo -u [facta-daemon-username] python ./delete-all-facta-semantic-data.py [semanttic-store-name]

Note that if you do the above with store name "release_version_semantic_store", you will blow away the semantic store for the live API instance

To do: integrate pyld/jsonld functionality with RDFlib

