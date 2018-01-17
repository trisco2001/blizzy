#!/usr/bin/env bash

rm -f blizzy.zip

echo "Copying from Winders"
mkdir build
cp -r  . build/

echo "Zipping new Archive"
cd build
zip -X -r ../blizzy.zip *
cd ..

echo "Updating Function..."
aws lambda update-function-code --function-name item-level --zip-file fileb://blizzy.zip

rm -f blizzy.zip