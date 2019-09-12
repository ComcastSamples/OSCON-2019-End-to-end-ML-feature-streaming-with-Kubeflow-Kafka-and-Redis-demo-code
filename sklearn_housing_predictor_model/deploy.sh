#!/bin/bash

# when local with docker for mac k8s, you must use the kubeflow namespace
kubectl create -f sklearn_housing_predictor.json -n kubeflow
