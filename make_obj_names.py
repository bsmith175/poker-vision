import argparse

num_classes = 52
suits = ["d", "h", "c", "s"]
cards = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]

def create(path="./"):
    lines = []
    if (path == None):
        path = "./obj.names"
    else:
        path = path + "/obj.names"

    for suit in suits:
        for card in cards:
            lines.append(f"{card}{suit}\n")


    f = open(path, "w")
    print(f"Writing to file {f.name}")
    f.writelines(lines)
    f.close()

# Create obj.names file 
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--path", help="The path to the output file (default ./)")
    args = parser.parse_args()
    create(args.path)
