import os
import argparse

from bratviz.dataset_readers import ConllReader

# since the html files are written inside the `visualizations` folder
BRAT_PATH = "../brat/brat-v1.3_Crunchy_Frog"
LIB_PATH = "./bratviz"


def init_args():
    parser = argparse.ArgumentParser(description="Create brat visualizations from file")
    parser.add_argument(
        "-f",
        "--file_path",
        required=True,
        help="Path to the file to visualize.",
        type=str,
    )
    parser.add_argument(
        "-n",
        "--num_sent",
        required=False,
        help="Number of sentences to parse",
        type=int,
    )
    return parser.parse_args()


def read_template(path):
    path = os.path.join(LIB_PATH, path)
    with open(path, "r") as f:
        return "".join(f.readlines())


def write_viz(viz, idx):
    with open("./visualizations/{}.html".format(idx), "w") as f:
        f.write(viz)


def write_index(template, hrefs):
    with open("./visualizations/index.html", "w") as f:
        f.write(template.replace("$$LIST$$", "\n".join(hrefs)))


def main():
    args = init_args()
    viz_template = read_template("templates/html.html")
    index_template = read_template("templates/index.html")
    reader = ConllReader()
    href_list = []
    for idx, (text, ents, rels) in enumerate(reader.read(args.file_path)):
        href = '<a href="./{}.html">{}</a><br />'.format(idx, text)
        href_list.append(href)
        viz = (
            viz_template.replace("$$TEXT$$", text)
            .replace("$$ENTITIES$$", str(ents))
            .replace("$$RELATIONS$$", str(rels))
            .replace("$$BRAT_PATH$$", BRAT_PATH)
        )
        write_viz(viz, idx)
        if args.num_sent and args.num_sent == idx:
            break
    write_index(index_template, href_list)


if __name__ == "__main__":
    main()
