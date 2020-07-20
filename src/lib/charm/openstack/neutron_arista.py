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


class NeutronAristaCharm(charms_openstack.charm.OpenStackCharm):

    # Internal name of charm
    service_name = name = 'neutron-api-plugin-arista'

    # First release supported
    release = 'queens'

    # List of packages to install for this charm
    packages = ['python-networking-arista']

    def install(self):
        log('Starting arista installation')
        installed = len(filter_installed_packages(self.packages)) == 0
        if not installed:
            add_source(config('source'))
            apt_update(fatal=True)
            apt_install(self.packages[0], fatal=True)
