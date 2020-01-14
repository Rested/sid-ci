#!/bin/sh

exec /usr/bin/ssh -o StrictHostKeyChecking=no -i $ID_RSA_PATH "$@"
