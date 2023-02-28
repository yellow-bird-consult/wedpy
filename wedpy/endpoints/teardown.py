import os

from wedpy.seating_plan.seating_plan import SeatingPlan


def main() -> None:
    seating_plan_path: str = str(os.path.join(os.getcwd(), 'seating_plan.yml'))
    local_wedding_invite_path: str = str(os.path.join(os.getcwd(), 'wedding_invite.yml'))

    seating_plan = SeatingPlan(
        seating_plan_path=seating_plan_path,
        local_wedding_invite_path=local_wedding_invite_path
    )
    seating_plan.destroy_containers()
    seating_plan.destroy_network()


if __name__ == "__main__":
    from tqdm import tqdm
    import time

    my_list = [1, 2, 3, 4, 5]

    for item in tqdm(my_list, desc="Processing items", unit="item"):
        # Perform lengthy action on each item
        time.sleep(1)  # Simulate lengthy action