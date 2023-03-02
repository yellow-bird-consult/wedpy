"""
This file defines the Dependency class, which is used to define dependencies which can clone from repositories
and extract the wedding invites from those repositories.
"""
import os.path
import shutil
import subprocess

from wedpy.wedding_invite.wedding_invite import WeddingInvite


class Dependency:
    """
    The Dependency class is used to define dependencies which can clone from repositories and extract the wedding

    Attributes:
        name: the name of the dependency
        default_image_name: the default image name of the dependency if a docker image is built
        git_url: the git url of the dependency
        branch: the branch of the dependency to be checked out in order to build the docker image
        image_url: the dockerhub url of the dependency if the "remote" flag is set to True
    """
    def __init__(self, name: str, default_image_name: str, git_url: str, branch: str, image_url: str) -> None:
        """
        The constructor for the Dependency class.

        :param name: the name of the dependency
        :param default_image_name: the default image name of the dependency if a docker image is built
        :param git_url: the git url of the dependency
        :param branch: the branch of the dependency to be checked out in order to build the docker image
        :param image_url: the dockerhub url of the dependency if the "remote" flag is set to True
        """
        self.name: str = name
        self.default_image_name: str = default_image_name
        self.git_url: str = git_url
        self.branch: str = branch
        self.image_url: str = image_url

    def get_wedding_invite(self, venue_path: str) -> WeddingInvite:
        """
        Gets the wedding invite from the dependency.

        :param venue_path: the path to the venue directory where the dependencies are cloned
        :return: the wedding invite from the cloned dependency
        """
        file_path = os.path.join(venue_path, self.name, 'wedding_invite.yml')
        return WeddingInvite.from_yaml(filename=file_path)

    def clone_repo(self, venue_path: str) -> None:
        """
        Clones the repository of the dependency into the venue.

        :param venue_path: the path to the venue directory where the dependencies are cloned to
        :return: None
        """
        if self.git_url is None:
            return None

        clone_path = str(os.path.join(venue_path, self.name))

        if os.path.exists(clone_path):
            shutil.rmtree(clone_path)

        # Run the git clone command using Popen
        process = subprocess.Popen(f"cd {venue_path} && git clone {self.git_url}", stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, shell=True)
        # Wait for the process to complete and capture the output
        stdout, stderr = process.communicate()

        # Print the output
        if process.returncode == 0:
            print(f'Successfully cloned {self.name} to {venue_path}')

            process = subprocess.Popen(f"cd {clone_path} && git checkout {self.branch}",
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE,
                                       shell=True)
            # Wait for the process to complete and capture the output
            stdout, stderr = process.communicate()
            if process.returncode == 0:
                print(f'Successfully checked out {self.branch} branch for {self.name}')
            else:
                print(f'Error checking out {self.branch} branch for {self.name}:')
                print(stdout.decode())
                print(stderr.decode())
        else:
            print(f'Error cloning {self.name}:')
            print(stdout.decode())
            print(stderr.decode())
