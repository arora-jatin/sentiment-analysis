from kafka import KafkaProducer
from random import randint
import json

# Object to handle json data
class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__)

# producer setup
producer = KafkaProducer(bootstrap_servers='localhost:9092')
topic = "spark"

# read sample data
msgs = open("positives.txt", "r").readlines()
qstnIds = open("questionIds.json", "r").readlines()
respondentIds = open("respondentIds.txt", "r").readlines()
qstnTxts = open("questionTxts.txt", "r").readlines()

response = Object()
# survey ID
response.id = "0000ed4f-8be6-4753-83ee-4d708a1f74a8"

# send data in queue
for i in range(2000):
    response.response = msgs[randint(0,len(msgs)-1)].strip()
    response.qstnId = qstnIds[randint(0,len(qstnIds)-1)].strip()
    response.respondentId = respondentIds[randint(0,len(respondentIds)-1)].strip()
    response.qstnTxt = qstnTxts[randint(0,len(qstnTxts)-1)].strip()
    producer.send(topic, response.toJSON())
producer.flush()    
