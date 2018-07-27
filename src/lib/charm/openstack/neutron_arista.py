#!/usr/bin/env python
import subprocess

import charmhelpers.core.hookenv as hookenv
from charmhelpers.core.hookenv import (
    config,
    log,
    status_set,
    is_leader,
    leader_get,
    leader_set,
)
import charms_openstack.charm

from charmhelpers.contrib.python.packages import pip_install

from charmhelpers.contrib.openstack import context
from charmhelpers.contrib.openstack.utils import (
    CompareOpenStackReleases,
    os_release,
)

ML2_CONFIG_ARISTA = '/etc/neutron/plugins/ml2/ml2_conf_arista.ini'
TEMPLATES = 'templates/'


class NeutronAristaCharm(charms_openstack.charm.OpenStackCharm):

    # Internal name of charm
    service_name = name = 'neutron-arista'

    # First release supported
    release = 'queens'

    # List of packages to install for this charm
    packages = ['']

    def install(self):
        package_version = config('arista-version')
        package_name = 'networking-arista==%s' % package_version
        proxy = config('pip-proxy')
        if proxy:
            pip_install(package_name, fatal=True, proxy=proxy)
        else:
            pip_install(package_name, fatal=True)
        status_set('active', 'Unit is ready')


class AristaMl2Context(context.OSContextGenerator):

    def __call__(self):
        ctxt = {'eapi_host': config('eapi-host'),
                'eapi_username': config('eapi-username'),
                'eapi_password': config('eapi-password'),
                'region_name': config('region-name'),
                'api_type': config('api-type'),
                'arista_version': config('arista-version')}
        return ctxt


def register_configs(release=None):
    resources = OrderedDict([
        (ML2_CONFIG, {
            'services': ['neutron-server'],
            'contexts': [AristaMl2Context(), ]
        }),
        (ML2_CONFIG_ARISTA, {
            'services': ['neutron-server'],
            'contexts': [AristaMl2Context(), ]
        }),
    ])
    release = os_release('neutron-common')
    configs = templating.OSConfigRenderer(templates_dir=TEMPLATES,
                                          openstack_release=release)
    for cfg, rscs in resources.iteritems():
        configs.register(cfg, rscs['contexts'])
    return configs
