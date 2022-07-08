#!/usr/bin/env python3
# -*- coding:latin-1-*-

from sys import stderr, exit

from IPv4_lib_ita import *
from TALinputs import TALinput
from multilanguage import Env, TALcolors, Lang

args_list=[
  ('ip_address', str),
]

ENV = Env(args_list)
TAc = TALcolors(ENV)
LANG= Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')

# START CODING YOUR SERVICE:

TAc.print("\nInserire un indirizzo ip, riceverai i 3 possibili indirizzi internet a cui l'indirizzo ip può essere contenuto", "green", ["bold"])



Ip=(ENV['ip_address'], TAc, LANG)
#ip=TALinput(str, regex= f"regex: //([0-9]{1,3}\.){3}[0-9]{1,3}/gm", TAc=TAc,sep='.')#, regex_explained= "un indirizzo ip è un insieme di 4 terzine di numeri; ogni numero può andare da un minimo di 0 ad un massimo di 255")

Ip=input_ip()


TAc.print("\nL'indirizzo ip inserito può essere contenuto nei seguenti indirizzi internet:\n", "green", ["bold"])
TAc.print("1°-->   ", "green", end="")
TAc.print(Ip[0],"green", end="") 
TAc.print(".0.0.0\n", "green")
TAc.print("2°-->   ", "green", end="")
TAc.print(Ip[0],"green", end="")
TAc.print(".", "green", end="")
TAc.print(Ip[1], "green", end="")
TAc.print(".0.0\n", "green")
TAc.print("3°-->   ", "green", end="")
TAc.print(Ip[0],"green", end="")
TAc.print(".", "green", end="")
TAc.print(Ip[1],"green", end="")
TAc.print(".", "green", end="")
TAc.print(Ip[2], "green", end="")
TAc.print(".0\n", "green")