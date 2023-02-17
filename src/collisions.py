class Collisions(object):
    """
    A dataclass to hold any collision lists.
    """

    def __init__(self):
        """
        Set up the various lists
        """

        self.source_image_collision_identical = list()
        self.source_image_collision_different = list()
        self.destination_image_exists_identical = list()
        self.destination_image_exists_different = list()
        self.source_sidecar_collision_identical = list()
        self.source_sidecar_collision_different = list()
        self.destination_sidecar_exists_identical = list()
        self.destination_sidecar_exists_different = list()
