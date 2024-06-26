## About the connector
Enterprise-grade OT asset management software. OTbase is the gold standard for large scale OT asset inventories. It inventories OT devices from PLCs over network switches to sensors and actuators and integrates nicely with your existing tools and platforms.
<p>This document provides information about the OTbase Inventory Connector, which facilitates automated interactions, with a OTbase Inventory server using FortiSOAR&trade; playbooks. Add the OTbase Inventory Connector as a step in FortiSOAR&trade; playbooks and perform automated operations with OTbase Inventory.</p>
### Version information

Connector Version: 1.1.0

FortiSOAR&trade; Version Tested on: 7.4.1-3167

OTbase Inventory Version Tested on: 

Authored By: Fortinet

Certified: Yes
## Installing the connector
<p>Use the <strong>Content Hub</strong> to install the connector. For the detailed procedure to install a connector, click <a href="https://docs.fortinet.com/document/fortisoar/0.0.0/installing-a-connector/1/installing-a-connector" target="_top">here</a>.</p><p>You can also use the <code>yum</code> command as a root user to install the connector:</p>
<pre>yum install cyops-connector-otbase-inventory</pre>

## Prerequisites to configuring the connector
- You must have the credentials of OTbase Inventory server to which you will connect and perform automated operations.
- The FortiSOAR&trade; server should have outbound connectivity to port 443 on the OTbase Inventory server.

## Minimum Permissions Required
- Not applicable

## Configuring the connector
For the procedure to configure a connector, click [here](https://docs.fortinet.com/document/fortisoar/0.0.0/configuring-a-connector/1/configuring-a-connector)
### Configuration parameters
<p>In FortiSOAR&trade;, on the Connectors page, click the <strong>OTbase Inventory</strong> connector row (if you are in the <strong>Grid</strong> view on the Connectors page) and in the <strong>Configurations</strong> tab enter the required configuration details:</p>
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Server URL</td><td>Specify the URL of the OTbase Inventory server to connect and perform automated operations.
</td>
</tr><tr><td>Username</td><td>Specify the username to access the OTbase Inventory server to connect and perform automated operations.
</td>
</tr><tr><td>Password</td><td>Specify the password to access the OTbase Inventory server to connect and perform automated operations.
</td>
</tr><tr><td>PFX Path</td><td>Specify the path to PFX file(Personal Information Exchange) to access the OTbase Inventory server to connect and perform automated operations. Ex: /tmp/{pfx-file-name}
</td>
</tr><tr><td>PFX Password</td><td>Specify the password of PFX file(Personal Information Exchange) to access the OTbase Inventory server to connect and perform automated operations.
</td>
</tr><tr><td>Verify SSL</td><td>Specifies whether the SSL certificate for the server is to be verified or not. <br/>By default, this option is set to True.</td></tr>
</tbody></table>
## Actions supported by the connector
The following automated operations can be included in playbooks and you can also use the annotations to access operations from FortiSOAR&trade; release 4.10.0 and onwards:
<table border=1><thead><tr><th>Function</th><th>Description</th><th>Annotation and Category</th></tr></thead><tbody><tr><td>Get Devices List</td><td>Retrieves a list of devices from OTbase Inventory based on the input parameters you have specified.</td><td>get_devices_list <br/>Investigation</td></tr>
<tr><td>Get Device Details</td><td>Retrieves a specific device information from OTbase Inventory based on the device ID and include data you have specified.</td><td>get_device_details <br/>Investigation</td></tr>
<tr><td>Delete Device Details</td><td>Deletes an specific device information from OTbase Inventory based on the device ID you have specified.</td><td>delete_device_details <br/>Investigation</td></tr>
<tr><td>Get Vulnerabilities List</td><td>Retrieves a list of vulnerabilities from OTbase Inventory based on the input parameters you have specified.</td><td>get_vulnerabilities_list <br/>Investigation</td></tr>
<tr><td>Get Vulnerability Details</td><td>Retrieves a specific vulnerability information from OTbase Inventory based on the CVE ID you have specified.</td><td>get_vulnerability_details <br/>Investigation</td></tr>
<tr><td>Get Data Flow</td><td>Retrieves a list of data flow from OTbase Inventory based on the input parameter you have specified.</td><td>get_data_flow <br/>Investigation</td></tr>
<tr><td>Get Network List</td><td>Retrieves a list of networks from OTbase Inventory based on the input parameter you have specified.</td><td>get_network_list <br/>Investigation</td></tr>
<tr><td>Get Network Details</td><td>Retrieves a specific network information from OTbase Inventory based on the network ID you have specified.</td><td>get_network_details <br/>Investigation</td></tr>
</tbody></table>
### operation: Get Devices List
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Device Name</td><td>(Optional) Specify the name of the device based on which you want to retrieve devices from  OTbase Inventory.
</td></tr><tr><td>Location ID</td><td>(Optional) Specify the ID of the location based on which you want to retrieve devices from OTbase Inventory.
</td></tr><tr><td>OT System ID</td><td>(Optional) Specify the ID of the OT system based on which you want to retrieve devices from OTbase Inventory.
</td></tr><tr><td>OT System Name</td><td>(Optional) Specify the name of the OT system based on which you want to retrieve devices from OTbase Inventory.
</td></tr><tr><td>IP Address</td><td>(Optional) Specify the IP address based on which you want to retrieve devices from OTbase Inventory.
</td></tr><tr><td>Include Data</td><td>(Optional) Select the multiple options to include data in response that this operation returns. You can choose from the following options: Software, Vulnerabilities, Compliance, Modules, Admins, or All.
</td></tr><tr><td>Network ID</td><td>(Optional) Specify the ID of the network based on which you want to retrieve devices from OTbase Inventory.
</td></tr><tr><td>Modified DateTime</td><td>(Optional) Select the DateTime using which you want to filter the result set to only include only those items that have been modified after the specified timestamp. Ex: 2024-04-18 19:12:59
</td></tr><tr><td>Limit</td><td>(Optional) Specify the maximum number of results, per page, that this operation should return. By default, this option is set as 300.
</td></tr><tr><td>Offset</td><td>(Optional) Index of the first item to be returned by this operation. This parameter is useful for pagination and for getting a subset of items. By default, this is set as 0.
</td></tr></tbody></table>
#### Output
The output contains the following populated JSON schema:

<pre>{
    "data": [
        {
            "name": "",
            "tags": [],
            "zone": "",
            "stage": "",
            "safety": "",
            "context": {
                "location": "",
                "otSystem": "",
                "processes": [
                    {
                        "name": "",
                        "location": "",
                        "locationId": ""
                    }
                ],
                "locationId": "",
                "otSystemId": "",
                "deviceGroup": "",
                "referenceLocation": "",
                "referenceLocationId": ""
            },
            "release": "",
            "deviceId": "",
            "exposure": "",
            "hardware": {
                "type": "",
                "model": "",
                "vendor": "",
                "version": "",
                "endOfLife": "",
                "lifecycle": "",
                "vendorLink": "",
                "description": "",
                "orderNumber": ""
            },
            "hostedOn": "",
            "modified": "",
            "monitors": [],
            "warranty": "",
            "deviceRef": "",
            "last_seen": "",
            "connections": [],
            "criticality": "",
            "description": "",
            "os_firmware": "",
            "last_seen_by": "",
            "serialNumber": "",
            "documentation": "",
            "last_patch_date": "",
            "manufactureDate": "",
            "installationDate": "",
            "days_since_last_patch": ""
        }
    ],
    "info": {
        "user": "",
        "total": "",
        "offset": "",
        "origin": "",
        "next_offset": ""
    }
}</pre>
### operation: Get Device Details
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Device ID</td><td>Specify the ID of the device based on which you want to retrieve specific device details from OTbase Inventory.
</td></tr><tr><td>Include Data</td><td>(Optional) Select the multiple options to include data in response that this operation returns. You can choose from the following options: Software, Vulnerabilities, Compliance, Modules, Admins, or All.
</td></tr></tbody></table>
#### Output
The output contains the following populated JSON schema:

<pre>{
    "data": {
        "name": "",
        "tags": [],
        "zone": "",
        "stage": "",
        "safety": "",
        "context": {
            "location": "",
            "otSystem": "",
            "processes": [
                {
                    "name": "",
                    "location": "",
                    "locationId": ""
                }
            ],
            "locationId": "",
            "otSystemId": "",
            "deviceGroup": "",
            "referenceLocation": "",
            "referenceLocationId": ""
        },
        "release": "",
        "deviceId": "",
        "exposure": "",
        "hardware": {
            "type": "",
            "model": "",
            "vendor": "",
            "version": "",
            "endOfLife": "",
            "lifecycle": "",
            "vendorLink": "",
            "description": "",
            "orderNumber": ""
        },
        "hostedOn": "",
        "modified": "",
        "monitors": [],
        "warranty": "",
        "deviceRef": "",
        "last_seen": "",
        "connections": [],
        "criticality": "",
        "description": "",
        "os_firmware": "",
        "last_seen_by": "",
        "serialNumber": "",
        "documentation": "",
        "last_patch_date": "",
        "manufactureDate": "",
        "installationDate": "",
        "days_since_last_patch": ""
    },
    "info": {
        "user": "",
        "origin": ""
    }
}</pre>
### operation: Delete Device Details
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Device ID</td><td>Specify the ID of the device based on which you want to delete specific device details from OTbase Inventory.
</td></tr></tbody></table>
#### Output

 The output contains a non-dictionary value.
### operation: Get Vulnerabilities List
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Priority</td><td>(Optional) Select the priority of the vulnerabilities that this operation returns. You can choose from the following options: Critical, High, Medium, or Low.
</td></tr><tr><td>Location ID</td><td>(Optional) Specify the ID of the location based on which you want to retrieve vulnerabilities from OTbase Inventory.
</td></tr></tbody></table>
#### Output
The output contains the following populated JSON schema:

<pre>{
    "data": [
        {
            "kev": "",
            "cveId": "",
            "vector": "",
            "devices": [],
            "priority": "",
            "severity": "",
            "baseScore": "",
            "description": "",
            "datePublished": ""
        }
    ],
    "info": {
        "user": "",
        "total": "",
        "offset": "",
        "origin": "",
        "next_offset": ""
    }
}</pre>
### operation: Get Vulnerability Details
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>CVE ID</td><td>Specify the ID of the CVE based on which you want to retrieve specific vulnerability details from OTbase Inventory.
</td></tr></tbody></table>
#### Output
The output contains the following populated JSON schema:

<pre>{
    "data": {
        "kev": "",
        "cveId": "",
        "vector": "",
        "devices": [],
        "priority": "",
        "severity": "",
        "baseScore": "",
        "description": "",
        "datePublished": ""
    },
    "info": {
        "user": "",
        "origin": ""
    }
}</pre>
### operation: Get Data Flow
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Last Seen</td><td>(Optional) Select the DateTime using which you want to filter the result set to only include only those items that have been last seen after the specified timestamp.
</td></tr></tbody></table>
#### Output
The output contains the following populated JSON schema:

<pre>{
    "data": [],
    "info": {
        "user": "",
        "total": "",
        "offset": "",
        "origin": ""
    }
}</pre>
### operation: Get Network List
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Offset</td><td>(Optional) Index of the first item to be returned by this operation. This parameter is useful for pagination and for getting a subset of items. By default, this is set as 0.
</td></tr></tbody></table>
#### Output
The output contains the following populated JSON schema:

<pre>{
    "data": [
        {
            "name": "",
            "type": "",
            "vlan": "",
            "group": "",
            "address": "",
            "location": "",
            "networkId": "",
            "groupColor": "",
            "locationId": "",
            "description": "",
            "reserved_addresses": []
        }
    ],
    "info": {
        "user": "",
        "total": "",
        "offset": "",
        "origin": ""
    }
}</pre>
### operation: Get Network Details
#### Input parameters
<table border=1><thead><tr><th>Parameter</th><th>Description</th></tr></thead><tbody><tr><td>Network ID</td><td>Specify the ID of the network based on which you want to retrieve specific network details from OTbase Inventory.
</td></tr></tbody></table>
#### Output
The output contains the following populated JSON schema:

<pre>{
    "data": {
        "name": "",
        "type": "",
        "vlan": "",
        "group": "",
        "address": "",
        "location": "",
        "networkId": "",
        "groupColor": "",
        "locationId": "",
        "description": "",
        "reserved_addresses": []
    },
    "info": {
        "user": "",
        "origin": ""
    }
}</pre>
## Included playbooks
The `Sample - otbase-inventory - 1.1.0` playbook collection comes bundled with the OTbase Inventory connector. These playbooks contain steps using which you can perform all supported actions. You can see bundled playbooks in the **Automation** > **Playbooks** section in FortiSOAR&trade; after importing the OTbase Inventory connector.

- Delete Device Details
- Get Data Flow
- Get Device Details
- Get Devices List
- Get Network Details
- Get Network List
- Get Vulnerabilities List
- Get Vulnerability Details
- OTbase Inventory > Fetch and Create
- OTbase Inventory > Ingest

**Note**: If you are planning to use any of the sample playbooks in your environment, ensure that you clone those playbooks and move them to a different collection since the sample playbook collection gets deleted during connector upgrade and delete.
## Data Ingestion Support
Use the Data Ingestion Wizard to easily ingest data into FortiSOAR&trade; by pulling events/alerts/incidents, based on the requirement.

**TODO:** provide the list of steps to configure the ingestion with the screen shots and limitations if any in this section.