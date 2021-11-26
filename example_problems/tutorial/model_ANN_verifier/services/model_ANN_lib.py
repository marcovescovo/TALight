#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# from tabulate import tabulate
import pandas as pd
import copy
import random
import re
#import networkx as nx

### CONSTANTS #########################################
FORMAT_AVAILABLES = ['dat', 'txt']
DAT_STYLES_AVAILABLES = ['']
TXT_STYLES_AVAILABLES = ['only_values','values_with_info']
DEFAULT_FORMAT='only_values.txt'
#######################################################

# INSTANCE GENERATOR FUNCTIONS:
def gen_instance(n_nodes,seed:int):
    
    n_nodes = n_nodes.split(' ')
    n_nodes = list(map(int, n_nodes))
    assert len(n_nodes) >= 2 

    random.seed(seed)
    ann =[]

    # first append the total number of layers
    ann.append(len(n_nodes))

    # then we append the number of nodes for each layer
    ann.append(n_nodes)

    # then we generate n_nodes_i * n_nodes_i+1 weights
    for i in range(1,len(n_nodes)):
        weights = [round(random.uniform(-1,1),2) for _ in range(n_nodes[i-1]*n_nodes[i])] 
        ann.append(weights)

    return ann


def instance_to_txt(instance, style='only_values'):
    """This function returns the string representation of the given matrix instance according to the indicated style"""
    assert style in TXT_STYLES_AVAILABLES, f'Value [{style}] unsupported for the argument format_secondary when format_primary=txt'
    instance_str = 'Tot_layers: ' + str(instance[0]) + '\n' if style=='values_with_info' else str(instance[0]) + '\n'
    instance_str += 'Tot_Nodes: ' + ' '.join(str(e) for e in instance[1]) + '\n' if style=='values_with_info' else ' '.join(str(e) for e in instance[1]) + '\n'
    
    if style=='values_with_info':
        instance_str += 'ANN_weigths: \n' 

    for i in range(2,len(instance)):
        instance_str += ' '.join(str(e) for e in instance[i]) + '\n'

    return instance_str

#print(instance_to_txt([3, [3, 4, 1], [1,2,3,4,5,6,7,8,9,10,11,12], [1,2,3,4]],'values_with_info'))

def instance_to_dat(instance, style=''):
    """This function returns the dat representation of the given matrix instance according to the indicated style"""
    assert style in DAT_STYLES_AVAILABLES, f'Value [{style}] unsupported for the argument format_secondary when format_primary=txt'
    TOT_LAYERS = str(instance[0])
    N_NODES = ' '.join(str(e) for e in instance[1])

    output = f"param TOT_LAYERS := {TOT_LAYERS};  # Total Number of layers in the ANN\n"
    output += f"param N_NODES := {N_NODES};  # Number of nodes for each layer\n"
    output += "param ANN_WEIGTHS :=\n"

    for i in range(2,len(instance)):
        output += f"                     {i-1}   "
        output += ' '.join(str(e) for e in instance[i])
        output += " ;\n" if i == (len(instance) - 1) else "\n"
        
    output += "end;"
    return output

#print(instance_to_dat([3, [3, 4, 1], [1,2,3,4,5,6,7,8,9,10,11,12], [1,2,3,4]],''))

def instance_to_str(instance, format='default'):
    """This function returns the string representation of the given ANN instance according to the indicated format"""
    # Get default
    format = DEFAULT_FORMAT if format=='default' else format
    # Parsing format
    format_list = format.split('.')
    if len(format_list) == 1:
        format_primary = format_list[0]
        format_secondary = ''
    else:
        format_primary = format_list[1]
        format_secondary = format_list[0]

    # Get matrix in str format
    assert format_primary in FORMAT_AVAILABLES, f'Value [{format_primary}] unsupported for the argument format_primary.'
    if format_primary == 'dat':
        return instance_to_dat(instance, format_secondary)
    if format_primary == 'txt':
        return instance_to_txt(instance, format_secondary)


def get_instance_from_str(instance, format):
    """This function returns the string representation of the given ANN instance according to the indicated format."""
    # Parsing format
    format_list = format.split('.')
    if len(format_list) == 1:
        format_primary = format_list[0]
        format_secondary = ''
    else:
        format_primary = format_list[1]
        format_secondary = format_list[0]
    # Get pirellone in str format
    assert format_primary in FORMAT_AVAILABLES, f'Value [{format_primary}] unsupported for the argument format_primary.'
    if format_primary == 'dat':
        return get_instance_from_dat(instance, format_secondary)
    if format_primary == 'txt':
        return get_instance_from_txt(instance, format_secondary)


def get_instance_from_txt(instance, style='only_values'):
    """This function returns the string representation of the given ANN instance according to the indicated format."""
    assert style in TXT_STYLES_AVAILABLES, f'Value [{style}] unsupported for the argument format_secondary when format_primary=txt'
    final_instance = list()
    lines = instance.split('\n')

    for l in lines:
        if len(l) != 0:
            if len(l.split()) == 1:
                final_instance.append(int(l.split()[0]))
            else:
                final_instance.append([int(e) for e in l.split()])
    return final_instance

# to adapt with model_ANN_verifier
def get_instance_from_dat(pirellone, style=''):
    """This function returns the string representation of the given pirellone instance according to the indicated format."""
    assert style in DAT_STYLES_AVAILABLES, f'Value [{style}] unsupported for the argument format_secondary when format_primary=txt'
    instance = list()
    # Get lines
    lines = pirellone.split('\n')
    # Parse lines
    for l in lines:
        l = l.strip() # remove whitespace before and after
        # Filter the matrix lines
        if l != '' and l[:5] != 'param' and l[:3] != 'end':
            l = l.replace(';', '') #ignore ;
            row = list()
            for e in l.split()[1:]:
                row.append(int(e))
            instance.append(row)
    return instance


# Initialize a network
def initialize_network(instance):
    # [3, [3, 4, 3, 2], [-5, -3, -3, -9, -5, -7, -7, 8, 0, -3, -2, 9],[-5, -3, -3, -9, -5, -7, -7, 8, 0, -3, -2, 9], [-10, -3, -5]]

    # here we take the third element of instance list, i.e., the first list of weights between the input layer and the fist hidden layer
    hidden_layer = {}
    index = 1
    for i in range(2, len(instance)-1):
        weights = instance[i]
        n = instance[1][i-2]
        hidden_layer[f'h_{str(index)}'] = [weights[j:j + n] for j in range(0, len(instance[i]), n)]
        index += 1
        

    output_layer = {}
    weights = instance[-1]
    n = instance[1][-2]
    output_layer['out']=[weights[j:j + n] for j in range(0, instance[1][-1])]
   

    return hidden_layer, output_layer


# function (ReLU) for the neuron activation if required
def activate(value, activation):
    if activation == 'ReLU':
	    return max(0, value)
    
    return value


def compute_forward_propagation(instance, values_input_layer,activation):
    hidden_layers, output_layer = initialize_network(instance)
    input_values = values_input_layer

    # propagation for each hidden layer
    for node in hidden_layers:
        new_input = []
        for weights in hidden_layers[node]:
            new_value = 0
            for i in range(len(weights)):
                new_value += input_values[i] * weights[i]
                new_value = activate(new_value, activation)

            new_input.append(new_value)

        input_values = new_input
    
    # compute the output value/s
    for node in output_layer:
        final_output = []
        for weights in output_layer[node]:
            final_value = 0
            for i in range(len(weights)):
                final_value += input_values[i] * weights[i]
                final_value = activate(final_value, activation)
             
            final_output.append(final_value)

    return final_output