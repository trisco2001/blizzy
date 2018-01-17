rm -f blizzy.zip

echo "Zipping new Archive"
zip -X -r blizzy.zip *

echo "Updating Function..."
aws lambda update-function-code --function-name item-level --zip-file fileb://blizzy.zip

rm -f blizzy.zip
