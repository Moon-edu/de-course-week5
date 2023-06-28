#/bin/bash
EXIT_CODE=0
sleep 60

RETRY=20
while [ $RETRY -gt 0 ]; do
  HAS_DAG=$(curl -s http://localhost:8080/api/experimental/dags/stock/dag_runs | jq -e 'type == "array"')
  if [ "$HAS_DAG" == "true" ]; then
    DAG_RESULTS=$(curl -s http://localhost:8080/api/experimental/dags/stock/dag_runs | jq -r '.[]|.state' | wc -l)
    LC=$(echo "$DAG_RESULTS" | grep "running" | wc -l)
    echo "$DAG_RESULTS"
    if [ $LC != 1 ] && [ ${DAG_RESULTS[0]} == 31 ]; then
      echo "All scheduled has been done, checking result..."
      RETRY=0
    else
      echo "Schedules are not done yet, sleep 30 secs & will retry"
      RETRY=$((RETRY-1))
      sleep 30
    fi
  else
    echo "DAG stock not found"
    echo "Total score: 0"
    exit 1
  fi
done

echo "Running test"
poetry run pytest --json-report || EXIT_CODE=$?
if [ $EXIT_CODE != 0 ]; then
  sleep 10
  poetry run pytest --json-report || EXIT_CODE=$?
fi

echo "Printing out report"
OUTCOME=$(cat .report.json | jq -r '.tests[]|"\(.outcome),\(.nodeid)"')

while IFS= read -r line; do
  echo "Processing line: $line"

  IFS=',' read -r outcome nodeid <<< "$line"

  TEST_ID=$(echo $nodeid | awk -F"::" '{print $2}')
  if [ "$outcome" = "passed" ]; then
    echo "Test $TEST_ID passed, Adding ${SCORE[TEST_ID]}"
    TOTAL=100
  else
    echo "Test $TEST_ID failed"
    TOTAL=0
    EXIT_CODE=1
  fi
done <<< "$OUTCOME"
echo "Total score: $TOTAL"
exit $EXIT_CODE