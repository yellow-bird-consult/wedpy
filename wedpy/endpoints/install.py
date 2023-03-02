import os

from wedpy.seating_plan.seating_plan import SeatingPlan


def main() -> None:
    seating_plan_path: str = str(os.path.join(os.getcwd(), 'seating_plan.yml'))

    seating_plan = SeatingPlan(seating_plan_path=seating_plan_path)
    seating_plan.install()
