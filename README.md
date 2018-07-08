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

To do: integrate pyld/jsonld functionality with RDFlib

