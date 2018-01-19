#!/usr/bin/env bash

rm -rf ../blizzy.zip && zip -X -r ../blizzy.zip * && aws lambda update-function-code --function-name item-level --zip-file fileb://../blizzy.zip
