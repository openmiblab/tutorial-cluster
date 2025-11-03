# Tutorial and template for running jobs on the HPC in Sheffield

## 📚 Aim

This repository has a dual aim: 

- It forms a template for miblab repositories with processing pipelines.
- It forms a tutorial with a dummy job showing how to run jobs on the cluster.

## 🛠️Structure 

A pipeline repository in miblab has the following subfolders:

- **data**: source data. This is a read-only folder
- **build**: this is where all the output appears. The folder is created 
  by the scripts if it does not yet exist.
- **hpc**: folder with top-level unix scripts used to send jobs to the cluster.
- **logs**: folder where the HPC will deposit logs of the computations.
- **src**: folder with python source code. The top level contains 
  standalone main scripts that can be run on themselves or called from 
  the batch scripts in /hpc. Any number of subfolders can be used to 
  store helper functions and reusable utility that is used in multiple 
  scripts.
- **venv**: a virtual environment created when the code is executed.

The top level contains a file with the python requirements, as well
as the license (always Apache 2.0 in miblab) and this README.

## 💻 Usage

Typically pipelines are developed and tested locally with data either 
on a local hard drive or the shared data storage, and subsequently 
submitted as a batch job on the HPC. 

The following tutorial shows the steps using a simple script which reads 
the content of data/test.txt, attaches a counter and save the results 
in /build. It does this 11 times creating new files numbered 0 to 10.

In order to run the tutorial, first clone this repository. We will 
assumed it is cloned at *X:\abdominal_imaging\Shared\tutorial-cluster*.

### Step 1: create a virtual environment

The first step in that process is to create the virtual environment 
which contains the software needed to run the script. 

Open a terminal (e.g in VScode, or Windows Powershell) and do the 
following:

Navigate to the folder:

```bash
cd X:\abdominal_imaging\Shared\tutorial-cluster
```

Create a virtual environment (Note this can take a long time):

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
locally:

If you are starting a new session and the venv is not activated, then activate it first:

```bash
conda activate ./venv
```

Run the top level script locally:

```bash
python src/all_jobs.py
```

This should create the /build folder with 11 edited text files. 
The repository also contains a second script which can be 
call with a --num argument. Running this will produce a single file 
rather than all of them at the same time. To try it, delete the build 
folder and run this:

```bash
python src/one_job.py --num=5
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
cd /shared/abdominal_imaging/Shared/tutorial-cluster
```

Load conda:

```bash
module load Anaconda3/2019.07
```

activate the venv (note different command from windows):

```bash
source activate venv
```

Mow you can run the scripts as before:

```bash
python src/all_jobs.py
```
or:

```bash
python src/one_job.py --num=5
```


### Step 4: run the script as a job on the HPC

In order to run the job on the cluster, first make sure the batch 
files like hpc/all_jobs.sh are correctly configured. For instance 
you want to make sure status updates are sent to your email, that 
you request reasonable resources, etc.

Unfortunately the compute node on the HPC cannot access the shared 
drive directly (unlike the login node which is used for interactive 
computations). Therefore the first step is to copy the repository 
including any data to a dedicated storage on the HPC.

Log in to the HPC using your USERNAME:

```bash
ssh -X USERNAME@stanage.shef.ac.uk
```

Copy the repository to a scratch folder in your user folder. Make sure 
to substitute USERNAME by your user name:

```bash
cp -r /shared/abdominal_imaging/Shared/tutorial-cluster/ /mnt/parscratch/users/USERNAME/tutorial-cluster
```

When this is done, navigate the new folder and check everything is there:

```bash
cd -r /mnt/parscratch/users/USERNAME/tutorial-cluster
```

You should see a list of all the subfolders (`ls`). Now you can 
submit the job like this:

```bash
sbatch hpc/all_jobs.sh
```

You should get a message that the batch job is submitted, which will 
include a number that identifies the job:

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
bash -n hpc/all_jobs.sh
```

And you can run the script locally with tracing to see what would happen (safe test)

```bash
bash -x hpc/all_jobs.sh
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

