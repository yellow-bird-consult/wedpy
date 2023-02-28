import os
from typing import List, Optional

import docker
import yaml
from docker.errors import NotFound

from wedpy.seating_plan.dependency import Dependency
from wedpy.wedding_invite.wedding_invite import WeddingInvite


class SeatingPlan:
    def __init__(self, seating_plan_path: str, local_wedding_invite_path: str) -> None:
        self.config: dict = self.load_config(seating_plan_path)
        self.network_name: str = self.config['network_name']
        self.venue: str = self.config['venue']
        self.dependencies: List[Dependency] = [Dependency(**dep) for dep in self.config['attendees']]
        self.local_wedding_invite: WeddingInvite = WeddingInvite.from_yaml(filename=local_wedding_invite_path)
        self.client = docker.from_env()
        self.network = None
        self.full_venue_path: str = str(os.path.join(os.getcwd(), self.venue))

    @staticmethod
    def load_config(config_file) -> dict:
        with open(config_file) as f:
            return yaml.safe_load(f)

    @property
    def invites(self) -> List[WeddingInvite]:
        return [depencency.get_wedding_invite(venue_path=self.venue) for depencency in self.dependencies]

    def create_network(self) -> None:
        self.network = self.client.networks.create(self.network_name)

    def get_network(self) -> None:
        try:
            self.network = self.client.networks.get(self.network_name)
        except NotFound:
            self.create_network()

    def run_containers(self) -> None:
        self.local_wedding_invite.run_containers(runner=self.client.containers, network_name=self.network_name)
        for invite in self.invites:
            invite.run_containers(runner=self.client.containers, network_name=self.network_name)

    def stop_containers(self) -> None:
        for container in self.network.containers:
            container.stop()

    def destroy_containers(self) -> None:
        for container in self.network.containers:
            container.remove()

    def destroy_network(self) -> None:
        self.network.remove()

    def wipe_images(self) -> None:
        self.local_wedding_invite.wipe_images()
        for invite in self.invites:
            invite.wipe_images()

    def install(self) -> None:
        for dependency in self.dependencies:
            dependency.clone_repo(venue_path=self.full_venue_path)

    def build(self, remote: bool = False) -> None:
        # full_path = str(os.getcwd())
        # path = str(os.path.join(*full_path.split("/")[0:-2]))
        self.local_wedding_invite.guest = False
        self.local_wedding_invite.build_images(venue_path=".", remote=False)
        for invite in self.invites:
            invite.build_images(venue_path=self.full_venue_path, remote=remote)
