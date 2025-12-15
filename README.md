# ====== PROJECT S.P.M INSTRUCTIONS ======

Authors: 
Basuil, Jesus Lorenzo C.
Esler, Rafiq Reos M.
Quiel, Cedric Nichole


Below are some straightforward guidelines on how to execute "Project S.P.M" on your local device in order to run the application

# ===== Files and Folders =====

There are 2 ways to run the program: 
An .exe file !! (RECOMMENDED) !!
Directly as Python Code 

For the sake of project checking and / or end user consumption, please run the program's .exe file

The .exe file can be found within the folder called 'dist'. Access the folder to find the .exe file, then double click it and wait for the program to initialize

<img width="703" height="173" alt="image" src="https://github.com/user-attachments/assets/83a4c5d5-0b8b-444b-8532-ffe96bd862ea" />

The project also contains various files and folders. DO NOT DELETE OR TAMPER WITH THEM. Specifically:
⦁	__pycache__
⦁	build
⦁	.gitignore
⦁	Project-SPM.spec
⦁	tempCodeRunnerFile.py


# ======= Execution Procedure ======= 

Upon running the program for the first time, you will be greeted by a window interface. This interface has a button to upload a csv file. 

<img width="1914" height="537" alt="image" src="https://github.com/user-attachments/assets/1f59ad5d-58fb-493a-a637-6330ffbd21f5" />

Click the button and select any valid csv file. You can use the provided csv files found within the folder called "Sniper_Recruit_Data".

Double click on your desired csv. Once done, wait for the application to process, and you will be greeted by a dashboard window . 

<img width="1197" height="745" alt="image" src="https://github.com/user-attachments/assets/4cfc2812-add7-42c8-a904-caf9b574c8fb" />


The dashboard window is divided into two parts: 

LEFT PANEL: The left panel displays the accuracy data. The panel with the accuracy readings and error readings are a scrollable element. Feel free to scroll through them as you please.

RIGHT PANEL: The right panel displays the graph of mark distances with respect to round numbers. You can also view the round predictions (1-3 rounds advance), by pressing the arrow keys beside the text "Round X Prediction" where x   is the current round prediction. For manipulation of accuracy, you can also adjust the data points at the very bottom, similar to how you would do for the round prediction adjustment.


# ======= Interpretation of Results =======

RELATIVE ERROR: 
<ul>
  <li>All accuracy rates are calculated via: (1-relative error) * 100, to be displayed in percentage form.</li>
  <li>Any percentage that might be negative (due to some issues in calculations of error) can be interpreted as '0%', as the shot did not hit the target at all</li>
</ul>

<img width="418" height="178" alt="image" src="https://github.com/user-attachments/assets/60bd2a8c-6996-44eb-92cc-d1962ef1177a" />


POLYNOMIAL LAGRANGE EXTRAPOLATON: 
<ul>
  <li>The ideal mark distance (distance from edge of target to target center) is 5. The larger the mark distance, the more accurate the shot is.</li>
  <li>Mark distances that are (somehow) going to be greater than 5 are dealt with in the following manner: (10- mark distance). Which just means it's going to be measured from the opposite side. This is due to the wild and non-linear behavior of the dataset.</li>
  <li>Should you wish to verify the Lagrange Calculations yourself, you may run "ExtrapolationAndError.py" and enter the values for the no. of data points, and Y values.</li>
  <li>The X values are present as 1,2,3,4,5. Again, this is due to the non-linear nature of the dataset.</li>
</ul>


<img width="836" height="189" alt="image" src="https://github.com/user-attachments/assets/627899af-732d-46cd-bff6-8be16a387a01" />

