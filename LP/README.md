## VLSI with CP
To run the code you should get to the src directory in LP, to do that from terminal navigate to the folder of the project. Then execute:<br>
<code> cd LP/src/ </code> <br>
To run all instances with the main solver (GUROBI_CMD) withot rotation use: <br>
<code> python lp.py </code> <br>
Add tag <code>-r</code> to use the main solution with rotation.  <br>
<code> python lp.py -r</code><br>
To run one instance use <code>-i</code> and then the number:<br>
<code> python lp.py -i 12</code><br>
You can choose to use PULP_CBC_CMD with tag <code> -p </code><br>
If you want your execution to draw the solution use tag <code> -d</code><br>
Use flag <code> -all </code> to run all searches consequently for no trotation.
Example:<br>
<code> python cp.py -all</code><br>
Or with rotation:<br>
<code> python cp.py -all -r</code><br>
