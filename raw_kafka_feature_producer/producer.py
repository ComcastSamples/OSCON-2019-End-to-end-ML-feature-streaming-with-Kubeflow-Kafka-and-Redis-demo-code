from kafka import KafkaProducer
import numpy as np
from sklearn import datasets
from time import sleep

# start our producer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'])

# fetch and load the housing data set
d = datasets.fetch_california_housing()

# loop forever and publish 5 msgs per sec
while True:
    # get a random row
    random_row = d.data[np.random.randint(len(d.data))]

    # for demo purposes, divide each geographical unit by 5 (to aggregate later)
    divided_features = np.concatenate((random_row[0:6] / 5, np.array([random_row[6], random_row[7]])), axis=0)
    short_feature_names = d.feature_names
    features_and_names = np.array([short_feature_names, divided_features])

    # publish divided features
    for i in range(0, 5):
        future = producer.send('housing-topic', features_and_names.tobytes())
    print('produced 5 messages')
    sleep(0.5)
