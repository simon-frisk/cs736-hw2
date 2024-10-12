import json


def main():
    with open("output.json", 'r') as file:
        jsonString = file.read()
        analyzeOutput(jsonString)


def analyzeOutput(jsonString):
    data = json.loads(jsonString)
    jobs = data["jobs"]

    bandwidthMeasures = {}

    for job in jobs:
        name = job["jobname"]
        nameList = name.split("-")
        driver = nameList[0]
        mode = nameList[1]
        bs = nameList[2]
        numjobs = nameList[3]
        bw = job[mode]["bw"]

        if not (mode in bandwidthMeasures):
            bandwidthMeasures[mode] = {}
        if not (bs in bandwidthMeasures[mode]):
            bandwidthMeasures[mode][bs] = {}
        if not (numjobs in bandwidthMeasures[mode][bs]):
            bandwidthMeasures[mode][bs][numjobs] = {}

        bandwidthMeasures[mode][bs][numjobs][driver] = bw

    for mode in bandwidthMeasures:
        for bs in bandwidthMeasures[mode]:
            for numjobs in bandwidthMeasures[mode][bs]:
                for measureDMBN in bandwidthMeasures[mode][bs][numjobs]:
                    measures = bandwidthMeasures[mode][bs][numjobs]
                    metric = measures["/dev/rnullb0"] / measures["/dev/nullb0"]
                    print(f"{mode} {bs} {numjobs} - {metric}")


if __name__ == '__main__':
    main()
