"""
This file defines the endpoint for wedpy-build which builds the images for a package.
"""
import argparse
import os

from wedpy.seating_plan.seating_plan import SeatingPlan
from wedpy.wedding_invite.local_wedding_invite import LocalWeddingInvite


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-remote', action='store_true')
    parser.add_argument('-dev', action='store_true')
    parser.add_argument('-no_pool', action='store_true')

    args = parser.parse_args()

    remote: bool = args.remote if args.remote else False
    dev: bool = args.dev if args.dev else False
    pool: bool = False if args.no_pool else True

    seating_plan_path: str = str(os.path.join(os.getcwd(), 'seating_plan.yml'))
    local_wedding_invite_path: str = str(os.path.join(os.getcwd(), 'wedding_invite.yml'))

    local_wedding_invite = LocalWeddingInvite(local_wedding_invite_path=local_wedding_invite_path)

    if pool is True:
        local_wedding_invite.build_images(dev=dev)
    else:
        local_wedding_invite.build_images_without_pool(dev=dev)

    seating_plan = SeatingPlan(seating_plan_path=seating_plan_path)
    if remote is True:
        seating_plan.venue = seating_plan.post_office_path
        seating_plan.full_venue_path = seating_plan.full_post_office_path
    seating_plan.build(remote=remote, pool=pool)
