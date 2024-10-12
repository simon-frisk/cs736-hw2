import json


def main():
    with open("output.json", 'r') as file:
        jsonString = file.read()
        analyzeOutput(jsonString)


def analyzeOutput(jsonString):
    data = json.loads(jsonString)
    jobs = data["jobs"]
    print(len(jobs))
    print(jobs)


if __name__ == '__main__':
    main()
