"""
This file defines the tests around the WeddingInvite class.
"""
from unittest import TestCase, main
from unittest.mock import patch, MagicMock

from wedpy.wedding_invite.wedding_invite import WeddingInvite
from wedpy.wedding_invite.build import Build
from wedpy.core_unit import CoreUnit


class TestWeddingInvite(TestCase):

    def setUp(self) -> None:
        # below is a list of dictionaries that represent dict representations of the CoreUnit class.
        self.build_dicts = [
            {
                'name': 'wedding_invite',
                'git_url': 'some_git_url',
                'image_url': 'some_image_url',
                'branch': 'some_branch',
                'default_image_tag': 'some_default_image_tag',
                'build_root': 'some_build_root',
                'build_files': 'some_build_files',
                'build_lock': True,
                'config': {
                    'some_key': 'some_value'
                },
                'outside_port': 80,
                'inside_port': 80,
                'default_container_name': 'some_default_container_name'
            },
            {
                'name': 'wedding_invite_two',
                'git_url': 'some_git_url_two',
                'image_url': 'some_image_url_two',
                'branch': 'some_branch_two',
                'default_image_tag': 'some_default_image_tag_two',
                'build_root': 'some_build_root_two',
                'build_files': 'some_build_files_two',
                'build_lock': False,
                'config': {
                    'some_key_two': 'some_value_two'
                },
                'outside_port': 8080,
                'inside_port': 8080,
                'default_container_name': 'some_default_container_name_two'
            }
        ]
        self.init_build_dicts = [
            {
                'name': 'wedding_invite_three',
                'git_url': 'some_git_url_three',
                'image_url': 'some_image_url_three',
                'branch': 'some_branch_three',
                'default_image_tag': 'some_default_image_tag_three',
                'build_root': 'some_build_root_three',
                'build_files': 'some_build_files_three',
                'build_lock': True,
                'config': {
                    'some_key_three': 'some_value_three'
                },
                'outside_port': 80,
                'inside_port': 80,
                'default_container_name': 'some_default_container_name_three'
            },
            {
                'name': 'wedding_invite_four',
                'git_url': 'some_git_url_four',
                'image_url': 'some_image_url_four',
                'branch': 'some_branch_four',
                'default_image_tag': 'some_default_image_tag_four',
                'build_root': 'some_build_root_four',
                'build_files': 'some_build_files_four',
                'build_lock': False,
                'config': {
                    'some_key_four': 'some_value_four'
                },
                'outside_port': 8080,
                'inside_port': 8080,
                'default_container_name': 'some_default_container_name_four'
            }
        ]
        self.package_name = "test_package"
        self.wedding_invite = WeddingInvite(
            build_dicts=self.build_dicts,
            init_build_dicts=self.init_build_dicts,
            package_name=self.package_name
        )

    def test___init__(self):
        """
        Tests that the __init__ method sets the attributes.
        :return: None
        """
        self.assertEqual(len(self.wedding_invite.builds), 2)
        self.assertEqual(len(self.wedding_invite.init_builds), 2)
        self.assertEqual(self.wedding_invite.package_name, self.package_name)


if __name__ == '__main__':
    main()
