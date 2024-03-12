class SoftDeleteError(Exception):
    """Exception raised for errors related to soft deletion."""

    def __init__(self, message="Object is already soft deleted."):
        self.message = message
        super().__init__(self.message)
