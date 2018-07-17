import sys, json
from pyld import jsonld

def reformat_type(t):
    return({"uri": "IRI", "literal": "literal", "bnode": "blank node"}[t])

def reformat_value(val):
    return {"type": reformat_type(val["type"]), "value": val["value"]}

def reformat_node(node):
    return dict([(name, reformat_value(val)) for name, val in node.items()])

result_data = json.loads(sys.stdin.read())

if result_data["head"]["vars"] != ["subject", "predicate", "object"]:
    raise Exception("result not in s/p/o format")

result = {"@default": map(reformat_node, result_data["results"]["bindings"])}

print json.dumps(jsonld.from_rdf(result), indent=4)

