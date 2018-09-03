import eikon as ek

from eikon_manager import EikonManager
from config import EIKON_KEY


def build_eikon_manager():
    return EikonManager(EIKON_KEY, ek)