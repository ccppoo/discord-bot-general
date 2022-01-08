from dataclasses import dataclass

@dataclass(frozen=True)
class __response_types:
    PONG: int =  1
    ACK_NO_SOURCE : int =  2 
    MESSAGE_NO_SOURCE: int = 3 
    MESSAGE_WITH_SOURCE: int =  4 
    ACK_WITH_SOURCE: int =  5

RESPONSE_TYPES = __response_types()

PING_PONG = {
    "type": 1
}

def ping_pong(body):
    if body.get("type") == RESPONSE_TYPES.PONG:
        return True
    return False