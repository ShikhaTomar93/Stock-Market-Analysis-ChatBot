## Congifuring Oracle XE DB in Python and SQL Developer

Step 1: Install Oracle Database XE from https://www.oracle.com/database/technologies/appdev/xe/quickstart.html

Step 2: Vaigate to the installation folder C:\app\<you-user>\product\21c\dbhomeXE\bin and run sqlplus.exe

Step 3: Execute the below commands for connecting to PDB
<kbd>![image](https://user-images.githubusercontent.com/64169078/144718895-b6849a80-5bb0-4190-910e-da0e21095a06.png)

Step 4: Create user for each developer or on a project level like below:
<kbd>![image](https://user-images.githubusercontent.com/64169078/144719061-6f982819-bf2b-4f6c-b9ce-8290c1129030.png)

See references for cpoying the commands.

Step 5: Configure the Oracle XE DB for the Python project. Cretae a new table, insert data and verify if its retrievable.
<kbd>![image](https://user-images.githubusercontent.com/64169078/144719108-e080a0c4-6897-4783-ae4a-477592591ab7.png)

Step 6: To view DB objects using a GUI, install https://www.oracle.com/tools/downloads/sqldev-downloads.html

Step 7: Configure a new connection with the user that was created in Step 4. 
<kbd>![image](https://user-images.githubusercontent.com/64169078/144719755-42c4e4fe-7d5d-42c5-a07c-cfeaacc64fe3.png)

Step 8: Connect and run SELECT to view the table created in Step 5.
<kbd>![image](https://user-images.githubusercontent.com/64169078/144719809-4f126f20-5def-41bc-a673-d680f314849d.png)

All the commands and code used in the screenshots can be found in the Refrences.

References:
https://www.oracle.com/database/technologies/appdev/python/quickstartpythononprem.html
  
https://www.youtube.com/watch?v=wiEsR_j36yw&ab_channel=Oracle.NETandWindows
