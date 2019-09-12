#!/bin/bash

# Use source-to-image to build our seldon core model image
s2i build -E environment_rest . seldonio/seldon-core-s2i-python3:0.6-SNAPSHOT sklearn-house-pred:0.1
