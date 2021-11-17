#!/usr/bin/env python
from charmhelpers.core.hookenv import (
    config,
    log
)
import charms_openstack.charm

from charmhelpers.fetch import (
    apt_install,
    apt_update,
    filter_installed_packages,
    add_source,
)


class BaseNeutronAristaCharm(charms_openstack.charm.OpenStackCharm):
    abstract_class = True

    # Internal name of charm
    service_name = name = 'neutron-api-plugin-arista'

    # Package to be used to determine the OpenStack release:
    release_pkg = version_package = 'neutron-common'

    def install(self):
        log('Starting arista installation')
        installed = len(filter_installed_packages(self.packages)) == 0
        if not installed:
            add_source(config('source'))
            apt_update(fatal=True)
            apt_install(self.packages[0], fatal=True)


class QueensNeutronAristaCharm(BaseNeutronAristaCharm):
    """The Queens incarnation of the charm."""
    abstract_class = False

    release = 'queens'
    python_version = 2

    # List of packages to install for this charm
    packages = ['python-networking-arista']


class RockyNeutronAristaCharm(BaseNeutronAristaCharm):
    """The Rocky incarnation of the charm."""
    abstract_class = False

    release = 'rocky'
    python_version = 3

    # List of packages to install for this charm
    packages = ['python3-networking-arista']


class WallabyNeutronAristaCharm(RockyNeutronAristaCharm):
    """The Wallaby incarnation of the charm."""
    abstract_class = False

    release = 'wallaby'

    # List of packages to install for this charm
    packages = ['python3-networking-arista', 'openstack-release']
