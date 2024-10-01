from infrahub_sdk import InfrahubClientSync


create_prefix = """
mutation {
  IpamIPPrefixCreate(data: {
    prefix: {value: "10.0.0.0/24"},
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
  CoreIPAddressPoolCreate(data: {
    name: {value: "My IP address pool"},
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



allocate_ip = """
mutation {
  IPAddressPoolGetResource(
    data: {
      id: "<id or resource pool>",
      data: {
        description: "my first allocated ip"
      }
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

def main():
    # Needs environment variable `INFRAHUB_API_TOKEN`
    client = InfrahubClientSync(address="http://localhost:8000")
    
    # Create prefix
    result = client.execute_graphql(create_prefix)
    prefix_id = result["IpamIPPrefixCreate"]["object"]["id"]
    print(prefix_id)
    
    
    # Create resource pool for IPs
    result = client.execute_graphql(create_resource_manager % prefix_id)
    print(result)

    print(use_pool_in_node % "TESTTESTETEST")
if __name__ == "__main__":
    main()
