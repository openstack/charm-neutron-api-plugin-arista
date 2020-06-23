# Overview

This principle charm provides the Arista ML2 Plugin support to the OpenStack
Neutron API service.

When this charm is related to the neutron-api charm it will install the
Arista Neutron packages on each neutron-api unit in the region and supply the
desired configuration to the neutron-api service.

# Usage

To deploy (partial deployment only):

    juju deploy neutron-api
    juju deploy neutron-openvswitch
    juju deploy neutron-api-plugin-arista

    juju add-relation neutron-api neutron-api-plugin-arista
    juju add-relation neutron-api mysql
    juju add-relation neutron-api rabbitmq-server
    juju add-relation neutron-api neutron-openvswitch
    juju add-relation neutron-api nova-cloud-controller
