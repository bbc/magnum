# Copyright 2015 EasyStack, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


import mock

from magnum.api import attr_validator
from magnum.common import exception
from magnum.tests import base


class TestAttrValidator(base.BaseTestCase):

    def test_validate_flavor_with_vaild_flavor(self):
        mock_flavor = mock.MagicMock()
        mock_flavor.name = 'test_flavor'
        mock_flavor.id = 'test_flavor_id'
        mock_flavors = [mock_flavor]
        mock_nova = mock.MagicMock()
        mock_nova.flavors.list.return_value = mock_flavors
        mock_os_cli = mock.MagicMock()
        mock_os_cli.nova.return_value = mock_nova
        attr_validator.validate_flavor(mock_os_cli, 'test_flavor')
        self.assertTrue(mock_nova.flavors.list.called)

    def test_validate_flavor_with_invaild_flavor(self):
        mock_flavor = mock.MagicMock()
        mock_flavor.name = 'test_flavor_not_equal'
        mock_flavor.id = 'test_flavor_id_not_equal'
        mock_flavors = [mock_flavor]
        mock_nova = mock.MagicMock()
        mock_nova.flavors.list.return_value = mock_flavors
        mock_os_cli = mock.MagicMock()
        mock_os_cli.nova.return_value = mock_nova
        self.assertRaises(exception.FlavorNotFound,
                          attr_validator.validate_flavor,
                          mock_os_cli, 'test_flavor')

    def test_validate_external_network_with_valid_network(self):
        mock_networks = {'networks': [{'name': 'test_ext_net',
                         'id': 'test_ext_net_id'}]}
        mock_neutron = mock.MagicMock()
        mock_neutron.list_networks.return_value = mock_networks
        mock_os_cli = mock.MagicMock()
        mock_os_cli.neutron.return_value = mock_neutron
        attr_validator.validate_external_network(mock_os_cli, 'test_ext_net')
        self.assertTrue(mock_neutron.list_networks.called)

    def test_validate_external_network_with_invalid_network(self):
        mock_networks = {'networks': [{'name': 'test_ext_net_not_equal',
                         'id': 'test_ext_net_id_not_equal'}]}
        mock_neutron = mock.MagicMock()
        mock_neutron.list_networks.return_value = mock_networks
        mock_os_cli = mock.MagicMock()
        mock_os_cli.neutron.return_value = mock_neutron
        self.assertRaises(exception.NetworkNotFound,
                          attr_validator.validate_external_network,
                          mock_os_cli, 'test_ext_net')

    @mock.patch('magnum.objects.baymodel.BayModel.get_by_uuid')
    @mock.patch('magnum.common.clients.OpenStackClients')
    def test_validate_os_resources_with_invalid_flavor(self,
                                                       mock_os_cli,
                                                       mock_baymodel_by_uuid):
        mock_baymodel_by_uuid.return_value = {'flavor_id': 'test_flavor'}
        mock_flavor = mock.MagicMock()
        mock_flavor.name = 'test_flavor_not_equal'
        mock_flavor.id = 'test_flavor_id_not_equal'
        mock_flavors = [mock_flavor]
        mock_nova = mock.MagicMock()
        mock_nova.flavors.list.return_value = mock_flavors
        mock_os_cli.nova.return_value = mock_nova
        mock_context = mock.MagicMock()
        self.assertRaises(exception.FlavorNotFound,
                          attr_validator.validate_os_resources,
                          mock_context, 'baymodel_id')