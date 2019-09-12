URL=http://localhost:5000/predict

echo "1"
time curl -d "@test_local.json" -X POST $URL
echo "10"
time curl -d "@test_10_local.json" -X POST $URL
echo "100"
time curl -d "@test_100_local.json" -X POST $URL
echo "1000"
time curl -d "@test_1000_local.json" -X POST $URL

