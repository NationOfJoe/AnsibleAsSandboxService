import json
import os
import cloudshell.api.cloudshell_api as api
import cloudshell.helpers.scripts.cloudshell_scripts_helpers as scripthelpers

# Production
reservation_details = scripthelpers.get_reservation_context_details()
resource_context = scripthelpers.get_resource_context_details()
connectivity_details = scripthelpers.get_connectivity_context_details_dict()

template_json = '''
{
    "additionalArgs": "",
    "timeoutMinutes": "10",
    "repositoryDetails" : {
        "url": "",
        "username": "",
        "password": ""
    },
    "hostsDetails": [
    {
        "ip": "",
        "username": "",
        "password": "",
        "accessKey": "",
        "connectionMethod": "ssh",
        "connectionSecured": "true",
        "groups": [],
        "parameters": []
    }]
}
'''

class AnsibleExecutioner():
    def __init__(self):
        pass

    def executePlaybookScript(self):
        # AppName = os.environ['App_Name']
        session = api.CloudShellAPISession(host=connectivity_details['serverAddress'],
                                           token_id=connectivity_details['adminAuthToken'],
                                           domain=reservation_details.domain)
        reservation_details_data = session.GetReservationDetails(reservation_details.id).ReservationDescription
        JsonDetails = self._sort_out_json(template_json, session)
        session.WriteMessageToReservationOutput(reservation_details.id, JsonDetails)
        self._run_ansible_playbook(session,
                                   reservation_details.id,
                                   JsonDetails,
                                   scripthelpers.get_resource_context_details().name)
        return None


    def _run_ansible_playbook(self, session, resid, JsonDetails, service_Name):
        command_inputs = [
            api.InputNameValue(
                Name='ansible_configuration_json',
                Value=JsonDetails
            )
        ]

        session.ExecuteCommand(
            reservationId=resid,
            targetName=service_Name,
            targetType='Service',
            commandName='execute_playbook',
            commandInputs=command_inputs
        )

    def _parse_parameters(self):
        try:
            raw_params = os.environ['Ansible_Parameters']
            user_params = []
            params = [x.split(',') for x in raw_params.split(';')]
            for item in params:
                user_params.append(
                {
                    "name": '{0}'.format(item[0]),
                    "value": '{0}'.format(item[1])
                }
                )
        except:
            user_params = []
        return user_params

    def _sort_out_json(self, json_string, session):
        # get data from sandbox
        try:
            ip = os.environ['Host_IP']
        except:
            raise Exception('No IP was selected to run playbook against')
        try:
            playbook_url = os.environ['URL']
        except:
            raise Exception('No URL was selected to run playbook from')
        attrs = scripthelpers.get_resource_context_details().attributes
        try:
            username = os.environ['Username']
        except:
            raise Exception('No Username was selected to run playbook from')
        try:
            passwrd = os.environ['Password']
        except:
            raise Exception('No Password was selected to run playbook from')
        TimeoutMinutes = attrs['Timeout Minutes']
        # playbook_url = attrs['URL']
        JsonDetails = json.loads(json_string)
        # fill it up in the Json object
        JsonDetails['hostsDetails'][0]['username'] = username
        JsonDetails['hostsDetails'][0]['password'] = passwrd
        JsonDetails['hostsDetails'][0]['ip'] = ip
        JsonDetails['hostsDetails'][0]['parameters'] = self._parse_parameters()
        JsonDetails['timeoutMinutes'] = TimeoutMinutes
        JsonDetails['repositoryDetails']['url'] = playbook_url
        JsonDetails['repositoryDetails']['username'] = attrs['repo_username']
        JsonDetails['repositoryDetails']['password'] = session.DecryptPassword(attrs['repo_password']).Value
        json_string = json.dumps(JsonDetails)
        return json_string