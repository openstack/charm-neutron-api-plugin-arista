# Copyright 2016 Canonical Ltd
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#  http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import charms.reactive as reactive

from charmhelpers.core.hookenv import (
    config,
    log,
)

from charms_openstack.charm import (
    provide_charm_instance,
    use_defaults,
)


use_defaults('update-status')


@reactive.when_not('arista-package.installed')
@reactive.when('neutron-plugin-api-subordinate.available')
def install_arista():
    with provide_charm_instance() as charm_class:
        charm_class.install()
    reactive.set_state('arista-package.installed')


@reactive.when_any('config.changed.eapi-host',
                   'config.changed.eapi-username',
                   'config.changed.eapi-password',
                   'config.changed.region-name',
                   'config.changed.api-type',
                   'neutron-plugin-api-subordinate.connected')
def configure_principle():
    try:
        api_principle = reactive.endpoint_from_flag(
            'neutron-plugin-api-subordinate.connected')

        mechanism_drivers = ','.join((
            api_principle.neutron_config_data.get('mechanism_drivers', ''),
            'arista'))
    except AttributeError:
        log("The principle charm isn't ready yet. "
            "Postponing its configuration...")
        return

    log('Configuring the principle charm...')

    sections = {
        'ml2_arista': [
            ('eapi_host', config('eapi-host')),
            ('eapi_username', config('eapi-username')),
            ('eapi_password', config('eapi-password')),
            ('region_name', config('region-name')),
            ('api_type', config('api-type')),
        ],
    }

    api_principle.configure_plugin(
        neutron_plugin='arista',
        mechanism_drivers=mechanism_drivers,
        subordinate_configuration={
            'neutron-api': {
                '/etc/neutron/plugins/ml2/ml2_conf.ini': {
                    'sections': sections,
                },
            },
        }
    )
