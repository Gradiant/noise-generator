#!/bin/bash

docker build -t gradiant/noise-generator:0.1.0 .

docker network create --subnet=172.30.0.0/24 --gateway=172.30.0.254 noisenet

docker run -d --name noise-gen --net=noisenet --ip 172.30.0.2 -p 5001:5001 gradiant/noise-generator:0.1.0

docker run -d --name iperf3-server --net=noisenet --ip 172.30.0.1 alpine:3.8 /bin/sh -c '(apk add --no-cache iperf3; iperf3 -s)'


echo " Open http://localhost:5001 at your browser."
echo "An iperf-server is also deployed at 172.30.0.1. Get output with docker logs iperf3-server"
read -p "Press a key to stop and clean."
echo "cleaning"
docker rm -f noise-gen iperf3-server; docker network rm noisenet
