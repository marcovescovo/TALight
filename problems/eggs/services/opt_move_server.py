#!/usr/bin/env python3

# METADATA OF THIS TAL_SERVICE:
problem="eggs"
service="opt_move"
args_list = [
    ('n_eggs',int),
    ('n_floors',int),
    ('lang',str),
    ('ISATTY',bool),
]

from sys import exit, argv
from random import randrange
from math import inf as IMPOSSIBLE

from multilanguage import Env, Lang, TALcolors
ENV =Env(args_list, problem, service, argv[0])
TAc =TALcolors(ENV)
LANG=Lang(ENV, lambda fstring: eval(f"f'{fstring}'"))
TAc.print(LANG.opening_msg, "green")

# START CODING YOUR SERVICE:


# INITIALIZATON: allocation, base cases, sentinels
table = [ [0] + [IMPOSSIBLE] * ENV['n_floors'] ]
for u in range(ENV['n_eggs']):
    table.append([0] + [None] * ENV['n_floors'])

# INDUCTTVE STEP: the min-max recursion with nature playing against
for u in range(1,1+ENV['n_eggs']):
    for f in range(1,1+ENV['n_floors']):
        table[u][f] = IMPOSSIBLE
        best_launch_floor = None
        for first_launch_floor in range(1,1+f):
            if table[u][f] > 1+max(table[u][f-first_launch_floor],table[u-1][first_launch_floor-1]):
                best_launch_floor = first_launch_floor
                table[u][f] = 1+max(table[u][f-first_launch_floor],table[u-1][first_launch_floor-1])

print(f"When you are given {ENV['n_eggs']} eggs and the floors are {ENV['n_floors']} then there exists a policy that guarantees you to find out the truth in no more than than {table[ENV['n_eggs']][ENV['n_floors']]} launches.\nThis is optimal.\nA possible first move for such an optimal strategy is to launch one egg from floor {best_launch_floor}.")

exit(0)
