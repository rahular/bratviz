#!/bin/bash
# script borrowed from https://github.com/gabrielStanovsky/brat-visualizer

echo "Downloading Brat..."
mkdir -p brat
cd brat
wget http://weaver.nlplab.org/~brat/releases/brat-v1.3_Crunchy_Frog.tar.gz
tar -xvzf brat-v1.3_Crunchy_Frog.tar.gz
rm http://weaver.nlplab.org/~brat/releases/brat-v1.3_Crunchy_Frog.tar.gz
cd ..
echo "Brat downloaded successfully!"

