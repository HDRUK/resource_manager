# resource_manager

This is a simple tool to orchestrate resource sharing. It does not require admin permissions and may be used as a simple solution to share resources.

In the testbed it was used to split the use of 3 GPUs.

## Features
- works via tcp/ip
- out-of-order requisition (lucky goes first)
- process pid stored and checked for exit

## How to use
- start the server (e.g. `python 20181024_manager_gpu.py`)
- a consumer requests for a resource (call `resource_manager_client.try_resource`)
- close the process after using the resource (or call `resource_manager_client.release_resource`)

## Issues

Docker might change the pid of the process, it might require some changes to work properly
