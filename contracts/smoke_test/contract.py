from pyteal import *
from helpers import program
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).absolute().parent.parent))

UINT64_MAX = 0xFFFFFFFFFFFFFFFF


def approval():
    return Approve()


def clear():
    return Approve()