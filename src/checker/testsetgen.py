import os
import sys

tsize = {'smol':(20, 2), 'stronk':(200, 1), 'yuge':(2000, 1)}

extras = {'e':(1, 1), 'v':(3, 0), 'f':(1, 4)}

LTYPES = 5

def useful_number(ltype, candidate):
    return candidate if ltype != 0 else 0

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python3 testsetgen.py <suite_name>')
        sys.exit(1)
    my_path = os.path.dirname(os.path.abspath(sys.argv[0]))
    suite_name = sys.argv[1]
    suite_path = os.path.join(my_path, suite_name)
    if os.path.isdir(suite_path):
        print('{} already exists, choose a different name'.format(suite_name))
        sys.exit(1)
    for name, param in tsize.items():
        total = param[0]
        test_num = param[1]
        generated = [0] * LTYPES
        productive = accessible = total // 2
        for it in range(test_num):
            for ltype in range(LTYPES):
                useful = useful_number(ltype, total // 4)
                command = "python3 {} {} {} {} {} {} {} {}-{}-{} eauvf".format(os.path.join(my_path, 'gen.py'), useful, accessible, productive, total,
                    ltype, suite_name, name, ltype, generated[ltype])
                print(command)
                os.system(command)
                generated[ltype] += 1
            for tag,(cnt, ltype) in extras.items():
                useful = useful_number(ltype, total // 4)
                for i in range(cnt):
                    command = "python3 {} {} {} {} {} {} {} {}-{}-{} {}".format(os.path.join(my_path, 'gen.py'), useful, accessible,
                            productive, total, ltype, suite_name, name, ltype, generated[ltype], tag)
                    print(command)
                    os.system(command)
                    generated[ltype] += 1
