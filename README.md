# AnsibleAsSandboxService


this is a project that allows the use of ansible service as a sandbox element.

prerequistes:
 - linux execution server with ansible server.
 
 installation:
 1. import the .zip pacakge.
 
 
 Usage:
 1. on the ansible service , set the repository username and password if applicable.
 2. on that service also choose the execution server selector
 3. set the ansible playbook attribute on relevant DUTs.
 4. set the ansible parameters on the DUT , if applicable.
 5. make sure that the DUT has the relevant script ( the same ones that the DUT resources that come with the package have
 
 
 
 available commands:
 1. on the service itself , run directly on the ansible server (the linux execution Server)
 2. on the DUT , a command that would execute the service's command with the DUT's details from the attributes
 3. there is a blueprint command to execute all the DUT commands in the sandbox
 
 
 
