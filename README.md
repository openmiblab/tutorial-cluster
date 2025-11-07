# Running jobs on the HPC in Sheffield: a tutorial

## 📚 Aim

This repository has a dual aim: 

- It forms a template structure for miblab processing pipelines.
- It forms a tutorial with a dummy job showing how to run jobs on the cluster.

See also the University's [documentation](https://docs.hpc.shef.ac.uk/) on the HPC (High Performance Computer), or *cluster*, for short.


## 🛠️Structure 

Any pipeline will ultimately read data from a specific location, and write output elsewhere. Generally the data will live on a separate read-only folder somewhere in the file system, and the results will be written out in another folder. 

To mimick this process, this tutorial has three top-level folders. In reality these may exist at three different locations in the file system:

- **data**: source data. This is a read-only folder.
- **code**: This contains the actual pipeline code including any functionality needed to run on the cluster. 
- **build**: this is where all the output appears. The folder is created by the scripts if it does not yet exist.

It's best to keep those three folders completely separate as they will be used differently. The **data** folder may be quite big, and copying it over to the cluster may take a long time, so it's usually not done all too often. The **code** may change more frequently, e.g. if new features are added, versions increased, bugs fixed etc. It's also small in size so this will typically be copied to the cluster more frequently. The **build** folder is most dynamic as it is modified or recreated every time a script is run. 

The **code** folder has the following files:

- **environment.yml**: This lists the necessary software that is available through conda.
- **requirements.txt**: This lists python packages not available on conda, and any editable installations.

The **code** folder has the following directories:

- **src**: python source code. The top level contains standalone main scripts. Any number of subfolders can be used to store helper functions and reusable utility that is used in multiple scripts.
- **hpc**: folder with top-level unix scripts used to send jobs to the cluster.
- **logs**: folder where the HPC will deposit logs of the computations.

## 💻 Usage

Typically pipelines are developed and tested locally with data either on a local hard drive or the shared data storage, and subsequently submitted as a batch job on the HPC. Testing, debugging and editing on the cluster is possible but difficult as no user friendly development environments like VSCode are available. So it's best to first develop and test a script locally before running it on the cluster. We will do this using a conda environment so code and installation is tested locally under similar conditions as it will run on the cluster. 

The following tutorial shows the whole process using a simple script which reads the content of data/test.txt, attaches a counter and save the results in /build. It does this 11 times creating new files numbered 0 to 10. It also exports dmr files so you can test the usage of packages that are not on conda. 

In order to run the tutorial, first clone this repository. We will assumed it is cloned at:

*C:\Users\USERNAME\Documents\GitHub\tutorial-cluster*

<mark>Throughout this tutorial, replace *USERNAME* by your sheffield USERNAME.</mark> If you clone the repository on a different location, make sure to changes the paths accordingly.

We also assume you already have python and conda installed. Other tools such as VSCode are optional as the tutorial can be run from a console.


## Run the script locally

To make things easier to read we'll first define a path variable that we can reuse throughout - <mark>please make sure to adapt the paths before running this</mark>:

```bash
$LOCAL_DIR = "C:\Users\USERNAME\Documents\GitHub\tutorial-cluster"
```

The first step is to create the virtual environment which contains the software needed to run the script. On your laptop or personal computer, open a terminal (e.g in VScode, or Windows Powershell) and do the following steps.

Create a virtual environment named *tutorial-cluster*, installing the software listed in the *environment.yml* file:

```bash
conda env create -n tutorial-cluster -f $LOCAL_DIR/code/environment.yml
```

Activate the environment:

```bash
conda activate tutorial-cluster
```

Run the top level script locally; tell it where the data are and where you want the results to go:

```bash
python $LOCAL_DIR/code/src/all_jobs.py --data=$LOCAL_DIR/data --build=$LOCAL_DIR/build
```

This should create the /build folder with 11 edited text files, and 11 dmr files.

The repository also contains a second script which can be called with a `--num` argument. Running this will produce a single file rather than all of them at the same time. To try it, remove the build folder 

```bash
rm -r $LOCAL_DIR/build
```

and run the `one_job` script:

```bash
python $LOCAL_DIR/code/src/one_job.py --num=5 --data=$LOCAL_DIR/data --build=$LOCAL_DIR/build
```

This has now only created results for iteration 5. The `one_job.py` script is included as script of this type is needed to send multiple jobs to the HPC at the same time. This is typically used to run identical analyses on multiple subjects, where each subject is a separate job.


## Run the script as a job on the HPC

Once it is all running as intended locally, we can run the script on the HPC. To start, delete the local build folder again:

```bash
rm -r $LOCAL_DIR/build
```

In these next steps we will copy code and data over to the cluster, run the script on the cluster, and copy results back to the local drive. 

We'll start by defining a path variable pointing to the location on the cluster where this needs to go:

```bash
$REMOTE_DIR = "/mnt/parscratch/users/USERNAME"
```

Copy the tutorial to the cluster:

```bash
scp -r $LOCAL_DIR USERNAME@stanage.shef.ac.uk:$REMOTE_DIR
```

Log in to the HPC:

```bash
ssh -X USERNAME@stanage.shef.ac.uk
```

Define a local variable again (note we are in UNIX now so slightly different syntax):

```bash
REMOTE_DIR="/mnt/parscratch/users/USERNAME/tutorial-cluster"
```

Load the latest Anaconda module:

```bash
module load Anaconda3/2024.02-1
```

Create an environment in the same way as before:

```bash
conda env create -n tutorial-cluster -f $REMOTE_DIR/code/environment.yml
```

We are almost ready to submit the job, but first we clean the file to be safe. This is often necessary if the file has been edited in a windows editor:

```bash
dos2unix $REMOTE_DIR/code/hpc/all_jobs.sh
```

Now we can submit the job:

```bash
sbatch $REMOTE_DIR/code/hpc/all_jobs.sh
```

You should get a message that the batch job is submitted, which will include a number (job ID) that identifies the job:

```bash
Submitted batch job 8469461
```

If everything has gone OK you should now see the build folder with all the expected output. This should be almost instant. You can check by listing the contents of the folder:

```bash
ls $REMOTE_DIR/build
```

After that you can pull results back to your local drive. Exit the cluster:

```bash
exit
```

Define paths:

```bash
$LOCAL_DIR="C:\Users\USERNAME\Documents\GitHub\tutorial-cluster"
$REMOTE_DIR="/mnt/parscratch/users/USERNAME/tutorial-cluster"
```

And copy the results from the cluster:

```bash
scp -r USERNAME@stanage.shef.ac.uk:$REMOTE_DIR/build $LOCAL_DIR\build
```

After this the results should be in your local build folder.

## Appendix 1: Cleaning up

The data from your tutorial, as well as the environment, are still on the cluster. You can leave them there, but if you don't need them any more you may want to clean up.

Log in to the cluster again:

```bash
ssh -X USERNAME@stanage.shef.ac.uk
```

Delete the data:

```bash
rm -rf /mnt/parscratch/users/USERNAME/tutorial-cluster
```

And remove the environment:

```bash
conda env remove --name tutorial-cluster
```

## Appendix 2: Troubleshooting batch jobs

You can check the status of running jobs like this

```bash
squeue -u $USER
```

To check status of a specific completed job, use the job ID (8469461 in this case):

```bash
sacct -j 8469461
```

If the script has failed, you can syntax-check it before running it:

```bash
bash -n $REMOTE_DIR/code/hpc/all_jobs.sh
```

And you can also run it in debug mode on the login node:

```bash
bash -x $REMOTE_DIR/code/hpc/all_jobs.sh
```

This generates a detailed log in the terminal. This is handy if the script has not even run, which may happen for instance if your paths to data or code are incorrect. If the script has failed after running, you can get detailed error messages by inspecting the files in the `code/logs` folder.

## Appendix 3: Copying large amounts of data

We have previously copied the data using `scp`, but this has limited functionality. For instance, if a large amount of data is transferred, and the transfer is interrupted at some point in the middle (e.g. because you are using wifi), then you do not want to start over. In this case you want to copy only the data that have not yet been transferred over. 

This type of functionality is available through `sync` but this is a Linux program, so you need to install a Linux emulator `WSL` first (Windows Subsystem for Linux):

```bash
wsl --install
```

After installing WSL you can install `rsync` in a Linux console:

```bash
sudo apt update
sudo apt install rsync
```

Then you can use it to copy files. Effectively it will synch two directories so it will only copy files that are not yet there:

```bash
rsync -av --progress "$LOCAL_DIR/" "$REMOTE_DIR/"
```

If it was interrupted for some reason you can just run it again and it will continue.

`rsync` has other features to improve stability and avoid interruptions. This command will resume partially transferred data (rather than delete and start over), copy in place for speed and try 5 minutes before giving up:

```bash
rsync -av --progress --partial --inplace --timeout=300 -e "ssh -o TCPKeepAlive=yes -o ServerAliveInterval=60" "$LOCAL_DIR/" "$REMOTE_DIR/"
```

You can also do a dry run to check if the transfer is complete without actually copying anything:

```bash
rsync -av --dry-run --itemize-changes "$LOCAL_DIR/" "$REMOTE_DIR/"
```


## 👥 Contributors

If you have suggestions for improving this tutorial, please submit an issue.

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

