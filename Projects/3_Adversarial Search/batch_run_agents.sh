#!/bin/bash
exec 1>>batch_run_agents.log
exec 2>&1

timer="/usr/bin/time"
run_match_command="python run_match.py -f -r 50"

echo "================================================================================"
echo "New batch run started `date`"
echo "Using command: $run_match_command"
echo

for f in agents/*.py; do 
    echo "--------------------------------------------------------------------------------"
    echo "Agent:" $(basename "$f" .py)
    echo
    cp "$f" my_custom_player.py
    $timer $run_match_command
    echo
done
echo "--------------------------------------------------------------------------------"
echo