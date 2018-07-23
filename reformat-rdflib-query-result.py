import sys, json
from pyld import jsonld

def reformat_value(val):
    typ = ({"uri": "IRI",
            "typed-literal": "literal",
            "literal": "literal",
            "bnode": "blank node"}[val["type"]])
    if typ == "literal":
        datatype = val.get("datatype", "http://www.w3.org/2001/XMLSchema#string")
        return {"type": typ, "value": val["value"], "datatype": datatype}
    else:
        return {"type": typ, "value": val["value"]}

def reformat_node(node):
    return dict([(name, reformat_value(val)) for name, val in node.items()])

result_data = json.loads(sys.stdin.read())["result"]

# print json.dumps(result_data, indent=4)

if result_data["head"]["vars"] != ["subject", "predicate", "object"]:
    raise Exception("result not in s/p/o format")

result = {"@default": map(reformat_node, result_data["results"]["bindings"])}

context =  {
    "@context": {
        "@vocab": "http://facta.kendra.io/vocab#",
        "kv": "http://facta.kendra.io/vocab#",
        "kendra": "http://kendra.io/types#",
        "kuid": "http://kendra.io/uuid#",
        "schema": "http://schema.org/"
    }
}

# print json.dumps(result, indent=4)
print json.dumps(jsonld.compact(jsonld.from_rdf(result), context), indent=4)

