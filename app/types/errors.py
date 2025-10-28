class AppError(Exception):
    """Service level handled errors"""
    def __init__(self, message="Error Occurred"):
        self.message = message
        super().__init__(self.message)