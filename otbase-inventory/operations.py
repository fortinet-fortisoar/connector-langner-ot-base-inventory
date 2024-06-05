"""
Copyright start
MIT License
Copyright (c) 2024 Fortinet Inc
Copyright end
"""

import json

import requests
import requests_pkcs12
from connectors.core.connector import ConnectorError, get_logger

logger = get_logger("otbase-inventory")

headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


class OTBase(object):
    def __init__(self, config, *args, **kwargs):
        self.username = config.get('username')
        self.password = config.get('password')
        if config.get('pfx_path') is not None:
            self.pfx_path = config.get('pfx_path')
            self.pfx_password = config.get('pfx_password')
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
            # CURL UTILS CODE
            try:
                from connectors.debug_utils.curl_script import make_curl
                make_curl(method, url, headers=headers, params=params, data=data, verify_ssl=self.verify_ssl)
            except Exception as err:
                logger.error(f"Error in curl utils: {str(err)}")

            if self.pfx_path is not None:
                response = requests_pkcs12.request(url=url,
                                                   method=method, auth=(self.username, self.password),
                                                   pkcs12_filename=self.pfx_path,
                                                   pkcs12_password=self.pfx_password,
                                                   verify=self.verify_ssl, data=data, params=params, headers=headers)
            else:
                response = requests.request(method, url, data=data, params=params, auth=(self.username, self.password),
                                            headers=headers,
                                            verify=self.verify_ssl)
            # logger.debug("response_content {0}:{1}".format(response.status_code, response.content))
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
    lan = OTBase(config)
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
    lan = OTBase(config)
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
    lan = OTBase(config)
    endpoint = 'devices/{0}'.format(params.get('device_id'))
    response = lan.make_rest_call(endpoint, 'DELETE')
    if response:
        return {'message': 'Successfully deleted device: {0}'.format(params.get('device_id'))}


def get_vulnerabilities_list(config, params):
    lan = OTBase(config)
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
    lan = OTBase(config)
    endpoint = 'vulnerabilities/{0}'.format(params.get('cve_id'))
    response = lan.make_rest_call(endpoint, 'GET')
    return response


def get_data_flow(config, params):
    lan = OTBase(config)
    endpoint = 'dataflow'
    payload = check_payload(params)
    response = lan.make_rest_call(endpoint, 'GET', params=payload)
    return response


def get_network_list(config, params):
    lan = OTBase(config)
    endpoint = 'networks'
    payload = check_payload(params)
    response = lan.make_rest_call(endpoint, 'GET', params=payload)
    return response


def get_network_details(config, params):
    lan = OTBase(config)
    endpoint = 'networks/{0}'.format(params.get('network_id'))
    response = lan.make_rest_call(endpoint, 'GET')
    return response


def custom_endpoint(config, params):
    lan = OTBase(config)
    endpoint = params.pop('endpoint')
    method = params.pop('method')
    body = params.pop('body')
    if method == "GET":
        payload = body
        data = None
    else:
        data = json.dumps(body)
        payload = None
    response = lan.make_rest_call(endpoint, method=method, params=payload, data=data)
    return response


def _check_health(config):
    try:
        get_devices_list(config, params={})
        return True
    except Exception as err:
        raise ConnectorError(f'Error in Check Health {err}')


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