#!/bin/bash
exec 1>match_logs/summary.log
exec 2>&1

agent_files=$@
timer="/usr/bin/time"
run_match_command="python run_match.py"
run_match_args="-f -r 50"
#run_match_args="-f -r 50 -t 1000"

echo "================================================================================"
echo "Batch run started `date`"
echo "Using command: $run_match_command $run_match_args"
echo

for f in $agent_files; do 
    agent_name=$(basename "$f" .py)
    echo "--------------------------------------------------------------------------------"
    echo "Agent:" $agent_name
    echo
    cp "$f" my_custom_player.py
    $timer $run_match_command $run_match_args
    cp matches.log "match_logs/$agent_name.log"
    echo
done
echo "--------------------------------------------------------------------------------"
echo