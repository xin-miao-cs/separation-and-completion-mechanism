# -*- coding: utf-8 -*-
from random import sample
from file_io import read_json_file, write_json_file


def random_sample(complete_file, sampled_file, proportion):
    """Sample proportion% of data from the complete dataset."""
    complete_instances = read_json_file(complete_file)
    sampled_instances = sample(
        complete_instances, int(proportion * len(complete_instances))
    )
    write_json_file(sampled_file, sampled_instances)


if __name__ == "__main__":
    random_sample("../data/re-tacred/1.0/train.json", "../data/re-tacred/0.1/train-0.1.json", 0.1)
