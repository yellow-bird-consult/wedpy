import os
import platform
from typing import Optional

import docker
from docker.client import ContainerCollection
from docker.errors import ImageNotFound

from wedpy.core_unit import CoreUnit


class Build:

    def __init__(self, unit: CoreUnit) -> None:
        self.core_unit: CoreUnit = unit

    def pull_image(self) -> None:
        docker_client = docker.from_env()
        docker_client.images.pull(self.core_unit.image_url)

    def build_image(self, package_root: str, tag: Optional[str], remote: bool = False) -> None:

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
        container = runner.get(self.core_unit.default_container_name)
        if container is not None:
            container.remove(force=True)

    def delete_image(self) -> None:
        client = docker.from_env()
        try:
            image = client.images.get(self.core_unit.default_container_name)
            client.images.remove(image.id, force=True)
            print(f"{self.core_unit.default_container_name} deleted successfully.")
        except ImageNotFound as e:
            print(f"Error deleting {self.core_unit.default_container_name}: {e}")

    def run_container(self, runner: ContainerCollection, network_name: str) -> None:
        if self.core_unit.outside_port is None:
            ports = None
        else:
            ports = {f'{self.core_unit.outside_port}/tcp': ('0.0.0.0', self.core_unit.outside_port)}
        runner.run(
            image=self.core_unit.default_image_tag,
            environment=self.core_unit.config,
            detach=True,
            network=network_name,
            name=self.core_unit.default_container_name,
            ports=ports,
        )
