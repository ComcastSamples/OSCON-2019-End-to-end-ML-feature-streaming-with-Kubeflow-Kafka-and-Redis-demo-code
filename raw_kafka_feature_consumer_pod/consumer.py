from kafka import KafkaConsumer
import numpy as np
import redis
import json
import time as tm
import sys

# single local redis (not cluster)
redis_client = redis.Redis(host='host.docker.internal', port=6379)

# create kafka consumer for latest messages
kafka_consumer = KafkaConsumer('housing-topic',
                         group_id='test-group',
                         bootstrap_servers = ['host.docker.internal:9092'])

# perform the redis set and get to aggregate the features
def aggregate_features(features):
    # start = tm.time()
    # get the cached features for lat/lon
    key = features[6] + ":" + features[7]
    cached_features_json = redis_client.get(key)

    current_features = features[0:6]
    current_features.append(1)  # add a counter
    cached_features = current_features
    if cached_features_json is not None:
        cached_feature_list = json.loads(cached_features_json.decode())
        cached_features = \
            (np.array(cached_feature_list, dtype=np.dtype(float)) +
             np.array(current_features, dtype=np.dtype(float))).tolist()

    redis_client.set(key, json.dumps(cached_features))
    # end = tm.time()
    # print(end - start)
    return cached_features


# number of features with key (lat/lon)
total_features = 8
# number of raw features minus key
raw_features = total_features - 2

# consume messages from kafka
print('starting raw kafka feature consumer', file=sys.stdout)
for message in kafka_consumer:
    features_and_names = np.frombuffer(message.value, dtype=np.dtype(('U', 32)))
    names = features_and_names[0:total_features]
    features = features_and_names[total_features:total_features * 2]

    agg_features = aggregate_features(features.tolist())

    # if we've seen the required number of aggregated features, then publish to the redis stream
    if agg_features[6] == 5:
        print("publishing aggregated features to stream for lat/lon ", features[6], "/", features[7])
        fs = agg_features[0:raw_features]
        fs.append(features[6])
        fs.append(features[7])
        d = dict(zip(names[0:total_features], fs))
        redis_client.xadd("housing-features-stream", d)
