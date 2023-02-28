from typing import List, Optional

import docker
import yaml
from docker.errors import NotFound

from wedpy.seating_plan.dependency import Dependency
from wedpy.wedding_invite.wedding_invite import WeddingInvite


class SeatingPlan:
    def __init__(self, config_file: str) -> None:
        self.config: dict = self.load_config(config_file)
        self.network_name: str = self.config['network_name']
        self.venue: str = self.config['venue']
        self.dependencies: List[Dependency] = [Dependency(**dep) for dep in self.config['attendees']]
        self.client = docker.from_env()
        self.network = None
        self.invites: Optional[List[WeddingInvite]] = None

    @staticmethod
    def load_config(config_file) -> dict:
        with open(config_file) as f:
            return yaml.safe_load(f)

    def get_invites(self) -> None:
        self.invites = [depencency.get_wedding_invite(venue_path=self.venue) for depencency in self.dependencies]

    def create_network(self) -> None:
        self.network = self.client.networks.create(self.network_name)

    def get_network(self) -> None:
        try:
            self.network = self.client.networks.get(self.network_name)
        except NotFound:
            self.create_network()

    def run_containers(self) -> None:
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

    def install(self) -> None:
        for dependency in self.dependencies:
            dependency.clone_repo(venue_path=self.venue)

    def build(self) -> None:
        for invite in self.invites:
            invite.build_images(venue_path=self.venue)
