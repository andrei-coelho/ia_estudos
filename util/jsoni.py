import json
from decimal import Decimal

class fakefloat(float):
    def __init__(self, value):
        self._value = value
    def __repr__(self):
        return str(self._value)

def defaultencode(o):
    if isinstance(o, Decimal):
        return fakefloat(o)
    raise TypeError(repr(o) + " is not JSON serializable")


def encode(data):
    return json.dumps(data, ensure_ascii=False, default=defaultencode).encode('utf8').decode()
    
def decode(string):
    return json.loads(string, parse_float=Decimal)