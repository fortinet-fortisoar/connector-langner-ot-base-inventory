"""
Copyright start
MIT License
Copyright (c) 2024 Fortinet Inc
Copyright end
"""

import os
import sys
import json
import pytest
import inspect
import logging
import requests
import importlib
from connectors.core.connector import ConnectorError

# Removing "Invalid" types usecases, Since the API is responding with ok status even if the parameter is wrong
with open('tests/config_and_params.json', 'r') as file:
    params = json.load(file)

current_directory = os.path.dirname(__file__)
parent_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
grandparent_directory = os.path.abspath(os.path.join(parent_directory, os.pardir))
sys.path.insert(0, str(grandparent_directory))

with open('info.json', 'r') as file:
    info_json = json.load(file)

module_name = 'otbase-inventory_1_1_0.connector'
connector_module = importlib.import_module(module_name)
connector_classes = inspect.getmembers(connector_module, inspect.isclass)
for name, cls in connector_classes:
    if cls.__module__ == module_name:
        connector_instance = cls(info_json=info_json)

logger = logging.getLogger(__name__)


# To test with different configuration values, update the code below.
@pytest.fixture(scope="session")
def valid_configuration():
    conn_config = params.get('config')[0].copy()
    connector_label = info_json.get('label')
    connector_name = info_json.get('name')
    connector_version = info_json.get('version')
    get_connectors = requests.request('GET', f'http://localhost:8000/integration/connectors?search={connector_label}')
    connectors = get_connectors.json()
    connector_id = ''
    if connectors.get('totalItems') > 0:
        for connector in connectors.get('data'):
            if connector.get('name') == connector_name and connector.get('version') == connector_version:
                connector_id = connector.get('id')
    payload = {
        "connector": connector_id,
        "name": "pytest_config",
        "config": conn_config
    }
    add_config = requests.request('POST', f'http://localhost:8000/integration/configuration/?format=json', json=payload)
    config = add_config.json()
    delete_config = config.get('id')
    params.get('config')[0].update({"config_id": config.get('config_id')})
    yield params.get('config')[0]
    requests.request('DELETE', f'http://localhost:8000/integration/configuration/{delete_config}/?format=json')


@pytest.fixture(scope="session")
def valid_configuration_with_token(valid_configuration):
    config = valid_configuration.copy()
    connector_instance.check_health(config)
    return config


@pytest.mark.check_health
def test_check_health_success(valid_configuration):
    config = valid_configuration.copy()
    result = connector_instance.check_health(config)
    logger.info(result)


@pytest.mark.check_health
def test_check_health_invalid_server_url(valid_configuration):
    invalid_config = valid_configuration.copy()
    invalid_config['server_url'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        result = connector_instance.check_health(invalid_config)
        logger.info(result)


@pytest.mark.check_health
def test_check_health_invalid_username(valid_configuration):
    invalid_config = valid_configuration.copy()
    invalid_config['username'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        result = connector_instance.check_health(invalid_config)
        logger.info(result)


@pytest.mark.check_health
def test_check_health_invalid_pfx_path(valid_configuration):
    invalid_config = valid_configuration.copy()
    invalid_config['pfx_path'] = params.get('invalid_params')['text']
    with pytest.raises(ConnectorError):
        result = connector_instance.check_health(invalid_config)
        logger.info(result)


@pytest.mark.check_health
def test_check_health_invalid_pfx_password(valid_configuration):
    invalid_config = valid_configuration.copy()
    invalid_config['pfx_password'] = params.get('invalid_params')['password']
    with pytest.raises(ConnectorError):
        result = connector_instance.check_health(invalid_config)
        logger.info(result)


@pytest.mark.check_health
def test_check_health_invalid_password(valid_configuration):
    invalid_config = valid_configuration.copy()
    invalid_config['password'] = params.get('invalid_params')['password']
    with pytest.raises(ConnectorError):
        result = connector_instance.check_health(invalid_config)
        logger.info(result)


@pytest.mark.get_devices_list
@pytest.mark.parametrize("input_params", params['get_devices_list'])
def test_get_devices_list_success(valid_configuration_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    result = connector_instance.execute(valid_configuration_with_token.copy(), 'get_devices_list', input_params.copy())
    logger.info(result)
    assert result


# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# Add logic for validating conditional_output_schema or if schema is other than dict.
@pytest.mark.get_devices_list
@pytest.mark.schema_validation
def test_validate_get_devices_list_output_schema(valid_configuration_with_token):
    input_params = params.get('get_devices_list')[0].copy()
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'get_devices_list':
            if "conditional_output_schema" in operation or "api_output_schema" in operation:
                pytest.skip("Skipping test because conditional_output_schema or api_output_schema is not supported.")
            else:
                schema = operation.get('output_schema')
            break
    resp = connector_instance.execute(valid_configuration_with_token.copy(), 'get_devices_list', input_params)
    if isinstance(schema, dict) and isinstance(resp, dict):
        logger.info("output_schema: {0} \n API_response: {1}".format(schema, resp))
        assert resp.keys() == schema.keys()
    else:
        pytest.skip("Skipping test because output_schema is not a dict.")


@pytest.mark.get_device_details
@pytest.mark.parametrize("input_params", params['get_device_details'])
def test_get_device_details_success(valid_configuration_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    result = connector_instance.execute(valid_configuration_with_token.copy(), 'get_device_details',
                                        input_params.copy())
    logger.info(result)
    assert result


# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# Add logic for validating conditional_output_schema or if schema is other than dict.
@pytest.mark.get_device_details
@pytest.mark.schema_validation
def test_validate_get_device_details_output_schema(valid_configuration_with_token):
    input_params = params.get('get_device_details')[0].copy()
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'get_device_details':
            if "conditional_output_schema" in operation or "api_output_schema" in operation:
                pytest.skip("Skipping test because conditional_output_schema or api_output_schema is not supported.")
            else:
                schema = operation.get('output_schema')
            break
    resp = connector_instance.execute(valid_configuration_with_token.copy(), 'get_device_details', input_params)
    if isinstance(schema, dict) and isinstance(resp, dict):
        logger.info("output_schema: {0} \n API_response: {1}".format(schema, resp))
        assert resp.keys() == schema.keys()
    else:
        pytest.skip("Skipping test because output_schema is not a dict.")


@pytest.mark.get_vulnerabilities_list
@pytest.mark.parametrize("input_params", params['get_vulnerabilities_list'])
def test_get_vulnerabilities_list_success(valid_configuration_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    result = connector_instance.execute(valid_configuration_with_token.copy(), 'get_vulnerabilities_list',
                                        input_params.copy())
    logger.info(result)
    assert result


# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# Add logic for validating conditional_output_schema or if schema is other than dict.
@pytest.mark.get_vulnerabilities_list
@pytest.mark.schema_validation
def test_validate_get_vulnerabilities_list_output_schema(valid_configuration_with_token):
    input_params = params.get('get_vulnerabilities_list')[0].copy()
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'get_vulnerabilities_list':
            if "conditional_output_schema" in operation or "api_output_schema" in operation:
                pytest.skip("Skipping test because conditional_output_schema or api_output_schema is not supported.")
            else:
                schema = operation.get('output_schema')
            break
    resp = connector_instance.execute(valid_configuration_with_token.copy(), 'get_vulnerabilities_list', input_params)
    if isinstance(schema, dict) and isinstance(resp, dict):
        logger.info("output_schema: {0} \n API_response: {1}".format(schema, resp))
        assert resp.keys() == schema.keys()
    else:
        pytest.skip("Skipping test because output_schema is not a dict.")


@pytest.mark.get_vulnerability_details
@pytest.mark.parametrize("input_params", params['get_vulnerability_details'])
def test_get_vulnerability_details_success(valid_configuration_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    result = connector_instance.execute(valid_configuration_with_token.copy(), 'get_vulnerability_details',
                                        input_params.copy())
    logger.info(result)
    assert result


# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# Add logic for validating conditional_output_schema or if schema is other than dict.
@pytest.mark.get_vulnerability_details
@pytest.mark.schema_validation
def test_validate_get_vulnerability_details_output_schema(valid_configuration_with_token):
    input_params = params.get('get_vulnerability_details')[0].copy()
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'get_vulnerability_details':
            if "conditional_output_schema" in operation or "api_output_schema" in operation:
                pytest.skip("Skipping test because conditional_output_schema or api_output_schema is not supported.")
            else:
                schema = operation.get('output_schema')
            break
    resp = connector_instance.execute(valid_configuration_with_token.copy(), 'get_vulnerability_details', input_params)
    if isinstance(schema, dict) and isinstance(resp, dict):
        logger.info("output_schema: {0} \n API_response: {1}".format(schema, resp))
        assert resp.keys() == schema.keys()
    else:
        pytest.skip("Skipping test because output_schema is not a dict.")


@pytest.mark.get_data_flow
@pytest.mark.parametrize("input_params", params['get_data_flow'])
def test_get_data_flow_success(valid_configuration_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    result = connector_instance.execute(valid_configuration_with_token.copy(), 'get_data_flow', input_params.copy())
    logger.info(result)
    assert result


# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# Add logic for validating conditional_output_schema or if schema is other than dict.
@pytest.mark.get_data_flow
@pytest.mark.schema_validation
def test_validate_get_data_flow_output_schema(valid_configuration_with_token):
    input_params = params.get('get_data_flow')[0].copy()
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'get_data_flow':
            if "conditional_output_schema" in operation or "api_output_schema" in operation:
                pytest.skip("Skipping test because conditional_output_schema or api_output_schema is not supported.")
            else:
                schema = operation.get('output_schema')
            break
    resp = connector_instance.execute(valid_configuration_with_token.copy(), 'get_data_flow', input_params)
    if isinstance(schema, dict) and isinstance(resp, dict):
        logger.info("output_schema: {0} \n API_response: {1}".format(schema, resp))
        assert resp.keys() == schema.keys()
    else:
        pytest.skip("Skipping test because output_schema is not a dict.")


@pytest.mark.get_network_list
@pytest.mark.parametrize("input_params", params['get_network_list'])
def test_get_network_list_success(valid_configuration_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    result = connector_instance.execute(valid_configuration_with_token.copy(), 'get_network_list', input_params.copy())
    logger.info(result)
    assert result


# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# Add logic for validating conditional_output_schema or if schema is other than dict.
@pytest.mark.get_network_list
@pytest.mark.schema_validation
def test_validate_get_network_list_output_schema(valid_configuration_with_token):
    input_params = params.get('get_network_list')[0].copy()
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'get_network_list':
            if "conditional_output_schema" in operation or "api_output_schema" in operation:
                pytest.skip("Skipping test because conditional_output_schema or api_output_schema is not supported.")
            else:
                schema = operation.get('output_schema')
            break
    resp = connector_instance.execute(valid_configuration_with_token.copy(), 'get_network_list', input_params)
    if isinstance(schema, dict) and isinstance(resp, dict):
        logger.info("output_schema: {0} \n API_response: {1}".format(schema, resp))
        assert resp.keys() == schema.keys()
    else:
        pytest.skip("Skipping test because output_schema is not a dict.")


@pytest.mark.get_network_details
@pytest.mark.parametrize("input_params", params['get_network_details'])
def test_get_network_details_success(valid_configuration_with_token, input_params):
    logger.info("params: {0}".format(input_params))
    result = connector_instance.execute(valid_configuration_with_token.copy(), 'get_network_details',
                                        input_params.copy())
    logger.info(result)
    assert result


# Ensure that the provided input_params yield the correct output schema, or adjust the index in the list below.
# Add logic for validating conditional_output_schema or if schema is other than dict.
@pytest.mark.get_network_details
@pytest.mark.schema_validation
def test_validate_get_network_details_output_schema(valid_configuration_with_token):
    input_params = params.get('get_network_details')[0].copy()
    schema = {}
    for operation in info_json.get("operations"):
        if operation.get('operation') == 'get_network_details':
            if "conditional_output_schema" in operation or "api_output_schema" in operation:
                pytest.skip("Skipping test because conditional_output_schema or api_output_schema is not supported.")
            else:
                schema = operation.get('output_schema')
            break
    resp = connector_instance.execute(valid_configuration_with_token.copy(), 'get_network_details', input_params)
    if isinstance(schema, dict) and isinstance(resp, dict):
        logger.info("output_schema: {0} \n API_response: {1}".format(schema, resp))
        assert resp.keys() == schema.keys()
    else:
        pytest.skip("Skipping test because output_schema is not a dict.")