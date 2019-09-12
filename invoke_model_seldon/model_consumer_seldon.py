import redis
import requests
import pandas as pd
from sklearn import datasets
from sklearn.preprocessing import MinMaxScaler
import json

# load the data set for normalization (ideally you'll have the min/max here)
d = datasets.fetch_california_housing(data_home='/root', download_if_missing=False)

# combine the data into a single data frame
df = pd.DataFrame(d.data, columns=d.feature_names)

# normalize the data
norm = MinMaxScaler().fit(X=df)
med_house_val_scaler = MinMaxScaler().fit(d.target.reshape(-1, 1))

# listen for messages, parse them, send to redis for windowing then invoke the model
#  for a single redis instance (not a cluster)
r = redis.Redis(host='host.docker.internal', port=6379)

url = 'http://seldon-sklearn-house-deploy-seldon-sklearn-house-dep:8000/api/v0.1/predictions'
print('starting consumer seldon')
while True:
    # note that the $ is just for demo purposes only - to correctly implement this
    # one would need to either use 'xreadgroup >' or do an 'xread $' to get the
    # first message id, then use 'xread LAST_READ_MESSAGE_ID' (https://redis.io/commands/xread)
    for msg in r.xread({'housing-features-stream': '$'}, block=100):
        for m in msg[1]:
            msg_id = m[0]
            msg_dict = m[1]
            # decode the values from the redis stream
            msg_dict = {k.decode(): v.decode() for k, v in msg_dict.items()}

            # organize features and transform
            feature_names = list(msg_dict.keys())
            features = [list(map(float, list(msg_dict.values())))]
            m_df = pd.DataFrame(features, columns=feature_names)
            m_df = pd.DataFrame(norm.transform(X=m_df), columns=feature_names)

            # call predict and output the transformed price
            jsonData = {"data": {"names": feature_names,
                                 "tensor": {"shape": [1, 8], "values": m_df.values.tolist()[0]}}}

            response = requests.post(url, json=jsonData)
            response_json = json.loads(response.text)
            prediction = response_json['data']['tensor']['values']
            transformed_prediction = med_house_val_scaler.inverse_transform([prediction])
            print('seldon msg_id=', msg_id, ', lat/lon=', features[0][6:8],
                    ', prediction = $', str(transformed_prediction[0][0]*100_000))
