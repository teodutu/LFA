import numpy as np
import sys
import random
import string
import os
import re

alphabet_pool = list(string.digits + string.ascii_letters + '`-=[];\'\\./~!@#$%^&*_+:"|<>?')

def check(argv):
    if len(argv) != 9:
        print_usage('Wrong number of arguments')

    try:
        useful = int(argv[1])
        accessible = int(argv[2])
        productive = int(argv[3])
        total = int(argv[4])
        ltype = int(argv[5])
        prefix = argv[6]
        name = argv[7]
        uses = argv[8]
    except ValueError:
        print_usage('Wrong argument format')

    if ' ' in name:
        print_usage('<name> must not contain spaces')

    if not bool(re.search('^[eauvf]+$', uses)):
        print_usage('<uses> must not be empty and must only contain valid tests (e, a, u, v, f)')

    if ltype < 0 or ltype >=5:
        print_usage('<ltype> must be between 0 and 4')

    if useful < 0 or accessible < 0 or productive < 0 or total < 0:
        print_usage('<useful>, <accessible>, <productive> and <total> must be positive')

    if total < accessible + productive - useful:
        print_usage('<total> must be at least <accessible> + <productive> - <useful>')

    if useful > accessible or useful > productive:
        print_usage('<useful> must not be larger than <accessible> and <productive>')

    if accessible < 1:
        print_usage('<accessible> must be at least 1')

    if (ltype == 0 and useful != 0) or (ltype != 0 and useful == 0):
        print_usage('<useful> must be 0 iff <ltype> is 0')

    if is_finite(ltype) and accessible - useful == 0:
        print_usage('If the language is finite, <accessible> - <useful> must not be 0')

    if not has_e(ltype) and useful == 1:
        print_usage('If the language does not contain e, <useful> must be at least 2')

    return useful, accessible, productive, total, ltype, prefix, '{}-{}'.format(name, uses)

def print_usage(message):
    print(message)
    print( """Usage: python3 gen.py <useful> <accessible> <productive> <total> <ltype> <name> <uses>
    <useful>: number of useful states (productive and accessible)
    <accessible>: number of states accessible from the initial state
    <productive>: number of productive states
    <total>: total number of states
    <ltype>:
        - 0 if the language is the empty set
        - 1 if the language is finite and contains the empty string
        - 2 if the language is finite, not empty and does not contain the empty string
        - 3 if the language is infinite and contains the empty set
        - 4 if the language is infinite and does not contain the empty string
    <prefix>: directory where the files will be generated
    <name>: name of the test.
    <uses>: arguments that will be tested (e, a, u, v, f)
    """)
    sys.exit(-1)

def has_e(ltype):
    return ltype == 1 or ltype == 3

def is_finite(ltype):
    return ltype <= 2

def gen_range(tuples):
    r = []
    for tup in tuples:
        r = r + list(range(tup[0], tup[1]))
    return r

def gen_req(data, delta, param):
    start = param[0][0]
    stop = param[0][1]
    if start == stop:
        return
    for i in range(start, stop):
        if param[1] and i > 0 and 'chain' not in data[i]:
            padre = random.randint(0, i - 1)
            data[i]['padre'] = padre
            data[i]['chain'] = data[padre]['chain'] + 1
            delta.append((padre, data[padre]['tran'], i))
            data[padre]['tran'] += 1
        if param[2] and 'final' not in data[i]:
            if random.random() > 0.8 and i > 0:
                data[i]['final'] = True
            else:
                hijo = random.choice(param[3][i - start + 1:])
                delta.append((i, data[i]['tran'], hijo))
                data[i]['tran'] += 1
                if param[1] and ('chain' not in data[hijo] or data[i]['chain'] >= data[hijo]['chain']):
                    data[hijo]['padre'] = i
                    data[hijo]['chain'] = data[i]['chain'] + 1

def force_cycle(data, delta, zone):
    index = np.argmax([elem['chain'] for elem in data[zone[0] : zone[1]]])
    limit = data[index]['chain']
    stops = [random.randint(0, limit), random.randint(0,limit)]
    fst = max(stops)
    snd = min(stops)
    while data[index]['chain'] != fst:
        index = data[index]['padre']
    src = index
    while data[index]['chain'] != snd:
        index = data[index]['padre']
    dst = index
    delta.append((src, data[src]['tran'], dst))
    data[src]['tran'] += 1

def gen_fill(data, delta, param, target, finite):
    start = param[0][0]
    stop = param[0][1]
    for i in range(start, stop):
        while data[i]['tran'] < target:
            hijo = random.choice(param[4][finite * (i - start + 1):])
            delta.append((i, data[i]['tran'], hijo))
            data[i]['tran'] += 1

def gen_alphabet(target):
    global alphabet_pool
    random.shuffle(alphabet_pool)
    result = alphabet_pool[0:target]
    del alphabet_pool[0:target]
    return result

def gen_pool():
    pool = string.ascii_letters + string.digits + '_'
    return list(pool)

def gen_names(name_pool, target):
    min_len = 1 + np.floor(np.log(target) / np.log(len(name_pool))).astype('int')
    names = set([])
    while len(names) < target:
        length = random.randint(min_len, min_len * 2 + 1)
        name = ''.join(random.choice(name_pool) for i in range(length))
        names.add(name)
    return list(names)

def attach_suffix(prefix, name, suffix):
    return os.path.join(prefix, '{}.{}'.format(name, suffix))

def output_binary(prefix, name, suffix, condition):
    with open(attach_suffix(prefix, name, suffix), 'wt') as f:
        print('Yes' if condition else 'No', file = f)

def output_states(prefix, name, suffix, states):
    states.sort()
    with open(attach_suffix(prefix, name, suffix), 'wt') as f:
        for state in states:
            print(state, file = f)

def export_results(prefix, name, data, delta, names, alphabet, ltype, zones):
    prefix = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), prefix)
    if not os.path.isdir(prefix):
        os.makedirs(prefix)

    transitions = ['({},{},{})'.format(names[p], alphabet[a], names[q]) for (p, a, q) in delta]

    initial_state_str = names[0]

    final_states = [names[i] for i, elem in enumerate(data) if 'final' in elem]
    productive_states = [names[st] for st in gen_range([zones[0], zones[2]])]
    accessible_states = [names[st] for st in gen_range([zones[0], zones[1]])]
    useful_states = [names[st] for st in gen_range([zones[0]])]

    output_binary(prefix, name, 'e', has_e(ltype))

    output_binary(prefix, name, 'v', ltype == 0)

    output_binary(prefix, name, 'f', is_finite(ltype))

    output_states(prefix, name, 'p', productive_states)

    output_states(prefix, name, 'a', accessible_states)

    output_states(prefix, name, 'u', useful_states)

    random.shuffle(names)
    states_str = '{{{}}}'.format(','.join(names))

    random.shuffle(alphabet)
    alphabet_str = '{{{}}}'.format(','.join(alphabet))

    random.shuffle(transitions)
    transitions_str = '({})'.format(','.join(transitions))

    random.shuffle(final_states)
    final_states_str = '{{{}}}'.format(','.join(final_states))

    with open(attach_suffix(prefix, name, 'in'), 'wt') as fin:
        print('({},{},{},{},{})'.format(states_str, alphabet_str, transitions_str, initial_state_str, final_states_str), file = fin)

    with open(os.path.join(prefix, 'gen.log'), 'a+') as log:
        print("{}".format(' '.join(sys.argv)), file = log)

if __name__ == '__main__':
    useful, accessible, productive, total, ltype, prefix, name = check(sys.argv)

    data = [{'tran':0} for i in range(total)]

    zones = [(0, useful),
            (useful, accessible),
            (accessible, accessible + productive - useful),
            (accessible + productive - useful, total)
            ]

    #(zone, accessibility, productivity, prod range, fill range
    params = [
            (zones[0], True, True, gen_range([zones[0]]), gen_range([zones[0], zones[1]])),
            (zones[1], True, False, [], gen_range([zones[1]])),
            (zones[2], False, True, gen_range([zones[2], zones[0]]), gen_range(zones)),
            (zones[3], False, False, [], gen_range([zones[1], zones[3]]))
            ]

    #start state
    data[0]['chain'] = 0

    #mandatory final states
    if useful != 0:
        data[zones[0][1] - 1]['final'] = True
    elif productive - useful != 0:
        data[zones[2][1] - 1]['final'] = True
    if has_e(ltype):
        data[0]['final'] = True

    delta = []

    for i in range(len(zones)):
        gen_req(data, delta, params[i])

    if not is_finite(ltype):
        force_cycle(data, delta, zones[0])

    tran_cnt = max([elem['tran'] for elem in data])

    tran_target = random.randint(tran_cnt, min(len(alphabet_pool), int(tran_cnt * 1.5)))

    for i in range(len(zones)):
        gen_fill(data, delta, params[i], tran_target, is_finite(ltype) and i == 0)

    alphabet = gen_alphabet(tran_target)

    name_pool = gen_pool()

    names = gen_names(name_pool, len(data))

    export_results(prefix, name, data, delta, names, alphabet, ltype, zones)
