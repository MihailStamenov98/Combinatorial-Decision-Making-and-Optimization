include "globals.mzn";

%int: restart;
%int: changeVal;
%
int: chip_width;
int: chip_max_height;
int: n_blocks;   % Number of blocks
set of int: BLOCKS = 1..n_blocks;
array[BLOCKS] of int: widths;
array[BLOCKS] of int: heights;

array[BLOCKS] of var 0..chip_width: blocks_x;
array[BLOCKS] of var 0..chip_max_height: blocks_y;

constraint cumulative(blocks_y, heights, widths, chip_width);
var int: chip_height = max(b in BLOCKS)(blocks_y[b] + heights[b]);
constraint cumulative(blocks_x, widths, heights, chip_height);

array[1..2*n_blocks] of var int: flat_board;

constraint forall (i in BLOCKS) ( flat_board[i] = blocks_x[i] /\ flat_board[n+i] = blocks_y[i] );
% symmetry breaking (horizontal flip, vertical flip and 180° rotation)
constraint symmetry_breaking_constraint(
           lex_lesseq(flat_board, [ (if i <= n 
                                      then abs(w - blocks_x[i] - widths[i]) 
                                      else flat_board[i]) | i in 1..2*n])
        /\ lex_lesseq(flat_board, [ (if i > n 
                                      then abs(chip_height - blocks_y[i] - heights[i]) 
                                      else flat_board[i]) | i in 1..2*n])
        /\ lex_lesseq(flat_board, [ (if i > n 
                                      then abs(chip_height - blocks_y[i] - heights[i]) 
                                      else abs(w - blocks_x[i] - widths[i])) | i in 1..2*n]]));

%ann: search_ann_x = int_search(blocks_x, changeVal, indomain_min)
%if heuristic == 1 then
%  int_search(blocks_x, input_order, indomain_min)
%elseif heuristic == 2 then
%  int_search(blocks_x, first_fail, indomain_min)
%elseif heuristic == 3 then
%  int_search(blocks_x, dom_w_deg, indomain_min)
%elseif heuristic == 4 then
%  int_search(blocks_x, input_order, indomain_random)
%elseif heuristic == 5 then
%  int_search(blocks_x, first_fail, indomain_random)
%else
%  int_search(blocks_x, dom_w_deg, indomain_random)
%endif;

%ann: search_ann_y = int_search(blocks_y, changeVal, indomain_min)
%if heuristic == 1 then
%  int_search(blocks_y, input_order, indomain_min)
%elseif heuristic == 2 then
%  int_search(blocks_y, first_fail, indomain_min)
%elseif heuristic == 3 then
%  int_search(blocks_y, dom_w_deg, indomain_min)
%elseif heuristic == 4 then
%  int_search(blocks_y, input_order, indomain_random)
%elseif heuristic == 5 then
%  int_search(blocks_y, first_fail, indomain_random)
%else
%  int_search(blocks_y, dom_w_deg, indomain_random)
%endif;

%ann: restart_ann =
%if restart == 1 then
%  restart_constant(100)
%elseif restart == 2 then
%  restart_linear(100)
%elseif restart == 3 then
%  restart_geometric(1.5,100)
%elseif restart == 4 then
%  restart_luby(100)
%else
%  restart_none
%endif;

solve minimize chip_height;
%:: search_ann_x
      %:: search_ann_y
      %:: restart_ann
      