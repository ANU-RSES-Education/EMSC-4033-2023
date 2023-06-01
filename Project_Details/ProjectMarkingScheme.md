## Project Marking

For your projects we expect you to upload all your code and/or notebooks to the repository. 

Depending on the nature of the project you selected to do, it may make sense that you gather lots 
of functions and/or class definitions in a python module and then have some notebooks that demonstrate
your project's functionality to the **typical user**.

The comments in the code and the notebooks should not be addressed to the lecturers (as if you are
commenting on the assessment). Instead, the code and notebooks should be kept in the form like you are
addressing a **typical user**.

Along with your code and notebooks, we will also expect you to upload the "Project Report" in the form
of a markdown file `ProjectReport.md`. In the report you could include comments towards the class 
lecturers, e.g., discuss why functionality X was hard or impossible to implement and therefore you
chose a different approach using module `blahblah` that included functionality Y. You may even 
include figures.

In summary, for your projects we expect you to upload to your repository the following items:

- Project Plan
  
  We partially did that together, but we will be expecting it to be filled up completely and updated to reflect the project you ended up doing.
  
- Project Jupyter Notebook(s) & Code
  
  You have a chance to explain the structure of your code in the presentation and in the report. The presentations provided an opportunity for the lecturers to get a first taste of your project and give you feedback. This feedback is hopefully helpful for you in preparing the final report.

- Project Report (markdown file).



| Task | Assessment | Mark percentage %|
|:-------------- |:-----------:|:-----:|
| Project Plan                                   | - |  15 |
|                    | Clarity of Exec Summary          | A | 
|                    | Clarity of Requirements          | A | 
|                    | Clarity of Timeline              | A | 
|                    | Review of Existing codes         | A | 
|                    | Testing Plan                     | A | 
| Jupyter Notebook(s) (& Code)                   | - |  55 |
|                    | Does it run ?                    | Y |
|                    | Is it easy/obvious to use ?      | A |
|                    | Clear Coding Style               | A |
|                    | Tests / coverage (100%/50% ?)    | A |
|                    | Match to objectives              | A |
|                    | Use of modules / widgets to keep code clean | A  |
|                    | Exception handling ?             | A |
| Project Report  (additional notebooks)         | - |  20 |
|                    | Instructions                     | A |
|                    | List of dependencies             | A |
|                    | Describe testing                 | A |
|                    | Limitations / Future Improvments | A |
| Project Repository | - |  10 |
|                    | README                           | A |
|                    | License                          | Y |
|                    | Tagged Release                   | Y |
|                                       | TOTAL      | 100 |


### Marking Scheme Explained

| Mark     |   What you need to do   |  Value  |
|:--:      |:---                     |:--:     |
| A        |   A complete answer, hitting all relevant points, not necessarily perfect | 100% |
| B        |   A strong answer that may miss a few things here and there               | 75 % |
| C        |   OK but not complete or missing the point at times, not misleading or wrong | 50 % |
| F        |   Incomplete or wrong                                                        | 0%   | 


### Project Submission

We would like everything to be pushed up in the Github repository by Friday, June 3rd, 11:59pm.

During the presentations (Wednesday, June 9th, 2pm-5pm) we will guide you make a tagged release of your project's code.


### Expected Github Repository structure

```
.
├── README.md               # Basic info for the repo that shows up in the landing page
├── LICENSE                 # The project's license
├── .gitinore
├── code                    # Code developed for the project
│   ├── assets
│   │   ├── data.nc
│   │   ├── image.png
│   │   └── ...
│   ├── packageA.py
│   ├── packageB.py
│   └── ...
├── notebooks               # Jupyter notebooks demonstrating the project's functionality
│   ├── assets
│   │   ├── data.nc
│   │   ├── image.png
│   │   └── ...
│   ├── notebookA.ipynb
│   ├── notebookB.ipynb
│   └── ...
├── project
│   ├── ProjectPlan.md      # The project plan
│   └── ProjectReport.md    # The project report
└── ...

```
