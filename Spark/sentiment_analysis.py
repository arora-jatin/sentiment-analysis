from __future__ import print_function
import sys

from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from textblob import TextBlob
from kafka import SimpleProducer, KafkaClient
import json
import pickle
from couchbase.cluster import Cluster
from couchbase.cluster import PasswordAuthenticator


cluster = Cluster('couchbase://10.193.8.23')
authenticator = PasswordAuthenticator('Administrator', 'password')
cluster.authenticate(authenticator)
bucket = cluster.open_bucket('Data')
def handler(message):
    kafka = KafkaClient("localhost:9092")
    producer = SimpleProducer(kafka)
    records = message.collect()
    #train = [("Satisfied", 'pos'),
    #("not happy",'neg'),
    #("happy",'pos')]
    #cl = NaiveBayesClassifier(train)
    for record in records:
        inputJson = json.loads(record[1])
        response = inputJson['response']
        questionId = inputJson['qstnId']
        qstnTxt = inputJson['qstnTxt']
        surveyId = inputJson['id']
        analysis = TextBlob(response)
        if analysis.sentiment.polarity > 0:
            result = 'positive'
        elif analysis.sentiment.polarity == 0:
            result = 'neutral'
        else:
            result = 'negative'
        prevStates = []

        try:
            rv = bucket.get(surveyId)
            existingId = 0
            prevStates = rv.value['questions']
            for prevState in prevStates:
                if prevState['id'] == questionId:
                    existingId = 1
                    prevState['total'] = prevState['total']+1
                    prevState['qstnTxt'] = qstnTxt
                    if result == 'positive':
                        prevState['positive'] = prevState['positive']+1
                    elif result == 'negative':
                        prevState['negative'] = prevState['negative']+1
                    else:
                        prevState['neutral'] = prevState['neutral']+1
                    producer.send_messages('spark.out', str(prevState))
                    break;
            #newStates.add
            if existingId == 0:
                newId = dict()
                newId['id'] = questionId
                newId['total'] = 1
                newId['qstnTxt'] = qstnTxt
                if result == 'positive':
                    newId['positive'] = 1
                    newId['negative'] = 0
                    newId['neutral'] = 0
                elif result == 'negative':
                    newId['positive'] = 0
                    newId['negative'] = 1
                    newId['neutral'] = 0
                else:
                    newId['positive'] = 0
                    newId['negative'] = 0
                    newId['neutral'] = 1
                prevStates.append(newId)
                producer.send_messages('spark.out', str(newId))
            bucket.upsert(surveyId, {'questions': prevStates})
        except:
            newId = dict()
            newId['id'] = questionId
            newId['total'] = 1
            newId['qstnTxt'] = qstnTxt
            if result == 'positive':
                newId['positive'] = 1
                newId['negative'] = 0
                newId['neutral'] = 0
            elif result == 'negative':
                newId['positive'] = 0
                newId['negative'] = 1
                newId['neutral'] = 0
            else:
                newId['positive'] = 0
                newId['negative'] = 0
                newId['neutral'] = 1
            prevStates.append(newId)
            producer.send_messages('spark.out', str(newId))
            bucket.upsert(surveyId, {'questions': prevStates})


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: kafka_wordcount.py <zk> <topic>", file=sys.stderr)
        exit(-1)
    sc = SparkContext(appName="PythonStreamingKafkaSentimentAnalysisgoo")
    ssc = StreamingContext(sc, 1)

    zkQuorum, topic = sys.argv[1:]
    kvs = KafkaUtils.createStream(ssc, zkQuorum, "spark-streaming-consumer", {topic: 1})
    kvs.foreachRDD(handler)
    ssc.start()
    ssc.awaitTermination()
