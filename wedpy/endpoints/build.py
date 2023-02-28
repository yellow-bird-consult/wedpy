import argparse
import os

from wedpy.seating_plan.seating_plan import SeatingPlan


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('-remote', action='store_true')

    args = parser.parse_args()

    remote = args.remote if args.remote else False
    seating_plan_path: str = str(os.path.join(os.getcwd(), 'seating_plan.yml'))
    local_wedding_invite_path: str = str(os.path.join(os.getcwd(), 'wedding_invite.yml'))

    seating_plan = SeatingPlan(
        seating_plan_path=seating_plan_path,
        local_wedding_invite_path=local_wedding_invite_path
    )
    seating_plan.build(remote=remote)
