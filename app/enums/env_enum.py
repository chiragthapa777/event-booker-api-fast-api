from enum import Enum


class Env(str, Enum):
    LOCAL="local"
    DEV="dev"
    STAGE="stage"
    PROD="prod"