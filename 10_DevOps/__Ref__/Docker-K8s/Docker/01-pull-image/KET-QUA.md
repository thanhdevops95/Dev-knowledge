# Bài 01 — Kết quả thực chạy

## docker pull hello-world
Using default tag: latest
latest: Pulling from library/hello-world
58dee6a49ef1: Pulling fs layer
58dee6a49ef1: Download complete
58dee6a49ef1: Pull complete
c3bdf82c34d1: Download complete
Digest: sha256:0e760fdfbc48ba8041e7c6db999bb40bfca508b4be580ac75d32c4e29d202ce1
Status: Downloaded newer image for hello-world:latest
docker.io/library/hello-world:latest

## docker pull python:3.11-slim
3.11-slim: Pulling from library/python
Digest: sha256:9a7765b36773a37061455b332f18e265e7f58f6fea9c419a550d2a8b0e9db834
Status: Downloaded newer image for python:3.11-slim
docker.io/library/python:3.11-slim

## docker pull alpine:latest
latest: Pulling from library/alpine
d17f077ada11: Pulling fs layer
2bf6ea167e4a: Download complete
4c52853c1057: Download complete
d17f077ada11: Download complete
d17f077ada11: Pull complete
Digest: sha256:5b10f432ef3da1b8d4c7eb6c487f2f5a8f096bc91145e68878dd4a5019afde11
Status: Downloaded newer image for alpine:latest
docker.io/library/alpine:latest

## Verify
python        3.11-slim   214MB
alpine        latest      13.6MB
hello-world   latest      22.6kB
docker: 'docker images' requires at most 1 argument

Usage:  docker images [OPTIONS] [REPOSITORY[:TAG]]

Run 'docker images --help' for more information
