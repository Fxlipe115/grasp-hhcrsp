#!/user/bin/env python3

import argparse
import sys

class HhcrspInstance:
    def __init__(self, file_path):
        with open(file_path) as f:
            _ = f.readline()
            self.nbNodes = int(f.readline())

            _ = f.readline()
            self.nbVehi = int(f.readline())

            _ = f.readline()
            self.nbServi = int(f.readline())

            _ = f.readline()
            self.r = []
            for i in range(self.nbNodes):
                self.r.append([int(x) for x in f.readline().split()])

            _ = f.readline()
            self.DS = [int(x) for x in f.readline().split()]

            _ = f.readline()
            self.a = []
            for i in range(self.nbVehi):
                self.a.append([int(x) for x in f.readline().split()])

            _ = f.readline()
            self.x = [int(x) for x in f.readline().split()]

            _ = f.readline()
            self.y = [int(x) for x in f.readline().split()]

            _ = f.readline()
            self.d = []
            for i in range(self.nbNodes):
                self.d.append([float(x) for x in f.readline().split()])

            _ = f.readline()
            self.p = []
            for i in range(self.nbNodes * self.nbVehi):
                self.p.append([float(x) for x in f.readline().split()])

            _ = f.readline()
            self.mind = [int(x) for x in f.readline().split()]

            _ = f.readline()
            self.maxd = [int(x) for x in f.readline().split()]

            _ = f.readline()
            self.e = [int(x) for x in f.readline().split()]

            _ = f.readline()
            self.l = [int(x) for x in f.readline().split()]
            
    def __str__(self):
        return 'nbNodes' + '\n' + \
            str(self.nbNodes) + '\n' + \
            'nbVehi' + '\n' + \
            str(self.nbVehi) + '\n' + \
            'nbServi' + '\n' + \
            str(self.nbServi) + '\n' + \
            'r' + '\n' + \
            '\n'.join(map(lambda l: ' '.join(str(x) for x in l) ,self.r)) + '\n' + \
            'DS' + '\n' + \
            ' '.join(str(x) for x in self.DS) + '\n' + \
            'a' + '\n' + \
            '\n'.join(map(lambda l: ' '.join(str(x) for x in l) ,self.a)) + '\n' + \
            'x' + '\n' + \
            ' '.join(str(x) for x in self.x) + '\n' + \
            'y' + '\n' + \
            ' '.join(str(x) for x in self.y) + '\n' + \
            'd' + '\n' + \
            '\n'.join(map(lambda l: ' '.join(str(x) for x in l) ,self.d)) + '\n' + \
            'p' + '\n' + \
            '\n'.join(map(lambda l: ' '.join(str(x) for x in l) ,self.p)) + '\n' + \
            'mind' + '\n' + \
            ' '.join(str(x) for x in self.mind) + '\n' + \
            'maxd' + '\n' + \
            ' '.join(str(x) for x in self.maxd) + '\n' + \
            'e' + '\n' + \
            ' '.join(str(x) for x in self.e) + '\n' + \
            'l' + '\n' + \
            ' '.join(str(x) for x in self.l) 


# Functions goes here


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GRASP-GGCRSP')
    parser.add_argument('-f', dest='file', required=True, help='The instance file.\n')
    parser.add_argument('-o', dest='outfile', help='Output Filename, for best solution and time elapsed')

    args = parser.parse_args()
    out = sys.stdout if args.outfile is None else open(args.outfile, 'w')

    instance = HhcrspInstance(args.file)

    # always pass file=out parameter to print
    # just to test parameter reading
    print(instance, file=out)

    # TODO everything else
