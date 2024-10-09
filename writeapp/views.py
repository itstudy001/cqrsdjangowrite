from rest_framework.response import Response
from rest_framework.decorators import api_view

from kafka import KafkaProducer
import json

#메시지를 전송하는 카프카 프로듀서 클래스
class MessageProducer:
    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic

        self.producer = KafkaProducer(
            bootstrap_servers = self.broker,
            value_serializer = lambda x : json.dumps(x).encode("utf-8"),
            acks=0,
            api_version=(2, 5, 0),
            key_serializer=str.encode,
            retries=3,
        )

    def send_message(self, msg, auto_close=True):
        try:
            future = self.producer.send(self.topic, value=msg,
                                        key="key")
            self.producer.flush()
            future.get(timeout=2)
            return {"status_code":200, "error":None}
        except Exception as exc:
            raise exc


@api_view(['GET'])
def helloAPI(request):
    return Response("hello world")


from .models import Book
from .serializers import BookSerializer
from rest_framework import status

@api_view(['POST'])
def bookAPI(request):
    #전송된 데이터 읽기
    data = request.data

    #숫자로 변환
    data['pages'] = int(data['pages'])
    data['price'] = int(data['price'])

    #Model 형태로 변환
    serializer = BookSerializer(data=data)
    if serializer.is_valid():
        serializer.save() #테이블에 저장
        #성공한 경우
        return Response(serializer.data, 
                        status=status.HTTP_201_CREATED)
    #실패한 경우
    return Response(serializer.errors, 
                    status = status.HTTP_400_BAD_REQUEST)