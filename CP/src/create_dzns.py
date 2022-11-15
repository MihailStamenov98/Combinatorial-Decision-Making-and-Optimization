import os
import sys

cur_path = os.path.dirname(__file__)
cur_path = os.path.join(
    cur_path,
    os.pardir)
PROJECT_ROOT = os.path.abspath(os.path.join(
    cur_path,
    os.pardir))
sys.path.append(PROJECT_ROOT)
from utils import ReadData, readFile



def createDZN(i:int, search, restart, data: ReadData = None):
    outfile = os.path.join(
    cur_path,
    "instances_dzn",
    f'ins-{i}.dzn')
    if data is None:
        data = readFile(i)
    with open(outfile, 'w') as out:
        out.write(f"n_blocks={data.n};\n")
        out.write(f"chip_width={data.w};\n")
        out.write(f"widths={data.dimensions[0]};\n")
        out.write(f"heights={data.dimensions[1]};\n")
        out.write(f"search={search};\n")
        out.write(f"restart={restart};\n")
    
