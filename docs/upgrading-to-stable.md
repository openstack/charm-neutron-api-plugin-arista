<!-- WARNING: the release notes
( https://docs.openstack.org/charm-guide/latest/2008.html ) point to this file.
Do not delete or move it. -->

# Upgrading to the first stable revision

Prior to the
[first stable revision](https://jaas.ai/u/openstack-charmers-next/neutron-api-plugin-arista/2)
the
[prototype charm](https://jaas.ai/u/openstack-charmers-next/neutron-api-plugin-arista/1)
relied on a
[special neutron-api fork](https://jaas.ai/u/aurelien-lourot/neutron-api-arista-test-fixture):

```
applications:

  neutron-api:
    charm: cs:~aurelien-lourot/neutron-api-arista-test-fixture
    options:
      enable-arista: True
      manage-neutron-plugin-legacy-mode: True
      [...]

  neutron-api-plugin-arista:
    charm: cs:~openstack-charmers-next/neutron-api-plugin-arista-1
    num_units: 0
    options:
      eapi-host: 192.0.2.42
      eapi-username: admin
      eapi-password: password123
      api-type: EAPI
      service-plugins: router

  [...]

relations:
- - neutron-api
  - neutron-api-plugin-arista
- - neutron-api:neutron-plugin-api-subordinate
  - neutron-api-plugin-arista:neutron-plugin-api-subordinate
[...]
```

The [first stable revision](https://jaas.ai/u/openstack-charmers-next/neutron-api-plugin-arista/2)
is now a real neutron-api plugin:

```
applications:

  neutron-api:
    charm: cs:~openstack-charmers-next/neutron-api
    options:
      manage-neutron-plugin-legacy-mode: False
      # No need for `enable-arista` anymore
      [...]

  neutron-api-plugin-arista:
    charm: cs:~openstack-charmers-next/neutron-api-plugin-arista-2
    num_units: 0
    options:
      eapi-host: 192.0.2.42
      eapi-username: admin
      eapi-password: password123
      api-type: EAPI
      # The misbehaving `service-plugins` option has been removed

  [...]

relations:
- - neutron-api
  - neutron-api-plugin-arista
- - neutron-api:neutron-plugin-api-subordinate
  - neutron-api-plugin-arista:neutron-plugin-api-subordinate
[...]
```
