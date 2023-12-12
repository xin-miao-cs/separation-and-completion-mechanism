from utils.file_io import read_json_file, read_tsv_file, append_tsv_file


class Dataset(object):
    def __init__(self, file_path):
        self.instances = read_json_file(file_path)
        self.triplets = self.extract_triplets(self.instances)

    @staticmethod
    def extract_triplets(instances):
        triplets = []
        for instance in instances:
            tokens = instance["token"]
            subj_start = instance["subj_start"]
            subj_end = instance["subj_end"]
            obj_start = instance["obj_start"]
            obj_end = instance["obj_end"]
            relation = instance["relation"]

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

            entity1 = " ".join(tokens[entity1_start: entity1_end + 1])
            entity2 = " ".join(tokens[entity2_start: entity2_end + 1])
            entity_pair = "-".join([entity1, entity2])
            entity1 = " ".join(["<e1>", entity1, "</e1>"])
            entity2 = " ".join(["<e2>", entity2, "</e2>"])
            entity = (entity_pair, entity1, entity2)

            tokens[entity1_start] = " ".join(["<e1>", tokens[entity1_start]])
            tokens[entity1_end] = " ".join([tokens[entity1_end], "</e1>"])
            tokens[entity2_start] = " ".join(["<e2>", tokens[entity2_start]])
            tokens[entity2_end] = " ".join([tokens[entity2_end], "</e2>"])
            sentence_front = " ".join(tokens[: entity1_start])
            sentence_middle = " ".join(tokens[entity1_start: entity2_end + 1])
            sentence_rear = ""
            if entity2_end < len(tokens) - 1:
                sentence_rear = " ".join(tokens[entity2_end + 1:])
            sentence = (sentence_front, sentence_middle, sentence_rear)

            triplets.append((sentence, entity, relation))
        return triplets

    def count_total_number(self):
        return len(self.instances)

    def count_average_length(self):
        total_length = 0
        for instance in self.instances:
            instance_length = len(instance["token"])
            total_length += instance_length
        total_number = self.count_total_number()
        average_length = total_length/total_number
        return average_length


class Saver(object):
    def __init__(self, file_path):
        self.file_path = file_path

    def save_instance(self, instance):
        append_tsv_file(self.file_path, instance)

    def count_total_number(self):
        return len(read_tsv_file(self.file_path))
