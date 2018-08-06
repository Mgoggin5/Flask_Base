import requests
from datetime import datetime
from urllib import error, parse, request

# Module constants
# URIs stored as str; each used for its own use within a Server method
ACCOUNT_URI = '/redfish/v1/AccountService/'
BIOS_URI = '/redfish/v1/systems/1/bios/settings/'
CHASSIS_URI = '/redfish/v1/Chassis/1/'
MANAGERS_URI = '/redfish/v1/Managers/1/'
POWER_URI = '/redfish/v1/Systems/1/Actions/ComputerSystem.Reset/'
SESSION_URI = '/redfish/v1/SessionService/Sessions/'
SYSTEMS_URI = '/redfish/v1/Systems/1/'
# Root URIs of the server
ROOT_URIS = [
    ACCOUNT_URI, CHASSIS_URI, MANAGERS_URI, SYSTEMS_URI
]
# URIs within the root URIs that cause recurrsion, thus needing to be skipped
SKIP_URIS = [
    '/redfish/v1/Chassis/1/Power/#PowerSupplies/0/',
    '/redfish/v1/Chassis/1/Power/#PowerSupplies/1/',
    '/redfish/v1/Managers/1/LogServices/IEL/Entries/'
]


# Abstraction of a server running the Redfish API as python object
class Server(object):

    # Constructor requires only information used to connect to the server
    def __init__(self, ip, username, password):
        self.__ip = 'https://' + ip
        self.__login = (username, password)
        self.__check_connection()

    # Returns identified setting in BIOS and it's value
    def get_bios_setting(self, key):
        return key + ': ' + requests.get(
                self.__ip + BIOS_URI, auth=self.__login,
                verify=False).json["Attributes"][key]

    # Changes identified setting in BIOS (key) to the given val
    # Returns the HTTP request status code
    def set_bios_setting(self, key, val):
        payload = {"Attributes": {key: val}}
        return requests.patch(
                self.__ip + BIOS_URI, auth=self.__login,
                json=payload, verify=False).status_code

    # Changes server current powerstate to user input
    # Returns the HTTP request status code
    # Accepted input: str == 'on', 'off', 'restart'
    def set_power(self, state):
        if state.lower() == 'restart':
            if self.get_power() == "Off":
                raise ValueError('Server must be turned on to restart')
            command = "ForceRestart"
        elif state.lower() == 'on':
            if self.get_power() == "On":
                raise ValueError('Server is already turned on')
            command = "On"
        elif state.lower() == 'off':
            if self.get_power() == "Off":
                raise ValueError('Server is already turned off')
            command = "ForceOff"
        else:
            raise ValueError(
                'must be one of following str: \'on\', \'off\', \'restart\'')
        json = {"ResetType": command}
        return requests.post(
                self.__ip + POWER_URI, auth=self.__login,
                json=json, verify=False).status_code

    # Returns current powerstate of the server
    def get_power(self):
        return requests.get(
                self.__ip + SYSTEMS_URI, auth=self.__login,
                verify=False).json()['PowerState']

    # Compiles and returns a JSON object of the entire URI tree for the server
    def complete_json(self):
        data = {}
        data["Chassis"] = self.__uri_tree(
                self.__request_json(ROOT_URIS[1]), ROOT_URIS[1])
        data["Manager"] = self.__uri_tree(
                self.__request_json(ROOT_URIS[2]), ROOT_URIS[2])
        data["System"] = self.__uri_tree(
                self.__request_json(ROOT_URIS[3]), ROOT_URIS[3])
        return data

    # Tests the parameters of the server object in its creation
    def __check_connection(self):
        test = requests.get(
            self.__ip + SESSION_URI, auth=self.__login, verify=False)
        return test.status_code

    # Returns a JSON object from the one given,
    # Converts nested URIs into JSON objects from the data stored at each URI
    # If latest is set to True, stored logs will only return the latest entry
    def __uri_tree(self, json, uri, latest=True):
        id_tag = '@odata.id'
        for key, val in json.items():
            if isinstance(val, dict):
                if list(val.keys())[0] == id_tag:
                    if self.__check_uri(val[id_tag], uri):
                        json[key] = self.__request_json(val[id_tag])
                self.__uri_tree(json[key], uri)
            elif isinstance(val, list):
                if latest:
                    if key == 'PowerDetail':
                        json[key] = self.__latest_time(val)
                else:
                    for index in range(len(val)):
                        if isinstance(val[index], dict):
                            if list(val[index].keys())[0] == id_tag:
                                if self.__check_uri(val[index][id_tag], uri):
                                    json[key][index] = self.__request_json(
                                        val[index][id_tag])
                            self.__uri_tree(json[key][index], uri)
        return json

    # Checks if a URI may cause recurrsion
    def __check_uri(self, uri, parent):
        if parent.lower() not in uri.lower():
            if ROOT_URIS[0] not in uri:
                return False
        if uri in SKIP_URIS:
            return False
        return True

    # Returns JSON object containing data stored at the given URI
    def __request_json(self, uri):
        return requests.get(
                self.__ip + uri, auth=self.__login,
                verify=False).json()

    # Returns the latest entry of a list containing "Time" keys
    def __latest_time(self, lst):
        latest = lst[0]
        for i in range(1, len(lst)):
            if (datetime.strptime(latest["Time"], '%Y-%m-%dT%H:%M:%SZ') <
                    datetime.strptime(lst[i]["Time"], '%Y-%m-%dT%H:%M:%SZ')):
                latest = lst[i]
        return latest

    # Server class private variables
    __ip = ''
    __login = ('', '')
