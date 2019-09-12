#curl -k -H "Content-Type: application/json" -d "@test.json" -X POST \
#http://localhost:5000/predict

URL=http://localhost:5000/predict
curl -d "@test.json" -X POST \
$URL