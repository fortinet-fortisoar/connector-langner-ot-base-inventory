"""
Copyright start
MIT License
Copyright (c) 2024 Fortinet Inc
Copyright end
"""

import requests, json
from connectors.core.connector import ConnectorError, get_logger

logger = get_logger('langner-ot-base-inventory')

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


class LangnerOTBase(object):
    def __init__(self, config, *args, **kwargs):
        self.username = config.get('username')
        self.password = config.get('password')
        url = config.get('server_url').strip('/')
        if not url.startswith('https://') and not url.startswith('http://'):
            self.base_url = 'https://{0}/ot-base/api/v1/'.format(url)
        else:
            self.base_url = url + '/ot-base/api/v1/'
        self.verify_ssl = config.get('verify_ssl')

    def make_rest_call(self, endpoint, method, data=None, params=None):
        try:
            url = self.base_url + endpoint
            logger.debug("Endpoint {0}".format(url))
            response = requests.request(method, url, data=data, params=params, auth=(self.username, self.password),
                                        headers=headers,
                                        verify=self.verify_ssl)
            logger.debug("response_content {0}:{1}".format(response.status_code, response.content))
            if response.ok or response.status_code == 204:
                logger.info('Successfully got response for url {0}'.format(url))
                if 'json' in str(response.headers):
                    return response.json()
                else:
                    return response
            elif response.status_code == 404:
                return response
            else:
                logger.error("{0}".format(response.status_code))
                raise ConnectorError("{0}:{1}".format(response.status_code, response.content))
        except requests.exceptions.SSLError:
            raise ConnectorError('SSL certificate validation failed')
        except requests.exceptions.ConnectTimeout:
            raise ConnectorError('The request timed out while trying to connect to the server')
        except requests.exceptions.ReadTimeout:
            raise ConnectorError(
                'The server did not send any data in the allotted amount of time')
        except requests.exceptions.ConnectionError:
            raise ConnectorError('Invalid Credentials')
        except Exception as err:
            raise ConnectorError(str(err))


def check_payload(payload):
    result = {}
    for k, v in payload.items():
        if isinstance(v, dict):
            x = check_payload(v)
            if len(x.keys()) > 0:
                result[k] = x
        elif isinstance(v, list):
            p = []
            for c in v:
                if isinstance(c, dict):
                    x = check_payload(c)
                    if len(x.keys()) > 0:
                        p.append(x)
                elif c is not None and c != '':
                    p.append(c)
            if p != []:
                result[k] = p
        elif v is not None and v != '':
            result[k] = v
    return result


def get_devices_list(config, params):
    lan = LangnerOTBase(config)
    endpoint = 'devices'
    include = params.get('include')
    if include:
        for data in include:
            include = "".join(data.lower())
        params.update({'include': include})
    payload = check_payload(params)
    response = lan.make_rest_call(endpoint, 'GET', params=payload)
    return response


def get_device_details(config, params):
    lan = LangnerOTBase(config)
    endpoint = 'devices/{0}'.format(params.get('device_id'))
    include = params.get('include')
    if include:
        for data in include:
            include = "".join(data.lower())
        params.update({'include': include})
    payload = check_payload(params)
    response = lan.make_rest_call(endpoint, 'GET', params=payload)
    return response


def delete_device_details(config, params):
    lan = LangnerOTBase(config)
    endpoint = 'devices/{0}'.format(params.get('device_id'))
    response = lan.make_rest_call(endpoint, 'DELETE')
    if response:
        return {'message': 'Successfully deleted device: {0}'.format(params.get('device_id'))}


def get_vulnerabilities_list(config, params):
    lan = LangnerOTBase(config)
    endpoint = 'vulnerabilities'
    priority = params.get('priority')
    if priority:
        for data in priority:
            priority = "".join(data.lower())
        params.update({'priority': priority})
    payload = check_payload(params)
    response = lan.make_rest_call(endpoint, 'GET', params=payload)
    return response


def get_vulnerability_details(config, params):
    lan = LangnerOTBase(config)
    endpoint = 'vulnerabilities/{0}'.format(params.get('cve_id'))
    response = lan.make_rest_call(endpoint, 'GET')
    return response


def get_data_flow(config, params):
    lan = LangnerOTBase(config)
    endpoint = 'dataflow'
    payload = check_payload(params)
    response = lan.make_rest_call(endpoint, 'GET', params=payload)
    return response


def get_network_list(config, params):
    lan = LangnerOTBase(config)
    endpoint = 'networks'
    payload = check_payload(params)
    response = lan.make_rest_call(endpoint, 'GET', params=payload)
    return response


def get_network_details(config, params):
    lan = LangnerOTBase(config)
    endpoint = 'networks/{0}'.format(params.get('network_id'))
    response = lan.make_rest_call(endpoint, 'GET')
    return response


def custom_endpoint(config, params):
    endpoint = params.get('endpoint')
    body = params.get('body')
    method = params.get('method')
    if method == "GET":
        payload = check_payload(body)
        data = None
    else:
        data = json.dumps(check_payload(body))
        payload = None
    response = requests.request(method=method, url=endpoint, auth=(config.get('username'), config.get('password')),
                                headers=headers, params=payload, data=data, verify=config.get('verify_ssl'))
    return response.json()


def _check_health(config):
    try:
        response = get_devices_list(config, params={})
        if response.ok:
            return True
        else:
            raise ConnectorError('Invalid Credentials!')
    except Exception as err:
        raise ConnectorError('Invalid Credentials!')


operations = {
    'get_devices_list': get_devices_list,
    'get_device_details': get_device_details,
    'delete_device_details': delete_device_details,
    'get_vulnerabilities_list': get_vulnerabilities_list,
    'get_vulnerability_details': get_vulnerability_details,
    'get_data_flow': get_data_flow,
    'get_network_list': get_network_list,
    'get_network_details': get_network_details,
    'custom_endpoint': custom_endpoint
}
