import requests
import json


def http_request(verb, url, headers, payload=None):
    request = getattr(requests, verb.lower())

    if verb.lower() in ['post', 'put']:
        response = request(url, headers=headers, data=json.dumps(payload))
    else:
        response = request(url, headers=headers)

    if response.status_code in [404]:
        return response

    response.raise_for_status()
    return response
