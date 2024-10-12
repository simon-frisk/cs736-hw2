import json
import matplotlib.pyplot as plt
import numpy as np


def main():
    with open("output_1.json", 'r') as file:
        jsonString = file.read()
        analyzeOutput(jsonString)


def analyzeOutput(jsonString):
    data = json.loads(jsonString)
    jobs = data["jobs"]

    blockSizes = set()
    jobSizes = set()

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

            for i, bs in enumerate(sorted(bandwidthMeasures[mode].keys())):
                for j, numjobs in enumerate(sorted(bandwidthMeasures[mode][bs].keys())):
                    measures = bandwidthMeasures[mode][bs][numjobs]
                    metric = measures["/dev/rnullb0"] / measures["/dev/nullb0"]
                    matrix[i,j] = metric
                    metrics.write(f"/dev/rnullb0 {mode} {bs} {numjobs} - {measures["/dev/rnullb0"]}\n")
                    metrics.write(f"/dev/nullb0 {mode} {bs} {numjobs} - {measures["/dev/nullb0"]}\n")

            plt.imshow(matrix, cmap='coolwarm_r', interpolation='nearest', vmin=0.5, vmax=2)
            plt.colorbar()
            for i in range(matrix.shape[0]):
                for j in range(matrix.shape[1]):
                    plt.text(j, i, f'{matrix[i, j]:.2f}', ha='center', va='center', color='white')
            plt.title(mode)
            plt.xlabel('I/O jobs')
            plt.ylabel('bs')
            plt.xticks(ticks=np.arange(matrix.shape[1]), labels=[i+1 for i in range(matrix.shape[1])])
            plt.yticks(ticks=np.arange(matrix.shape[0]), labels=[4*(2**(i)) for i in range(matrix.shape[0])])
            plt.show()



if __name__ == '__main__':
    main()
