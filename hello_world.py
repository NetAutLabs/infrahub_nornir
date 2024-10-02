import os

from nornir import InitNornir
from nornir.core import Nornir
from nornir.core.task import Task, Result

from nornir_infrahub.plugins.inventory.infrahub import InfrahubInventory
from nornir_rich.functions import print_inventory, print_result


def get_nonir() -> Nornir:
    nr = InitNornir(
        inventory={
            "plugin": "InfrahubInventory",
            "options": {
                "address": "http://localhost:8000",
                "token": os.getenv("INFRAHUB_API_TOKEN"),
                "host_node": {"kind": "NetworkDevice"},
                # maps a Nornir Host property to an InfraNode attributes or relation
                # name is the name of the Nornir Host property we want to map
                # mapping is the attribute or relation of the Node from which we have to extract the value
                "schema_mappings": [
                    {
                        "name": "hostname",
                        "mapping": "name",
                    },
                    # {
                    #     "name": "platform",
                    #     "mapping": "platform.nornir_platform",
                    # },
                ],
                # create Nornir groups from InfraNode attributesor relations
                # groups is created as attribute__value `site__jfk1`
                # "group_mappings": ["site.name"],
                # "group_file": "dummy.yml",
            },
        }
    )
    return nr


def hello_world(task: Task) -> Result:
    return Result(task.host, result=f"My name is {task.host.hostname}!")


if __name__ == "__main__":
    nr = get_nonir()
    print_inventory(nr)

    result = nr.run(hello_world)
    print_result(result)
