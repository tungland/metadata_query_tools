import os
import requests

BASEPATH = "https://api.nb.no/dhlab"

def metadata_query(params):
    """_summary_

    :param params: _description_
    :type params: _type_
    :return: _description_
    :rtype: _type_
    """
    return requests.post("https://api.nb.no/dhlab/metadata_query", json=params).json()


def metadata_from_urn(urns):
    """Get Marc 21 json records for urns.
    Query on the form:
    {
        urns :  [URN:123154, URN:5425 ... ]
    }

    :param params: query
    :type params: json
    :return: requests
    :rtype: requests object
    """
    params = {"urns" : urns}
    return requests.post("https://api.nb.no/dhlab/metadata_from_urn", json=params).json()