import os.path
import shutil
import subprocess
from wedpy.wedding_invite.wedding_invite import WeddingInvite


class Dependency:

    def __init__(self, name: str, default_image_name: str, git_url: str, branch: str, image_url: str) -> None:
        self.name: str = name
        self.default_image_name: str = default_image_name
        self.git_url: str = git_url
        self.branch: str = branch
        self.image_url: str = image_url

    def get_wedding_invite(self, venue_path: str) -> WeddingInvite:
        file_path = os.path.join(venue_path, self.name, 'wedding_invite.yml')
        return WeddingInvite.from_yaml(filename=file_path)

    def clone_repo(self, venue_path: str) -> None:
        # The URL of the repository to clone
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
