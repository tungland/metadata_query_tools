from configparser import ConfigParser
from pymongo import MongoClient

DB = "nasjonalbibliografien4_test"
COLLECTION = "records"

def connect():
    config = ConfigParser()
    config.read("config.cfg")    
    
    client = MongoClient(
                    config["fulltekst_api"]['host'],
                    username=config["fulltekst_api"]['username'],
                    password=config["fulltekst_api"]['pwd'],
                    authSource=config["fulltekst_api"]['authSource'])

    return client

class MetadataQuery():
    """
    Query form:
    [
        {
            "field" : "100",
            "subfield" : "a",
            "value" : "Ibsen"
        },
        {
            "field" : "100",
            "subfield" : "d",
            "value" : "1828"
        }
    ]
    
    
    """
    def __init__(self, params):
        
        # parse params
        jsn = [self._create_con(x) for x in params["conditions"]]
        self.conditions = self._combine(jsn)
        self.limit = params.get("limit", 5)
        
        self.collection = connect()[DB][COLLECTION]
        
        #self.query_dct = 
        #return self.query()

    def _create_con(self, condition_lst):
        dct = {
            "field" : condition_lst[0], 
            "subfield" : condition_lst[1], 
            "value" : condition_lst[2]
        }
        if len(condition_lst) > 3:
            dct.update({
                "ind1" : condition_lst[3],
                "ind2" : condition_lst[4]
                })
        
        return dct
        
    def _elem_match(self, conditions):
        """elemMatch query

        :param conditions: _description_
        :type conditions: _type_
        :return: _description_
        :rtype: _type_
        """
        dct = {
            "fields" : {
            "$elemMatch" : {
                f"{conditions['field']}.subfields.{conditions['subfield']}" : 
                    {"$regex" : conditions["value"]}
                            }    
                        }
                }
        
        if "ind1" in conditions:
            dct["fields"].update({"ind1" : conditions["ind1"]})
        if "ind2" in conditions:
            dct["fields"].update({"ind2" : conditions["ind2"]})
            
        return dct
        
    def _combine(self, conditions):
        """Combine elemMatch query conditions

        :return: _description_
        :rtype: _type_
        """
        base = {"$and" : []}
        
        for condition in conditions:
            base["$and"].append(self._elem_match(condition))

        return base
        
    def query(self):
        
        result = self.collection.find(
            self.conditions,
            {"_id" : 0, "urn": 1}
        ).limit(self.limit)
        
        return [x["urn"] for x in result]

def metadata_from_urn(urn_list):
    records = connect()
    
    result_list = list()
    
    for urn in urn_list:
        res = records.find_one(
            {
                "urn" : urn
            },
            {"_id" : False}
        )
        result_list.append(res)
        
    return result_list
    