import json
import os
import cloudshell.api.cloudshell_api as api
import cloudshell.helpers.scripts.cloudshell_scripts_helpers as scripthelpers

reservation_details = scripthelpers.get_reservation_context_details()
resource_context = scripthelpers.get_resource_context_details()
connectivity_details = scripthelpers.get_connectivity_context_details_dict()


class AnsibleExecutioner():
    def __init__(self):
        pass

    def executePlaybookScript(self):
        session = scripthelpers.get_api_session()
        Ansible_services = [service for service in
                           session.GetReservationDetails(reservation_details.id).ReservationDescription.Services
                           if service.ServiceName == 'AnsibleServer']
        if Ansible_services== []:
            raise Exception('Ansible Server not found!')
        elif Ansible_services.__len__() > 1:
            raise Exception('Multiple Ansible Servers found!')
        else:
            Ansible_service = Ansible_services[0]
        # Build Inputs:
        command_inputs = [
            api.InputNameValue('Host_IP', resource_context.address),
            api.InputNameValue('URL', resource_context.attributes['Ansible Playbook URL']),
            api.InputNameValue('Ansible_Parameters', resource_context.attributes['Ansible Parameters']),
            api.InputNameValue('Username', resource_context.attributes['User']),
            api.InputNameValue('Password', resource_context.attributes['Password'])
        ]
        session.ExecuteCommand(
            reservationId=reservation_details.id,
            targetName=Ansible_service.Alias,
            targetType='Service',
            commandName='AnsibleExecutePlaybook',
            commandInputs=command_inputs
        )
