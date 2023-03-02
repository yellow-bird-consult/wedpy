import os

from wedpy.seating_plan.seating_plan import SeatingPlan
from wedpy.wedding_invite.local_wedding_invite import LocalWeddingInvite


def main() -> None:
    seating_plan_path: str = str(os.path.join(os.getcwd(), 'seating_plan.yml'))
    local_wedding_invite_path: str = str(os.path.join(os.getcwd(), 'wedding_invite.yml'))

    seating_plan = SeatingPlan(seating_plan_path=seating_plan_path)
    seating_plan.destroy_containers()
    seating_plan.destroy_network()

    local_wedding_invite = LocalWeddingInvite(local_wedding_invite_path=local_wedding_invite_path)
    local_wedding_invite.destroy_init_containers()
