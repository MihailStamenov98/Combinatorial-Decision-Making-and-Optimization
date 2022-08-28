include "globals.mzn";

int: chip_width;
int: n_blocks;   % Number of blocks
set of int: BLOCKS = 1..n_blocks;  
array[BLOCKS] of int: widths; % block width
array[BLOCKS] of int: heights; % block width
int: max_height = sum(i in BLOCKS)(heights[i]);
array[1..n_blocks] of var 0..chip_width-1: blocks_x;
array[1..n_blocks] of var 0..max_height-1: blocks_y;

constraint cumulative(blocks_y, heights, widths, chip_width);
%chip_height as objective function
var int: chip_height = max(b in BLOCKS)(blocks_y[b] + heights[b]);

constraint cumulative(blocks_x, widths, heights, chip_height);



solve minimize chip_height;

output [
    "x-s   =", show(blocks_x), "\n",
    "y-s   =", show(blocks_y), "\n",
    "chip_height = ", show(chip_height), "\n"
];
