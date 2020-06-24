# Overview

This is a "source" charm, which is intended to be strictly the top
layer of a built charm.  This structure declares that any included
layer assets are not intended to be consumed as a layer from a
functional or design standpoint.

# Test and Build

Building, pushing and publishing to the charm store is automated
by CI to ensure consistent flow.  Manually building is useful for
development and testing, however.

```
tox -e pep8
tox -e py3
tox -e build
cd build/builds/neutron-api-plugin-arista

# Set one of these env vars, depending on whether you want to
# download the Arista image from a remote place or have it already
# locally:
export TEST_ARISTA_IMAGE_REMOTE=http://example.com/swift/v1/images/arista-cvx-virt-test.qcow2
export TEST_ARISTA_IMAGE_LOCAL=/tmp/arista-cvx-virt-test.qcow2

tox -e func
```
