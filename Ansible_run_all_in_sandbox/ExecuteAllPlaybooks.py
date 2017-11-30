import json
import os
import cloudshell.api.cloudshell_api as api
import cloudshell.helpers.scripts.cloudshell_scripts_helpers as scripthelpers

reservation_details = scripthelpers.get_reservation_context_details()
connectivity_details = scripthelpers.get_connectivity_context_details_dict()


class AnsibleExecutioner():
    def __init__(self):
        pass

    def executePlaybookScript(self):
        session = scripthelpers.get_api_session()
        Ansible_resources = []
        Ansible_resources_raw = [resource for resource in
                           session.GetReservationDetails(reservation_details.id).ReservationDescription.Resources]
        for res in Ansible_resources_raw:
            res_det = session.GetResourceDetails(res.Name).ResourceAttributes
            Ansible_playbook_url = [attr.Value for attr in res_det if attr.Name == 'Ansible Playbook URL']
            if Ansible_playbook_url.__len__() == 1:
                Ansible_resources.append(res)

        if Ansible_resources == []:
            raise Exception('no resources with Ansible capabilities  found!')


        for Ansible_resource in Ansible_resources:
            session.ExecuteCommand(
                reservationId=reservation_details.id,
                targetName=Ansible_resource.Name,
                targetType='Resource',
                commandName='DUTExecutePlaybook',
                commandInputs=[]
            )
