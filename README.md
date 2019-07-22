# resource_manager

This tool servers to allocate resources for processes in the same machine.
- works via tcp/ip
- this tool does not respect any order (the first process to request gets the access)
- it stores the pid of the process that requested it

## How to use
- call the sample code for requesting resources
- close the process after using the resource
