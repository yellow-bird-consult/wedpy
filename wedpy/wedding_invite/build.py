"""
This file defines the Build class, which is used to build/pull a docker image and run a container for each build.
"""
import os
import platform
from typing import Optional

import docker
from docker.client import ContainerCollection
from docker.errors import ImageNotFound

from wedpy.core_unit import CoreUnit


class Build:
    """
    The Build class is used to build/pull a docker image and run a container for each build.

    Attributes:
        core_unit (CoreUnit): the CoreUnit data loaded from the wedding invite for each build object to build.
    """
    def __init__(self, unit: CoreUnit) -> None:
        """
        The constructor for the Build class.

        :param unit: the CoreUnit data loaded from the wedding invite for each build object to build.
        """
        self.core_unit: CoreUnit = unit

    def pull_image(self) -> None:
        """
        Pulls the docker image from the docker registry.

        :return: None
        """
        docker_client = docker.from_env()
        docker_client.images.pull(self.core_unit.image_url)

    def build_image(self, package_root: str, tag: Optional[str], remote: bool = False) -> None:
        """
        Builds the docker image from the Dockerfile.

        :param package_root: root directory of the package
        :param tag: tag to use for the image build
        :param remote: whether to pull the image from the registry or build it locally if True, pull it
        :return: None
        """
        if self.core_unit.git_url is None or remote is True:
            self.pull_image()
            return None

        build_context_path = str(os.path.join(package_root, self.core_unit.build_root))

        if self.core_unit.build_lock is True:
            dockerfile_path = "Dockerfile"
        else:
            cpu_arch = platform.processor()
            dockerfile_path = self.core_unit.build_files[cpu_arch]

        if tag is None:
            image_tag = self.core_unit.default_image_tag
        else:
            image_tag = tag

        docker_client = docker.from_env()
        image, build_logs = docker_client.images.build(
            path=build_context_path,
            dockerfile=dockerfile_path,
            tag=image_tag
        )

    def delete_container(self, runner: ContainerCollection) -> None:
        """
        Deletes the container.

        :param runner: the runner of the network to delete the container from.
        :return: None
        """
        container = runner.get(self.core_unit.default_container_name)
        if container is not None:
            container.remove(force=True)

    def delete_image(self) -> None:
        """
        Deletes the image from the local docker registry.

        :return: None
        """
        client = docker.from_env()
        try:
            image = client.images.get(self.core_unit.default_image_tag)
            client.images.remove(image.id, force=True)
            print(f"{self.core_unit.default_container_name} deleted successfully.")
        except ImageNotFound as e:
            print(f"Error deleting {self.core_unit.default_container_name}: {e}")

    def run_container(self, runner: ContainerCollection, network_name: str, remote: bool = False) -> None:
        """
        Runs the container.

        :param runner: the runner of the network to run the container in.
        :param network_name: the name of the network to run the container in.
        :return: None
        """
        if self.core_unit.outside_port is None:
            ports = None
        else:
            ports = {f'{self.core_unit.inside_port}/tcp': ('0.0.0.0', self.core_unit.outside_port)}
        if remote is True:
            image = self.core_unit.image_url
        else:
            image = self.core_unit.default_image_tag
        runner.run(
            image=image,
            environment=self.core_unit.config,
            detach=True,
            network=network_name,
            name=self.core_unit.default_container_name,
            ports=ports,
        )
