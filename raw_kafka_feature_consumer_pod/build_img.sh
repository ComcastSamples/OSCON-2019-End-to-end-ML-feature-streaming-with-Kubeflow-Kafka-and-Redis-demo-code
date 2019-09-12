#!/bin/bash

VERSION=$1
echo $VERSION

time docker build -t housing-kafka-consumer:$VERSION .
