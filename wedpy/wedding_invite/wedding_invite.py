"""
This file defines the WeddingInvite class which is responsible for building the images for a package.
"""
import os
import time
from multiprocessing import Pool
from typing import List

import docker
import yaml
from docker.client import ContainerCollection
from tqdm import tqdm

from wedpy.core_unit import CoreUnit
from wedpy.wedding_invite.build import Build


class WeddingInvite:
    """
    The WeddingInvite class is responsible for building the images for a package.

    Attributes:
        builds (List[Build]): the builds defined in the wedding invite yaml file
        init_builds (List[Build]): the init builds defined in the wedding invite yaml file
        package_name (str): the name of the package loaded from the wedding invite yaml file
    """
    def __init__(self, build_dicts: List[dict], init_build_dicts: List[dict], package_name: str) -> None:
        """
        The constructor for the WeddingInvite class.

        :param build_dicts: build dicts loaded from the wedding invite yaml file
        :param init_build_dicts: init build dicts loaded from the wedding invite yaml file
        :param package_name: the name of the package loaded from the wedding invite yaml file
        """
        self.builds: List[Build] = [Build(unit=CoreUnit.from_dict(b)) for b in build_dicts]
        self.init_builds: List[Build] = [Build(unit=CoreUnit.from_dict(b)) for b in init_build_dicts]
        self.package_name: str = package_name

    def build_images(self, venue_path: str, remote: bool = False) -> None:
        """
        Builds the docker images defined in the wedding invite.

        :param venue_path: the path to where the dependencies are located
        :param remote: whether or not to pull images from the registry, if True, pull them
        :return: None
        """
        package_root = str(os.path.join(venue_path, self.package_name))

        total_builds: List[Build] = self.builds + self.init_builds

        with Pool(processes=4) as pool:
            results = []
            for build in total_builds:
                results.append(pool.apply_async(build.build_image, args=(package_root, None, remote)))

            # Wait for all processes to finish
            for result in tqdm(results, desc=f"{self.package_name} builds", unit="item",
                               total=len(total_builds)):
                result.get()

    def run_containers(self, runner: ContainerCollection, network_name: str) -> None:
        """
        Runs the containers defined in the wedding invite.

        :param runner: the docker client container collection
        :param network_name: the name of the docker network to connect the containers to
        :return: None
        """
        for build in tqdm(self.builds, desc=f"{self.package_name} running containers", unit="item"):
            build.run_container(runner=runner, network_name=network_name)
        time.sleep(10)
        for build in tqdm(self.init_builds, desc=f"{self.package_name} running init containers", unit="item"):
            build.run_container(runner=runner, network_name=network_name)

    def destroy_init_containers(self) -> None:
        """
        Destroys the init containers defined in the wedding invite.

        :return: None
        """
        client = docker.from_env()
        for build in self.init_builds:
            container = client.containers.get(build.core_unit.default_container_name)
            container.remove(force=True)
            print(f"{build.core_unit.default_container_name} destroyed successfully.")

    def wipe_images(self) -> None:
        """
        Wipes the images defined in the wedding invite.

        :return: None
        """
        for build in self.builds:
            build.delete_image()
        for build in self.init_builds:
            build.delete_image()

    @classmethod
    def from_yaml(cls, filename: str) -> "WeddingInvite":
        """
        Loads a wedding invite from a yaml file.

        :param filename: the path to the yaml file
        :return: a WeddingInvite object
        """
        with open(filename, 'r') as f:
            data = yaml.safe_load(f)
        return cls(build_dicts=data.get('builds', []),
                   init_build_dicts=data.get('init_builds', []),
                   package_name=data['package_name'])
