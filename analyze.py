import json
import matplotlib.pyplot as plt
import numpy as np


def main():
    with open("output.json", 'r') as file:
        jsonString = file.read()
        analyzeOutput(jsonString)


def analyzeOutput(jsonString):
    data = json.loads(jsonString)
    jobs = data["jobs"]

    blockSizes = {}
    jobSizes = {}

    bandwidthMeasures = {}

    for job in jobs:
        name = job["jobname"]
        nameList = name.split("-")
        driver = nameList[0]
        mode = nameList[1]
        readOrWrite = 'read' if (mode == 'read' or mode == 'randread') else 'write'
        bs = nameList[2]
        numjobs = nameList[3]
        bw = job[readOrWrite]["bw"]

        blockSizes.add(bs)
        jobSizes.add(numjobs)

        if not (mode in bandwidthMeasures):
            bandwidthMeasures[mode] = {}
        if not (bs in bandwidthMeasures[mode]):
            bandwidthMeasures[mode][bs] = {}
        if not (numjobs in bandwidthMeasures[mode][bs]):
            bandwidthMeasures[mode][bs][numjobs] = {}

        bandwidthMeasures[mode][bs][numjobs][driver] = bw

    with open("metrics.txt", 'w') as metrics:
        for mode in bandwidthMeasures:
            matrix = np.empty((len(blockSizes), len(jobSizes)))

            for bs in bandwidthMeasures[mode]:
                for numjobs in bandwidthMeasures[mode][bs]:
                    for measureDMBN in bandwidthMeasures[mode][bs][numjobs]:
                        measures = bandwidthMeasures[mode][bs][numjobs]
                        metric = measures["/dev/rnullb0"] / measures["/dev/nullb0"]
                        matrix[bs, numjobs] = metric
                        metrics.write(f"{"/dev/rnullb0"} {mode} {bs} {numjobs} - {measures["/dev/rnullb0"]}")
                        metrics.write(f"{"/dev/nullb0"} {mode} {bs} {numjobs} - {measures["/dev/nullb0"]}")

            plt.imshow(matrix, cmap='coolwarm', interpolation='nearest')
            plt.colorbar()
            for i in range(matrix.shape[0]):
                for j in range(matrix.shape[1]):
                    plt.text(j, i, f'{matrix[i, j]:.2f}', ha='center', va='center', color='white')

            plt.xlabel('I/O jobs')
            plt.ylabel('bs')
            plt.show()



if __name__ == '__main__':
    main()
