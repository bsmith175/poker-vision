import argparse
import os

def create(path="data/obj"):
    lines = []
    if (path == None):
        path = "data/obj"

    for filename in os.listdir(path):
        if not filename.endswith('.jpg'): continue
        fullname = os.path.join(path, filename)
        lines.append(fullname)


    print(f"Found {len(lines)} images")
    f = open("./train.txt", "w")
    print(f"Writing to file {f.name}")
    f.writelines(lines)
    f.close()

# Create train.txt file 
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", help="Path to the image directory, relative to darknet executable (default ./data/obj)")
    args = parser.parse_args()
    create(args.dir)
