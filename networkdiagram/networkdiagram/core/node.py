from typing import List


class Node:
    """Represents an activity node in the network diagram."""
    
    def __init__(self, name: str, duration: float = 0) -> None:
        """
        Constructor for declaring a new Node or Activity

        Args:
            name (str): Name of the activity usually single character
            duration (float, optional): Duration of the activity. Defaults to 0.
        """
        self.name: str = name
        self.duration: float = duration
        self.predecessors: List[str] = []
        self.successors: List[str] = []  # Tells which activities can start once the current activity is finished
        self.early_start: float = 0
        self.early_finish: float = 0
        self.latest_start: float = 0
        self.latest_finish: float = 0
        
    def add_successor(self, node: 'Node') -> None:
        """
        Used to add a successor of a specific activity

        Args:
            node (Node): Object of Node
        """
        self.successors.append(node.name)
        node.predecessors.append(self.name)
        
    def node_summary(self) -> str:
        """
        Generates Summary report of an Activity

        Returns:
            str: contains information like name, duration and successors.
        """
        return f"Name : {self.name}, Duration : {self.duration}, Successor : {self.successors}"
        
    def __repr__(self) -> str:
        """String representation of the node."""
        return f"Node(name='{self.name}', duration={self.duration})"
