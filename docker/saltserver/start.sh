#!/bin/bash
set -e
source /etc/lsb-release
echo "id: $DISTRIB_ID-$DISTRIB_RELEASE-$(hostname)" >> /etc/salt/minion
service salt-master start
python