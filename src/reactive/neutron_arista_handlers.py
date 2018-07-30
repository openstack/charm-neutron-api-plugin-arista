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
)
from charms_openstack.charm import (
    provide_charm_instance,
    use_defaults,
)
import charm.openstack.neutron_arista as arista  # noqa
from charm.openstack.neutron_arista import register_configs

CONFIGS = register_configs()

use_defaults('update-status')


@reactive.when('neutron-plugin-api-subordinate.connected')
def configure_principle(api_principle):
    inject_config = {
        'neutron-api': {
            '/etc/neutron/neutron.conf': {
                'sections': {
                    'DEFAULT': [
                    ],
                }
            }
        }
    }
    CONFIGS.write_all()
    api_principle.configure_plugin(
        neutron_plugin='arista',
        core_plugin='neutron.plugins.ml2.plugin.Ml2Plugin',
        neutron_plugin_config='/etc/neutron/plugins/ml2/ml2_conf_arista.ini',
        service_plugins=config('service-plugins'),
        subordinate_configuration=inject_config)
