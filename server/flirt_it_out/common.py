from collections import namedtuple
import configparser

config = configparser.ConfigParser()

Message = namedtuple("Message", "id sender content")

def find(predicate, lst):
    return next(x for x in lst if predicate(x))

class Packet:
    pass

class PacketAgent:
    pass