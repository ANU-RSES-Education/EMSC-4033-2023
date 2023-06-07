## EMSC4033 - Project Report

### Instructions

The application is based on the following files: 
- User_Application.ipynb : main application notebook/interface; for the user
- Automatic_Wave_Processing.ipynb : same as the user file but with more explanations to make it easier to follow the project flow; not for the user but for people interested in adding to the code and for marking.
- functions.py : main function module; all functions are commented and assigned to a specific "Stage" of the programm
- network_list.py and phases_list.py : function files to help read and use the data form the json files
- network_names.json and phase_parameters.json : input files that introduce important parameters into the system -> can be changed/new items can be added.
- test_file.py : simple test/test run to make sure the programme works as intended.

The programme will create a new file in the same directory. If a user wants to run the programme multiple times, they should delete the existing folder or move it to a different directory.

Please see "process_overview.pdf" for a broad overview of the order of processes and which file is generated when.

### List of dependencies

- **obspy**: a package to acquire, process and visualize seismological data; widely used in the scientific community
- **os**: a package to use operating sytem dependent functionality (e.g., create new folders, determine if files exist in directory,...)
- **IPython**: a package to make python more interactive; included a Jupyter kernel that enbales the user to create interactive input widgets and format output
- **json**: built-in python package that can be used to work with json data
- **pandas**: data analyis and manipulation tool; often used in the scientific community.

*Note* Creation of requirements.txt file was not possible in compute2 environment. However, no specific versions for the above listed packages are required, meaning that all of them can be installed with: 

pip install package_name

Obspy builds the main core of the programm and most if not all functions and processes would not be possible without it. Especially obspy.core is essential as it includes all tools needed to read and analyse the data. 
  
Os is needed to create new folders (for nicer structure) and to check if files already exist or not which is important when working with multiple servers that could potentially provide data. 
  
IPython can be seen as a non-essential feature as it only adds to a nicer interface by clearing long output. If possible extension 2 was realized, IPython would become a very essential feature. In my opinion, this package can add a lot of value to an application in Jupyter Notebooks.
 
Json is used to read the two json files which provide important data to the project. The package is therfore essential but could possibly be replaced if the files were saved in a different format. However, this would add complexity.
  
Pandas is used to create and work with the dataframes created from the json files. This is especially important for displaying the data which is a great help for the user if they are unsure about what input is valid.

  
### Testing

Input validation plays a major role in my project and I was surprised by how complicated and how much work it was to ensure that the user can only progree when entering a valid input. Every time the user was asked to input data, I conducted an input validation. In most cases I worked with "while loops" that would only end if specifc input criteria were met and the input validation variable changed its value. I think this is a very elegant solution as it approaches the problem from the angle "what should it be?" rather than "what can't it be?". Latter would be impossible to address in some cases (e.g. with station names) as there are infinite different options the user could input. I also think that the displayed tables help the user in making a valid choice. This could be further improved by including widgets that limit the user to specific input choices as descrived in extension 2. 
  
 Testing was a bit less straight forward. For most functions there is not another value that results can be compared to, meaning that testing can only be used to test if a function works or raises an exception. This is done by running an example before running the application to test if the data acquisiton and processing are working. 
  
 Exception handling was another big part of my project. As I am dealing with large datasets, and many different stations and events, many different exceptions could occur. It is impossible to test every single possible variation and account for the specific exception which is why I often had to use generalized try and except statements which is not best practice but necessary in this case.


### Limitations

Overall, the code fulfills its aims. However, there are many aspects that could be improved or are limited by the available data: 

**Data Acquistion:**
- Data Availability: My project is only based on three servers. More could be used to ensure a wider cover of stations. 
- Server Connection: Connection to the servers depends on an internet connection. If the connection fails, there is no other way to execute the programme.
- Station data: For some stations, station metadata is missing or seismic records are patchy. This is unforntunately out of my control and the user is responsible of adapting their seach parameters accordingly should they run into a problem.
- So far, the programme is limited to PKJKP and PKIKP. However, new phases can easily be added in the respective json file.

**Data Processing**
- Data processing follows a very basic workflow. More complex processing parameters could be added. Overall, this would improve the application from a scientific point of view but probably would not add to the complexity of this project.
- Visalization: The application could include more visualizations and waveform plots.
- If a folder created in the data processing already exists, the algorithm raises an error. This means that the programme can only run once unless the existing folder is deleted or moved.

**Interface**
- Input cells are on top of the page while ouput cells which often contain instructions are on the bottom. This can be a bit unintuitive.
- The user still has access to some lines of codes which is sub-optimal. This could be improved by hiding cells.



### Future Improvements	

Overall, this code was intended to provide a basis for more complex analyses. It can be easily adapted to more sophisticated purposes. However, it might lose some of its simplicity which makes it easy to use. In my opinion, there are two main ways how the application could be elevated to the next level: 

**Extension 1: More Automatisation**

Here, the main goal would be to enable the user to run the same request multiple times. In the first run, the user would use the Jupyter Notebook as usual but then the input variables would be saved. An additional .py file would then be executed each time the user decides to run the variables again (taking the input from a text file for example). This would be useful for scientists and students who are interested in the observation of one specific phase at a specific station and who are waiting for new events that could improve the dataset. One main advantage of this extension is that it would use a regular python file instead of the Jupyter Notebook which is not the best/most intuitive environment for my application.

**Extension 2: Improved User Interface**

To further rectrict the user and to prevent accidential changes and edits a more sophisticated interface would be helpful. This could be done by use the IPyhton widgets and by hiding cells. Jupyter Notebook is not the best environment for such applications and maybe an implementation in a completely different application and based on a different programming language might be helpful.

