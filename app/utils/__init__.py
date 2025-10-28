import uuid

def is_valid_uuid(uuid_string):
    """
    Checks if a string is a valid UUID v4.

    Args:
        uuid_string (str): The string to validate.

    Returns:
        bool: True if the string is a valid UUID v4, False otherwise.
    """
    try:
        # Attempt to create a UUID object from the string
        uuid_obj = uuid.UUID(uuid_string, version=4)
    except ValueError:
        # If a ValueError is raised, the string is not a valid UUID
        return False

    # Ensure the string representation of the created UUID object matches the original string
    # This handles cases where the UUID constructor might normalize the input (e.g., case)
    return str(uuid_obj) == uuid_string