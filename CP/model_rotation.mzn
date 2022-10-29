include "globals.mzn";

int: chip_width;
int: chip_max_height; % upper bound for y coordinates
int: n_blocks;   % Number of blocks
set of int: BLOCKS = 1..n_blocks;
array[BLOCKS, 1..2] of int: dimensions;
array[BLOCKS] of var bool: rotated; % variables to know if pice is rotated

array[BLOCKS] of var int: widths; % we do not know if the pice will be rotated
array[BLOCKS] of var int: heights; % we do not know if the pice will be rotated
array[BLOCKS] of var 0..chip_width: blocks_x;
array[BLOCKS] of var 0..chip_max_height: blocks_y;

constraint forall(i in BLOCKS)( widths[i] = if rotated[i] then dimensions[i,2] else dimensions[i,1] endif);
constraint forall(i in BLOCKS)( heights[i] = if rotated[i] then dimensions[i,1] else dimensions[i,2] endif);
constraint cumulative(blocks_y, heights, widths, chip_width);
var int: chip_height = max(b in BLOCKS)(blocks_y[b] + heights[b]);
constraint cumulative(blocks_x, widths, heights, chip_height);


ann: search_ann_x = 
%if heuristic == 1 then
%  int_search(p_x, input_order, indomain_min)
%elseif heuristic == 2 then
%  int_search(p_x, first_fail, indomain_min)
%elseif heuristic == 3 then
%  int_search(p_x, dom_w_deg, indomain_min)
%elseif heuristic == 4 then
%  int_search(p_x, input_order, indomain_random)
%elseif heuristic == 5 then
%  int_search(p_x, first_fail, indomain_random)
%else
%  int_search(p_x, dom_w_deg, indomain_random)
%endif;

ann: search_ann_y = 
if heuristic == 1 then
  int_search(blocks_y, input_order, indomain_min)
elseif heuristic == 2 then
  int_search(blocks_y, first_fail, indomain_min)
elseif heuristic == 3 then
  int_search(blocks_y, dom_w_deg, indomain_min)
elseif heuristic == 4 then
  int_search(blocks_y, input_order, indomain_random)
elseif heuristic == 5 then
  int_search(blocks_y, first_fail, indomain_random)
else
  int_search(blocks_y, dom_w_deg, indomain_random)
endif;

ann: restart_ann =
if restart == 1 then
  restart_constant(100)
elseif restart == 2 then
  restart_linear(100)
elseif restart == 3 then
  restart_geometric(1.5,100)
elseif restart == 4 then
  restart_luby(100)
else
  restart_none
endif;

solve :: search_ann_x
      :: search_ann_y
      :: restart_ann
         minimize chip_height;
