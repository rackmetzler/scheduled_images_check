from datetime import datetime
from datetime import timedelta

from libs.common import http_request


IDENTITY_ENDPOINT = 'https://identity.api.rackspacecloud.com/v2.0/tokens'


def convert_to_datetime(strdatetime, format="%Y-%m-%dT%H:%M:%S.%fZ"):
    return datetime.strptime(strdatetime, format)


def check_expired(dt_expiration, expire_early=10):
    if dt_expiration is None:
        return True

    if not isinstance(dt_expiration, datetime):
        dt_expiration = convert_to_datetime(dt_expiration)

    dt_diff = dt_expiration - datetime.utcnow()
    if dt_diff < timedelta(minutes=expire_early):
        return True
    else:
        return False


class CloudAuth(object):
    def __init__(self, username, apikey, identity_endpoint=IDENTITY_ENDPOINT):
        self.tenant_id = None
        self.identity_endpoint = identity_endpoint
        self.token = None
        self.token_exp = None
        self.service_catalog = None
        self.auth_response = None
        self.username = username
        self.apikey = apikey

    def authenticate(self):
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        data = {
            "auth": {
                "RAX-KSKEY:apiKeyCredentials":
                    {
                        "username": self.username,
                        "apiKey": self.apikey
                    }
            }
        }

        response = http_request('POST', self.identity_endpoint,
                                headers, payload=data)

        self.auth_response = response.json()

        return response

    def get_token(self):
        if not check_expired(self.auth_response['access']['token']['expires']):
            return self.auth_response['access']['token']['id']

        self.authenticate()
        return self.auth_response.get('access', {}).get('token', {}).get('id')

    def get_service_catalog(self, service_type=None, region=None):
        if not self.auth_response:
            self.authenticate()
        service_catalog = None
        if (self.auth_response and
                'serviceCatalog' in self.auth_response['access']):
            service_catalog = \
                self.auth_response['access']['serviceCatalog']

        if service_type is None:
            service_type = ""

        service_type_list_return = []
        for service in service_catalog:
            if service_type != "" and service['type'] != service_type:
                continue
            endpoint_list = []
            for endpoint in service['endpoints']:
                if region is not None:
                    if endpoint.get('region', 'global') == region:
                        endpoint_list.append(endpoint)
                    elif (region.lower() == "global" and
                          'region' not in endpoint):
                        endpoint_list.append(endpoint)
                else:  # region is None
                    endpoint_list.append(endpoint)

            if len(endpoint_list) > 0:
                service_type_list_return.append({
                    'name': service['name'],
                    'type': service['type'],
                    'endpoints': endpoint_list
                })
        if len(service_type_list_return) > 0:
            return service_type_list_return

        return None

    def get_service_url(self, service_type, region):
        serv_cat = self.get_service_catalog(
            service_type=service_type, region=region)

        if len(serv_cat) == 0:
            return None

        return serv_cat[0]['endpoints'][0]['publicURL']

    def get_regions(self, service_type=None):
        regions = []
        service_catalog = self.get_service_catalog()
        if service_type is not None:
            services = [service for service in service_catalog
                        if 'type' in service and
                        service['type'].lower() == service_type.lower()]
            for service in services:
                for endpoint in service['endpoints']:
                    regions.append(
                        endpoint.get('region', 'global')
                    )
        else:
            services = [service for service in service_catalog]
            for service in services:
                for endpoint in service['endpoints']:
                    regions.append(
                        endpoint.get('region', 'global')
                    )

        if len(regions) > 0:
            return list(set(regions))

        return None

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-Auth-Token': self.get_token()
        }
