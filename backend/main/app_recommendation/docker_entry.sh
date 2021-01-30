#!/bin/bash

cd $DST_DIR/app/src

gunicorn \
--workers=3 \
--worker-class=gevent \
--worker-connections=1000 \
--log-level=$GUNICORN_LOG_LEVEL \
--bind 0.0.0.0:$APP_PORT patched:app
