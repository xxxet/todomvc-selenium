#!/usr/bin/env bash
docker build . -t todomvc-tests
docker compose -f docker-compose-dyn_grid.yml up
docker run -v  $(pwd)/:/root/projects/ui-tests  todomvc-tests ./entrypoint.sh
