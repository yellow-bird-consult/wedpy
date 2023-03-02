"""
This file defines the tests for the seating plan class.
"""
import os
import shutil
import tempfile
from unittest import main, TestCase
from unittest.mock import patch, MagicMock, PropertyMock

from wedpy.seating_plan.seating_plan import SeatingPlan


class TestSeatingPlan(TestCase):

    @patch('wedpy.seating_plan.seating_plan.Dependency')
    @patch('wedpy.seating_plan.seating_plan.docker.from_env')
    def setUp(self, mock_docker_from_env, mock_dependency) -> None:
        """
        The setUp method is used to set up the unit tests for the SeatingPlan class.
        """
        self.dependency_mock = MagicMock()
        self.docker_mock = MagicMock()
        mock_docker_from_env.return_value = self.docker_mock
        mock_dependency.return_value = self.dependency_mock
        self.venue_path = tempfile.mkdtemp()
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(script_dir, '../assets/seating_plan.yml')
        self.seating_plan = SeatingPlan(seating_plan_path=self.file_path)
        self.expected_file_data = {
            "network_name": "test_network",
            "venue": "../../sandbox/",
            "attendees": [
                {
                    "name": "taxonomist",
                    "default_image_name": "taxonomist",
                    "git_url": "https://github.com/yellow-bird-consult/taxonomist.git",
                    "image_url": "yellowbirdconsulting/taxonomy-server",
                    "branch": "development"
                }
            ]
        }

    def tearDown(self) -> None:
        """
        The tearDown method is used to tear down the unit tests for the SeatingPlan class.
        """
        shutil.rmtree(self.venue_path)

    def test_load_config(self) -> None:
        """
        Tests that the load_config method loads the data from the seating plan file.
        :return: None
        """
        self.assertEqual(SeatingPlan.load_config(config_file=self.file_path), self.expected_file_data)

    @patch('wedpy.seating_plan.seating_plan.docker.from_env')
    @patch('wedpy.seating_plan.seating_plan.Dependency')
    def test_init(self, mock_dependency, mock_docker_from_env) -> None:
        """
        Tests that the constructor for the SeatingPlan class sets the attributes correctly.
        :return: None
        """
        self.seating_plan = SeatingPlan(seating_plan_path=self.file_path)
        self.assertEqual(self.seating_plan.config, self.expected_file_data)
        self.assertEqual(self.seating_plan.network_name, self.expected_file_data['network_name'])
        self.assertEqual(self.seating_plan.venue, self.expected_file_data['venue'])
        self.assertEqual(self.seating_plan.client, mock_docker_from_env.return_value)
        self.assertEqual(self.seating_plan.full_venue_path, os.path.join(os.getcwd(), self.expected_file_data['venue']))
        mock_dependency.assert_called_once_with(
            name=self.expected_file_data['attendees'][0]['name'],
            default_image_name=self.expected_file_data['attendees'][0]['default_image_name'],
            git_url=self.expected_file_data['attendees'][0]['git_url'],
            branch=self.expected_file_data['attendees'][0]['branch'],
            image_url=self.expected_file_data['attendees'][0]['image_url']
        )
        self.assertEqual(self.seating_plan.dependencies, [mock_dependency.return_value])

    def test_invites(self) -> None:
        """
        Tests that the invites property returns a list of WeddingInvite objects.
        :return: None
        """
        invites = self.seating_plan.invites
        self.assertEqual(len(invites), len(self.expected_file_data['attendees']))
        self.dependency_mock.get_wedding_invite.assert_called_once_with(
            venue_path=self.seating_plan.venue,
        )
        self.assertEqual(len(self.seating_plan.invites), len(self.expected_file_data['attendees']))

    @patch('wedpy.seating_plan.seating_plan.SeatingPlan.invites', new_callable=PropertyMock)
    def test_run_containers(self, mock_invites) -> None:
        """
        Tests that the run_containers method runs the containers for the dependencies.
        :return: None
        """
        dep_mock = MagicMock()
        mock_invites.return_value = [dep_mock]
        self.seating_plan.run_containers()
        dep_mock.run_containers.assert_called_once_with(
            runner=self.docker_mock.containers,
            network_name=self.seating_plan.network_name
        )

    def test_stop_containers(self) -> None:
        """
        Tests that the stop_containers method stops the containers for the dependencies.
        :return: None
        """
        container_one = MagicMock()
        container_two = MagicMock()
        self.seating_plan.network.containers = [container_one, container_two]
        self.seating_plan.stop_containers()
        container_one.stop.assert_called_once_with()
        container_two.stop.assert_called_once_with()

    @patch('wedpy.seating_plan.seating_plan.SeatingPlan.invites', new_callable=PropertyMock)
    def test_destroy_containers(self, mock_invites) -> None:
        """
        Tests that the destroy_containers method destroys the containers for the dependencies.
        :return: None
        """
        dep_mock = MagicMock()
        mock_invites.return_value = [dep_mock]
        container_one = MagicMock()
        container_two = MagicMock()

        self.seating_plan.network.containers = [container_one, container_two]
        self.seating_plan.destroy_containers()

        container_one.remove.assert_called_once_with(force=True)
        container_two.remove.assert_called_once_with(force=True)
        dep_mock.destroy_init_containers.assert_called_once_with()

    def test_destroy_network(self) -> None:
        """
        Tests that the destroy_network method destroys the network.
        :return: None
        """
        self.seating_plan.destroy_network()
        self.seating_plan.network.remove.assert_called_once_with()

    @patch('wedpy.seating_plan.seating_plan.SeatingPlan.invites', new_callable=PropertyMock)
    def test_wipe_images(self, mock_invites) -> None:
        """
        Tests that the wipe_images method removes the images for the dependencies.
        :return: None
        """
        dep_mock = MagicMock()
        mock_invites.return_value = [dep_mock]

        self.seating_plan.wipe_images()
        dep_mock.wipe_images.assert_called_once_with()

    def test_install(self) -> None:
        """
        Tests that the install method installs the dependencies.
        :return: None
        """
        self.seating_plan.install()
        self.dependency_mock.clone_repo.assert_called_once_with(venue_path=self.seating_plan.full_venue_path)

    @patch('wedpy.seating_plan.seating_plan.SeatingPlan.invites', new_callable=PropertyMock)
    def test_build(self, mock_invites) -> None:
        """
        Tests that the build method builds the dependencies.
        :return: None
        """
        dep_mock = MagicMock()
        mock_invites.return_value = [dep_mock]

        self.seating_plan.build(remote=False)
        dep_mock.build_images.assert_called_once_with(venue_path=self.seating_plan.full_venue_path, remote=False)


if __name__ == '__main__':
    main()
