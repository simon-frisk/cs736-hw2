import json


def main():
    with open("output.json", 'r') as file:
        jsonString = file.read()
        analyzeOutput(jsonString)


def analyzeOutput(jsonString):
    data = json.loads(jsonString)
    jobs = data["jobs"]

    bandwidthMeasures = []

    for job in jobs:
        name = job["jobname"]
        read_bw = job["read"]["bw"]
        write_bw = job["write"]["bw"]
        # print(f"{name} {read_bw} {write_bw}")

        nameList = name.split("-")
        mode = nameList[1]
        bs = nameList[2]
        numjobs = nameList[3]
        bw = job[mode]["bw"]
        bandwidthMeasures.append(((name, mode, bs, numJobs), bw))

    print(bandwidthMeasures)

if __name__ == '__main__':
    main()
