URL=http://localhost:8001/api/v1/namespaces/models/services/http:seldon-sklearn-housing-pred-dep-seldon-sklearn-housing-pred-dep:8000/proxy/api/v0.1/predictions

echo "1"
time curl -k -H "Content-Type: application/json" -d "@test.json" -X POST $URL
echo "10"
time curl -k -H "Content-Type: application/json" -d "@test_10.json" -X POST $URL
echo "100"
time curl -k -H "Content-Type: application/json" -d "@test_100.json" -X POST $URL
echo "1000"
time curl -k -H "Content-Type: application/json" -d "@test_1000.json" -X POST $URL

