"""
Dialogue Choice System - Interactive dialogue trees with consequences
"""


class DialogueChoice:
    """Represents a dialogue choice in a conversation."""
    
    def __init__(self, text, consequence=None, relationship_impact=0):
        """Initialize a dialogue choice.
        
        Args:
            text: The text of the choice
            consequence: Function or text describing what happens
            relationship_impact: How this affects relationship (-100 to 100)
        """
        self.text = text
        self.consequence = consequence
        self.relationship_impact = relationship_impact


class DialogueNode:
    """Represents a node in a dialogue tree."""
    
    def __init__(self, npc_name, text, choices=None):
        """Initialize a dialogue node.
        
        Args:
            npc_name: Name of the NPC speaking
            text: What the NPC says
            choices: List of DialogueChoice objects
        """
        self.npc_name = npc_name
        self.text = text
        self.choices = choices or []
    
    def add_choice(self, choice):
        """Add a choice to this dialogue node.
        
        Args:
            choice: DialogueChoice object
        """
        self.choices.append(choice)


class DialogueTree:
    """Represents a complete dialogue tree with a character."""
    
    def __init__(self, npc_name):
        """Initialize dialogue tree.
        
        Args:
            npc_name: Name of the NPC
        """
        self.npc_name = npc_name
        self.nodes = {}
        self.current_node = None
    
    def add_node(self, node_id, node):
        """Add a node to the tree.
        
        Args:
            node_id: Unique node ID
            node: DialogueNode object
        """
        self.nodes[node_id] = node
    
    def get_node(self, node_id):
        """Get a dialogue node.
        
        Args:
            node_id: Node ID
            
        Returns:
            DialogueNode or None
        """
        return self.nodes.get(node_id)
    
    def start_dialogue(self, start_node_id="start"):
        """Start dialogue at a specific node.
        
        Args:
            start_node_id: Node to start from
            
        Returns:
            DialogueNode or None
        """
        self.current_node = start_node_id
        return self.get_node(start_node_id)


class DialogueManager:
    """Manages all NPC dialogue trees."""
    
    def __init__(self):
        """Initialize dialogue manager."""
        self.trees = {}
        self._create_dialogue_trees()
    
    def _create_dialogue_trees(self):
        """Create dialogue trees for all NPCs."""
        self.trees["Commissioner"] = self._create_commissioner_dialogue()
        self.trees["R. Daneel Olivaw"] = self._create_daneel_dialogue()
        self.trees["Records Clerk"] = self._create_clerk_dialogue()
    
    def _create_commissioner_dialogue(self):
        """Create Commissioner dialogue tree.
        
        Returns:
            DialogueTree
        """
        tree = DialogueTree("Commissioner")
        
        start_node = DialogueNode(
            "Commissioner",
            """The Commissioner looks at you seriously.

"We have a serious matter. Dr. Rimbauer was found dead in his apartment.
You're assigned to investigate. However, I'm also assigning you a robot
partner. His name is R. Daneel Olivaw. I know you won't like it, but
this is non-negotiable."

What do you want to say?"""
        )
        
        start_node.add_choice(DialogueChoice(
            "I don't work with robots.",
            relationship_impact=-20
        ))
        start_node.add_choice(DialogueChoice(
            "Why was a robot chosen for this?",
            relationship_impact=10
        ))
        start_node.add_choice(DialogueChoice(
            "I accept. When can I meet my partner?",
            relationship_impact=20
        ))
        
        tree.add_node("start", start_node)
        return tree
    
    def _create_daneel_dialogue(self):
        """Create R. Daneel dialogue tree.
        
        Returns:
            DialogueTree
        """
        tree = DialogueTree("R. Daneel Olivaw")
        
        start_node = DialogueNode(
            "R. Daneel Olivaw",
            """R. Daneel Olivaw extends his hand in greeting. His movements
are smooth and mechanical, yet somehow graceful.

"Good morning, Detective. I am R. Daneel Olivaw. I understand you may have
reservations about working with a humanoid robot, but I assure you that I am
bound by the Three Laws of Robotics. I cannot harm humans, and I must follow
human orders as long as they don't conflict with the First Law.

Are you ready to investigate together?"

What do you say?"""
        )
        
        start_node.add_choice(DialogueChoice(
            "I don't trust robots.",
            relationship_impact=-15
        ))
        start_node.add_choice(DialogueChoice(
            "Tell me about the Three Laws.",
            relationship_impact=5
        ))
        start_node.add_choice(DialogueChoice(
            "Yes, let's begin the investigation.",
            relationship_impact=25
        ))
        
        tree.add_node("start", start_node)
        return tree
    
    def _create_clerk_dialogue(self):
        """Create Records Clerk dialogue tree.
        
        Returns:
            DialogueTree
        """
        tree = DialogueTree("Records Clerk")
        
        start_node = DialogueNode(
            "Records Clerk",
            """The Records Clerk looks tired, surrounded by data terminals
and filing systems.

"Detective. I heard about Dr. Rimbauer. Tragic. He was here often,
researching... well, things. Can I help you find something specific?"

What do you need?"""
        )
        
        start_node.add_choice(DialogueChoice(
            "Information on the suspects.",
            relationship_impact=10
        ))
        start_node.add_choice(DialogueChoice(
            "Records on Dr. Rimbauer's research.",
            relationship_impact=15
        ))
        start_node.add_choice(DialogueChoice(
            "Where were you this afternoon?",
            relationship_impact=-5
        ))
        
        tree.add_node("start", start_node)
        return tree
    
    def get_dialogue_tree(self, npc_name):
        """Get dialogue tree for an NPC.
        
        Args:
            npc_name: NPC name
            
        Returns:
            DialogueTree or None
        """
        return self.trees.get(npc_name)
    
    def get_available_dialogues(self):
        """Get list of NPCs with dialogue trees.
        
        Returns:
            list: NPC names with dialogue options
        """
        return list(self.trees.keys())
