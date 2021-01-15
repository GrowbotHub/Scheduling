# Growbothub Scheduling



This program optimize the number of plants produced by GrowBotHub in function of different parameters as input.

To run the program, run main.py with python3 :

​	**python3 main.py**

For the program to run, you will need to install the Pulp solver, free open source software.

All the file must be in the same directory than main.py:

- classes.py
- edges.py
- graph_construction_and_draw.py
- inputs.py
- optimization.py
- outputs.py
- plants_array.py

The program must read the text file **data.txt** to properly work. The syntax of this file is very specific :

each line should begin by a key word, the data (all indexes begin at 0).

- "TRAYS" then "|" with the number of desired trays (growth modules)

- "HOLES" then "|" with the desired number of holes per tray (growth modules)

- "HORIZON" then "|" with the number of days we have to produce a maximum of plants

- "MAX_SIZE" then "|", this the max distances between pairs of holes to be respected, you should start by the max_size value then ":" with the index of holes such as "0,1", between the pairs use "," and between the differents values of max size ";".

   Example with two max sizes of 15 and 14 : **MAX_SIZE|15:0,1-3,4;14:0,2-1,2-3,2-4,2**

-  "MAX_TIME" then "|" the number of minutes before the time out of optimization. It will only count the actual optimization, the construction of graph and variables might take some time too.

- "PLANT" then "|" to add one type of plant, you must indicate different values separated by "|". First the name, the total days of growth, the color for the graph (b,g,y,purple,orange,c), the sizes : one value for each day separated by ",", the indexes of the trays it should go through separated by "," then the pair of indexes of days it must stay in each trays, the pairs should be separated by ";" and the values in the pairs by ",".

  Example with fictive value of plant of a total days of growth of 5 days :

  **MAX_SIZE|15:0,1-3,4;14:0,2-1,2-3,2-4,2**

Any error in the data will crash the program.



The program returns 2 outputs and draws graphs. First it returns the list of all instructions the robotic arm must do every day in **output.txt**. Then in **output2.txt**, the status of each trays each day : which plant are in it. It will draw the raw graph it has constructed for the optimization in **graph.png** and the optimized one, with the color of the plants, in **optimized.png**.























