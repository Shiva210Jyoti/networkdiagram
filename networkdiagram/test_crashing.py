"""
Test file for Time-Cost Trade-off (Crashing) implementation.
Run from root folder: python test_crashing.py
"""
import sys
sys.path.insert(0, '.')
from networkdiagram.networkdiagram import CriticalPathMethod


def test_crashing():
    """
    Standard textbook crashing example.
    Network: O -> A -> C -> E (critical path)
             O -> B -> D
    """
    cpm = CriticalPathMethod()

    # Add origin node
    cpm.add_activity('O', 0)

    # Add activities: duration, normal_cost, crash_cost, crash_duration
    cpm.add_activity('A', 6, normal_cost=800,  crash_cost=1000, crash_duration=4)
    cpm.add_activity('B', 4, normal_cost=500,  crash_cost=700,  crash_duration=2)
    cpm.add_activity('C', 5, normal_cost=600,  crash_cost=900,  crash_duration=3)
    cpm.add_activity('D', 3, normal_cost=400,  crash_cost=500,  crash_duration=2)
    cpm.add_activity('E', 4, normal_cost=700,  crash_cost=1100, crash_duration=2)

    # Add relations using existing method
    cpm.add_relation('A', '-')   # A starts from origin
    cpm.add_relation('B', '-')   # B starts from origin
    cpm.add_relation('C', 'A')   # C follows A
    cpm.add_relation('D', 'B')   # D follows B
    cpm.add_relation('E', 'C')   # E follows C

    # Run crashing to target 13 days
    crash_schedule = cpm.crash_project(target_duration=13)
    cpm.display_crash_schedule(crash_schedule)

    # Verify results
    assert cpm.total_project_duration <= 13, "Target duration not reached"
    assert len(crash_schedule) > 0, "No crashing iterations recorded"
    print("All tests passed!")


if __name__ == "__main__":
    test_crashing()