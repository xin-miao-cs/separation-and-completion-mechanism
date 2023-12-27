

class Checker(object):
    def __init__(self, task):
        self.legal_relations = TASK_LEGAL_RELATION_MAPPING[task]

    @staticmethod
    def has_causal_words(causal_words_analysis):
        if "no" in causal_words_analysis and "causal" in causal_words_analysis:
            return False
        else:
            return True

    @staticmethod
    def is_format_correct(output_sentence):
        if output_sentence.count("<e1>") == 1 and output_sentence.count("</e1>") == 1\
          and output_sentence.count("<e2>") == 1 and output_sentence.count("</e2>") == 1:
            return True
        else:
            return False

    @staticmethod
    def is_entity_consistent(output_sentence, entity1, entity2):
        if entity1 in output_sentence and entity2 in output_sentence:
            return True
        else:
            return False

    def is_relation_legal(self, relation):
        if relation in self.legal_relations:
            return True
        else:
            return False

    @staticmethod
    def is_label_flipped(original_relation, new_relation):
        if original_relation != new_relation:
            return True
        else:
            return False

    def is_plausible_counterfactual(self, output_sentence, new_relation, entity1, entity2, original_relation):
        if self.is_format_correct(output_sentence):
            if self.is_entity_consistent(output_sentence, entity1, entity2):
                if self.is_relation_legal(new_relation):
                    if self.is_label_flipped(original_relation, new_relation):
                        return True
        return False


SEMEVAL_LEGAL_RELATIONS = (
    "Message-Topic(e1,e2)",
    "Message-Topic(e2,e1)",
    "Entity-Origin(e1,e2)",
    "Entity-Origin(e2,e1)",
    "Entity-Destination(e1,e2)",
    "Entity-Destination(e2,e1)",
    "Content-Container(e1,e2)",
    "Content-Container(e2,e1)",
    "Cause-Effect(e1,e2)",
    "Cause-Effect(e2,e1)",
    "Component-Whole(e1,e2)",
    "Component-Whole(e2,e1)",
    "Member-Collection(e1,e2)",
    "Member-Collection(e2,e1)",
    "Instrument-Agency(e1,e2)",
    "Instrument-Agency(e2,e1)",
    "Product-Producer(e1,e2)",
    "Product-Producer(e2,e1)"
)


ACE2005_LEGAL_RELATIONS = (
    "ORG-AFF",
    "GEN-AFF",
    "ART",
    "PHYS"
)


TACRED_PER_LEGAL_RELATIONS = (
    "per:employee_of",
    "per:cities_of_residence",
    "per:children",
    "per:title",
    "per:siblings",
    "per:religion",
    "per:age",
    "per:stateorprovinces_of_residence",
    "per:countries_of_residence",
    "per:spouse",
    "per:origin",
    "per:stateorprovince_of_birth",
    "per:date_of_death",
    "per:parents",
    "per:schools_attended",
    "per:cause_of_death",
    "per:city_of_death",
    "per:stateorprovince_of_death",
    "per:country_of_birth",
    "per:date_of_birth",
    "per:city_of_birth",
    "per:charges",
    "per:country_of_death"
)


TACRED_ORG_LEGAL_RELATIONS = (
    "org:founded_by",
    "org:website",
    "org:member_of",
    "org:top_members/employees",
    "org:city_of_headquarters",
    "org:members",
    "org:country_of_headquarters",
    "org:stateorprovince_of_headquarters",
    "org:number_of_employees/members",
    "org:parents",
    "org:subsidiaries",
    "org:political/religious_affiliation",
    "org:dissolved",
    "org:shareholders",
    "org:founded"
)


TASK_LEGAL_RELATION_MAPPING = {"episodic_semeval": SEMEVAL_LEGAL_RELATIONS,
                               "ace2005": ACE2005_LEGAL_RELATIONS,
                               "tacred_per": TACRED_PER_LEGAL_RELATIONS,
                               "tacred_org": TACRED_ORG_LEGAL_RELATIONS}
