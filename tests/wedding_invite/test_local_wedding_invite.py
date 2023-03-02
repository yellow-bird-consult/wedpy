"""
This file defines the tests around the LocalWeddingInvite class.
"""
from unittest import TestCase, main
from unittest.mock import patch, MagicMock

from wedpy.wedding_invite.local_wedding_invite import LocalWeddingInvite


class TestLocalWeddingInvite(TestCase):

    @patch('wedpy.wedding_invite.local_wedding_invite.WeddingInvite')
    def setUp(self, mock_invite) -> None:
        self.mock_invite = mock_invite
        self.local_path = "local/path"
        self.num_processes = 4
        self.test = LocalWeddingInvite(local_wedding_invite_path=self.local_path, num_processes=self.num_processes)

    @patch('wedpy.wedding_invite.local_wedding_invite.WeddingInvite')
    def test___init__(self, mock_invite):
        """
        Tests that the __init__ method sets the core_unit attribute.
        :return: None
        """
        test = LocalWeddingInvite(local_wedding_invite_path=self.local_path, num_processes=self.num_processes)
        mock_invite.from_yaml.assert_called_once_with(filename=self.local_path)
        self.assertEqual(test.local_wedding_invite, mock_invite.from_yaml.return_value)
        self.assertEqual(test.num_processes, self.num_processes)

    @patch('wedpy.wedding_invite.local_wedding_invite.Pool')
    @patch('wedpy.wedding_invite.local_wedding_invite.tqdm')
    def test_build_images(self, mock_tqdm, mock_pool):
        """
        Tests that the build_images method builds the images.
        :return: None
        """
        build_one = MagicMock()
        build_two = MagicMock()

        self.mock_invite.from_yaml().builds.__add__.return_value = [build_one, build_two]

        self.test.build_images()
        mock_pool.assert_called_once_with(processes=self.num_processes)

        self.assertEqual(mock_pool().__enter__().apply_async.call_args_list[0][0][0], build_one.build_image)
        self.assertEqual(mock_pool().__enter__().apply_async.call_args_list[1][0][0], build_two.build_image)
        self.assertEqual(mock_pool().__enter__().apply_async.call_args_list[0][1], {'args': ('.', None, False)})
        self.assertEqual(mock_pool().__enter__().apply_async.call_args_list[1][1], {'args': ('.', None, False)})

        mock_tqdm.assert_called_once_with([
                mock_pool().__enter__().apply_async.return_value,
                mock_pool().__enter__().apply_async.return_value
            ],
            desc=f"{self.mock_invite.from_yaml().package_name} builds",
            unit='item',
            total=2
        )

    def test_run_containers(self):
        """
        Tests that the run_containers method runs the containers.
        :return: None
        """
        runner = MagicMock()
        network_name = "network_name"
        self.test.run_containers(runner=runner, network_name=network_name)
        self.mock_invite.from_yaml().run_containers.assert_called_once_with(runner=runner, network_name=network_name)

    def test_destroy_init_containers(self):
        """
        Tests that the destroy_init_containers method destroys the init containers.
        :return: None
        """
        self.test.destroy_init_containers()
        self.mock_invite.from_yaml().destroy_init_containers.assert_called_once_with()

    def test_wipe_images(self):
        """
        Tests that the wipe_images method wipes the images.
        :return: None
        """
        self.test.wipe_images()
        self.mock_invite.from_yaml().wipe_images.assert_called_once_with()


if __name__ == '__main__':
    main()
