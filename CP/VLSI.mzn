include "globals.mzn";

int: chip_width;
int: n_blocks;   % Number of blocks
set of int: BLOCKS = 1..n_blocks;
array[BLOCKS, 1..2] of int: dimensions;

array[BLOCKS] of int: widths = [dimensions[i,1] | i in BLOCKS] ;
array[BLOCKS] of int: heights = [dimensions[i,2] | i in BLOCKS] ;
int: max_height = sum(i in BLOCKS)(heights[i]);
array[BLOCKS] of var 0..chip_width-1: blocks_x;
array[BLOCKS] of var 0..max_height-1: blocks_y;
constraint cumulative(blocks_y, heights, widths, chip_width);
var int: chip_height = max(b in BLOCKS)(blocks_y[b] + heights[b]);
constraint cumulative(blocks_x, widths, heights, chip_height);

solve minimize chip_height;
