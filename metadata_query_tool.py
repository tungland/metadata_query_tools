import os
import requests

BASEPATH = "https://api.nb.no/dhlab"

def api_call_deco(service):
    """Decorator for calling a service from DH-lab API

    :param service: Name of service
    """
    def inner_decorator(func):
        """Inner decorator

        :param func: function to decorate. Must return params
        """
        def wrapper(*args, **kwargs):
            params = func(*args, **kwargs)        
            return requests.post(os.path.join(BASEPATH, service), json=params).json()
        return wrapper
    return inner_decorator 
    
@api_call_deco("metadata_query")
def metadata_query(conditions, limit=5):    
    params = {
        "conditions" : conditions,
        "limit" : limit
    }
    return params

@api_call_deco("metadata_from_urn")
def metadata_from_urn(urns):
    """Gets MARC 21 json for a URN or list of URN

    :param urns: list of URNs
    :return: API call parameters
    """
    params = {"urns" : urns}
    return params
