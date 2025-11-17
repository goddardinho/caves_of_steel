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
        self.trees["Julius Enderby"] = self._create_commissioner_dialogue()
        self.trees["R. Daneel Olivaw"] = self._create_daneel_dialogue()
        self.trees["Records Clerk"] = self._create_clerk_dialogue()

        # Jessie Bailey - family dialogue (original content inspired by family concerns)
        jessie = DialogueTree("Jessie Bailey")
        j_start = DialogueNode(
            "Jessie Bailey",
            """Jessie looks anxious but relieved to see you. 'We're all worried,' she says.""",
        )
        j_start.add_choice(DialogueChoice("Ask how she's holding up.", relationship_impact=5))
        j_start.add_choice(DialogueChoice("Ask about family routines.", relationship_impact=3))
        j_start.add_choice(DialogueChoice("Offer reassurance.", relationship_impact=10))
        jessie.add_node("start", j_start)
        self.trees["Jessie Bailey"] = jessie

        # Ben Bailey - short, age-appropriate dialogue
        ben = DialogueTree("Ben Bailey")
        b_start = DialogueNode(
            "Ben Bailey",
            """Ben looks up, clutching a small model rocket. 'Hi,' he says, watching you closely.""",
        )
        b_start.add_choice(DialogueChoice("Ask about the rocket.", relationship_impact=8))
        b_start.add_choice(DialogueChoice("Ask how he's feeling.", relationship_impact=5))
        b_start.add_choice(DialogueChoice("Offer to play a quick game.", relationship_impact=10))
        ben.add_node("start", b_start)
        self.trees["Ben Bailey"] = ben

        # Vince Barrett - colleague who lost position to robot
        vince = DialogueTree("Vince Barrett")
        v_start = DialogueNode(
            "Vince Barrett",
            """Vince looks frustrated. 'Another robot case,' he mutters. 'My old job, now a machine does it.'""",
        )
        v_start.add_choice(DialogueChoice("Sympathize with him.", relationship_impact=10))
        v_start.add_choice(DialogueChoice("Ask about his experience.", relationship_impact=5))
        v_start.add_choice(DialogueChoice("Move on.", relationship_impact=0))
        vince.add_node("start", v_start)
        self.trees["Vince Barrett"] = vince

        # R. Sammy - robot colleague
        sammy = DialogueTree("R. Sammy")
        s_start = DialogueNode(
            "R. Sammy",
            """R. Sammy's optical sensors blink in sequence. 'Detective. I have processed the available case data.'""",
        )
        s_start.add_choice(DialogueChoice("Request the analysis.", relationship_impact=5))
        s_start.add_choice(DialogueChoice("Ask about integration with humans.", relationship_impact=8))
        s_start.add_choice(DialogueChoice("Ignore the robot.", relationship_impact=-5))
        sammy.add_node("start", s_start)
        self.trees["R. Sammy"] = sammy

        # Han Fastolfe - Spacer roboticist diplomat
        han = DialogueTree("Han Fastolfe")
        h_start = DialogueNode(
            "Han Fastolfe",
            """Han greets you with understated courtesy, but his expression carries urgency.

'Detective. I was acquainted with Dr. Sarton's research. He was more than
a scientist — he was a bridge between our worlds. His death troubles us deeply.
But perhaps it will serve a greater purpose if it teaches your people the value
of cooperation with robots.'

His eyes study you intently, as if assessing your potential.""",
        )
        h_start.add_choice(DialogueChoice("Ask about Sarton's true work.", relationship_impact=10))
        h_start.add_choice(DialogueChoice("Inquire about Spacer interests on Earth.", relationship_impact=8))
        h_start.add_choice(DialogueChoice("Ask directly if he has information.", relationship_impact=5))
        han.add_node("start", h_start)
        self.trees["Han Fastolfe"] = han

        # Dr. Anthony Gerrigel - roboticist researcher
        gerrigel = DialogueTree("Dr. Anthony Gerrigel")
        g_start = DialogueNode(
            "Dr. Anthony Gerrigel",
            """Dr. Gerrigel looks up from his work. 'I heard about Roj. A tragic loss for our field.'""",
        )
        g_start.add_choice(DialogueChoice("Ask about his relationship with Sarton.", relationship_impact=8))
        g_start.add_choice(DialogueChoice("Request technical details on robotics.", relationship_impact=10))
        g_start.add_choice(DialogueChoice("Ask if anyone wanted Sarton dead.", relationship_impact=5))
        gerrigel.add_node("start", g_start)
        self.trees["Dr. Anthony Gerrigel"] = gerrigel

        # Francis Clousarr - anti-robot activist suspect
        clousarr = DialogueTree("Francis Clousarr")
        c_start = DialogueNode(
            "Francis Clousarr",
            """Francis eyes you coldly from behind the detention glass. 'Come to interrogate me, Detective?'""",
        )
        c_start.add_choice(DialogueChoice("Ask directly about Sarton.", relationship_impact=0))
        c_start.add_choice(DialogueChoice("Inquire about his whereabouts.", relationship_impact=5))
        c_start.add_choice(DialogueChoice("Question his anti-robot activities.", relationship_impact=-10))
        clousarr.add_node("start", c_start)
        self.trees["Francis Clousarr"] = clousarr

        # Commander Lije Bailey - superior officer
        commander = DialogueTree("Commander Lije Bailey")
        cmd_start = DialogueNode(
            "Commander Lije Bailey",
            """The Commander nods curtly. 'You're back. Any progress on the Sarton case?'""",
        )
        cmd_start.add_choice(DialogueChoice("Report what you've found.", relationship_impact=8))
        cmd_start.add_choice(DialogueChoice("Ask for guidance.", relationship_impact=10))
        cmd_start.add_choice(DialogueChoice("Say you're still investigating.", relationship_impact=5))
        commander.add_node("start", cmd_start)
        self.trees["Commander Lije Bailey"] = commander

    def _create_commissioner_dialogue(self):
        """Create Julius Enderby (Commissioner) dialogue tree.

        Returns:
            DialogueTree
        """
        tree = DialogueTree("Julius Enderby")

        start_node = DialogueNode(
            "Julius Enderby",
            """The Commissioner looks at you seriously. There's a slight nervousness in his manner.

"We have a serious matter. Dr. Roj Nemennuh Sarton was found dead in his apartment.
You're assigned to investigate. However, I'm also assigning you a robot
partner. His name is R. Daneel Olivaw. I know you won't like it, but
this is non-negotiable."

He adjusts his eyeglasses with a slight tremor in his hand. Something seems off.

What do you want to say?""",
        )

        start_node.add_choice(
            DialogueChoice("I don't work with robots.", relationship_impact=-20)
        )
        start_node.add_choice(
            DialogueChoice("Why was a robot chosen for this?", relationship_impact=10)
        )
        start_node.add_choice(
            DialogueChoice(
                "I accept. When can I meet my partner?", relationship_impact=20
            )
        )

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

What do you say?""",
        )

        start_node.add_choice(
            DialogueChoice("I don't trust robots.", relationship_impact=-15)
        )
        start_node.add_choice(
            DialogueChoice("Tell me about the Three Laws.", relationship_impact=5)
        )
        start_node.add_choice(
            DialogueChoice(
                "Yes, let's begin the investigation.", relationship_impact=25
            )
        )

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

"Detective. I heard about Dr. Roj Nemennuh Sarton. Tragic. He was here often,
researching... well, things. Can I help you find something specific?"

What do you need?""",
        )

        start_node.add_choice(
            DialogueChoice("Information on the suspects.", relationship_impact=10)
        )
        start_node.add_choice(
            DialogueChoice("Records on Dr. Sarton's research.", relationship_impact=15)
        )
        start_node.add_choice(
            DialogueChoice("Where were you this afternoon?", relationship_impact=-5)
        )

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
