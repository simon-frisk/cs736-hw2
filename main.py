import itertools
import subprocess
import json


def main():
    jobFile = "jobFileCreate.fio"
    createJobFile(jobFile)
    json = runJobs(jobFile)


def createJobFile(fileName):
    with open(fileName, 'w') as file:
        file.write("[global]\nioengine=psync\nbs=4k\nsize=1G\nruntime=30s\ntime_based\ndirect=1\nioscheduler=mq-deadline\n\n")

        drivers=['/dev/nullb0','/dev/rnullb0']
        xDim = ['read', 'write', 'randread', 'randwrite']
        blockSizes = ['4k', '8k', '16k', '32k', '64k', '128k']
        numJobs = ['1', '2', '3', '4']
        
        for (mode, blockSize, jobs, driver) in itertools.product(xDim, blockSizes, numJobs, drivers):
            file.write(f"[{driver}-{mode}-{blockSize}-{jobs}]\n")
            file.write(f"filename={driver}\n")
            file.write(f"readwrite={mode}\n")
            file.write(f"numjobs={jobs}\n")
            file.write(f"bs={blockSize}\n")
            file.write("group_reporting\n")
            file.write("stonewall\n")
            file.write(f"\n")


def runJobs(jobFile):
    print("Running jobs")
    result = subprocess.run(['sudo', 'fio', jobFile, "--output-format=json", "--output=output.json"], capture_output=True, text=True)
    return result.stdout


if __name__ == '__main__':
    main()  