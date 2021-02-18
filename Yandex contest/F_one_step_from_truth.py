import requests
import argparse

def make_request(host, port):
    response = requests.get(f"{host}:{port}/desk/test/index.txt")
    return response.json()

def process_data(data, not_mult, smallest):
    res = {}
    sumAndCount = {}
    for key in data[0]:
        res[key] = [0 for x in range(4)]
        res[key][1] += 100000000
        sumAndCount[key] = {"sum" : 0, "count" : 0}

    for setNumber in range(len(data)):
        for key in data[setNumber]:
            for value in data[setNumber][key]:
                if value % not_mult != 0 and value >= smallest:
                    if res[key][0] < value:
                        res[key][0] = value
                    if res[key][1] > value:
                        res[key][1] = value
                    sumAndCount[key]["sum"] += value
                    sumAndCount[key]["count"] += 1
    for key in sumAndCount:
        res[key][2] = round(sumAndCount[key]["sum"] / sumAndCount[key]["count"], 2)
        res[key][3] = sumAndCount[key]["sum"]
    resText = []
    for key in res:
        resText.append(str(key) + ';' + ';'.join(map(str, res[key])))
    resText.sort()
    with open("truth.csv", 'w') as out:
        for i in resText:
            out.write(f"{i}\n")
    return 0



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("host")
    parser.add_argument("port")
    parser.add_argument("--not_mult", default=100, type=int, help="Don't consider values divisible by this value")
    parser.add_argument("--smallest", default=0, type=int, help="Consider only values less than this value")
    args = parser.parse_args()
    data = make_request(args.host, args.port)
    process_data(data, args.not_mult, args.smallest)