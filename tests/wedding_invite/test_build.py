"""
This file defines the tests around the Build class.
"""
from unittest import TestCase, main
from unittest.mock import patch, MagicMock

from wedpy.wedding_invite.build import Build


class TestBuild(TestCase):

    def setUp(self) -> None:
        self.core_unit_mock = MagicMock()
        self.build = Build(self.core_unit_mock)

    def test___init__(self):
        """
        Tests that the __init__ method sets the core_unit attribute.
        :return: None
        """
        self.assertEqual(self.build.core_unit, self.core_unit_mock)

    @patch('wedpy.wedding_invite.build.docker.from_env')
    def test_pull_image(self, mock_docker_from_env) -> None:
        """
        Tests that the pull_image method pulls the docker image from the docker registry.
        :return: None
        """
        self.build.pull_image()
        mock_docker_from_env.return_value.images.pull.assert_called_once_with(self.core_unit_mock.image_url)

    @patch('wedpy.wedding_invite.build.platform.processor')
    @patch('wedpy.wedding_invite.build.docker.from_env')
    @patch('wedpy.wedding_invite.build.Build.pull_image')
    def test_build_image(self, mock_pull_image, mock_docker_from_env, mock_processor) -> None:
        """
        Tests that the build_image method builds the docker image from the Dockerfile.
        :return: None
        """
        package_root = 'root'
        tag = 'tag'
        remote = True
        self.build.core_unit.build_root = 'build_root'
        mock_docker_from_env.return_value.images.build.return_value = (None, None)
        mock_processor.return_value = 'arm'
        self.build.core_unit.build_files = {'arm': 'Dockerfile.arm'}
        self.build.core_unit.default_image_tag = 'default_image_tag'

        self.build.build_image(package_root=package_root, tag=tag, remote=remote)

        mock_pull_image.assert_called_once_with()
        mock_pull_image.reset_mock()

        self.build.core_unit.git_url = None
        self.build.build_image(package_root=package_root, tag=tag, remote=False)

        mock_pull_image.assert_called_once_with()
        mock_pull_image.reset_mock()

        self.build.core_unit.git_url = "git_url"
        self.build.core_unit.build_lock = True
        self.build.build_image(package_root=package_root, tag=tag, remote=False)

        mock_pull_image.assert_not_called()
        mock_docker_from_env.return_value.images.build.assert_called_once_with(
            path="root/build_root",
            dockerfile="Dockerfile",
            tag=tag
        )
        mock_docker_from_env.return_value.images.build.reset_mock()

        self.build.core_unit.build_lock = False
        self.build.build_image(package_root=package_root, tag=tag, remote=False)

        mock_pull_image.assert_not_called()
        mock_docker_from_env.return_value.images.build.assert_called_once_with(
            path="root/build_root",
            dockerfile="Dockerfile.arm",
            tag=tag
        )
        mock_docker_from_env.return_value.images.build.reset_mock()

        self.build.build_image(package_root=package_root, tag=None, remote=False)
        mock_docker_from_env.return_value.images.build.assert_called_once_with(
            path="root/build_root",
            dockerfile="Dockerfile.arm",
            tag="default_image_tag"
        )

    def test_delete_container(self) -> None:
        """
        Tests that the delete_container method deletes the container.
        :return: None
        """
        runner_mock = MagicMock()
        container_mock = MagicMock()
        runner_mock.get.return_value = container_mock

        self.build.delete_container(runner=runner_mock)
        container_mock.remove.assert_called_once_with(force=True)

        container_mock.reset_mock()
        runner_mock.get.return_value = None

        self.build.delete_container(runner=runner_mock)
        container_mock.remove.assert_not_called()

    @patch('wedpy.wedding_invite.build.docker.from_env')
    def test_delete_image(self, mock_docker_from_env) -> None:
        """
        Tests that the delete_image method deletes the image.
        :return: None
        """
        mock_image = MagicMock()
        mock_docker_from_env.return_value.images.get.return_value = mock_image

        self.build.delete_image()
        mock_docker_from_env.return_value.images.remove.assert_called_once_with(mock_image.id, force=True)

    def test_run_container(self) -> None:
        """
        Tests that the run_container method runs the container.
        :return: None
        """
        runner_mock = MagicMock()
        # container_mock = MagicMock()
        # runner_mock.get.return_value = container_mock

        self.build.run_container(runner=runner_mock, network_name="test_network")
        runner_mock.run.assert_called_once_with(
            image=self.core_unit_mock.default_image_tag,
            environment=self.core_unit_mock.config,
            detach=True,
            network="test_network",
            name=self.core_unit_mock.default_container_name,
            ports={f'{self.core_unit_mock.outside_port}/tcp': ('0.0.0.0', self.core_unit_mock.inside_port)},
        )


if __name__ == '__main__':
    main()
