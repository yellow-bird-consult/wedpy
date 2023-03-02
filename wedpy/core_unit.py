"""
This file defines the CoreUnit class which is responsible for storing the data for each build in the wedding invite.
"""
from typing import Dict, Optional


class CoreUnit:
    """
    The CoreUnit class is used to store the data for each build in the wedding invite.

    Attributes:
        name (str): the name of the build
        git_url (str): the git url of the build
        image_url (str): the image url of the build
        branch (str): the github branch of the build
        default_image_tag (str): the default image tag of the build
        build_root (str): the path to the build root of the build
        build_files (Dict[str, str]): a map pointing to different build files depending on the CPU architecture
        build_lock (bool): a boolean indicating whether or not to lock the build, if True, the build will not check CPU architecture
        config (Dict[str, str]): a map of configuration options for the build to be passed into the docker build
        outside_port (int): the port to be exposed on the host machine
        inside_port (int): the port to be exposed on the container
    """
    def __init__(self, name: str, git_url: str, image_url: str, branch: str,
                 default_image_tag: str, build_root: str, build_files: Optional[Dict[str, str]],
                 build_lock: bool, config: Dict[str, str],
                 outside_port: Optional[int], inside_port: Optional[int], default_container_name: str) -> None:
        """
        The constructor for the CoreUnit class.

        :param name: the name of the build
        :param git_url: the git url of the build
        :param image_url: the image url of the build
        :param branch: the github branch of the build
        :param default_image_tag: the default image tag of the build
        :param build_root: the path to the build root of the build
        :param build_files: a map pointing to different build files depending on the CPU architecture
        :param build_lock: a boolean indicating whether or not to lock the build, if True, the build will not check CPU architecture
        :param config: a map of configuration options for the build to be passed into the docker build
        :param outside_port: the port to be exposed on the host machine
        :param inside_port: the port to be exposed on the container
        :param default_container_name: the default name of the container
        """
        self.name: str = name
        self.git_url: str = git_url
        self.image_url: str = image_url
        self.branch: str = branch
        self.default_image_tag: str = default_image_tag
        self.build_root: str = build_root
        self.build_files: Optional[Dict[str, str]] = build_files
        self.build_lock: bool = build_lock
        self.config: Dict[str, str] = config
        self.outside_port: Optional[int] = outside_port
        self.inside_port: Optional[int] = inside_port
        self.default_container_name: str = default_container_name

    def __str__(self):
        return f"Name: {self.name}\nGit URL: {self.git_url}\nImage URL: {self.image_url}\n" \
               f"Branch: {self.branch}\nDefault Image Tag: {self.default_image_tag}\n" \
               f"Build Root: {self.build_root}\nBuild Files: " \
               f"{self.build_files}"

    @classmethod
    def from_dict(cls, build_dict) -> "CoreUnit":
        """
        Creates a CoreUnit object from a dictionary.

        :param build_dict: the dictionary to create the CoreUnit object from
        :return: the CoreUnit object created from the dictionary
        """
        name: str = build_dict['name']
        git_url: Optional[str] = build_dict.get('git_url')
        image_url = build_dict['image_url']
        branch: Optional[str] = build_dict.get('branch')
        default_image_tag: str = build_dict['default_image_tag']
        build_root: Optional[str] = build_dict.get('build_root')
        build_files: Optional[str] = build_dict.get('build_files')
        build_lock: bool = build_dict.get('build_lock', False)
        config: Dict[str, str] = build_dict.get('config', {})
        outside_port: Optional[int] = build_dict.get('outside_port')
        inside_port: Optional[int] = build_dict.get('inside_port')
        default_container_name: str = build_dict['default_container_name']

        return cls(name, git_url, image_url, branch, default_image_tag,
                   build_root, build_files, build_lock, config,
                   outside_port, inside_port, default_container_name)
