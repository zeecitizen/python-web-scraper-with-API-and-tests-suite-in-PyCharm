#!/usr/bin/env bash

git clone git@github.com:zeecitizen/python-web-scraper-with-API-and-tests-suite-in-PyCharm.git
image_id=$(docker build --no-cache -q . | awk -F':' '{print $2}')
docker run $image_id /bin/sh -c 'cd python-web-scraper-with-API-and-tests-suite-in-PyCharm && python /tests/test_1.py'

