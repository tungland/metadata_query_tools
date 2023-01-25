"""Tools for querying the Norwegian National Bibliography Marc 21
"""
from api import metadata_query

def tuple_to_json(tup, limit = 5):
    """Takes tuple on the form:
    ("100", "a", "Ibsen", ind1 = "1", ind2 = "")

    :param tup: _description_
    :type tup: _type_
    """
    
    field = tup[0]
    subfield = tup[1]
    value = tup[2]
    ind1 = False
    ind2 = False
    if len(tup) == 5:
        ind1 = tup[3]
        ind2 = tup[4]
        
    dct = {
        "conditions" : [{
    "field" : field,
    "subfields" : [{
            subfield : value
        }],
    "regex" : True
        }],
        "limit" : limit
    } 
    
    if ind1 and ind2:
        dct.update({
            "ind1" : ind1,
            "ind2" : ind2
            })
        
    return dct  

def query(*query_tpls):
    for tpl in query_tpls:
        
   
   
   query_json = tuple_to_json(query_tpl) 
   return metadata_query(query_json) 
    