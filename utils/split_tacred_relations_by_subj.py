# -*- coding: utf-8 -*-
from file_io import read_file, write_file


def split_tacred_relations_by_subj(label_file, per_label_file, org_label_file):
    """Splits the relations of TACRED into person-related or organization-related group."""
    labels = read_file(label_file)
    per_labels = []
    org_labels = []

    for label in labels:
        if "per:" in label:
            per_labels.append(label)
        elif "org:" in label:
            org_labels.append(label)

    write_file(per_label_file, per_labels)
    write_file(org_label_file, org_labels)


if __name__ == "__main__":
    split_tacred_relations_by_subj(
        "../data/re-tacred/label.txt", "../data/re-tacred/label_per.txt", "../data/re-tacred/label_org.txt"
    )
