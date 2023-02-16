#!/bin/bash
set -eu

# docker.sock から gid を取得して、docker グループの gid を変更
docker_group_id=$(stat /var/run/docker.sock --format="%g")
sudo groupmod --gid ${docker_group_id} docker

# 無限待ち（vscode デフォルトの entrypoint と同じ方法で）
while sleep 1000; do :; done
