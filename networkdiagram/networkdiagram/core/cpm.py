from typing import Dict, List, Optional, Tuple, Union

import networkx as nx

from networkdiagram.core.node import Node
from networkdiagram.visualization.network_plot import display_network as _display_network
from networkdiagram.visualization.network_plot import get_hierarchical_layout as _get_hierarchical_layout


class CriticalPathMethod:
    """
    It is a Network diagram method used in Project management in which duration of all activities are already known
    """
    
    def __init__(self) -> None:
        """
        Constructor for declaring a new Network
        """
        self.nodes: Dict[str, Node] = {}  # nodes (dict): A dictionary with (key,value) = (name or alias, object of Node)
        self.probable_paths: List[List[str]] = []  # List of all possible paths that are possible
        self.total_project_duration: float = -1  # The maximum time that the project will take to complete
        self.duration_unit: str = "days"  # By default duration is in days
        self.critical_path: List[str] = []  # It is a probable path having the maximum completion time
        self.edges: List[Tuple[str, str, Dict[str, float]]] = []  # Tuple (from,to,duration)
        
    def add_activity(self, name: str, duration: float) -> None:
        """
        Function to add a single activity

        Args:
            name (str): Name or alias of the activity
            duration (float): Duration of the activity
        """
        if name not in self.nodes:
            self.nodes[name] = Node(name, duration)
            
    def add_activities_relations(self, activities: List[str], durations: List[float], predecessors: List[str]) -> None:
        """
        Function to add multiple activities with its relation

        Args:
            activities (list): List of all activities
            durations (list): List of durations
            predecessors (list): List of predecessors
        """
        durations.append(0)  # For the Terminal Node
        for i in range(len(activities)):
            self.add_activity(activities[i], durations[i + 1])
            self.add_relation(activities[i], predecessors[i])
            
    def add_relation(self, cur: str, predecessors: str) -> None:
        """
        Function to add a relation of a single activity

        Args:
            cur (str): Current Activity
            predecessors (str): Consist of predecessors separated by ',' in which of multiple Predecessors
        """
        for p in predecessors.split(','):
            p = p.strip()
            
            if p == '-':
                """
                The first node will not have any predecessor so we will add origin as the predecessor
                """
                if 'O' in self.nodes:
                    parent = self.nodes['O']
                    parent.successors.append(cur)
                if cur in self.nodes:
                    self.nodes[cur].predecessors.append('O')
            
            elif p in self.nodes:
                parent = self.nodes[p]
                parent.successors.append(cur)
                if cur in self.nodes:
                    self.nodes[cur].predecessors.append(p)
            
    def find_probable_paths(self, cur: Optional[str] = None, path: Optional[Union[str, List[str]]] = None) -> None:
        """
        Function to find all probable paths

        Args:
            cur (str, optional): Current Activity name. Defaults to None.
            path (Union[str, List[str]], optional): Path starting from origin to current activity. Defaults to None.
        """
        if cur is None:
            if 'O' in self.nodes:
                cur = 'O'
            else:
                return
        
        if path is None:
            path = []
        elif isinstance(path, str):
            path = [p.strip() for p in path.split(',') if p.strip()]

        path = path + [cur]
            
        if len(self.nodes[cur].successors) == 0:
            self.probable_paths.append(path)
            return
        
        for c in self.nodes[cur].successors:
            if c in self.nodes:
                self.find_probable_paths(c, path)
    
    def find_critical_path(self, cur: Optional[str] = None) -> List[str]:
        """
        Function to find Critical Path

        Args:
            cur (str, optional): Current activity. Defaults to None.

        Returns:
            List[str]: The critical path as a list of activity names
        """
        if not self.probable_paths:
            self.find_probable_paths()
            
        self.critical_path = []
        self.total_project_duration = -1
        
        for probable_path in self.probable_paths:
            path_duration: float = sum(self.nodes[cur_node].duration for cur_node in probable_path)
            if path_duration > self.total_project_duration:
                self.critical_path = probable_path
                self.total_project_duration = path_duration
            elif path_duration == self.total_project_duration:
                if isinstance(self.critical_path, list) and not isinstance(self.critical_path[0] if self.critical_path else None, str):
                    # Handle case where critical_path might be a list of paths
                    pass
                    
        return self.critical_path

    def forward_pass(self) -> None:
        """
        Function to calculate Early Start (ES) and Early Finish (EF) for each node
        """
        for node in self.nodes.values():
            node.early_start = 0.0
            node.early_finish = node.duration
            
        changed: bool = True
        while changed:
            changed = False
            for node in self.nodes.values():
                if node.predecessors:
                    max_ef: float = max((self.nodes[p].early_finish for p in node.predecessors if p in self.nodes), default=0.0)
                    if max_ef > node.early_start:
                        node.early_start = max_ef
                        node.early_finish = node.early_start + node.duration
                        changed = True

    def backward_pass(self) -> None:
        """
        Function to calculate Late Start (LS) and Late Finish (LF) for each node
        """
        if self.total_project_duration == -1:
            self.total_project_duration = max((n.early_finish for n in self.nodes.values()), default=0.0)
            
        for node in self.nodes.values():
            node.latest_finish = self.total_project_duration
            node.latest_start = node.latest_finish - node.duration
            
        changed: bool = True
        while changed:
            changed = False
            for node in self.nodes.values():
                if node.successors:
                    min_ls: float = min((self.nodes[s].latest_start for s in node.successors if s in self.nodes), default=node.latest_finish)
                    if min_ls < node.latest_finish:
                        node.latest_finish = min_ls
                        node.latest_start = node.latest_finish - node.duration
                        changed = True
                
    def get_edges(self) -> List[Tuple[str, str, Dict[str, float]]]:
        """
        Function to convert activity and successors in form of edges for visualization

        Returns:
            List[Tuple[str, str, Dict[str, float]]]: List of edges with duration attributes
        """
        self.edges = []
        for node in self.nodes:
            if self.nodes[node].successors:
                for suc in self.nodes[node].successors:
                    self.edges.append((self.nodes[node].name, suc, {'duration': self.nodes[node].duration}))
            else:
                self.edges.append((self.nodes[node].name, 'T', {'duration': self.nodes[node].duration}))
        return self.edges
    
    def get_hierarchical_layout(self, graph: nx.Graph, start_node: str) -> Dict[str, Tuple[float, float]]:
        """
        Calculates node positions for a hierarchical layout.

        Args:
            graph (nx.Graph): The graph to lay out.
            start_node (str): The node to start the layout from (usually the root).

        Returns:
            Dict[str, Tuple[float, float]]: A dictionary of node positions {node: (x, y)}.
        """
        return _get_hierarchical_layout(graph, start_node)
    
    def display_network(self) -> None:
        """
        Function to Visualize the Network Diagram.
        Uses Networkx and Matplotlib for plotting.
        """
        _display_network(self)

    def network_summary(self) -> None:
        """
        Function to generate entire Network Summary including number of nodes, Activities, 
        Probable paths, Critical Path, Total Project Duration and Edges
        """
        print("\n\n---------------Network Summary-----------------\n\n")
        print("Total number of Activities/Nodes : ", len(self.nodes))
        print("Nodes : ", end="")
        for c in self.nodes:
            print(c, " ", end="")
            
        print("\nAll Probable Paths : ")
        for p in self.probable_paths:
            print(p)
        print("Critical Path : ", self.critical_path)
        print("Total project duration : ", self.total_project_duration)
        print("Duration unit :", self.duration_unit)
        
        self.get_edges()
        print("Edges : ", self.edges)
        
        print("\nNode Properties:")
        print(f"{'Node':<5} | {'ES':<3} | {'EF':<3} | {'LS':<3} | {'LF':<3}")
        print("-" * 35)
        for name, node in self.nodes.items():
            print(f"{name:<5} | {node.early_start:<3} | {node.early_finish:<3} | {node.latest_start:<3} | {node.latest_finish:<3}")


# Example usage
if __name__ == "__main__":
    # Create a sample network
    cpm = CriticalPathMethod()
    
    # Add origin node
    cpm.add_activity('O', 0)
    
    # Add activities with relations
    activities = ['A', 'B', 'C', 'D', 'E']
    durations = [3, 4, 2, 5, 2]
    predecessors = ['-', 'A', 'A', 'B,C', 'C']
    
    cpm.add_activities_relations(activities, durations, predecessors)
    
    # Calculate paths
    cpm.find_probable_paths()
    cpm.find_critical_path()
    cpm.forward_pass()
    cpm.backward_pass()
    
    # Display results
    cpm.network_summary()
    cpm.display_network()
