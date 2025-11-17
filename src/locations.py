"""
Locations - Game world locations and map
"""


class Location:
    """Represents a location in the game world."""

    def __init__(self, name, description, exits=None, npcs=None, items=None):
        """Initialize a location.

        Args:
            name: Location name
            description: Location description
            exits: Dict of exit names to location keys
            npcs: List of NPC names at this location
            items: List of items at this location
        """
        self.name = name
        self.description = description
        self.exits = exits or {}
        self.npcs = npcs or []
        self.items = items or []


# Define all locations in the game
LOCATIONS = {
    "bedroom": Location(
        name="Your Personal Quarters",
        description="""
        Your small but comfortable apartment in the residential sector.
        Gray walls glow softly with bioluminescent panels. A narrow bed,
        a small desk, and a door leading to the corridor are your
        surroundings. The hum of the city's life support systems is
        a constant background presence.
        """,
        exits={"corridor": "corridor_residential"},
        npcs=["R. Daneel Olivaw", "Jessie Bailey", "Ben Bailey"],
        items=["notebook", "communication_device"],
    ),
    "corridor_residential": Location(
        name="Residential Corridor",
        description="""
        A long, narrow corridor with identical apartment doors lining
        both sides. The walls are pale and featureless. Citizens pass
        by occasionally. The corridor extends in both directions, and
        you notice signs pointing toward the central plaza and the
        administrative sector.
        """,
        exits={
            "quarters": "bedroom",
            "plaza": "central_plaza",
            "administrative": "administrative_section",
        },
        npcs=["Neighbor"],
        items=[],
    ),
    "central_plaza": Location(
        name="Central Plaza",
        description="""
        The heart of the underground city. A vast cavern carved from
        solid rock with artificial lighting creating a perpetual day.
        Citizens of all types move purposefully through the plaza. Food
        dispensaries line the walls, and information displays show the
        city's vital statistics. The air is recycled and cool.
        """,
        exits={
            "residential": "corridor_residential",
            "administrative": "administrative_section",
            "police": "police_headquarters",
            "food_dispensary": "food_dispensary",
        },
        npcs=["City Official", "Street Vendor"],
        items=[],
    ),
    "police_headquarters": Location(
        name="Police Headquarters",
        description="""
        The imposing police headquarters stands against the cavern wall.
        Armed officers are stationed at the entrance. Inside, you find
        organized cubicles and a central briefing area. The scent of
        ozone and determination fills the air. This is where justice
        in the Caves of Steel is dispensed.
        """,
        exits={"plaza": "central_plaza", "commissioner_office": "commissioner_office", "robot_division": "robot_division", "detention": "detention_block"},
        npcs=["Commander Lije Bailey", "Desk Officer", "Vince Barrett"],
        items=["case_files"],
    ),
    "commissioner_office": Location(
        name="Commissioner's Office",
        description="""
        A stark, austere office with minimal furnishings. A large desk
        dominates the room, and pictures of past commissioners adorn
        the walls. A robot stands silently in the corner - R. Daneel
        Olivaw, your new partner. On the desk, you notice a pair of
        eyeglasses in a repair case — they appear to have broken lenses.
        """,
        exits={"headquarters": "police_headquarters"},
        npcs=["Julius Enderby", "R. Daneel Olivaw"],
        items=["eyeglass_evidence", "case_files"],
    ),
    "administrative_section": Location(
        name="Administrative Section",
        description="""
        Sleek and modern, this sector houses the bureaucratic machinery
        of the city. Officials move between offices with purpose. Records
        are stored in computer banks that line the walls. The smell of
        recycled air is stronger here, along with the faint sound of
        electronic humming.
        """,
        exits={"plaza": "central_plaza", "records": "records_office", "lab": "robotics_lab"},
        npcs=["Administrator"],
        items=[],
    ),
    "records_office": Location(
        name="Records Office",
        description="""
        Endless shelves of data storage devices and documents fill this
        vast room. A tired-looking clerk sits behind a counter. The
        records office keeps files on every citizen in the Caves of Steel.
        Finding the information you need may require persistence.
        """,
        exits={"admin": "administrative_section"},
        npcs=["Records Clerk"],
        items=["citizen_records"],
    ),
    "food_dispensary": Location(
        name="Food Dispensary",
        description="""
        Citizens queue patiently before mechanical dispensers that
        produce standardized nutrition packs. The food here is bland
        but efficient - just like life in the caves. You watch as
        people mechanically consume their rations and move on.
        """,
        exits={"plaza": "central_plaza"},
        npcs=["Dispensary Attendant"],
        items=["nutrition_pack"],
    ),
    "crime_scene": Location(
        name="Murder Crime Scene",
        description="""
        You stand in an apartment that has become a crime scene. The
        body has been removed, but evidence remains. Forensic markers
        indicate where the victim fell. A window port shows the outside
        world - the Outer Regions, where robots and humans rarely mix.
        The detective in you begins to sense this is no ordinary murder.
        """,
        exits={"residential": "corridor_residential"},
        npcs=["Scene Officer"],
        items=["forensic_evidence", "personal_effects"],
    ),
    "robot_division": Location(
        name="Robot Division",
        description="""
        A specialized wing of the police headquarters dedicated to
        robot operations and integration. Advanced terminals and
        diagnostic equipment line the walls. R. Sammy, a robot,
        works here processing data and assisting with investigations.
        """,
        exits={"headquarters": "police_headquarters"},
        npcs=["R. Sammy"],
        items=[],
    ),
    "spacer_embassy": Location(
        name="Spacer Embassy",
        description="""
        An elegant facility representing the interests of Earth's
        spacer colonies and allies. The air here feels different—cleaner,
        more controlled. Advanced technology lines the walls. Han Fastolfe,
        a roboticist from Aurora, conducts diplomatic and scientific work here.
        """,
        exits={"plaza": "central_plaza"},
        npcs=["Han Fastolfe"],
        items=[],
    ),
    "robotics_lab": Location(
        name="Robotics Research Laboratory",
        description="""
        A state-of-the-art laboratory filled with equipment for
        studying and constructing robots. Dr. Anthony Gerrigel works
        here, conducting cutting-edge research into humaniform robotics
        and artificial intelligence. The hum of machinery is constant.
        """,
        exits={"admin": "administrative_section"},
        npcs=["Dr. Anthony Gerrigel"],
        items=[],
    ),
    "detention_block": Location(
        name="Detention Block",
        description="""
        A secure area where suspects and prisoners are held pending
        trial. Security is tight; automated systems monitor all activity.
        Francis Clousarr, a man with a history of anti-robot activism,
        is held here pending questioning about recent incidents.
        """,
        exits={"headquarters": "police_headquarters"},
        npcs=["Francis Clousarr"],
        items=[],
    ),
}
