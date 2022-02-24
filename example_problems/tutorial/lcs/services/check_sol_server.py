#!/usr/bin/env python3
from sys import exit

from multilanguage import Env, Lang, TALcolors
from TALinputs import TALinput
from TALfiles import TALfilesHelper

from math_modeling import ModellingProblemHelper

import lcs_lib as ll

# METADATA OF THIS TAL_SERVICE:
args_list = [
    ('instance_id',int),
    ('instance_format',str),
    ('sol_format',str),
]

ENV =Env(args_list)
TAc =TALcolors(ENV)
LANG=Lang(ENV, TAc, lambda fstring: eval(f"f'{fstring}'"), print_opening_msg = 'now')
TALf = TALfilesHelper(TAc, ENV)

# START CODING YOUR SERVICE: 

if ENV["instance_id"] == 0:
    if not TALf.exists_input_file('instance'):
        TAc.print(LANG.render_feedback("missing-instance", f'This service requires that either the `instance_id` argument is different than 0 so that the intended instance can be taken from the catalogue, or that the handle to a local file containing the instance is passed through the `instance` filehandler. Two call examples:\n    1.   rtal connect lcs check_sol -asol_format=annotated_subseq -finstance=instances_catalogue/all_instances/instance_003.only_strings.txt -fsolution=my_sols/all_instances/solution_003.annotated_subseq.txt\n    2.   rtal connect lcs check_sol -asol_format=annotated_subseq -ainstance_id=3 -fsolution=my_sols/all_instances/solution_003.annotated_subseq.txt'), "red", ["bold"])
        exit(0)
    instance = None
else: # take instance from catalogue
    mph = ModellingProblemHelper(TAc, ENV.INPUT_FILES, ENV.META_DIR)
    instance_str = mph.get_file_str_from_id(ENV["instance_id"], format_name=ll.format_name_to_file_extension(ENV["instance_format"], 'instance'))
    instance = ll.get_instance_from_str(instance_str, instance_format_name=ENV["instance_format"])
    TAc.print(LANG.render_feedback("instance-from-catalogue-successful", f'The instance with instance_id={ENV["instance_id"]} has been successfully retrieved from the catalogue.'), "yellow", ["bold"])
if TALf.exists_input_file('instance'):
    instance2 = ll.get_instance_from_txt(TALf.input_file_as_str('instance'), instance_format_name=ENV["instance_format"])
    TAc.print(LANG.render_feedback("instance-successfully-loaded", 'The file you have associated to `instance` filehandler has been successfully loaded.'), "yellow", ["bold"])
    if instance2 == instance:
        TAc.print(LANG.render_feedback("same-instance", f'The instance contained in the loaded file is indeed the same as the instance from the catalogue with instance_id={ENV["instance_id"]}.'), "yellow", ["bold"])
    elif instance == None:
        instance = instance2
    else:
        TAc.print(LANG.render_feedback("different-instances", f'The instance contained in the loaded instance file differs from the one in the catalogue with instance_id={ENV["instance_id"]}.'), "red", ["bold"])
        
TAc.print(LANG.render_feedback("this-is-the-instance", "The instance is:"), "yellow", ["bold"])
TAc.print(ll.instance_to_str(instance), "white", ["bold"])
m=len(instance[0])
n=len(instance[1])
print()

if not TALf.exists_input_file('solution'):
    TAc.print(LANG.render_feedback("missing-solution", f'This service requires that the handle to a local file containing your solution is passed. Call example:\n    rtal connect lcs check_sol /asols_format=annotated_subseq -finstance=instances_catalogue/all_instances/instance_003.only_strings.txt -fsolution=my_sols/all_instances/solution_003.annotated_subseq.txt'), "red", ["bold"])
if ENV["sol_format"] == 'subseq':
    solution_subseq_as_string = TALf.input_file_as_str('solution')[:-1]
    solution_as_subseq = ll.str_to_sequence(solution_subseq_as_string)
    TAc.print(LANG.render_feedback("solution-successfully-loaded", f'Your `solution` file has been successfully loaded.'), "white", ["bold"])
    TAc.print(LANG.render_feedback("user-sol-as-subseq", f'Your solution is:\n{solution_subseq_as_string}'), "yellow", ["bold"])
if ENV["sol_format"] == 'annotated_subseq':
    solution_annotated_subseq = ll.read_annotated_subseq(TALf.input_file_as_str('solution'))
    solution_annotated_subseq_as_string = ll.render_annotated_subseq_as_str(solution_annotated_subseq)
    solution_as_subseq = ll.annotated_subseq_to_sequence(solution_annotated_subseq)
    TAc.print(LANG.render_feedback("solution-successfully-loaded", f'Your `solution` file has been successfully loaded.'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("user-sol-as-in-file", f'Your solution, as we have read it, is:'), "yellow", ["bold"])
    TAc.print(LANG.render_feedback("legend-annotated_subseq", f"(LCS Character - First string index - Second string index)"), "yellow", ["bold"])
    TAc.print(solution_annotated_subseq_as_string, "white", ["bold"])
    for line in solution_annotated_subseq_as_string.split('\n'):
        ll.check_input(TAc, LANG, line.split(), m, n)
        
if ll.check_sol_feas_and_opt(TAc, LANG, solution_as_subseq, 'subseq', instance[0], instance[1]):
    TAc.print(LANG.render_feedback("correct-sol", 'Your solution is correct. Well done! You have found the Longest Common Subsequence.'), "green", ["bold"]) 
exit(0)

