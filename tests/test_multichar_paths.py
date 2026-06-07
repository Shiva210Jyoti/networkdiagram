from networkdiagram import CriticalPathMethod


def test_find_critical_path_supports_multi_character_activity_names():
    cpm = CriticalPathMethod()
    cpm.add_activity("O", 0)
    cpm.add_activity("A1", 3)
    cpm.add_activity("B2", 5)
    cpm.add_activity("TaskX", 2)

    cpm.add_relation("A1", "-")
    cpm.add_relation("B2", "A1")
    cpm.add_relation("TaskX", "B2")

    cpm.find_probable_paths()
    cpm.find_critical_path()

    assert cpm.probable_paths == [["O", "A1", "B2", "TaskX"]]
    assert cpm.critical_path == ["O", "A1", "B2", "TaskX"]
    assert cpm.total_project_duration == 10
