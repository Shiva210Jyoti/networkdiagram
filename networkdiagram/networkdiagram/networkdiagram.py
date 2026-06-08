import networkx as nx
import matplotlib.pyplot as plt
from collections import deque

class Node:
    def __init__(self, name, duration=0, normal_cost=0, crash_cost=0, crash_duration=None):
        """
        Constructor for declaring a new Node or Activity

        Args:
            name (string): Name of the activity
            duration (int): Normal duration. Defaults to 0.
            normal_cost (float): Cost at normal duration. Defaults to 0.
            crash_cost (float): Cost at minimum duration. Defaults to 0.
            crash_duration (int): Minimum possible duration. Defaults to normal duration.
        """
        self.name = name
        self.duration = duration
        self.normal_duration = duration
        self.crash_duration = crash_duration if crash_duration is not None else duration
        self.normal_cost = normal_cost
        self.crash_cost = crash_cost
        self.predecessors = []
        self.successors = []
        self.early_start = self.early_finish = self.latest_start = self.latest_finish = 0
        
    def add_successor(self,node):
        """
        Used to add a successor of a specific activity

        Args:
            node (Node): Object of Node
        """
        self.successors.append(node)
        node.predecessors.append(self)
        
    def node_summary(self):
        """
        Generates Summary report of an Activity

        Returns:
            string: contains information like name, duration and successors.
        """
        return f"Name : {self.name}, Duration : {self.duration}, Successor : {self.successors}"
    
    def cost_slope(self):
        """
        Cost Slope = (Crash Cost - Normal Cost) / (Normal Duration - Crash Duration)
        Tells how much extra it costs to reduce duration by 1 unit.
        Returns infinity if activity cannot be crashed further.

        Returns:
            float: Cost per unit time reduction
        """
        if self.normal_duration <= self.crash_duration:
            return float('inf')
        return (self.crash_cost - self.normal_cost) / (self.normal_duration - self.crash_duration)

    def can_be_crashed(self):
        """
        Checks if this activity can still be crashed.
        Activity cannot go below its crash_duration.

        Returns:
            bool: True if current duration > crash_duration
        """
        return self.duration > self.crash_duration
        
class CriticalPathMethod:
    """
    It is a Network diagram method used in Project management in which duration of all activities are already known
    """
    def __init__(self):
        """
        Constructor for declaring a new Network
        """
        self.nodes = {} # nodes (dict): A dictionary with (key,value) = (name or alias, object of Node)
        self.probable_paths = [] # List of all possible paths that are possible
        self.total_project_duration = -1 # The maximum time that the project will take to complete
        self.duration_unit = "days" # By default duration is in days
        self.critical_path = [] # It is a probable path having the maximum completion time
        self.edges = [] # Tuple (from,to,duration)
        
    def add_activity(self, name, duration, normal_cost=0, crash_cost=0, crash_duration=None):
        """
        Function to add a single activity with optional crashing parameters

        Args:
            name (string): Name or alias of the activity
            duration (int): Normal duration of the activity
            normal_cost (float): Cost at normal duration. Defaults to 0.
            crash_cost (float): Cost at crash duration. Defaults to 0.
            crash_duration (int): Minimum possible duration. Defaults to normal duration.
        """
        if name not in self.nodes:
            if crash_duration is None:
                crash_duration = duration
            self.nodes[name] = Node(name, duration, normal_cost, crash_cost, crash_duration)
            
    def add_activities_relations(self,activities,durations,predecessors):
        """
        Function to add multiple activities with its relation

        Args:
            activities (list): List of all activities
            durations (list): List of durations
            predecessors (list): List of predecessors
        """
        
        durations.append(0) # For the Terminal Node
        for i in range(0,len(activities)):
            self.add_activity(activities[i],durations[i+1])
            self.add_relation(activities[i],predecessors[i])
            
    def add_relation(self,cur,predecessors):
        """
        Function to add a relation of a single activity

        Args:
            cur (string): Current Activity
            predecessors (string): Consist of predecessors seperated by ',' in which of multiple Predecessors
        """
        
        for p in predecessors.split(','):
            p = p.strip()
            
            if p == '-':
                """
                The first node will not have any predecessor so we will add origin as the predecessor
                """
                parent = self.nodes['O']
                parent.successors.append(cur)
                if cur in self.nodes:
                    self.nodes[cur].predecessors.append('O')
            
            elif p in self.nodes:
                parent = self.nodes[p]
                parent.successors.append(cur)
                if cur in self.nodes:
                    self.nodes[cur].predecessors.append(p)
            
    def find_probable_paths(self,cur=None,path=""):
        """
        Function to find all probable paths

        Args:
            cur (Node, optional): Current Activity. Defaults to None.
            path (string, optional): Path starting from origin to current activity. Defaults to "".
        """
        
        if cur is None:
            if 'O' in self.nodes:
                cur = self.nodes['O']
            else:
                return
        
        path +=  str(cur.name)
            
        if len(cur.successors) == 0:
            path = [p for p in path]
            self.probable_paths.append(path)
            return
        for c in cur.successors:
            if c in self.nodes:
                self.find_probable_paths(self.nodes[c],path)
    
    def find_critical_path(self,cur=None):
        """
        Function to find Critical Path

        Args:
            cur (Node, optional): Current activity. Defaults to None.
        """

        
        for probable_path in self.probable_paths:
            if(sum(self.nodes[cur_node].duration for cur_node in probable_path) > self.total_project_duration):
                self.critical_path = probable_path
                self.total_project_duration = sum(self.nodes[cur_node].duration for cur_node in probable_path)
            elif(sum(self.nodes[cur_node].duration for cur_node in probable_path) == self.total_project_duration):
                self.critical_path.append(probable_path)

    def forward_pass(self):
        """
        Function to calculate Early Start (ES) and Early Finish (EF) for each node
        """
        for node in self.nodes.values():
            node.early_start = 0
            node.early_finish = node.duration
            
        changed = True
        while changed:
            changed = False
            for node in self.nodes.values():
                if node.predecessors:
                    max_ef = max((self.nodes[p].early_finish for p in node.predecessors if p in self.nodes), default=0)
                    if max_ef > node.early_start:
                        node.early_start = max_ef
                        node.early_finish = node.early_start + node.duration
                        changed = True

    def backward_pass(self):
        """
        Function to calculate Late Start (LS) and Late Finish (LF) for each node
        """
        if self.total_project_duration == -1:
            self.total_project_duration = max((n.early_finish for n in self.nodes.values()), default=0)
            
        for node in self.nodes.values():
            node.latest_finish = self.total_project_duration
            node.latest_start = node.latest_finish - node.duration
            
        changed = True
        while changed:
            changed = False
            for node in self.nodes.values():
                if node.successors:
                    min_ls = min((self.nodes[s].latest_start for s in node.successors if s in self.nodes), default=node.latest_finish)
                    if min_ls < node.latest_finish:
                        node.latest_finish = min_ls
                        node.latest_start = node.latest_finish - node.duration
                        changed = True
                
    def get_edges(self):
        """
        Function to convert activity and successors in form of edges for visualization
        """
        for node in self.nodes:
            if self.nodes[node].successors:
                for suc in self.nodes[node].successors:
                    self.edges.append((self.nodes[node].name,suc,{'duration':self.nodes[node].duration}))
                
            else:
                self.edges.append((self.nodes[node].name,'T',{'duration':self.nodes[node].duration}))
    
    def get_hierarchical_layout(self,graph, start_node):
        """
        Calculates node positions for a hierarchical layout.

        Args:
            graph (nx.Graph): The graph to lay out.
            start_node: The node to start the layout from (usually the root).

        Returns:
            dict: A dictionary of node positions {node: (x, y)}.
        """
        pos = {}
        levels = {}

        # 1. Determine the level of each node using BFS
        q = deque([(start_node, 0)])
        visited = {start_node}
        levels[start_node] = 0

        while q:
            node, level = q.popleft()
            neighbors = sorted(list(graph.neighbors(node))) # Sort for consistent layout
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    levels[neighbor] = level + 1
                    q.append((neighbor, level + 1))

        # 2. Group nodes by level
        nodes_by_level = {}
        for node, level in levels.items():
            if level not in nodes_by_level:
                nodes_by_level[level] = []
            nodes_by_level[level].append(node)

        # 3. Assign x, y coordinates
        for level, nodes in nodes_by_level.items():
            num_nodes_in_level = len(nodes)
            # Center the nodes vertically
            y_start = - (num_nodes_in_level - 1) / 2

            for i, node in enumerate(nodes):
                pos[node] = (level, y_start + i)

        return pos
    
    def display_network(self):
        """
        Function to Visualize the Network Diagram.
        Uses Networkx and Matplotlib for plotting.
        """
        G = nx.Graph()
        plt.figure(figsize=(10,4))
        G.add_edges_from(self.edges)    
        
        color_edges = []
        l = 'O'
        for c in self.critical_path:
            color_edges.append((l,c))
            l = c
            
        color_edges.append((self.critical_path[-1],'T'))  
        
        # If the edge falls in critical path then color of edge will be red, else it will be black
        edges_colors = ['red' if ed in color_edges else 'black' for ed in G.edges()]
        
        initial_pos = {'O':(0,0),'T':(10,0)}

        fixed_nodes = ['O','T']

        pos = self.get_hierarchical_layout(G,'O')
        
        labels = {}
        for node in G.nodes():
            if node in self.nodes:
                n = self.nodes[node]
                labels[node] = f"{node}\nES:{n.early_start} EF:{n.early_finish}\nLS:{n.latest_start} LF:{n.latest_finish}"
            else:
                labels[node] = str(node)
        
        nx.draw(G,pos,labels=labels,with_labels=True,node_size=2500,font_size=8,edge_color=edges_colors,arrows=True,arrowstyle='-|>',arrowsize=20)
        
        edge_durations = nx.get_edge_attributes(G,'duration')
        
        nx.draw_networkx_edge_labels(G,pos,edge_labels=edge_durations)

        plt.title("Network diagram with critical Path")
        plt.show()


    def network_summary(self):
        """
        Function to generate entire Network Summary including number of nodes, Activities, Probable paths, Critical Path, Total Project Duration and Edges
        """
        print("\n\n---------------Network Summary-----------------\n\n")
        print("Total number of Activities/Nodes : ",len(self.nodes))
        # print("Nodes : ",self.nodes)
        print("Nodes : ",end="")
        for c in self.nodes:
            print(c," ",end="")
            
        print("\nAll Probable Paths : ")
        for p in self.probable_paths:
            print(p)
        print("Critical Path : ",self.critical_path)
        print("Total project duration : ",self.total_project_duration)
        print("Duration unit :",self.duration_unit)
        print("Edges : ",self.edges)
        
        print("\nNode Properties:")
        print(f"{'Node':<5} | {'ES':<3} | {'EF':<3} | {'LS':<3} | {'LF':<3}")
        print("-" * 35)
        for name, node in self.nodes.items():
            print(f"{name:<5} | {node.early_start:<3} | {node.early_finish:<3} | {node.latest_start:<3} | {node.latest_finish:<3}")

    def get_critical_path_activities(self):
        """
        Returns activity names on the critical path, excluding origin (O) and terminal (T).
        Handles both single critical path and multiple critical paths of equal duration.

        Returns:
            list: Activity names eligible for crashing
        """
        if not self.critical_path:
            return []

        activities = set()

        for item in self.critical_path:
            if isinstance(item, list):
                # Multiple critical paths case — item is itself a path list
                for act in item:
                    if isinstance(act, str) and act in self.nodes and act not in ('O', 'T'):
                        activities.add(act)
            elif isinstance(item, str):
                # Single critical path case — item is an activity name
                if item in self.nodes and item not in ('O', 'T'):
                    activities.add(item)

        return list(activities)

    def crash_project(self, target_duration):
        """
        Implements Time-Cost Trade-off (Crashing) Algorithm.

        Steps:
            1. Find critical path
            2. Find critical path activity with minimum cost slope
            3. Crash it by 1 time unit
            4. Recalculate critical path
            5. Repeat until target duration reached or no more crashing possible

        Args:
            target_duration (int): Desired project duration after crashing

        Returns:
            list: Crashing schedule — one dict per iteration
        """
        # Ensure paths are calculated before starting
        self.forward_pass()
        self.backward_pass()
        self.find_probable_paths()
        self.find_critical_path()

        crash_schedule = []
        total_extra_cost = 0
        iteration = 0

        print(f"\n{'='*60}")
        print(f"  TIME-COST TRADE-OFF (CRASHING) ANALYSIS")
        print(f"{'='*60}")
        print(f"  Initial Project Duration : {self.total_project_duration} days")
        print(f"  Target Duration          : {target_duration} days")
        print(f"{'='*60}\n")

        while self.total_project_duration > target_duration:

            # Get crashable activities on critical path
            critical_activities = self.get_critical_path_activities()
            crashable = [
                act for act in critical_activities
                if self.nodes[act].can_be_crashed()
            ]

            if not crashable:
                print("  No more activities can be crashed. Minimum duration reached.")
                break

            # Select activity with minimum cost slope — cheapest to speed up
            best_activity = min(crashable, key=lambda act: self.nodes[act].cost_slope())
            node = self.nodes[best_activity]
            slope = node.cost_slope()

            # Crash by 1 time unit
            node.duration -= 1
            total_extra_cost += slope
            iteration += 1

            # Recalculate after crashing
            self.probable_paths = []
            self.total_project_duration = -1
            self.forward_pass()
            self.backward_pass()
            self.find_probable_paths()
            self.find_critical_path()

            # Record iteration
            step = {
                'iteration': iteration,
                'activity_crashed': best_activity,
                'new_duration': node.duration,
                'cost_slope': round(slope, 2),
                'total_extra_cost': round(total_extra_cost, 2),
                'project_duration': self.total_project_duration,
                'critical_path': list(self.critical_path)
            }
            crash_schedule.append(step)

            print(f"  Iteration {iteration}:")
            print(f"    Activity Crashed     : {best_activity}")
            print(f"    New Duration         : {node.duration} days")
            print(f"    Cost Slope           : {round(slope, 2)}")
            print(f"    Total Extra Cost     : {round(total_extra_cost, 2)}")
            print(f"    New Project Duration : {self.total_project_duration} days")
            print(f"    Critical Path        : {' -> '.join(str(x) for x in self.critical_path)}")
            print()

        print(f"{'='*60}")
        print(f"  CRASHING COMPLETE")
        print(f"  Final Duration    : {self.total_project_duration} days")
        print(f"  Total Extra Cost  : {round(total_extra_cost, 2)}")
        print(f"{'='*60}\n")

        return crash_schedule

    def display_crash_schedule(self, crash_schedule):
        """
        Displays crashing schedule as a formatted table.

        Args:
            crash_schedule (list): Output from crash_project()
        """
        if not crash_schedule:
            print("No crashing was performed.")
            return

        print(f"\n{'='*70}")
        print(f"  CRASHING SCHEDULE")
        print(f"{'='*70}")
        print(f"  {'Iter':<6} {'Activity':<10} {'New Dur':<10} {'Cost Slope':<12} {'Total Cost':<12} {'Proj Dur'}")
        print(f"  {'-'*60}")

        for step in crash_schedule:
            print(
                f"  {step['iteration']:<6}"
                f"{step['activity_crashed']:<10}"
                f"{step['new_duration']:<10}"
                f"{step['cost_slope']:<12}"
                f"{step['total_extra_cost']:<12}"
                f"{step['project_duration']}"
            )
        print(f"{'='*70}\n")