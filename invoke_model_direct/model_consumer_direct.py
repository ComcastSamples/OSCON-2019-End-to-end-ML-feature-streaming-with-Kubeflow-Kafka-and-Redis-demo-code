import pickle
import redis
import pandas as pd
from sklearn import datasets
from sklearn.preprocessing import MinMaxScaler

# load the saved trained model
model_file = 'example_model.pkl'
model = pickle.load(open(model_file, 'rb'))

# load the data set for normalization (ideally you'll have the min/max here)
d = datasets.fetch_california_housing(data_home='/root/scikit_learn_data', download_if_missing=False)

# combine the data into a single data frame
df = pd.DataFrame(d.data, columns=d.feature_names)

# normalize the data
norm = MinMaxScaler().fit(X=df)
med_house_val_scaler = MinMaxScaler().fit(d.target.reshape(-1, 1))

# listen for messages, parse them, send to redis for windowing then invoke the model
# FOR SINGLE/LOCAL REDIS
r = redis.Redis(host='host.docker.internal', port=6379)

print('starting consumer direct')
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
            feature_names = msg_dict.keys()
            features = [list(map(float, list(msg_dict.values())))]
            m_df = pd.DataFrame(features, columns=feature_names)
            m_df = pd.DataFrame(norm.transform(X=m_df))

            # call predict and output the transformed price
            prediction = model.predict(m_df.values)
            transformed_prediction = med_house_val_scaler.inverse_transform([prediction])
            print('direct msg_id=', msg_id, ', lat/lon=', features[0][6:8],
                    ', prediction = $', str(transformed_prediction[0][0]*100_000))
