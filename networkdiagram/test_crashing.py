"""
Test file for Time-Cost Trade-off (Crashing) implementation.
Run from root folder: python test_crashing.py
"""
import sys
sys.path.insert(0, '.')
from networkdiagram.networkdiagram import CriticalPathMethod


def test_crashing():
    cpm = CriticalPathMethod()
    cpm.add_activity('O', 0)

    activities      = ['A', 'B', 'C', 'D', 'E']
    durations       = [6, 4, 5, 3, 4]
    predecessors    = ['-', '-', 'A', 'B', 'C']
    normal_costs    = [800, 500, 600, 400, 700]
    crash_costs     = [1000, 700, 900, 500, 1100]
    crash_durations = [4, 2, 3, 2, 2]

    cpm.add_activities_relations(
        activities, durations, predecessors,
        normal_costs=normal_costs,
        crash_costs=crash_costs,
        crash_durations=crash_durations
    )

    crash_schedule = cpm.crash_project(target_duration=13)
    cpm.display_crash_schedule(crash_schedule)

    assert cpm.total_project_duration <= 13
    assert len(crash_schedule) > 0
    print("All tests passed!")


if __name__ == "__main__":
    test_crashing()