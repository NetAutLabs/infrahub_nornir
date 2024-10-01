from infrahub_sdk import InfrahubClientSync


create_prefix = """
mutation {
  IpamIPPrefixCreate(data: {
    prefix: {value: "10.0.0.0/24"},
    description: {value: "mgmt subnet"},
    member_type: {value: "address"},
  })
  {
    ok
    object {
      id
    }
  }
}
"""

create_resource_manager = """
mutation {
  CoreIPAddressPoolUpsert(data: {
    name: {value: "mgmt IP address pool"},
    default_address_type: {value: "IpamIPAddress"},
    default_prefix_length: {value: 32},
    resources: [{id: "%s"}],
    ip_namespace: {id: "default"}
  })
  {
    ok
    object {
      id
    }
  }
}
"""

allocate_ip = """
mutation {
  IPAddressPoolGetResource(
    data: {
      id: "%s",
      identifier: "mgmt gw",
    }
  )
  {
    ok
    node {
      id
      display_label
    }
  }
}
"""

use_pool_in_node = """
mutation {
  InfraDeviceCreate(data: {
    name: {value: "dev-123"},
    primary_ip: {
      from_pool: {
        id: "%s"
      }
    }
  }) {
    ok
    object {
      display_label
      primary_ip {
        node {
          address {
            value
          }
        }
      }
    }
  }
}
"""

create_devices = [
    """
mutation MyMutation1 {
  NetworkDeviceUpsert(
    data: {name: {value: "switch01"}, status: {value: "active"} description: {value: "My awesome switch"}}
  ) {
    ok
  }
}""",
    """
mutation MyMutation2 {
  NetworkDeviceUpsert(
    data: {name: {value: "switch02"}, status: {value: "active"} description: {value: "My second awesome switch"}}
  ) {
    ok
  }
}
""",
]

get_devices = """
query MyQuery {
  NetworkDevice {
    edges {
      node {
        hfid
        name {
          value
        }
        description {
          value
        }
      }
    }
  }
}
"""


def main():
    # Needs environment variable `INFRAHUB_API_TOKEN`
    client = InfrahubClientSync(address="http://localhost:8000")

    # Create prefix
    result = client.execute_graphql(create_prefix)
    prefix_id = result["IpamIPPrefixCreate"]["object"]["id"]
    print(prefix_id)

    # Create resource pool for IPs
    result = client.execute_graphql(create_resource_manager % prefix_id)
    pool_id = result["CoreIPAddressPoolUpsert"]["object"]["id"]
    print(pool_id)

    # Allocate mgmt GW IP
    result = client.execute_graphql(allocate_ip % pool_id)
    print(result)

    # Create Devices
    for device_mutation in create_devices:
      result = client.execute_graphql(device_mutation)
      print(result)


if __name__ == "__main__":
    main()
