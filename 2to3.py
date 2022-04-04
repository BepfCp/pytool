import os
import argparse

"""
python 2to3.py --dir-path "[Your relative (or absolute) dir path]"
"""

parser = argparse.ArgumentParser(description='Convert Python 2 code to Python 3.')
parser.add_argument('--dir-path', type=str, default='.')
args = parser.parse_args()

dir_path = os.path.abspath(args.dir_path)

for file in os.listdir(dir_path):
    if file.endswith('.py'):
        os.system('2to3 -w {}'.format(os.path.join(dir_path, file)))