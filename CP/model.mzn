include "globals.mzn";

int: chip_width;
int: chip_max_height;
int: n_blocks;   % Number of blocks
set of int: BLOCKS = 1..n_blocks;
array[BLOCKS] of int: widths;
array[BLOCKS] of int: heights;

array[int] of int: order = arg_sort([-widths[i]*heights[i] | i in BLOCKS]); 

int: area_min = sum([heights[i] * widths[i] | i in BLOCKS]);
var 0..area_min: white_space = chip_width*chip_height - area_min;
int: min_height = max(max(heights), floor(area_min/chip_width));

array[BLOCKS] of var 0..chip_width-min(widths): blocks_x;
array[BLOCKS] of var 0..chip_max_height-min(heights): blocks_y;

constraint max([blocks_x[i] + widths[i] | i in BLOCKS]) <= chip_width;
constraint max([blocks_y[i] + heights[i] | i in BLOCKS]) <= chip_height;


constraint cumulative(blocks_y, heights, widths, chip_width);
var min_height..chip_max_height: chip_height = max(b in BLOCKS)(blocks_y[b] + heights[b]);
constraint cumulative(blocks_x, widths, heights, chip_height);
% relationships among circuits
constraint diffn(blocks_x, blocks_y, widths, heights);

array[1..2*n_blocks] of var int: flat_board;

constraint forall (i in BLOCKS) ( flat_board[i] = blocks_x[i] /\ flat_board[n_blocks+i] = blocks_y[i] );
% symmetry breaking (horizontal flip, vertical flip and 180° rotation)
constraint lex_lesseq(flat_board, [ if i <= n_blocks 
                                    then abs(chip_width - blocks_x[i] - widths[i]) 
                                    else flat_board[i] 
                                    endif | i in 1..2*n_blocks])
        /\ lex_lesseq(flat_board, [ if i > n_blocks 
                                    then abs(chip_height - blocks_y[i-n_blocks] - heights[i-n_blocks]) 
                                    else flat_board[i]
                                    endif | i in 1..2*n_blocks])
        /\ lex_lesseq(flat_board, [ if i > n_blocks 
                                    then abs(chip_height - blocks_y[i-n_blocks] - heights[i-n_blocks]) 
                                    else abs(chip_width - blocks_x[i] - widths[i])
                                    endif | i in 1..2*n_blocks]);

% full_bottom
array[BLOCKS] of var int: y_0 = [if blocks_y[i] = 0 then widths[i] else 0 endif | i in BLOCKS];
constraint sum(y_0) == chip_width;                                    

ann: search_ann_x = int_search(blocks_x, first_fail, indomain_min);
ann: search_ann_y = int_search(blocks_y, first_fail, indomain_min);

ann: restart_ann = restart_luby(100);

solve :: seq_search([int_search([blocks_x[i] | i in order], input_order, indomain_min, complete), int_search([blocks_y[i] | i in order], input_order, indomain_min, complete)]) minimize area_min*chip_height+white_space;

/*
solve :: search_ann_x
      :: search_ann_y
      :: restart_ann minimize area_min*chip_height+white_space;
      */
output ["\(blocks_x)\n",
        "\(blocks_y)\n",
        "\(chip_height)\n",
        ];
  