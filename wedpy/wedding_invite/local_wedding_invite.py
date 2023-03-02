"""
This file defines the LocalWeddingInvite class  which is used to build and run the local wedding invite for the
main repo but not the dependencies' wedding invites.
"""
from multiprocessing import Pool
from typing import List

from docker.client import ContainerCollection
from tqdm import tqdm

from wedpy.wedding_invite.build import Build
from wedpy.wedding_invite.wedding_invite import WeddingInvite


class LocalWeddingInvite:
    """
    The LocalWeddingInvite class is used to build and run the local wedding invite for the main repo but not the
    dependencies' wedding invites.

    Attributes:
        local_wedding_invite (WeddingInvite): the loaded local wedding invite
        num_processes (int): number of processes to use for building images
    """
    def __init__(self, local_wedding_invite_path: str, num_processes: int = 4) -> None:
        """
        The constructor for the LocalWeddingInvite class.

        :param local_wedding_invite_path: path to the local wedding invite yaml file
        :param num_processes: number of processes to use for building images
        """
        self.local_wedding_invite: WeddingInvite = WeddingInvite.from_yaml(filename=local_wedding_invite_path)
        self.num_processes: int = num_processes

    def build_images(self, dev: bool = False) -> None:
        """
        Builds the docker images for the local wedding invite.

        :param dev: whether or not to build the main images
        :return: None
        """
        package_root = "."
        if dev is False:
            total_builds: List[Build] = self.local_wedding_invite.builds + self.local_wedding_invite.init_builds
        else:
            total_builds: List[Build] = self.local_wedding_invite.init_builds

        with Pool(processes=self.num_processes) as pool:
            results = []
            for build in total_builds:
                results.append(pool.apply_async(build.build_image, args=(package_root, None, False)))

            # Wait for all processes to finish
            for result in tqdm(results, desc=f"{self.local_wedding_invite.package_name} builds", unit="item",
                               total=len(total_builds)):
                result.get()

    def run_containers(self, runner: ContainerCollection, network_name: str, dev: bool = False) -> None:
        """
        Runs the containers for the local wedding invite.

        :param runner: the docker client container collection
        :param network_name: the name of the docker network to connect the containers to
        :param dev: whether or not to run the main containers
        :return:
        """
        if dev is True:
            self.local_wedding_invite.builds = []
        self.local_wedding_invite.run_containers(runner=runner, network_name=network_name)

    def destroy_init_containers(self) -> None:
        """
        Destroys the init containers for the local wedding invite.

        :return: None
        """
        self.local_wedding_invite.destroy_init_containers()

    def wipe_images(self) -> None:
        """
        Wipes the images for the local wedding invite.

        :return: None
        """
        self.local_wedding_invite.wipe_images()
