# Running jobs on the HPC in Sheffield: a tutorial

## 📚 Aim

This repository has a dual aim: 

- It forms a template for miblab repositories with processing pipelines.
- It forms a tutorial with a dummy job showing how to run jobs on the cluster.

See also the University's [documentation](https://docs.hpc.shef.ac.uk/) on the HPC (High Performance Computer), or *cluster*, for short.


## 🛠️Structure 

Any pipeline will ultimately read data from a specific location, and write output elsewhere. Generally the data will live on a separate read-only folder somewhere in the file system, and the results will be written out in another folder. 

To mimick this process, this tutorial has three top-level folders. In reality these may exist at three different locations in the file system:

- **code**: This contains the actual pipeline code including any functionality needed to run on the cluster. 
- **data**: source data. This is a read-only folder.
- **build**: this is where all the output appears. The folder is created by the scripts if it does not yet exist.

The **code** folder has the following files:

- **environment.yml**: This lists the necessary software that is available through conda.
- **requirements.txt**: This lists python packages not available on conda, and any editable installations.

The **code** folder has the following directories:

- **src**: python source code. The top level contains standalone main scripts. Any number of subfolders can be used to store helper functions and reusable utility that is used in multiple scripts.
- **hpc**: folder with top-level unix scripts used to send jobs to the cluster.
- **logs**: folder where the HPC will deposit logs of the computations.

## 💻 Usage

Typically pipelines are developed and tested locally with data either on a local hard drive or the shared data storage, and subsequently submitted as a batch job on the HPC. 

The following tutorial shows the steps using a simple script which reads the content of data/test.txt, attaches a counter and save the results in /build. It does this 11 times creating new files numbered 0 to 10. It also exports dmr files so you can test the usage of packages that are not on conda. 

In order to run the tutorial, first clone this repository. We will assumed it is cloned at:

*C:\Users\USERNAME\Documents\GitHub\tutorial-cluster*

<mark>Throughout this tutorial, replace *USERNAME* by your sheffield username.</mark>

We also assume you already have python and conda installed. Other tools such as VSCode are optional as the tutorial can be run from a console.


## Run the script locally

Testing, debugging and editing on the cluster is possible but difficult as no user friendly development environments like VSCode are available. 

So it's best to first test a script locally before running it on the cluster. We will do this using a conda environment so the process is exactly the same as on the cluster, and all steps can be tested including installation.

The first step is to create the virtual environment which contains the software needed to run the script. On your laptop or personal computer, open a terminal (e.g in VScode, or Windows Powershell) and do the following:

Navigate to the folder with the code:

```bash
cd C:\Users\USERNAME\Documents\GitHub\tutorial-cluster\code
```

Create a virtual environment:

```bash
conda env create -n tutorial-cluster -f environment.yml
```

Once you have a virtual environment you can check if the code runs locally on your laptop or personal computer.

First activate the venv.

```bash
conda activate tutorial-cluster
```

Run the top level script locally:

```bash
python src/all_jobs.py --data=C:\Users\USERNAME\Documents\GitHub\tutorial-cluster\data --build=C:\Users\USERNAME\Documents\GitHub\tutorial-cluster\build
```

This should create the /build folder with 11 edited text files, and 11 dmr files.

The repository also contains a second script which can be called with a --num argument. Running this will produce a single file rather than all of them at the same time. To try it, delete the build folder and run this:

```bash
python src/one_job.py --num=5 --data=C:\Users\USERNAME\Documents\GitHub\tutorial-cluster\data --build=C:\Users\USERNAME\Documents\GitHub\tutorial-cluster\build
```

This has now only created results for iteration 5. 

The one_job.py script is included as script of this type is needed to send multiple jobs to the HPC at the same time. This is typically used to run identical analyses on multiple subjects, where each subject is a separate job.


## Run the script as a job on the HPC

Once it is all running as intended locally, we can run the script on the HPC. 

To start, delete the build folders and unnecessary folders such as .git. This means less data need to be copied over. 

Second, edit the last line of the hpc scripts `all_jobs.sh` and `series_of_jobs.sh` to make sure they are pointing to the paths on the HPC where you will be storing the data. In this case you will just have to replace USERNAME with your user name:

```bash
srun python code/src/all_jobs.py --data=/mnt/parscratch/users/USERNAME/tutorial-cluster/data --build=/mnt/parscratch/users/USERNAME/tutorial-cluster/build
```

Now we can copy the code and any data to these paths on the HPC. Since they are all in the same folder it can be done in a single step:

```bash
scp -r C:\Users\USERNAME\Documents\GitHub\tutorial-cluster USERNAME@stanage.shef.ac.uk:/mnt/parscratch/users/USERNAME/tutorial-cluster
```

Now that everything is copied over you can log in to the HPC to set things up and run the script:

```bash
ssh -X USERNAME@stanage.shef.ac.uk
```

Navigate to the folder and check everything is there:

```bash
cd /mnt/parscratch/users/USERNAME/tutorial-cluster/code
```

You should see a list of all the files and subfolders (`ls`). 

Load the latest Anaconda module:

```bash
module load Anaconda3/2024.02-1
```

Create an environment in the same way as before:

```bash
conda env create -n tutorial-cluster -f environment.yml
```

Now you can submit the job like this:

```bash
sbatch hpc/all_jobs.sh
```

You should get a message that the batch job is submitted, which will include a number that identifies the job:

```bash
Submitted batch job 8469461
```

If everything has gone OK you should now see the build folder appearing with all the expected output. This should be almost instant. 

After that you can pull results back to your local drive. Exit the cluster and do:

```bash
scp -r USERNAME@stanage.shef.ac.uk:/mnt/parscratch/users/USERNAME/tutorial-cluster/build C:\Users\USERNAME\Documents\GitHub\tutorial-cluster\build
```

## Trouble shooting batch jobs on the HPC

If you have edited your `all_jobs.sh` with a windows editor you will likely get an error with UNIX line breaks. To fix this, clean your file before running it:

```bash
dos2unix hpc/all_jobs.sh
```

You can check the status of running jobs like this

```bash
squeue -u $USER
```

To check status of a specific completed job:

```bash
sacct -j 8469461
```

If the script has failed, you can syntax-check it before running it:

```bash
bash -n hpc/all_jobs.sh
```

And you can also run it in debug mode on the login node:

```bash
bash -x hpc/all_jobs.sh
```

This generates a detailed log in the terminal. 


## 👥 Contributors

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tbody>
    <tr>
      <td align="center" valign="top" width="14.28%"><a href="https://github.com/plaresmedima"><img src="https://avatars.githubusercontent.com/u/6051075?v=4" width="100px;" alt="Steven Sourbron"/><br /><sub><b>Steven Sourbron</b></sub></a><br /></td>
    </tr>
  </tbody>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

