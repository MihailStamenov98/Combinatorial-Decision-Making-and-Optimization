include "globals.mzn";


int: search;
int: restart;

int: chip_width;
int: chip_max_height;
int: n_blocks;   % Number of blocks
set of int: BLOCKS = 1..n_blocks;
array[BLOCKS] of int: widths;
array[BLOCKS] of int: heights;
array[BLOCKS] of var bool: rotated; % variables to know if pice is rotated
int: min_size = min(min(widths), min(heights));
int: max_size = max(max(widths), max(heights));

array[BLOCKS] of int: order = reverse(arg_sort([max(heights[i], widths[i]) | i in BLOCKS]));
%array[int] of int: order = arg_sort([-widths[i]*heights[i] | i in BLOCKS]); 
int: area_of_blocks = sum([heights[i] * widths[i] | i in BLOCKS]);
var 0..area_of_blocks: empty_space = chip_width*chip_height - area_of_blocks;
int: min_height = max(max_size, floor(area_of_blocks/chip_width));

array[BLOCKS] of var min_size..max_size: rotation_widths;
array[BLOCKS] of var min_size..max_size: rotation_heights;
array[BLOCKS] of var 0..chip_width-min_size: blocks_x;
array[BLOCKS] of var 0..chip_max_height-min_size: blocks_y;

constraint max([blocks_x[i] + rotation_widths[i] | i in BLOCKS]) <= chip_width;
constraint max([blocks_y[i] + rotation_heights[i] | i in BLOCKS]) <= chip_height;

constraint forall(i in BLOCKS)(if rotated[i] then rotation_widths[i] = heights[i] /\ rotation_heights[i] = widths[i] else rotation_widths[i] = widths[i] /\ rotation_heights[i] = heights[i] endif);

constraint cumulative(blocks_y, rotation_heights, rotation_widths, chip_width);
var min_height..chip_max_height: chip_height = max(b in BLOCKS)(blocks_y[b] + rotation_heights[b]);
constraint cumulative(blocks_x, rotation_widths, rotation_heights, chip_height);
constraint diffn(blocks_x, blocks_y, rotation_widths, rotation_heights);

array[1..2*n_blocks] of var int: flat_board = [if i <= n_blocks 
                                               then blocks_x[i] 
                                               else blocks_y[i-n_blocks] 
                                               endif | i in 1..2*n_blocks];

% symmetry breaking (horizontal flip, vertical flip and 180° rotation)
constraint forall(i in BLOCKS)( if widths[i] == heights[i] then rotated[i] = false endif);
constraint lex_lesseq(flat_board, [ if i <= n_blocks 
                                    then abs(chip_width - blocks_x[i] - rotation_widths[i]) 
                                    else flat_board[i] 
                                    endif | i in 1..2*n_blocks])
        /\ lex_lesseq(flat_board, [ if i > n_blocks 
                                    then abs(chip_height - blocks_y[i-n_blocks] - rotation_heights[i-n_blocks]) 
                                    else flat_board[i]
                                    endif | i in 1..2*n_blocks])
        /\ lex_lesseq(flat_board, [ if i > n_blocks 
                                    then abs(chip_height - blocks_y[i-n_blocks] - rotation_heights[i-n_blocks]) 
                                    else abs(chip_width - blocks_x[i] - rotation_widths[i])
                                    endif | i in 1..2*n_blocks]);

% full_bottom
array[BLOCKS] of var int: y_0 = [if blocks_y[i] = 0 then rotation_widths[i] else 0 endif | i in BLOCKS];
constraint sum(y_0) == chip_width;


ann: search_ann_x = if search == 1 then
      int_search(blocks_x, input_order, indomain_min)
elseif search == 2 then
      int_search(blocks_x, first_fail, indomain_min)
elseif search == 3 then
      int_search(blocks_x, first_fail, indomain_random)
elseif search == 4 then
      int_search(blocks_x, dom_w_deg, indomain_random)
else
      int_search([blocks_x[i] | i in order], input_order, indomain_min, complete)
endif;

ann: search_ann_y = if search == 1 then
      int_search(blocks_y, input_order, indomain_min)
elseif search == 2 then
      int_search(blocks_y, first_fail, indomain_min)
elseif search == 3 then
      int_search(blocks_y, first_fail, indomain_random)
elseif search == 4 then
      int_search(blocks_y, dom_w_deg, indomain_random)
else
      int_search([blocks_y[i] | i in order], input_order, indomain_min, complete)
endif;

ann: restart_ann = if  restart == 1 then
      restart_linear(100)
elseif restart == 2 then
      restart_luby(100)
else
      restart_none
endif;

solve :: seq_search([search_ann_x, search_ann_y, restart_ann]) minimize area_of_blocks*chip_height+empty_space;

output ["\(blocks_x)\n",
        "\(blocks_y)\n",
        "\(chip_height)\n",
        "\(rotated)\n",
        ];
