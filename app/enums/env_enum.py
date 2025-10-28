from enum import Enum


class Env(str, Enum):
    LOCAL="local"
    DEV="DEV"
    STAGE="STAGE"
    PROD="PROD"