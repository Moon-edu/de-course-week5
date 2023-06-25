#/bin/bash
EXIT_CODE=0
echo "Running test"
poetry run pytest --json-report || EXIT_CODE=$?

echo "Printing out report"
OUTCOME=$(cat .report.json | jq -r '.tests[]|"\(.outcome),\(.nodeid)"')

while IFS= read -r line; do
  echo "Processing line: $line"

  IFS=',' read -r outcome nodeid <<< "$line"

  TEST_ID=$(echo $nodeid | awk -F"::" '{print $2}')
  if [ "$outcome" = "failed" ]; then
    echo "Test $TEST_ID failed"
    TOTAL=0
  else
    echo "Test $TEST_ID passed, Adding ${SCORE[TEST_ID]}"
    TOTAL=100
  fi
done <<< "$OUTCOME"
echo "Total score: $TOTAL"
exit $EXIT_CODE