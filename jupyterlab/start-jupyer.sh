#!/bin/bash

JUPYTER_SESSION=$((JUPYTER_SESSION * 60))

while true; do
  # Generate a new token
  export JUPYTER_TOKEN=$(python3 -c 'import uuid; print(uuid.uuid4())')
  echo "Generated token: ${JUPYTER_TOKEN}"
  echo jupyter lab --ip=0.0.0.0 --port=8888 --no-browser --NotebookApp.token=${JUPYTER_TOKEN} --NotebookApp.password='' --notebook-dir=/notebook --allow-root 
  # Save token to shared file
  echo "${JUPYTER_TOKEN}" > /notebook/token.file
  
  #echo "Clearing runtime sessions..."
  #rm -rf /root/.local/share/jupyter/runtime/*
  
  # Start JupyterLab in background
  jupyter lab \
    --ip=0.0.0.0 \
    --port=8888 \
    --no-browser \
    --NotebookApp.token=${JUPYTER_TOKEN} \
    --NotebookApp.password='' \
    --notebook-dir=/notebook \
    --allow-root &

  JUPYTER_PID=$!
  echo "Clearing runtime sessions..."
  rm -rf /root/.local/share/jupyter/runtime/*
  echo "Started JupyterLab (PID: $JUPYTER_PID). Will run for ${JUPYTER_SESSION} seconds."
  # Wait before killing
  sleep ${JUPYTER_SESSION}
  kill $JUPYTER_PID
  echo "JupyterLab process $JUPYTER_PID killed. Restarting..."
done

  