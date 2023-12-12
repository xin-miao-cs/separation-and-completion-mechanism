# -*- coding: utf-8 -*-
from tqdm import tqdm
from pathlib import Path
from argparse import ArgumentParser

from model import GPT
from prompt import Prompter
from check import Checker
from data import Dataset, Saver


TASK_DATASET_MAPPING = {
    "tacred_per": "tacred",
    "tacred_org": "tacred",
    "re-tacred_per": "re-tacred",
    "re-tacred_org": "re-tacred"
}


def main(args):
    model = GPT(args.model, args.max_tokens, args.temperature)
    prompter = Prompter(args.task)
    checker = Checker(args.task)

    data_path = Path(args.folder) / TASK_DATASET_MAPPING[args.task] / args.setting
    dataset_path = data_path / args.dataset
    dataset = Dataset(dataset_path)
    counterfactual_path = data_path / (args.model + ".tsv")
    counterfactual_saver = Saver(counterfactual_path)
    record_path = data_path / (args.model + "_record.tsv")
    record_saver = Saver(record_path)

    for (sentence, entity, original_relation) in tqdm(dataset.triplets):
        sentence_front, sentence_middle, sentence_rear = sentence
        entity_pair, entity1, entity2 = entity
        if checker.is_relation_legal(original_relation):
            question = prompter.form_prompt(sentence_middle, entity_pair, original_relation)
            answer = model.query(question)
            causal_words_analysis, output_sentence, new_relation = prompter.parse_answer(answer)

            if checker.has_causal_words(causal_words_analysis):
                tolerance = args.tolerance
                while True:
                    tolerance -= 1
                    if checker.is_plausible_counterfactual(output_sentence, new_relation, entity1, entity2, original_relation):
                        counterfactual_sentence = " ".join([sentence_front, output_sentence, sentence_rear])
                        counterfactual_saver.save_instance([new_relation, counterfactual_sentence])
                        record_saver.save_instance([answer])
                        record_saver.save_instance([])
                        break
                    if tolerance > 0:
                        answer = model.query(question)
                        _, output_sentence, new_relation = prompter.parse_answer(answer)
                    else:
                        break


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--model", default="gpt-3.5-turbo-0613", type=str)
    parser.add_argument("--max_tokens", default=1000, type=int)
    parser.add_argument("--temperature", default=0, type=float)
    parser.add_argument("--tolerance", default=3, type=int)

    parser.add_argument("--folder", default="data", type=str)
    parser.add_argument("--task", default="re-tacred_org", type=str)
    parser.add_argument("--setting", default="0.1", type=str)
    parser.add_argument("--dataset", default="train-0.1.json", type=str)
    main(parser.parse_args())
