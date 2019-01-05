#!/usr/bin/env bash

DATABASE_CONTAINER_NAME=atom-mongodb
COMPOSE_FILE=docker-compose.yml

function printHelp() {
    echo "Usage: "
    echo "  database.sh [<option> <option value>]"
    echo "    <mode> - 'up', 'down', 'reStart', 'destroy'"
    echo ""
    echo "      - 'up' - Starts the database container if old one available otherwise creates new one."
    echo "      - 'down' - Stops the database container"
    echo "      - 'reStart' -  Stops the database container and runs again."
    echo "      - 'destroy' - Stopping database service and removes container."
    echo ""
    echo "    <options> - one of --mode, --help"
    echo "      --mode - execution functionality"
    echo "      --help - help"
}

function up() {
    echo "Starting MongoDB..."
    docker-compose -f $COMPOSE_FILE up -d
}

function down() {
    docker-compose -f $COMPOSE_FILE kill
}

function reStart() {
    down
    up
}

function destroy() {
    echo "Destroying MongoDB Container..."
    docker-compose -f $COMPOSE_FILE down
    docker volume prune
}

function execute() {
  if [[ "$MODE" == "up" ]]; then
    up
  elif [[ "$MODE" == "down" ]]; then
    down
  elif [[ "$MODE" == "reStart" ]]; then
    reStart
  elif [[ "$MODE" == "destroy" ]]; then
    destroy
  else
    printHelp
    exit 1
  fi
}

function parseParam() {
  while [[ "$1" != "" ]]; do
    case $1 in
      --mode )
        MODE=$2
        ;;
      --help )
        printHelp
        exit 1
        ;;
      * )
        printHelp
        exit 1
        ;;
    esac
    shift
    shift
  done
}

parseParam $@
execute