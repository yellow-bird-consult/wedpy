import os

from wedpy.seating_plan.seating_plan import SeatingPlan
from wedpy.wedding_invite.local_wedding_invite import LocalWeddingInvite


def main() -> None:
    seating_plan_path: str = str(os.path.join(os.getcwd(), 'seating_plan.yml'))
    local_wedding_invite_path: str = str(os.path.join(os.getcwd(), 'wedding_invite.yml'))

    seating_plan = SeatingPlan(seating_plan_path=seating_plan_path)
    seating_plan.wipe_images()

    local_wedding_invite = LocalWeddingInvite(local_wedding_invite_path=local_wedding_invite_path)
    local_wedding_invite.wipe_images()
