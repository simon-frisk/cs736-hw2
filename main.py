import itertools
import subprocess

def main():
    jobFile = "jobFileCreate.fio"
    createJobFile(jobFile)
    runJobs(jobFile)

def createJobFile(fileName):
    with open(fileName, 'w') as file:
        file.write("[global]\nioengine=psync\nbs=4k\nsize=1G\nruntime=30s\ntime_based\ndirect=1\n")

        drivers=['/dev/nullb0','/dev/rnullb0']
        xDim = ["write", "read"]
        blockSizes = ['4k','8k']
        numJobs = ['1','2']
        
        for (mode, blockSize, jobs, driver) in itertools.product(xDim, blockSizes, numJobs, drivers):
            file.write(f"[{driver}-{mode}-{blockSize}-{jobs}]\n")
            file.write(f"filename={driver}\n")
            file.write(f"readwrite={mode}\n")
            file.write(f"numjobs={jobs}\n")
            file.write(f"bs={blockSize}\n")
            file.write(f"\n")

        


def runJobs(jobFile):
    print("Running jobs")
    result = subprocess.run(['sudo', 'fio', jobFile], capture_output=True, text=True)

    print("Finished ---")

    print(result)


if __name__ == '__main__':
    main()  