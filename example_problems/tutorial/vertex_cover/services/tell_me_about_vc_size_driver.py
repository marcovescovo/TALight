#!/usr/bin/env python3
from sys import stderr

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper

import random
import networkx as nx
import matplotlib.pyplot as plt
import vertex_cover_lib as vcl

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('source',str),
    ('collection',str),
    ('instance_id',int),
    ('instance_format',str),
    ('num_vertices',int),
    ('num_edges',int),
    ('weighted',bool),
    ('upper_bound',int),
    ('lower_bound',int),
    ('plot',bool),
    ('plot_sol',bool),
    ('seed',str),
    ('lang',str)
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE:
## Input Sources
if TALf.exists_input_file('instance'):
  instance = vcl.get_instance_from_str(TALf.input_file_as_str('instance'), instance_format_name=ENV["instance_format"])
  TAc.print(LANG.render_feedback("successful-load", 'The file you have associated to `instance` filehandler has been successfully loaded.'), "yellow", ["bold"])

elif ENV["source"] == 'terminal':
  instance = {}
  instance['num_vertices'] = ENV['num_vertices']
  instance['num_edges'] = ENV['num_edges']

  #TAc.print(LANG.render_feedback("waiting-line", f'#? Waiting for the graph.\nGraph format: (x,y) (w,z) ... (n,m)\n'), "yellow")
  TAc.print(LANG.render_feedback("waiting-line", f'#? Waiting for the graph.\n'), "yellow")

  TAc.print(LANG.render_feedback("insert-edges", f'Given {ENV["num_vertices"]} vertices labelled with the naturals in the interval [0,{ENV["num_vertices"]-1}], you are now expected to enter {ENV["num_edges"]} edges. To specify an edge, simply enter its two endonodes separated by spaces.'), "yellow", ["bold"])
  edges = []
  for i in range(1,1+ENV["num_edges"]):
    TAc.print(LANG.render_feedback("insert-edge", f'Insert the two endpoints of edge {i}, that is, enter a line with two naturals in the interval [0,{ENV["num_vertices"]-1}],  separated by spaces.'), "yellow", ["bold"])
    u,v = TALinput(int, 2, TAc=TAc)
    edges.append([u,v])

  for u,v in edges:
    if u not in range(ENV['num_vertices']) or v not in range(ENV['num_vertices']):
      TAc.print(f'Edge ({u}, {v}) is not a valid edge for the graph. Aborting.\n', "red", ["bold"], flush=True)
      exit(0)

  if len(edges) != ENV['num_edges']:
    TAc.print(LANG.render_feedback("wrong-edges-number", f'\nWrong number of edges ({len(edges)} instead of {ENV["num_edges"]})\n'), "red", ["bold"])
    exit(0)

  if ENV['weighted']:
    TAc.print(LANG.render_feedback("insert-weights", f'Enter nodes weights. Format: integers separated by spaces:'), "yellow", ["bold"])
    l = TALinput(str, line_recognizer=lambda val,TAc, LANG: True, TAc=TAc, LANG=LANG)

    if len(l) != ENV['num_vertices']:
      TAc.print(LANG.render_feedback("wrong-weights-number", f'\nWrong number of weights ({len(l)} instead of {ENV["num_vertices"]})\n'), "red", ["bold"])
      exit(0)

    for w in l:
      if not w.isdigit():
        TAc.print(LANG.render_feedback("wrong-weights-format", f'\nWeights must be integer numbers. Aborting.\n'), "red", ["bold"])
        exit(0)

  G = nx.Graph()
  G.add_nodes_from([int(v) for v in range(ENV['num_vertices'])])
  G.add_edges_from(edges)

  i = 0

  for v in G.nodes():
    G.add_node(v, weight=int(l[i]))
    i += 1

  instance['graph'] = G

  instance_str = vcl.instance_to_str(instance, format_name=ENV['instance_format'])
  output_filename = f"terminal_instance.{ENV['instance_format']}.txt"

elif ENV["source"] == 'randgen_1':
  # Get random instance
  if not ENV['weighted']:
    instance = vcl.instances_generator(1, 1, ENV['num_vertices'], ENV['num_edges'], ENV['seed'])[0]
  else:
    instance = vcl.instances_generator(1, 1, ENV['num_vertices'], ENV['num_edges'], ENV['seed'], 1)[0]

else: # take instance from catalogue
  #instance_str = TALf.get_catalogue_instancefile_as_str_from_id_and_ext(ENV["instance_id"], format_extension=vcl.format_name_to_file_extension(ENV["instance_format"],'instance'))
  instance_str = TALf.get_catalogue_instancefile_as_str_from_id_collection_and_ext(ENV["collection"], ENV["instance_id"], format_extension=vcl.format_name_to_file_extension(ENV["instance_format"],'instance'))
  instance = vcl.get_instance_from_str(instance_str, instance_format_name=ENV["instance_format"])
  TAc.print(LANG.render_feedback("instance-from-catalogue-successful", f'The instance with instance_id={ENV["instance_id"]} has been successfully retrieved from the catalogue.'), "yellow", ["bold"])

# Trovo il peso totale del grafo ("no cover")
total_weight = 0
for n,w in nx.get_node_attributes(instance['graph'], 'weight').items():
  total_weight += w

# Check parametri
if not ENV['weighted']:
  if ENV['upper_bound'] > ENV['num_vertices']:
    TAc.print(LANG.render_feedback("invalid-upper-bound", f'\nERROR: upper bound can\'t be greater than the number of vertices.\n'), "red", ["bold"])
    exit(0)
else:
  if ENV['upper_bound'] > total_weight:
    TAc.print(LANG.render_feedback("invalid-upper-bound-weighted", f'\nERROR: upper bound can\'t be greater than the number of vertices.\n'), "red", ["bold"])
    exit(0)

if ENV['lower_bound'] <= 0:
  TAc.print(LANG.render_feedback("invalid-lower-bound", f'\nERROR: lower bound must be greater than 0.\n'), "red", ["bold"])
  exit(0)

# Calcolo soluzione
if (ENV['source'] == "catalogue" and instance['exact_sol'] == 1) or (ENV['source'] != "catalogue"):
  if ENV['weighted']:
    vc_sol, size_sol, weight_sol = vcl.calculate_minimum_weight_vc(instance['graph'])
  else:
    vc_sol, size_sol = vcl.calculate_minimum_vc(instance['graph'])
else:
  vc_sol = instance['sol']
  vc_sol = [int(i) for i in vc_sol.split()]
  size_sol = len(vc_sol)

  if ENV['weighted']:
    weight_sol = instance['sol_weight']

TAc.print(LANG.render_feedback("this-is-the-instance", '\nThis is the instance:\n'), "white", ["bold"], flush=True)
TAc.print(vcl.instance_to_str(instance,ENV["instance_format"]), "white", ["bold"], flush=True)

TAc.print(LANG.render_feedback("insert-opt-value", f'\nWrite here your conjectured size k of the vertex cover: if exists a vertex cover of size at least k, you will get a positive answer. Otherwise, if you only intend to be told about the size k of the vertex cover, enter 0.'), "yellow", ["bold"], flush=True)

if ENV['plot']:
  vcl.plot_graph(instance['graph'])

answer = TALinput(str, line_recognizer=lambda val,TAc, LANG: True, TAc=TAc, LANG=LANG)
answer = int(answer[0])

  
if answer > instance['num_vertices']:
  TAc.print(LANG.render_feedback("invalid-k", f'ERROR: size k can\'t be higher than the number of vertices.'), "red", ["bold"])
  exit(0)

if (ENV['source'] == "catalogue" and instance['exact_sol'] != 1) or (ENV['source'] != "catalogue"):
  size, vc = vcl.calculate_minimum_vc(instance['graph'])
else:
  vc = instance['sol']
  size = len(instance['sol'].split())

if answer == 0:
  TAc.print(LANG.render_feedback("best-sol", f'Size k of the minimum vertex cover is: '), "green", ["bold"], flush=True, end='')
  TAc.print(f'{size}.', "white", ["bold"], flush=True)
else:

  if answer == size:
    TAc.OK()
    TAc.print(LANG.render_feedback("right-exact-sol", f'We agree, the graph has a vertex cover of size exactly '), "green", ["bold"], flush=True, end='')
    TAc.print(f'{answer}.', "white", ["bold"], flush=True)
  elif answer > size:
    TAc.print(LANG.render_feedback("right-sol", f'Yes, the graph has a vertex cover of size at least '), "yellow", ["bold"], flush=True, end='')
    TAc.print(f'{answer}.', "white", ["bold"], flush=True)
  else:
    TAc.NO()
    TAc.print(LANG.render_feedback("wrong-sol", f'We don\'t agree, the graph does not have a vertex cover of size at least {answer}.'), "red", ["bold"], flush=True)

if ENV['plot_sol']:
  vcl.plot_mvc(instance['graph'], vc)
exit(0)
