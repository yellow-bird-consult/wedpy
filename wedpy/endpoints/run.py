import argparse
import os

from wedpy.seating_plan.seating_plan import SeatingPlan
from wedpy.wedding_invite.local_wedding_invite import LocalWeddingInvite


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-remote', action='store_true')
    parser.add_argument('-dev', action='store_true')

    args = parser.parse_args()

    dev = args.dev if args.dev else False
    remote = args.remote if args.remote else False

    seating_plan_path: str = str(os.path.join(os.getcwd(), 'seating_plan.yml'))
    local_wedding_invite_path: str = str(os.path.join(os.getcwd(), 'wedding_invite.yml'))

    seating_plan = SeatingPlan(seating_plan_path=seating_plan_path)
    if remote is True:
        seating_plan.venue = seating_plan.post_office_path
    seating_plan.run_containers()

    local_wedding_invite = LocalWeddingInvite(local_wedding_invite_path=local_wedding_invite_path)
    local_wedding_invite.run_containers(
        runner=seating_plan.client.containers, network_name=seating_plan.network_name, dev=dev
    )
