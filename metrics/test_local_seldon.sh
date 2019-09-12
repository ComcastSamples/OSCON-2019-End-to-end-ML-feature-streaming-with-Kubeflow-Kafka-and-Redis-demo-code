#!/bin/bash

kubectl proxy &
sleep 0.5
NAME=seldon-sklearn-house-deploy-seldon-sklearn-house-dep
#URL=http://localhost:8080/seldon/$NAME/api/v0.1/predictions
#URL=https://localhost:6443/api/v1/namespaces/kubeflow/services/http:$NAME:8000/proxy/api/v0.1/predictions
# URL=https://localhost:6443/api/v1/namespaces/kubeflow/services/http:$NAME:8000/proxy/api/v0.1/predictions
URL=http://localhost:8001/api/v1/namespaces/kubeflow/services/http:$NAME:8000/proxy/api/v0.1/predictions

curl -k -H "Content-Type: application/json" -d "@test_local_seldon.json" -X POST \
$URL
