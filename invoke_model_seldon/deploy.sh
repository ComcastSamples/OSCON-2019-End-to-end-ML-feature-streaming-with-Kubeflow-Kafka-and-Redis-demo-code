#!/bin/bash

# when local with docker for mac k8s, you must use the kubeflow namespace
kubectl create -f housing-predictor-seldon.yaml -n kubeflow
