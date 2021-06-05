import random, math

def check_input_vector(vec, TAc, LANG):
    for i in range(1,len(vec)):
        if vec[i] == vec[i-1]:
            TAc.print(LANG.render_feedback("equal-values", f'No. Your vector contains entries with the same value vec[{i-1}] = {vec[i-1]} =vec[{i}].'), "red", ["bold"])
            exit(0)
        if vec[i] < vec[i-1]:
            TAc.print(LANG.render_feedback("decrease", f'No. Your vector is not incrisingly sorted: vec[{i-1}] = {vec[i-1]} > {vec[i]} = vec[{i}].'), "red", ["bold"])
            exit(0)

def random_vector(n, seed="random_seed"):
    if seed=="random_seed":
        random.seed()
        seed = random.randrange(0,1000000)
    else:
        seed = int(seed)
    random.seed(seed)
    first_magic = random.randint(0,n-1)
    last_magic = random.randint(0,n-1)
    vec = list(range(n))
    for i in range(last_magic+1,n):
        vec[i] = vec[i-1] + random.randint(2, 5)
    if first_magic > last_magic:
        first_magic = last_magic +1
    for i in range(first_magic-1,-1,-1):
        vec[i] = vec[i+1] - random.randint(2, 5)    
    return vec,seed

def spot_magic_index(vec):
    magic_indexes = []
    for i in range(len(vec)):
        if vec[i]==i:
            magic_indexes.append(i)
    return magic_indexes

# The worst case is the one where there are n/2 (rounded up) magic indexes on the left of the array. 
# After the first recursion we spot a magic index, so we don't have enough information to determine 
# in which part of the vector we have to search for the rest of the indexes.
# In O(log n base 2) we can spot the first left index, and then in n/2 rounded down (worst case) 
# questions we can spot the last one on the right (assuming more than one magic index).
# The final complexity is O(log n base 2 + n/2 rounded down)

def check_n_questions_worst_case(n):
	return check_n_questions_worst_case_support(n, n)

def check_n_questions_worst_case_support(n, nOriginal):
	"""
	Args:
		n: the vector lenght 
		nOriginal: the original vector lenght. it is used at the end to sum n/2 rounded down

	Returns:
		questions: the minumum number of questions to spot all the magic indexes in the worst case
	"""

	#base case
	if n == 0:
		return 0 + nOriginal//2 #default rounded down
	if n == 1:
		return 1 + nOriginal//2 #default rounded down
	
	return 1 + check_n_questions_worst_case_support((int(math.ceil(n / 2))) - 1, nOriginal)


#We define this method to create a random "worst-case" vector for the play service. 
# Basically, we take a random size between 5 and 20 for the vector and we fill the first 
# n//2 elements of magic indexes and the remaining elements of random values according to 
# the explanation of our worst-case described above.

def random_vector_worst_case():
    size = random.randrange(5,21)
    # create a vector and fill the first n//2 elements with MI
    vec = [i for i in range(0,(size//2)+1)]
    # create a list of random values without duplicates for the remaining elements  
    remaining_elements = random.sample(range(size,100), size-len(vec))
    # sort the random numbers created
    remaining_elements.sort()
    # merge the two lists
    vec.extend(remaining_elements)

    return size, vec
