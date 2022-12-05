## VLSI with CP
To run the code you should get to the src directory in CP, to do that from terminal navigate to the folder of the project. Then execute:<br>
<code> cd CP/src/ </code> <br>
To run all instances with the main solver (chuffed) withot rotation use: <br>
<code> python cp.py </code> <br>
Add tag <code>-r</code> to use the main solution with rotation.  <br>
<code> python cp.py -r</code><br>
To run one instance use <code>-i</code> and then the number:<br>
<code> python cp.py -i 12</code><br>
You can choose to use gecode with tag <code> -g </code><br>
If you want your execution to draw the solution use tag <code> -d</code><br>
If you want you can choose a search strategy. The alternatives are: <br>
* 1 input\_order indomain\_min
* 2 first\_fail indomain\_min
* 3 first\_fail indomain\_random 
* 4 dom\_w\_deg indomain\_random
* 5 (sorted by area) indomain\_order) <br>
The default selection is 5.<br>
Example:
<code> python cp.py -s 2</code>
You can choose restart. The oprions are:
* 1 restart_linear(100)
* 2 restart_luby(100)
* 3 restart_none <br><br>
The default is 2.<br>
Use flag <code> -all </code> to run all searches consequently.

