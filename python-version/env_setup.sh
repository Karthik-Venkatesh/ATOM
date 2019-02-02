#!/usr/bin/env bash

function printHelp() {
    echo "Usage: "
    echo "  env_setup.sh [<option> <option value>]"
    echo "    <mode> - one of 'createEnv', 'removeEnv', 'installRequirements', 'reinitializeEnv'"
    echo ""
    echo "      - 'createEnv' - Create conda env with name 'atom' and python 3.6"
    echo "      - 'removeEnv' - Removes conda env 'atom'"
    echo "      - 'installRequirements' - Install requirements which is in requirements.txt"
    echo "      - 'reinitializeEnv' - Completely removes 'atom' env, creates new one and installs all requirements"
    echo ""
    echo "Example: $ ./env_setup.sh --mode reinitializeEnv"
}

function createEnv() {
    conda create --name atom python=3.6 --no-default-packages -y
}

function removeEnv() {
    conda remove -n atom --all -y
}

function activateEnv() {
    source activate atom
}

function installRequirements() {
    pip install -r requirements.txt
}

function reinitializeEnv() {
    removeEnv
    createEnv
    activateEnv
    installRequirements
}

function parseParam() {
  while [[ "$1" != "" ]]; do
    case $1 in
      --mode )
        MODE=$2
        ;;
      --help )
        printHelp
        exit
        ;;
      * )
        exit
        ;;
    esac
    shift
    shift
  done
}

function execute() {
  if [[ "$MODE" == "createEnv" ]]; then
    createEnv
  elif [[ "$MODE" == "removeEnv" ]]; then
    removeEnv
  elif [[ "$MODE" == "installRequirements" ]]; then
    installRequirements
  elif [[ "$MODE" == "reinitializeEnv" ]]; then
    reinitializeEnv
  else
    printHelp
    exit 1
  fi
}

parseParam $@
execute