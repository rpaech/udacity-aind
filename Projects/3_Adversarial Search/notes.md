# Implementation notes

## Baseline

Note: All baseline tests applied using #my_moves - #opponent_moves heuristic provided in the sample players python file.

### Minimax with depth 3 search against greedy opponent

```
$ python run_match.py -f -o GREEDY -r 50
Running 100 games:
++-+-+++-++++++---++-+-++-+--+++-+-+-+++++---++-++++--++-++++++-+++++-++-+++--+-+-+-+-++-+--++--++++
Running 100 games:
+++++++-+++++++---+-++++++-++-+++-+++-++-++++-+++++++-+-++-+--+-+-+++-++-++++-+-++-+++-+-+-++++++-++
Your agent won 69.0% of matches against Greedy Agent
```

### Negamax with depth 3 search against greedy opponent

```
Running 100 games:
+-+---+++-++-+++-+-+-+-+++++++-+-++-++-+++-+-+-+++---+--+-+-+++++++--+-+-+--++--+++++-++++-+++++-+++
Running 100 games:
-++-+++-+-+++---++-+--+-+++++++--+-++++---++-++++++-+-+-++++-++-+-++++-++++++++---++----+-+---+-+-++
Your agent won 63.5% of matches against Greedy Agent
```

### AB negamax with depth 3 search against greedy opponent

```
Running 100 games:
+++--++++-++---++++-+------+++-----+-++-+-++-+++--++-+-+++-+++-+++-+-+-+-++++-+---+-+-+-++-+++--++-+
Running 100 games:
++++-++++++-+-+++++++-----+-+++----+--++++-++++++-+----+-+-++-++++-++++++++++-+--++-++----+-++++++++
Your agent won 61.5% of matches against Greedy Agent
```

### Minimax with depth 3 search against random opponent

```
Running 100 games:
++++-+++++++++++++++++++++++-++++-++++++++++++++++++++++++++++++++++++++++-+++++++++++-+++++++++++++
Running 100 games:
+++-+++++++++++++++++++++++++++++--++++-++++++++++-++++++++++++++++++++++++--+++++++++++++++++++-++-
Your agent won 93.0% of matches against Random Agent
```

### AB negamax with depth 3 search against random opponent

```
Running 100 games:
+++++++-+++++++--++++++++++++++++++++-+-++-+++++++++++++++++++++++++++++++-++++++++++-+++++-++++++++
Running 100 games:
++++++++++++++++++++++++++-++++++++++++++++++++++++++++++++++++++++++++-+++++++++++++++++++-+-++++++
Your agent won 93.5% of matches against Random Agent
```

