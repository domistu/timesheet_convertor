# timesheet_convertor
Converts CSV to the wanted format.


All files included in the folder should remain for the program to function properly.

venv folder
.gitignore
README.md (so there are instructions)
run_convertor.bat (to run the program easily)

There are two files that may be located. The first is the exported csv file: Work Session.csv. 
This file will always export to that name, so every Monday or whenever this file is exported from the 
website: https://phillipstown-my.sharepoint.com/personal/dominic_phillipstown_org_nz/Lists/Work%20Session/AllItems.aspx
it will come out as: Work Session.csv

With this file, you will move it to the folder containing the program and is named "timesheet_convertor". 
From here, it is as simple as double clicking the "run_convertor.bat" file. This will create a new csv that is 
formated and has the appropriate totals calculated. The name will show up as "Timesheet_week_of_YYYY-MM-DD"

The format for the csv is the following for one user. 

___________________________________________________________________________________
Timesheet		03/10/2022 to 09/10/2022						
								
Name	         Star Time	        Finish Time   	  Break	    Total Time	         Project	      Sick	  Annual	  Public Holiday

USER_EMAIL  
DATE: DD/MM/YYYY
Ada Lovelace	6/10/2022 18:06	    6/10/2022 23:59	    1.5	    4.383333333	      Working Bee	       N/A	   N/A	        No
Total Sick (Paid)	Total Sick (Unpaid)	Total Annual (Paid)	Total Annual (Unpaid)	Total Public Holiday	Total pay per hour (STD)
0	                        0         	           0	              0	                      0	                  4.383333333		

DATE: DD/MM/YYYY
Ada Lovelace	7/10/2022 18:06	    7/10/2022 23:59	    1.5	    4.383333333	      Working Bee	       N/A	   N/A	        No
Total Sick (Paid)	Total Sick (Unpaid)	Total Annual (Paid)	Total Annual (Unpaid)	Total Public Holiday	Total pay per hour (STD)
0	                        0         	           0	              0	                      0	                  4.383333333		

