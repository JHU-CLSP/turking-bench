# Web-Grounded Natural Language Instructions
<hr>


This repository maintains a large collection of tasks and their natural language instructions that are grounded in the visual information. 

Here are two example tasks:
![Screen Shot 2023-02-20 at 12 21 22 PM](https://user-images.githubusercontent.com/2441454/220168815-10c22ddd-2deb-422f-b41e-2203bee25e25.png)

**Where can I see more tasks?**
You can see the instructions for each task [here](mturk.html). 
Note, in this visualization, the variables are not filled in with any variables. 
During the evaluation, the variables are filled in with the input instances. 
We have prepared the necessary scripts for simulating the interaction with the templates (see below).


Background 
--- 

**Why define tasks in natural language?** While the current dominant paradigm (supervised learning with task-specific labeled examples) has been 
successful in building task-specific models, such models can't generalize to unseen tasks; for example, a model that is supervised to solve questions 
cannot solve a classification task. We hypothesize that a model equipped with understanding and reasoning with natural language instructions should be able to generalize to any task that can be defined in terms of natural language.

**How is it tied to the past work?** 
Most of the past work focus on raw-text task instructions. Here the instructions are multi-modal 
and grounded in the visual information. 


**Why collect this data?** 
We have collected about XX tasks that were originally created for crowdworkers. 
Each task comes with an HTML template `template.html` that contains the visual information and a natural language instruction.
Additionally the templates contain variables to be filled in by input instances maintained in `batch.csv` files.



Task schema  
--- 
TODO

How to contribute 
---
TODO

License
--- 
This work is licensed under Apache License 2.0.


Evaluation and Baselines 
--- 
To facilitate the evaluation of models on this data, we have included the scripts needed to simulate interaction with the templates. 
The scripts are in `scripts/` directory.
Here are the steps you need to follow: 
 1. Install the dependencies: `pip install -r requirements.txt`
 2. Create a server for visualizing the tasks `./scripts/run_server.sh` This will create a clone oof Turkle server at `http://localhost:8000` which we will use for visualizing the tasks. This will also ask you for a one-time username and password.  
 3. Run the script for copying the tasks to the server `python upload_tasks.py -u <username> -p <password> -t <task_name> -d <task_dir>`. 
 4. Go the website `http://localhost:8000`, click on a task, copy its frame URL. 
 5. Run the script for evaluating the baseline by passing in the names of the tasks: `python evaluation.py --tasks <task_names>`


![Screen Shot 2023-02-20 at 12 22 37 PM](https://user-images.githubusercontent.com/2441454/220168960-9080b552-446b-4385-bca3-7f662ce95e20.png)



Citation 
If you fnd this data useful, please cite this repository. 

<!-- 
Publication 
--- 
Feel free to cite us.  -->
