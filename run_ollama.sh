#!/bin/bash

# run_ollama.sh [model==phi3:mini] [ollama cmd == pull else run]

MODEL="$1"
RUN='pull'

if [ -z "$2" ]; then
  RUN='run'
fi

echo $MODEL, $RUN

if ! [ -f /usr/local/bin/ollama ]; then
  curl -fsSL https://ollama.com/install.sh | sh

  ollama serve &
  sleep 5

  echo "--------------------------------"
  echo        Installo model embed
  echo "--------------------------------"
  ollama pull nomic-embed-text
  sleep 12

  if [ -z "$1" ]; then
    MODEL="phi3:mini"
  else
    MODEL="$1"
  fi

  echo "--------------------------------"
  echo     pull model $MODEL
  echo "--------------------------------"
  ollama pull $MODEL

else
  echo "--------------------------------"
  echo       Ollama già installato
  echo "--------------------------------"
  ollama ps
fi