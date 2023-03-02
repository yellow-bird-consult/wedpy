"""
This file defines the unit tests for the Dependency class.
"""
import os
import shutil
import tempfile
from unittest import main, TestCase
from unittest.mock import patch

from wedpy.seating_plan.dependency import Dependency


class TestDependency(TestCase):
    """
    The TestDependency class is used to test the Dependency class.
    """
    def setUp(self) -> None:
        """
        The setUp method is used to set up the unit tests for the Dependency class.
        """
        self.venue_path = tempfile.mkdtemp()
        self.dependency = Dependency(
            name='test',
            default_image_name='test',
            git_url="www.test.com",
            branch='testb',
            image_url='test_image_url'
        )

    def tearDown(self) -> None:
        """
        The tearDown method is used to tear down the unit tests for the Dependency class.
        """
        shutil.rmtree(self.venue_path)

    @patch("wedpy.seating_plan.dependency.WeddingInvite")
    def test_get_wedding_invite(self, mock_wedding_invite) -> None:
        """
        The test_get_wedding_invite method is used to test the get_wedding_invite method of the Dependency class.
        """
        self.dependency.get_wedding_invite(venue_path=self.venue_path)

        mock_wedding_invite.from_yaml.assert_called_once_with(
            filename=os.path.join(self.venue_path, 'test', 'wedding_invite.yml')
        )

    @patch("wedpy.seating_plan.dependency.print")
    @patch("wedpy.seating_plan.dependency.subprocess")
    def test_clone_repo(self, mock_subprocess, mock_print) -> None:
        """
        The test_clone_repo method is used to test the clone_repo method of the Dependency class.
        """
        mock_subprocess.Popen.return_value.communicate.return_value = (b"test", b"test")
        mock_subprocess.Popen.return_value.returncode = 0
        self.dependency.clone_repo(venue_path=self.venue_path)

        self.assertEqual(mock_subprocess.Popen.call_count, 2)
        self.assertEqual(
            mock_subprocess.Popen.call_args_list[0][0][0],
            f"cd {self.venue_path} && git clone {self.dependency.git_url}"
        )
        self.assertEqual(
            mock_subprocess.Popen.call_args_list[1][0][0],
            f"cd {self.venue_path}/test && git checkout {self.dependency.branch}"
        )

        self.assertEqual(mock_print.call_count, 2)
        self.assertEqual(
            mock_print.call_args_list[0][0][0],
            f"Successfully cloned test to {self.venue_path}"
        )
        self.assertEqual(
            mock_print.call_args_list[1][0][0],
            f"Successfully checked out testb branch for test"
        )


if __name__ == '__main__':
    main()
