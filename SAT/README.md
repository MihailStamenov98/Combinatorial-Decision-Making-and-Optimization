## VLSI with SAT
To run the code you should get to the src directory in LP, to do that from terminal navigate to the folder of the project. Then execute:<br>
<code> cd SAT/src/ </code> <br>
To run all instances with the main solver (GUROBI_CMD) withot rotation use: <br>
<code> python sat.py </code> <br>
Add tag <code>-r</code> to use the main solution with rotation.  <br>
<code> python sat.py -r</code><br>
To run one instance use <code>-i</code> and then the number:<br>
<code> python sat.py -i 12</code><br>
You can choose to the encoding of the constraints with tag <code> -e </code><br>
The alternatives are:<br>
* 1-pairwise
* 2-sequential
* 3-bitwise
* 4-heule <br>
The default one is 1.
Example:<br>
<code> python sat.py -e</code><br>
If you want your execution to draw the solution use tag <code> -d</code><br>
Use flag <code> -all </code> to run all encodings consequently for no trotation.
Example:<br>
<code> python sat.py -all</code><br>
Or with rotation:<br>
<code> python sat.py -all -r</code><br>
