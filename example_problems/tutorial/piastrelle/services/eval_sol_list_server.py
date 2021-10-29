#!/usr/bin/env python3
from sys import stderr, exit
import random
from time import monotonic

from TALinputs import TALinput
from multilanguage import Env, Lang, TALcolors

from piastrelle_lib import Par

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('sorting_criterion',str),
    ('goal',str),
    ('code_lang',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"))

# START CODING YOUR SERVICE:
MAX_N_PAIRS = 14
if ENV["code_lang"]=="compiled":
    MAX_N_PAIRS += 1
instances = list(range(0,MAX_N_PAIRS + 1))
if ENV["goal"] == "efficient":
    MAX_N_PAIRS = 100
    if ENV["code_lang"]=="compiled":
        MAX_N_PAIRS *= 2
    scaling_factor = 1.2
    n = instances[-1]
    while True:
        n = 1 + int(n * scaling_factor)
        if n > MAX_N_PAIRS:
            break
        instances.append(n)

p = Par(MAX_N_PAIRS)
sorting_criterion=ENV['sorting_criterion']
def one_test(n_tiles):
    correct_list=[]
    num_sol=p.num_sol(n_tiles)
    for i in range (1,num_sol+1):
        risp_correct = p.unrank(n_tiles,i,sorting_criterion)
        #TAc.print(f"{risp_correct}", "yellow", ["bold"])
        correct_list.append(risp_correct)
    #print(correct_list)
    risp=[]
    start = monotonic()
    answ=input().split(' , ')
    end = monotonic()
    t = end - start # è un float, in secondi
    for elem in range(len(answ)):
        if answ[elem] != correct_list[elem]:
            #print('#',answ[elem:elem+n_tiles*2+1], correct_list[elem])
            TAc.print(LANG.render_feedback("not-correct", f'# No. Your solution is NOT correct.'), "red", ["bold"])                        
            exit(0)
    return t
for n_tiles in instances:
    print(n_tiles, sorting_criterion)
    time = one_test(n_tiles)
    print(f"#Correct! [took {time} secs on your machine]")
    if time > 1:
        if n_tiles > 13:
            TAc.print(LANG.render_feedback("seems-correct-weak", f'# Ok. :) Your solution correctly computes the list of well formed tilings of a corridor of dimension 1x{n_tiles} using as criterion {sorting_criterion}.'), "green")
        TAc.print(LANG.render_feedback("not-efficient", f'# No. You solution is NOT efficient. When run on your machine, it took more than one second to compute the list of well-formed tilings of a corridor of dimension 1x{n_tiles}.'), "red", ["bold"])        
        exit(0)

TAc.print(LANG.render_feedback("seems-correct-strong", f'# Ok. :)  Your solution appears to be correct (checked on several instances).'), "green")
TAc.print(LANG.render_feedback("efficient", f'# Ok. :) Your solution is efficient: its running time is polynomial in the length of the tilings.'), "green")
exit(0)
