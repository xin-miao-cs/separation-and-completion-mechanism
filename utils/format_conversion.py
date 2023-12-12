# -*- coding: utf-8 -*-
import tqdm
from file_io import read_json_file, write_tsv_file


def json_to_tsv(json_file, tsv_file):
    """Converts a json-formatted file into tsv-formatted file."""
    json_instances = read_json_file(json_file)
    tsv_instances = []

    for json_instance in tqdm.tqdm(json_instances):
        relation = json_instance["relation"]
        tokens = json_instance["token"]

        subj_start = json_instance["subj_start"]
        subj_end = json_instance["subj_end"]
        obj_start = json_instance["obj_start"]
        obj_end = json_instance["obj_end"]

        # The former entity is marked as entity1,
        # the latter entity is marked as entity2.
        if subj_start < obj_start:
            entity1_start = subj_start
            entity1_end = subj_end
            entity2_start = obj_start
            entity2_end = obj_end
        else:
            entity1_start = obj_start
            entity1_end = obj_end
            entity2_start = subj_start
            entity2_end = subj_end

        tokens[entity1_start] = "<e1> " + tokens[entity1_start]
        tokens[entity1_end] = tokens[entity1_end] + " </e1>"
        tokens[entity2_start] = "<e2> " + tokens[entity2_start]
        tokens[entity2_end] = tokens[entity2_end] + " </e2>"

        sentence = " ".join(tokens)
        tsv_instances.append([relation, sentence])

    write_tsv_file(tsv_file, tsv_instances)


if __name__ == "__main__":
    json_to_tsv("../data/re-tacred/0.1/train-0.1.json", "../data/re-tacred/0.1/train-0.1.tsv")
