#!/usr/bin/env python
from collections import OrderedDict
from charmhelpers.core.hookenv import config
import charms_openstack.charm

from charmhelpers.contrib.openstack import (
    context,
    templating,
)
from charmhelpers.contrib.openstack.utils import os_release


ML2_CONFIG = '/etc/neutron/plugins/ml2/ml2_conf_arista.ini'
TEMPLATES = 'templates/'


class NeutronAristaCharm(charms_openstack.charm.OpenStackCharm):

    # Internal name of charm
    service_name = name = 'neutron-arista'

    # First release supported
    release = 'queens'

    # List of packages to install for this charm
    packages = ['python-networking-arista']

    def write_config(self):
        configs = self.register_configs()
        configs.write_all()

    def register_configs(release=None):
        resources = OrderedDict([
            (ML2_CONFIG, {
                'services': ['neutron-server'],
                'contexts': [AristaMl2Context(), ]
            }),
        ])
        release = os_release('neutron-common')
        configs = templating.OSConfigRenderer(templates_dir=TEMPLATES,
                                              openstack_release=release)
        for cfg, rscs in resources.items():
            configs.register(cfg, rscs['contexts'])
        return configs


class AristaMl2Context(context.OSContextGenerator):

    def __call__(self):
        ctxt = {'eapi_host': config('eapi-host'),
                'eapi_username': config('eapi-username'),
                'eapi_password': config('eapi-password'),
                'region_name': config('region-name'),
                'api_type': config('api-type'),
                'arista_version': config('arista-version')}
        return ctxt
