import sys, json, itertools, re
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

def x_of(s, x):
    if type(s) == dict:
        return s.get(x)
    else:
        return None

def id_of(s):
    return x_of(s, "@id")

def type_of(s):
    return x_of(s, "@type")
    
def type_match(s, types):
    return x_of(s, "@type") in types
    
def list_concat(s):
    return list(itertools.chain.from_iterable(s))

# all items with both content and an id, throughout the graph
def contained_items(s):
    if type(s) == list:
        return list_concat([contained_items(ss) for ss in s])
    if type(s) == dict:
        if s.keys() == ["@id"]:
            return []
        else:
            if "@id" in s:
                return [(s["@id"], s)] + list_concat([contained_items(ss) for ss in s.values()])
            else:
                return list_concat([contained_items(ss) for ss in s.values()])
    # otherwise
    return []

def contained_references(s):
    if type(s) == list:
        return list_concat([contained_references(ss) for ss in s])
    if type(s) == dict:
        if s.keys() == ["@id"] and s["@id"]:
            return [(s["@id"], s)]
        else:
            return list_concat([contained_references(ss) for ss in s.values()])
    # otherwise
    return []

# look for various kinds of mangled data -- only for temporary development use
# just look at the text: a bit heuristic, but good enough for purpose
def bad_item(s):
    txt = json.dumps(s)
    if "home/neil" in txt:
        return 1
    if re.findall(r"schema.org[^/]", txt):
        return 1
    # bad IDs without a namespace -- let these through for now, something generates these internally
    # if [x for x in re.findall(r'"@id": "([^"]*)"', txt) if not ":" in x]:
    #    return 1
    return 0

def rewrite_references(s, statement_map):
    if type(s) == list:
        return [rewrite_references(ss, statement_map) for ss in s]
    if type(s) == dict:
        if s.keys() == ["@id"] and s["@id"] in statement_map:
            return rewrite_references(statement_map[s["@id"]], statement_map)
        else:
            return dict([(k, rewrite_references(ss, statement_map)) for k, ss in s.items()])
    # otherwise
    return s

def fix_leaves(s):
    if type(s) == list:
        return [fix_leaves(ss) for ss in s]
    if type(s) == dict:
        if set(s.keys()) == set(["@type", "@value"]):
            if s["@type"] == "xsd:integer":
                return int(s["@value"])
            if s["@type"] == "xsd:double":
                return float(s["@value"])
            return s
        else:
            return dict([(k, fix_leaves(v)) for k, v in s.items()])
    # otherwise
    return s

def filter_bad_ids(s):
    if type(s) == list:
        return [filter_bad_ids(ss) for ss in s]
    if type(s) == dict:
        return dict([(k, filter_bad_ids(v)) for k, v in s.items() if not (k=="@id" and not ":" in v)])
    # otherwise
    return s

def purge_blacklisted(s, blk):
    if type(s) == list:
        return [purge_blacklisted(v, blk) for v in s if id_of(v) not in blk]
    if type(s) == dict:
        return dict([(k, purge_blacklisted(v, blk)) for k, v in s.items() if id_of(v) not in blk])
    # otherwise
    return s

def extract_by_type(s, types):
    if type(s) == list:
        return [v for v in s if type_match(v, types)] + list_concat([extract_by_type(v, types) for v in s if not type_match(v, types)])
    if type(s) == dict:
        return [v for k, v in s.items() if type_match(v, types)] + list_concat([extract_by_type(v, types) for k, v in s.items() if not type_match(v, types)])
    # otherwise
    return []

def extract_salient_results(compacted_graph, contained, valid_types):
    return filter_bad_ids(
        extract_by_type(
            rewrite_references(
                [s for s in compacted_graph],
                contained),
            ["kendra:InclusionRelationship", "kendra:TextSelection"])),

def filter_dict_trees(x, match_fn):
    if type(x) in [list, tuple]:
        return [filter_dict_trees(y, match_fn) for y in x if type(y) != dict or match_fn(y)]
    return x

def get_items_recursive(d):
    if type(d) in [list, tuple]:
        return list_concat([get_items_recursive(v) for v in d])
    if type(d) == dict:
        return ([(k, v) for k, v in d.items() if isinstance(k, basestring) and isinstance(v, basestring)]
                + list_concat([get_items_recursive(v) for k, v in d.items()]))
    return []

# CAUTION: note that a tuple of unicode != tuple of string!!!!
def all_items_in(needed, proposed):
    return len([1 for e in set(proposed) if e in needed]) == len(set(needed))

def quicksearch(results, query):
    if query.get("@type") != "quicksearch":
        return "not a quicksearch"
    needed_pairs = query["match"].items()
    return filter_dict_trees(results,
                        lambda x: all_items_in(needed_pairs, get_items_recursive(x))) 

def result_data_to_jsonld(result_data, context):

    if set(result_data["head"]["vars"]) != set(["subject", "predicate", "object"]):
        raise Exception("result not in s/p/o format")

    result = {"@default": map(reformat_node, result_data["results"]["bindings"])}

    # print json.dumps(result, indent=4)
    compacted_graph = jsonld.compact(jsonld.from_rdf(result), context)["@graph"]
    
    # remove bad data generated by earlier code
    compacted_graph = [fix_leaves(s) for s in compacted_graph if not bad_item(s)]
    
    contained = dict(contained_items(compacted_graph))

    return compacted_graph, contained
    
    
