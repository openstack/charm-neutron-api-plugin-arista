import mock

import reactive.neutron_arista_handlers as handlers

import charms_openstack.test_utils as test_utils


class TestRegisteredHooks(test_utils.TestRegisteredHooks):

    def test_hooks(self):
        # test that the hooks actually registered the relation expressions that
        # are meaningful for this interface: this is to handle regressions.
        # The keys are the function names that the hook attaches to.
        hook_set = {
            'when': {
                'configure_principle': (
                    'neutron-plugin-api-subordinate.connected', ),
                'install_arista': (
                    'neutron-plugin-api-subordinate.available', )
            }
        }
        # test that the hooks were registered via the
        # reactive.barbican_handlers
        self.registered_hooks_test_helper(handlers, hook_set, [])


class TestHandlers(test_utils.PatchHelper):

    def test_configure_principal(self):
        mocked_reactive = mock.MagicMock()
        self.patch_object(handlers, 'reactive',
                          name='reactive',
                          new=mocked_reactive)
        principal_charm = mock.MagicMock()
        mocked_reactive.endpoint_from_flag.return_value = principal_charm
        principal_charm.neutron_config_data = {
            'mechanism_drivers': 'driver1,driver2'
        }

        mocked_config = mock.MagicMock()
        self.patch_object(handlers, 'config',
                          name='config',
                          new=mocked_config)
        mocked_config.return_value = 'my_config_value'

        handlers.configure_principle()
        principal_charm.configure_plugin.assert_called_once_with(
            neutron_plugin='arista',
            mechanism_drivers='driver1,driver2,arista',
            subordinate_configuration={
                'neutron-api': {
                    '/etc/neutron/plugins/ml2/ml2_conf.ini': {
                        'sections': {
                            'ml2_arista': [
                                ('eapi_host', 'my_config_value'),
                                ('eapi_username', 'my_config_value'),
                                ('eapi_password', 'my_config_value'),
                                ('region_name', 'my_config_value'),
                                ('api_type', 'my_config_value'),
                            ],
                        },
                    },
                },
            }
        )
