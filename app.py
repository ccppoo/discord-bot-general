import json
import os
from .validator import verify_signature
from .utils import PING_PONG, RESPONSE_TYPES
from .utils import ping_pong

print("Name is ({})".format(__name__))

# running in Python version 3.8

# docker, github action에서 사용되는 {{ secrets. }} 이것도 aws_lambda.yml에서 환경변수와 함께 배포되고
# 이건 이 이미지가 실행될 환경(AWS Lambda가 이미지를 가져와서 실행되는 AWS 클라우드 속 환경)의 변수로 쓰일 땐
# os.getenv를 통해서 접근할 수 있다.
# 정리 :: Docker의 env는 실행되는 환경과 일치하며, 이를 접근할 땐 os.getenv 를 통해서 접근할 수 있다.
PUBLIC_KEY =  os.getenv('DISCORD_PUBLIC_KEY')
    
def lambda_handler(event, context):

    # verify the signature
    try:
        verify_signature(event, PUBLIC_KEY)
    except Exception as e:
        raise Exception(f"[UNAUTHORIZED] Invalid request signature: {e}")

    # check if message is a ping
    body = event.get('body-json')
    
    if ping_pong(body):
        return PING_PONG

    # return dummy
    return {
        "type": RESPONSE_TYPES.MESSAGE_WITH_SOURCE,
        "data": {
            "tts": False,
            "content": "BEEP BOOP",
            "embeds": [],
            "allowed_mentions": []
        }
    }