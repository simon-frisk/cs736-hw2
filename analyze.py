import json


def main():
    with open("output.json", 'r') as file:
        jsonString = file.read()
        analyzeOutput(jsonString)


def analyzeOutput(jsonString):
    data = json.loads(jsonString)
    jobs = data["jobs"]

    for job in jobs:
        name = job["jobname"]
        read_bw = job["read"]["bw"]
        write_bw = job["write"]["bw"]
        print(f"{name} {read_bw} {write_bw}")



if __name__ == '__main__':
    main()
