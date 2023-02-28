import os
import time
from typing import List

import yaml
from docker.client import ContainerCollection

from wedpy.core_unit import CoreUnit
from wedpy.wedding_invite.build import Build


class WeddingInvite:
    def __init__(self, build_dicts: List[dict], init_build_dicts: List[dict], package_name: str) -> None:
        self.builds: List[Build] = [Build(unit=CoreUnit.from_dict(b)) for b in build_dicts]
        self.init_builds: List[Build] = [Build(unit=CoreUnit.from_dict(b)) for b in init_build_dicts]
        self.package_name: str = package_name
        self.guest: bool = True

    def build_images(self, venue_path: str, remote: bool = False) -> None:
        if self.guest is True:
            package_root = str(os.path.join(venue_path, self.package_name))
        else:
            package_root = "."
        for build in self.builds:
            build.build_image(package_root=package_root, tag=None, remote=remote)
        for build in self.init_builds:
            build.build_image(package_root=package_root, tag=None, remote=remote)

    def run_containers(self, runner: ContainerCollection, network_name: str) -> None:
        for build in self.builds:
            build.run_container(runner=runner, network_name=network_name)
        time.sleep(10)
        for build in self.init_builds:
            build.run_container(runner=runner, network_name=network_name)

    def wipe_images(self) -> None:
        for build in self.builds:
            build.delete_image()
        for build in self.init_builds:
            build.delete_image()

    @classmethod
    def from_yaml(cls, filename: str) -> "WeddingInvite":
        with open(filename, 'r') as f:
            data = yaml.safe_load(f)
        return cls(build_dicts=data.get('builds', []),
                   init_build_dicts=data.get('init_builds', []),
                   package_name=data['package_name'])


if __name__ == '__main__':
    import docker
    invite = WeddingInvite.from_yaml('../../tests/assets/wedding_invite.yml')
    network_name = 'my-network'

    # The name of the image to use for the database container
    db_image_name = 'postgres:latest'

    # The name to give the new database container
    db_container_name = 'my-db-container'

    # The name of the image to use for the app container
    app_image_name = 'my-app-image:latest'

    # The name to give the new app container
    app_container_name = 'my-app-container'

    # The Docker client
    docker_client = docker.from_env()

    # Create a new network for the containers to connect to
    network = docker_client.networks.create(network_name)

    invite.run_containers(runner=docker_client.containers, network_name=network_name)
    # print(os.getcwd())
    # invite.build_images('../../sandbox/')
    # print(invite.builds[0].core_unit.git_url)
    # for i in invite.builds:
    #     print(i)
    # print(invite.builds)
    # print(invite.init_builds)