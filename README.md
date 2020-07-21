# Resource Manager

_**The situation is**: you have to execute many scripts, however they use too much memory. You can execute them one after the other, install a large scale resource manager such as [slurm](https://slurm.schedmd.com/documentation.html) or even a [reduced slurm version](https://github.com/labrax/minimal-slurm), or you can use this resource manager._

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

- Docker might change the pid of the process, the manager won't be able to identify the pid correctly

- When using processes over the network the pid might not be passed correctly, changes to release the resource manually will be required
