"""
This file defines the SeatingPlan class for managing dependencies needed to run a service.
"""
import os
from typing import List
import shutil

import docker
import yaml
from docker.errors import NotFound

from wedpy.seating_plan.dependency import Dependency
from wedpy.wedding_invite.wedding_invite import WeddingInvite


class SeatingPlan:
    """
    The SeatingPlan class is used to manage dependencies needed to run a service.

    Attributes:
        network_name (str): the name of the network to manage the docker containers for service
        venue (str): the path to where the cloned dependency repos will be stored
        dependencies (List[Dependency]): the list of dependencies needed to run the service
        client (docker.client.DockerClient): the docker client used to manage the docker containers and builds
        full_venue_path (str): the full path to the venue directory
    """
    def __init__(self, seating_plan_path: str) -> None:
        """
        The constructor for the SeatingPlan class.

        :param seating_plan_path: the path to the seating plan file.
        """
        self.config: dict = self.load_config(seating_plan_path)
        self.network_name: str = self.config['network_name']
        self.venue: str = self.config['venue']
        self.dependencies: List[Dependency] = [Dependency(
            name=dep["name"], default_image_name=dep["default_image_name"],
            git_url=dep["git_url"], branch=dep["branch"],
            image_url=dep["image_url"]) for dep in self.config['attendees']]
        self.post_office_path: str = self.config['post_office']
        self.full_post_office_path: str = str(os.path.join(os.getcwd(), self.config['post_office']))
        self.client = docker.from_env()
        self.full_venue_path: str = str(os.path.join(os.getcwd(), self.venue))

    @staticmethod
    def load_config(config_file) -> dict:
        """
        Loads the data from the seating plan file.

        :param config_file: the path to the seating plan file.
        :return: the data from the seating plan file.
        """
        with open(config_file) as f:
            return yaml.safe_load(f)

    @property
    def invites(self) -> List[WeddingInvite]:
        return [depencency.get_wedding_invite(venue_path=self.venue) for depencency in self.dependencies]

    @property
    def network(self):
        try:
            return self.client.networks.get(self.network_name)
        except NotFound:
            self.client.networks.create(self.network_name)
            return self.client.networks.get(self.network_name)

    def post_invites(self) -> None:
        """
        Posts the wedding invites for the dependencies to the self.post_office_path.

        :return: None
        """
        for dependency in self.dependencies:
            dst_folder = os.path.join(self.full_post_office_path, dependency.name)
            if not os.path.exists(dst_folder):
                os.mkdir(dst_folder)
            dst_path = os.path.join(dst_folder, "wedding_invite.yaml")
            shutil.copy(dependency.invite_path(venue_path=self.full_venue_path), dst_path)

    def run_containers(self) -> None:
        """
        Runs the containers for the service.

        :return: None
        """
        _ = self.network
        for invite in self.invites:
            invite.run_containers(runner=self.client.containers, network_name=self.network_name)

    def stop_containers(self) -> None:
        """
        Stops the containers belonging to the network.

        :return: None
        """
        for container in self.network.containers:
            container.stop()

    def destroy_containers(self) -> None:
        """
        Destroys the containers belonging to the network.

        :return: None
        """
        for container in self.network.containers:
            container.stop()
            container.remove(force=True)
            print(f"{container.name} destroyed successfully.")
        for invite in self.invites:
            invite.destroy_init_containers()

    def destroy_network(self) -> None:
        """
        Destroys the network.

        :return: None
        """
        self.network.remove()

    def wipe_images(self) -> None:
        """
        Removes the images belonging to the network.

        :return: None
        """
        for invite in self.invites:
            invite.wipe_images()

    def install(self) -> None:
        """
        Clones all the dependencies in the seating plan.

        :return: None
        """
        for dependency in self.dependencies:
            dependency.clone_repo(venue_path=self.full_venue_path)

    def build(self, remote: bool = False) -> None:
        """
        Builds the images for the dependencies in the seating plan.

        :param remote: if True, the images will be pulled from DockerHub as opposed to building locally.
        :return: None
        """
        for invite in self.invites:
            invite.build_images(venue_path=self.full_venue_path, remote=remote)
