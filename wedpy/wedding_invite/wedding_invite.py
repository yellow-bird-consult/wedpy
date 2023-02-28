import os
import time
from typing import List

import yaml
from docker.client import ContainerCollection
from tqdm import tqdm

from wedpy.core_unit import CoreUnit
from wedpy.wedding_invite.build import Build
import docker


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
        for build in tqdm(self.builds, desc=f"{self.package_name} builds", unit="item"):
            build.build_image(package_root=package_root, tag=None, remote=remote)
        for build in tqdm(self.init_builds, desc=f"{self.package_name} init builds", unit="item"):
            build.build_image(package_root=package_root, tag=None, remote=remote)

    def run_containers(self, runner: ContainerCollection, network_name: str) -> None:
        for build in tqdm(self.builds, desc=f"{self.package_name} running containers", unit="item"):
            build.run_container(runner=runner, network_name=network_name)
        time.sleep(10)
        for build in tqdm(self.init_builds, desc=f"{self.package_name} running init containers", unit="item"):
            build.run_container(runner=runner, network_name=network_name)

    def destroy_init_containers(self) -> None:
        client = docker.from_env()
        for build in self.init_builds:
            container = client.containers.get(build.core_unit.default_container_name)
            container.remove(force=True)
            print(f"{build.core_unit.default_container_name} destroyed successfully.")

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
