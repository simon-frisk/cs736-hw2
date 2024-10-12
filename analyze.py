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
        nameList = name.split("-")
        driver = nameList[0]
        mode = nameList[1]
        bs = nameList[2]
        numjobs = nameList[3]
        bw = job[mode]["bw"]

        if not (driver in bandwidthMeasures):
            bandwidthMeasures[driver] = {}
        if not (mode in bandwidthMeasures[driver])
            bandwidthMeasures[driver][mode] = {}
        if not (bs in bandwidthMeasures[driver][mode])
            bandwidthMeasures[driver][mode][bs] = {}

        bandwidthMeasures[driver][mode][bs][numjobs] = bw

    print(bandwidthMeasures)

if __name__ == '__main__':
    main()
