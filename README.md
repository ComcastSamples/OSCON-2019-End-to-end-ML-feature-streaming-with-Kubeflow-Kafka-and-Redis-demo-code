# OSCON demo

This repository contains the demo code presented during the talk [End-to-end ML streaming with Kubeflow, Kafka, and Redis at scale](https://conferences.oreilly.com/oscon/oscon-or/public/schedule/detail/79363) at O'Reilly OSCON 2019.

The code basically shows how to:
1. train and save a simple model from the California Housing prices dataset from scikit-learn
1. serve that model with seldon core kubernetes
1. stream raw features to kafka
1. aggregate features (perform feature engineering) and stream engineered features to redis
1. invoke model directly from redis engineered features

To run this demo, follow the [jupyter notebook](Demo.ipynb)

The slides from my talk are available [here](https://cdn.oreillystatic.com/en/assets/1/event/295/End-to-end%20ML%20streaming%20with%20Kubeflow,%20Kafka,%20and%20Redis%20at%20scale%20Presentation.pdf)

The following great projects were used / referenced:
* Python, scikit-learn, MLFlow
* Kafka, Redis, Docker, Kubernetes, Kubeflow, Seldon Core
* Prometheus, Grafana

Troubleshooting:
* Make sure not to use some VPN software while running this demo as it may interfere with docker desktop and k8s routing
* If your network changes, you may need to restart kafka and the redis docker container
* Make sure `kubectl proxy` isn't running

The code samples here are licensed under the Apache 2.0 License
