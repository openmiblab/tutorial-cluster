# Tutorial and template for running jobs on the HPC in Sheffield

## 📚 Aim

This repository has a dual aim: 

- It forms a template for miblab repositories with processing pipelines.
- It forms a tutorial with a dummy job showing how to run jobs on the cluster.

## 🛠️Structure 

Any pipeline will ultimately read data from a specific location, and 
write output elsewhere. Generally the data will live on a separate 
read-only folder somewhere in the file system, and the results will be 
written out in another folder. To mimick this process, this tutorial 
has three top-level folders. In reality these may exist at three 
different locations in the file system:

- **data**: source data. This is a read-only folder.
- **build**: this is where all the output appears. The folder is created 
  by the scripts if it does not yet exist.
- **code**: This contains the actual pipeline code including any 
  functionality needed to run on the cluster. 

The **code** folder has a file withe python requirements and the 
following subfolders:

- **venv**: a virtual environment with the required software installations.
- **src**: python source code. The top level contains 
  standalone main scripts. Any number of subfolders can be used to 
  store helper functions and reusable utility that is used in multiple 
  scripts.
- **hpc**: folder with top-level unix scripts used to send jobs to the cluster.
- **logs**: folder where the HPC will deposit logs of the computations.

## 💻 Usage

Typically pipelines are developed and tested locally with data either 
on a local hard drive or the shared data storage, and subsequently 
submitted as a batch job on the HPC. 

The following tutorial shows the steps using a simple script which reads 
the content of data/test.txt, attaches a counter and save the results 
in /build. It does this 11 times creating new files numbered 0 to 10.

In order to run the tutorial, first clone this repository. We will 
assumed it is cloned at *X:\abdominal_imaging\Shared\tutorial-cluster*. 
While this can be done on a local hard drive as well, having it on 
shared storage means that the data are visible from the cluster's login 
node, which means computations can be run interactively without 
transferring the data to the cluster. When the computation is submitted 
as a job the data will still need to be copied to the cluster first 
as the compute nodes unfortunately can't access the shared storage.

We also assume you already have python and conda installed. Other tools 
such as VSCode are optional as the tutorial can be run from a console as well.

### Step 1: create a virtual environment

The first step in that process is to create the virtual environment 
which contains the software needed to run the script. 

On your laptop or personal computer, open a terminal (e.g in VScode, 
or Windows Powershell) and do the following:

Navigate to the folder with the code:

```bash
cd X:\abdominal_imaging\Shared\tutorial-cluster\code
```

Create a virtual environment (note this can take a long time on the 
shared storage):

```bash
conda create --prefix ./venv python=3.11
```

When this is done you should see the venv folder appearing. 

Activate it:

```bash
conda activate ./venv
```

and install the requirements:

```bash
pip install -r requirements.txt
```

### Step 2: run the script locally

Once you have a virtual environment you can check if the code runs 
locally on your laptop of personal computer.

If you are starting a new session and the venv is not activated, 
then activate it first:

```bash
conda activate ./venv
```

Run the top level script locally:

```bash
python src/all_jobs.py --data=X:\abdominal_imaging\Shared\tutorial-cluster\data --build=X:\abdominal_imaging\Shared\tutorial-cluster\build
```

This should create the /build folder with 11 edited text files. 
The repository also contains a second script which can be 
call with a --num argument. Running this will produce a single file 
rather than all of them at the same time. To try it, delete the build 
folder and run this:

```bash
python src/one_job.py --num=5 --data=X:\abdominal_imaging\Shared\tutorial-cluster\data --build=X:\abdominal_imaging\Shared\tutorial-cluster\build
```

This has now only created a single file 5. The one_job.py script is 
included as script of this type is needed to send multiple jobs to 
the scanner at the same time. These will then be executed sequentially, 
and results will appear one by one. This is typically used for instance 
to run identical analyses on single subjects, where each subject is a 
separate job.

### Step 3: run the script interactively on the HPC

Once everything is fine locally, you can try running the script 
interactively on the cluster. This is not a good way of running large 
numbers of jobs but helps to test and debug any issues running scripts 
on the cluster.

Log in to the HPC using your USERNAME:

```bash
ssh -X USERNAME@stanage.shef.ac.uk
```

You will be asked to enter a password and DUO code.

Once logged in go to the shared dir:

```bash
cd /shared/abdominal_imaging/Shared/tutorial-cluster/code
```

Load conda:

```bash
module load Anaconda3/2019.07
```

activate the venv (note different command from windows):

```bash
source activate venv
```

Now you can run the scripts as before:

```bash
python src/all_jobs.py --data=/shared/abdominal_imaging/Shared/tutorial-cluster/data --build=/shared/abdominal_imaging/Shared/tutorial-cluster/build
```
or:

```bash
python src/one_job.py --num=5 --data=/shared/abdominal_imaging/Shared/tutorial-cluster/data --build=/shared/abdominal_imaging/Shared/tutorial-cluster/build
```

Note there was no need to copy the data to the cluster, and the results 
appear directly on the share storage. This is because the login nodes 
that run interactive computations can access shared storage directly.

### Step 4: run the script as a job on the HPC

Unfortunately the compute node which runs computations submitted as 
jobs cannot access the shared storage directly. Therefore the first 
step is to copy the code and any data to a dedicated storage on the HPC.

Log in to the HPC using your USERNAME if you haven't already:

```bash
ssh -X USERNAME@stanage.shef.ac.uk
```

Copy the code and data to a scratch folder in your user folder. Make sure 
to substitute USERNAME by your user name:

```bash
cp -r /shared/abdominal_imaging/Shared/tutorial-cluster/ /mnt/parscratch/users/USERNAME/tutorial-cluster
```

When this is done, navigate to the new folder and check everything is there:

```bash
cd /mnt/parscratch/users/USERNAME/tutorial-cluster
```

You should see a list of all the files and subfolders (`ls`). 

In order to run the job on the cluster, first make sure the batch 
files like `all_jobs.sh` are correctly configured. For instance 
you want to make sure status updates are sent to your email, that 
you request reasonable resources, and especially that the last line 
which runs the script is pointing to the correct paths. In this case 
the last line of `all_jobs.sh` should read:

```bash
srun python code/src/all_jobs.py --data=/mnt/parscratch/users/USERNAME/tutorial-cluster/data --build=/mnt/parscratch/users/USERNAME/tutorial-cluster/build
```

Now you can submit the job like this:

```bash
sbatch code/hpc/all_jobs.sh
```

If all is well you should get a message that the 
batch job is submitted, which will include a number that identifies the job:

```bash
Submitted batch job 8469461
```

If everything has gone OK you should now see the build folder appearing 
with all the expected output. This should be very quick for the tutorial 
job. After that you can copy results back to the shared drive:

```bash
cp -r /mnt/parscratch/users/USERNAME/tutorial-cluster/build/ /shared/abdominal_imaging/Shared/tutorial-cluster/build 
```

### Trouble shooting batch jobs

If you have edited your `all_jobs.sh` with a windows editor you will 
likely get an error with UNIX line breaks. To fix this, first clean 
your file:

```bash
dos2unix code/hpc/all_jobs.sh
```

Then try again. 

You can check the status of running jobs like this

```bash
squeue -u $USER
```

To check status of a specific completed job:

```bash
sacct -j 8469461
```

If the job has run you should find a log in /logs folder. If there 
is no log it means the job did not even run, maybe because the 
batch script had errors, data were not found, etc.

You can syntax-check the script before actually running it:

```bash
bash -n code/hpc/all_jobs.sh
```

And you can run the script locally with tracing to see what would happen (safe test)

```bash
bash -x code/hpc/all_jobs.sh
```

This generates a detailed log in the terminal. If you have built your 
script.sh in a windows apps like notepad, a common issue is that windows has included line 
breaks that are invalid in unix. You can clean your script like this:

```bash
dos2unix all_jobs.sh
```


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

