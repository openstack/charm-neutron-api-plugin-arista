# Overview

This subordinate charm provides the
[Arista ML2 Plugin][python-networking-arista] support to the
[OpenStack Neutron API service][charm-neutron-api].

> **Note**: For upgrading from earlier prototypes of this charm see
> [Upgrading to stable charm][upgrading-to-stable].

When this charm is related to the neutron-api charm it will install the Arista
Neutron packages on each neutron-api unit in the region and supply the desired
configuration to the neutron-api service.

# Usage

## Configuration

This section covers common and/or important configuration options. See file
`config.yaml` for the full list of options, along with their descriptions and
default values. See the [Juju documentation][juju-docs-config-apps] for details
on configuring applications.

#### `eapi-host`

The `eapi-host` option is the IP address serving the Arista API (a.k.a. eAPI)
from the charm's perspective.

#### `eapi-username`

The `eapi-username` option is the username to be used for authenticating to the
Arista API.

#### `eapi-password`

The `eapi-password` option is the password to be used for authenticating to the
Arista API.

## Deployment

Because this is a subordinate charm a relation will need to be added to another
application to have the charm deployed on a machine.

To deploy (partial deployment only):

    juju deploy neutron-api
    juju deploy neutron-openvswitch
    juju deploy neutron-api-plugin-arista --config eapi-host=...

    juju add-relation neutron-api neutron-api-plugin-arista
    juju add-relation neutron-api neutron-openvswitch

# Bugs

Please report bugs on [Launchpad][lp-bugs-neutron-arista].

For general questions please refer to the [OpenStack Charm Guide][cg].

<!-- LINKS -->

[charm-neutron-api]: https://jaas.ai/neutron-api
[cg]: https://docs.openstack.org/charm-guide
[python-networking-arista]: https://opendev.org/x/networking-arista
[lp-bugs-neutron-arista]: https://bugs.launchpad.net/charm-neutron-api-plugin-arista/+filebug
[juju-docs-config-apps]: https://juju.is/docs/configuring-applications
[upgrading-to-stable]: https://github.com/openstack/charm-neutron-api-plugin-arista/blob/master/docs/upgrading-to-stable.md
