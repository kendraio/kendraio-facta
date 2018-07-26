import sys, json
import sparql_to_jsonld as s2j

default_query = json.loads(json.dumps({
    "@type": "quicksearch",
    "match": {
	"@type": "kendra:InclusionRelationship",
	"schema:name": "Dog"
    }
}))

def main():
    context =  {
        "@context": {
            "@vocab": "http://facta.kendra.io/vocab#",
            "kv": "http://facta.kendra.io/vocab#",
            "kendra": "http://kendra.io/types#",
            "kuid": "http://kendra.io/uuid#",
            "schema": "http://schema.org/",
            "xsd": "http://www.w3.org/2001/XMLSchema#"
        }
    }

    compacted_graph, contained = s2j.result_data_to_jsonld(json.loads(sys.stdin.read()), context)

    results = s2j.extract_salient_results(
        compacted_graph,
        contained,
        ["kendra:InclusionRelationship", "kendra:TextSelection"])

    # Apply the very simple "quicksearch" mapper
    results = s2j.quicksearch(results, default_query)
    
    print json.dumps(results, indent=4)

main()
