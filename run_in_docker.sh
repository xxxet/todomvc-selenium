#!/usr/bin/env bash
allure_rep=./allure_results/$(date +%Y%m%d_%H:%M:%S)
docker build . -t todomvc-tests
docker compose -f docker-compose-dyn_grid.yml up -d
mkdir -p $allure_rep
docker run --network todomvc-selenium_default -v $(pwd)/:/root/projects/ui-tests  todomvc-tests ./entrypoint.sh $allure_rep
docker compose  -f docker-compose-dyn_grid.yml  stop
allure serve $allure_rep
