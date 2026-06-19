from networkdiagram import CriticalPathMethod

cpm = CriticalPathMethod()

activities = ['A', 'B', 'C', 'D']
durations = [2, 5, 4, 2]
predecessors = ['-', 'A', 'B', 'B,C']

cpm.add_activity('O', 0)

cpm.add_activities_relations(
    activities,
    durations,
    predecessors
)

cpm.find_probable_paths()
cpm.find_critical_path()

cpm.forward_pass()
cpm.backward_pass()

cpm.network_summary()

cpm.get_edges()
cpm.display_network()