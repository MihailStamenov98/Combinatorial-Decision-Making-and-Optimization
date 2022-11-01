import os
import sys

cur_path = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(
    cur_path,
    os.pardir)
)
sys.path.append(PROJECT_ROOT)
from utils.read_file import ReadData, readFile, computeMaxHeight



def createDZN(i:int, restart, changeVal, data: ReadData = None ):
    outfile = cur_path + f'\\instances_dzn\\ins-{i}.dzn'
    if data is None:
        data = readFile(i)
    with open(outfile, 'w') as out:
        out.write(f"n_blocks={data.n};\n")
        out.write(f"chip_width={data.w};\n")
        out.write(f"widths={data.dimensions[0]};\n")
        out.write(f"heights={data.dimensions[1]};\n")
        out.write(f"chip_max_height={computeMaxHeight(data.dimensions, data.w)}")
        out.write(f"")
    
