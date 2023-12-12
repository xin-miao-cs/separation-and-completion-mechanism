

class Prompter(object):
    def __init__(self, task):
        self.incontext = TASK_INCONTEXT_MAPPING[task]
        self.relation_explanation = TASK_RELATION_EXPLANATION_MAPPING[task]
        self.explanation_relation = TASK_EXPLANATION_RELATION_MAPPING[task]

    def form_prompt(self, sentence, entities, relation):
        prompt = (self.incontext
                  + f"Input: {sentence}\n"
                  + f"Entities: {entities}\n"
                  + f"Relation: {self.relation_explanation[relation]}\n")
        return prompt

    def parse_answer(self, answer):
        causal_words_analysis = answer.split("\n")[0].replace("Identify causal words: ", "")
        output_sentence = answer.split("\n")[-2].replace("Output: ", "")
        new_relation = self.explanation_relation.get(answer.split("\n")[-1].replace("New relation: ", ""))
        return causal_words_analysis, output_sentence, new_relation


TACRED_PER_INCONTEXT = (
    "Task definition: change the relation between entities based on minimal context editing.\n"
    "Instruction: the process can be divided into the following six steps. (1) Identify causal"
    " words: find the context words that are causally related to the relation. (2) Deconstruct"
    " entities: based on the attributes of the entities, deconstruct the entities into several"
    " primary properties. (3) Reconstruct scenarios: based on the deconstructed properties,"
    " reconstruct the scenarios that the entities may constitute. (4) Identify decisive scenario:"
    " select a scenario that contribute the most to the relation. (5) Uncover potential relation:"
    " select another scenario and match the most suitable relation from the candidate relations."
    " (6) Replace causal words: replace the identified causal words with suitable words to change"
    " the original relation to the potential one.\n"
    "Candidate relations: employee of, cities of residence, children, title, siblings, religion,"
    " age, state or provinces of residence, countries of residence, spouse, origin, state or province"
    " of birth, date of death, parents, schools attended, cause of death, city of death, state or"
    " province of death, country of birth, date of birth, city of birth, charges, country of death.\n"
    "\n"
    "Example 1:\n"
    "Input: <e1> Jack </e1> is a famous movie director, died at <e2> Los Angeles </e2>\n"
    "Entities: Jack-Los Angeles\n"
    "Relation: city of death\n"
    'Identify causal words: the context words "died at" are causally related to the relation'
    ' "city of death".\n'
    'Deconstruct entities: based on the attributes of the entities, "Jack" can be deconstructed'
    " into the several primary properties: form: normal person, usage: learn skills, purpose:"
    ' raise family; "Los Angeles" can be deconstructed into the several primary properties:'
    " form: large city, usage: provide shelter, purpose: nurture human.\n"
    'Pair the properties between "Jack" and "Los Angeles" to reconstruct the following three'
    ' scenarios:\n'
    'Reconstruct the first scenario: based on the "form: normal person" property of "Jack"'
    ' and the "usage: provide shelter" property of "Los Angeles", "Jack" can spend his'
    ' entire life peacefully in "Los Angeles", hence we can reconstruct the scenario:'
    " retirement purpose: Jack spend his final moments in Los Angeles.\n"
    'Reconstruct the second scenario: based on the "usage: learn skills" property of "Jack"'
    ' and the "purpose: nurture human" property of "Los Angeles", "Jack" can lean skills'
    ' and grow up in "Los Angeles", hence we can reconstruct the scenario: growth purpose:'
    " Jack grow up in Los Angeles.\n"
    'Reconstruct the third scenario: based on the "purpose: raise family" property of "Jack"'
    ' and the "form: large city" property of "Los Angeles", "Jack" can live in "Los Angeles"'
    ' to make money to raise his family, hence we can reconstruct the scenario: survival'
    " purpose: Jack live in Los Angeles.\n"
    'Identify decisive scenario: the scenario "retirement purpose: Jack spend his final'
    ' moments in Los Angeles" contribute the most to the relation "city of death".\n'
    'Uncover potential relation: if we focus on another scenario "growth purpose: Jack grow'
    ' up in Los Angeles", in the scenario, "Los Angeles" is the birth city of "Jack", hence'
    ' the commonsense relation is "city of birth".\n'
    'Replace causal words: to change the original relation to the potential one "city of birth",'
    ' the identified causal words can be replaced with "born in".\n'
    "Output: <e1> Jack </e1> is a famous movie director, born in <e2> Los Angeles </e2>\n"
    "New relation: city of birth\n"
    "\n"
    "Example 2:\n"
    "Input: <e1> Jack </e1> is a famous movie director, died at <e2> Los Angeles </e2>\n"
    "Entities: Jack-Los Angeles\n"
    "Relation: city of death\n"
    'Identify causal words: the context words "died at" are causally related to the relation'
    ' "city of death".\n'
    'Deconstruct entities: based on the attributes of the entities, "Jack" can be deconstructed'
    " into the several primary properties: form: normal person, usage: learn skills, purpose:"
    ' raise family; "Los Angeles" can be deconstructed into the several primary properties:'
    " form: large city, usage: provide shelter, purpose: nurture human.\n"
    'Pair the properties between "Jack" and "Los Angeles" to reconstruct the following three'
    ' scenarios:\n'
    'Reconstruct the first scenario: based on the "form: normal person" property of "Jack"'
    ' and the "usage: provide shelter" property of "Los Angeles", "Jack" can spend his'
    ' entire life peacefully in "Los Angeles", hence we can reconstruct the scenario:'
    " retirement purpose: Jack spend his final moments in Los Angeles.\n"
    'Reconstruct the second scenario: based on the "usage: learn skills" property of "Jack"'
    ' and the "purpose: nurture human" property of "Los Angeles", "Jack" can lean skills'
    ' and grow up in "Los Angeles", hence we can reconstruct the scenario: growth purpose:'
    " Jack grow up in Los Angeles.\n"
    'Reconstruct the third scenario: based on the "purpose: raise family" property of "Jack"'
    ' and the "form: large city" property of "Los Angeles", "Jack" can live in "Los Angeles"'
    ' to make money to raise his family, hence we can reconstruct the scenario: survival'
    " purpose: Jack live in Los Angeles.\n"
    'Identify decisive scenario: the scenario "retirement purpose: Jack spend his final'
    ' moments in Los Angeles" contribute the most to the relation "city of death".\n'
    'Uncover potential relation: if we focus on another scenario "survival purpose: Jack live'
    ' in Los Angeles", in the scenario, "Los Angeles" is the residence city of "Jack", hence'
    ' the commonsense relation is "cities of residence".\n'
    'Replace causal words: to change the original relation to the potential one "cities of'
    ' residence", the identified causal words can be replaced with "reside in".\n'
    "Output: <e1> Jack </e1> is a famous movie director, reside in <e2> Los Angeles </e2>\n"
    "New relation: cities of residence\n"
    "\n"
    "Exam (complete the remaining content and maintain consistency with the format of the above"
    " examples):\n"
)


TACRED_ORG_INCONTEXT = (
    "Task definition: change the relation between entities based on minimal context editing.\n"
    "Instruction: the process can be divided into the following six steps. (1) Identify causal"
    " words: find the context words that are causally related to the relation. (2) Deconstruct"
    " entities: based on the attributes of the entities, deconstruct the entities into several"
    " primary properties. (3) Reconstruct scenarios: based on the deconstructed properties,"
    " reconstruct the scenarios that the entities may constitute. (4) Identify decisive scenario:"
    " select a scenario that contribute the most to the relation. (5) Uncover potential relation:"
    " select another scenario and match the most suitable relation from the candidate relations."
    " (6) Replace causal words: replace the identified causal words with suitable words to change"
    " the original relation to the potential one.\n"
    "Candidate relations: founded by, website, member of, top members/employees, city of headquarters,"
    " members, country of headquarters, state or province of headquarters, number of employees/members,"
    " parents, subsidiaries, political/religious affiliation, dissolved, shareholders, founded.\n"
    "\n"
    "Example 1:\n"
    "Input: <e1> Steve Jobs </e1> is the president of <e2> Apple Inc </e2>\n"
    "Entities: Steve Jobs-Apple Inc\n"
    "Relation: top members/employees\n"
    'Identify causal words: the context words "president of" are causally related to the'
    ' relation "top members/employees".\n'
    'Deconstruct entities: based on the attributes of the entities, "Steve Jobs" can be'
    " deconstructed into the several primary properties: form: leading man, usage: complete"
    ' work, purpose: create value; "Apple Inc" can be deconstructed into the several primary'
    " properties: form: large company, usage: conduct production, purpose: make money.\n" 
    'Pair the properties between "Steve Jobs" and "Apple Inc" to reconstruct the following'
    ' three scenarios:\n'
    'Reconstruct the first scenario: based on the "form: leading man" property of "Steve Jobs"'
    ' and the "usage: conduct production" property of "Apple Inc", "Steve Jobs" should lead'
    " employees to conduct production, hence we can reconstruct the scenario: leadership"
    " purpose: Steve Jobs manages Apple Inc.\n"
    'Reconstruct the second scenario: based on the "usage: finish work" property of "Steve'
    ' Jobs" and the "purpose: make money" property of "Apple Inc", "Apple Inc" can employ'
    ' "Steve Jobs" to help it make money, hence we can reconstruct the scenario: employment'
    " purpose: Steve Jobs is employed by Apple Inc.\n"
    'Reconstruct the third scenario: based on the "purpose: create value" property of "Steve'
    ' Jobs" and the "form: large company" property of "Apple Inc", "Steve Jobs" founded the'
    ' large company "Apple Inc" to create his value, hence we can reconstruct the scenario:'
    " creation purpose: Steve Jobs founded Apple Inc.\n"
    'Identify decisive scenario: the scenario "leadership purpose: Steve Jobs manages Apple'
    ' Inc" contribute the most to the relation "top members/employees".\n'
    'Uncover potential relation: if we focus on another scenario "employment purpose: Steve'
    ' Jobs is employed by Apple Inc", in the scenario, "Steve Jobs" is a member of "Apple'
    ' Inc", hence the commonsense relation is "member of".\n'
    'Replace causal words: to change the original relation to the potential one "member of",'
    ' the identified causal words can be replaced with "member of".\n'
    "Output: <e1> Steve Jobs </e1> is the member of <e2> Apple Inc </e2>\n"
    "New relation: member of\n"
    "\n"
    "Example 2:\n"
    "Input: <e1> Steve Jobs </e1> is the president of <e2> Apple Inc </e2>\n"
    "Entities: Steve Jobs-Apple Inc\n"
    "Relation: top members/employees\n"
    'Identify causal words: the context words "president of" are causally related to the'
    ' relation "top members/employees".\n'
    'Deconstruct entities: based on the attributes of the entities, "Steve Jobs" can be'
    " deconstructed into the several primary properties: form: leading man, usage: complete"
    ' work, purpose: create value; "Apple Inc" can be deconstructed into the several primary'
    " properties: form: large company, usage: conduct production, purpose: make money.\n" 
    'Pair the properties between "Steve Jobs" and "Apple Inc" to reconstruct the following'
    ' three scenarios:\n'
    'Reconstruct the first scenario: based on the "form: leading man" property of "Steve Jobs"'
    ' and the "usage: conduct production" property of "Apple Inc", "Steve Jobs" should lead'
    " employees to conduct production, hence we can reconstruct the scenario: leadership"
    " purpose: Steve Jobs manages Apple Inc.\n"
    'Reconstruct the second scenario: based on the "usage: finish work" property of "Steve'
    ' Jobs" and the "purpose: make money" property of "Apple Inc", "Apple Inc" can employ'
    ' "Steve Jobs" to help it make money, hence we can reconstruct the scenario: employment'
    " purpose: Steve Jobs is employed by Apple Inc.\n"
    'Reconstruct the third scenario: based on the "purpose: create value" property of "Steve'
    ' Jobs" and the "form: large company" property of "Apple Inc", "Steve Jobs" founded the'
    ' large company "Apple Inc" to create his value, hence we can reconstruct the scenario:'
    " creation purpose: Steve Jobs founded Apple Inc.\n"
    'Identify decisive scenario: the scenario "leadership purpose: Steve Jobs manages Apple'
    ' Inc" contribute the most to the relation "top members/employees".\n'
    'Uncover potential relation: if we focus on another scenario "creation purpose: Steve Jobs'
    ' founded Apple Inc", in the scenario, "Steve Jobs" is the founder of "Apple Inc", hence'
    ' the commonsense relation is "founded by".\n'
    'Replace causal words: to change the original relation to the potential one "founded by",'
    ' the identified causal words can be replaced with "founder of".\n'
    "Output: <e1> Steve Jobs </e1> is the founder of <e2> Apple Inc </e2>\n"
    "New relation: founded by\n"
    "\n"
    "Exam (complete the remaining content and maintain consistency with the format of the above"
    " examples):\n"
)


RE_TACRED_PER_INCONTEXT = (
    'Task definition: change the relation between entities based on minimal context editing.\n'
    'Instruction: the process can be divided into the following six steps. (1) Identify causal words: find the context words that'
    ' are causally related to the relation. (2) Deconstruct entities: based on the attributes of the entities, deconstruct the'
    ' entities into several primary properties. (3) Reconstruct scenarios: based on the deconstructed properties, reconstruct the'
    ' scenarios that the entities may constitute. (4) Identify decisive scenario: select a scenario that contribute the most to'
    ' the relation. (5) Uncover potential relation: select another scenario and match the most suitable relation from the'
    ' candidate relations. (6) Replace causal words: replace the identified causal words with suitable words to change the'
    ' original relation to the potential one.\n'
    'Candidate relations: children, origin, countries of residence, employee of, title, religion, age, date of death, state or'
    ' provinces of residence, spouse, siblings, state or province of birth, parents, charges, schools attended, cause of death,'
    ' city of death, state or province of death, country of death, country of birth, date of birth, cities of residence, city of'
    ' birth.\n'
    '\n'
    'Example 1:\n'
    'Input: <e1> Jack </e1> is a famous movie director, died at <e2> Los Angeles </e2>\n'
    'Entities: Jack-Los Angeles\n'
    'Relation: city of death\n'
    'Identify causal words: the context words "died at" are causally related to the relation "city of death".\n'
    'Deconstruct entities: based on the attributes of the entities, "Jack" can be deconstructed into the several primary'
    ' properties: form: normal person, usage: learn skills, purpose: raise family; "Los Angeles" can be deconstructed into the'
    ' several primary properties: form: large city, usage: provide shelter, purpose: nurture human.\n'
    'Pair the properties between "Jack" and "Los Angeles" to reconstruct the following three  scenarios:\n'
    'Reconstruct the first scenario: based on the "form: normal person" property of "Jack" and the "usage: provide shelter"'
    ' property of "Los Angeles", "Jack" can spend his entire life peacefully in "Los Angeles", hence we can reconstruct the' 
    ' scenario: retirement purpose: Jack spend his final moments in Los Angeles.\n'
    'Reconstruct the second scenario: based on the "usage: learn skills" property of "Jack" and the "purpose: nurture human"'
    ' property of "Los Angeles", "Jack" can lean skills and grow up in "Los Angeles", hence we can reconstruct the scenario:'
    ' growth purpose: Jack grow up in Los Angeles.\n'
    'Reconstruct the third scenario: based on the "purpose: raise family" property of "Jack" and the "form: large city" property'
    ' of "Los Angeles", "Jack" can live in "Los Angeles" to make money to raise his family, hence we can reconstruct the'
    ' scenario: survival purpose: Jack live in Los Angeles.\n'
    'Identify decisive scenario: the scenario "retirement purpose: Jack spend his final moments in Los Angeles" contribute the'
    ' most to the relation "city of death".\n'
    'Uncover potential relation: if we focus on another scenario "growth purpose: Jack grow up in Los Angeles", in the scenario,'
    ' "Los Angeles" is the birth city of "Jack", hence the commonsense relation is "city of birth".\n'
    'Replace causal words: to change the original relation to the potential one "city of birth", the identified causal words can'
    ' be replaced with "born in".\n'
    'Output: <e1> Jack </e1> is a famous movie director, born in <e2> Los Angeles </e2>\n'
    'New relation: city of birth\n'
    '\n'
    'Example 2:\n'
    'Input: <e1> Jack </e1> is a famous movie director, died at <e2> Los Angeles </e2>\n'
    'Entities: Jack-Los Angeles\n'
    'Relation: city of death\n'
    'Identify causal words: the context words "died at" are causally related to the relation "city of death".\n'
    'Deconstruct entities: based on the attributes of the entities, "Jack" can be deconstructed into the several'
    ' primary properties: form: normal person, usage: learn skills, purpose: raise family; "Los Angeles" can be'
    ' deconstructed into the several primary properties: form: large city, usage: provide shelter, purpose: nurture'
    ' human.\n'
    'Pair the properties between "Jack" and "Los Angeles" to reconstruct the following three  scenarios:\n'
    'Reconstruct the first scenario: based on the "form: normal person" property of "Jack" and the "usage: provide'
    ' shelter" property of "Los Angeles", "Jack" can spend his entire life peacefully in "Los Angeles", hence we can'
    ' reconstruct the scenario: retirement purpose: Jack spend his final moments in Los Angeles.\n'
    'Reconstruct the second scenario: based on the "usage: learn skills" property of "Jack" and the "purpose: nurture'
    ' human" property of "Los Angeles", "Jack" can lean skills and grow up in "Los Angeles", hence we can reconstruct'
    ' the scenario: growth purpose: Jack grow up in Los Angeles.\n'
    'Reconstruct the third scenario: based on the "purpose: raise family" property of "Jack" and the "form: large city"'
    ' property of "Los Angeles", "Jack" can live in "Los Angeles" to make money to raise his family, hence we can'
    ' reconstruct the scenario: survival purpose: Jack live in Los Angeles.\n'
    'Identify decisive scenario: the scenario "retirement purpose: Jack spend his final moments in Los Angeles"'
    ' contribute the most to the relation "city of death".\n'
    'Uncover potential relation: if we focus on another scenario "survival purpose: Jack live in Los Angeles", in the'
    ' scenario, "Los Angeles" is the residence city of "Jack", hence the commonsense relation is "cities of residence".'
    '\n'
    'Replace causal words: to change the original relation to the potential one "cities of residence", the identified'
    ' causal words can be replaced with "reside in".\n'
    'Output: <e1> Jack </e1> is a famous movie director, reside in <e2> Los Angeles </e2>\n'
    'New relation: cities of residence\n'
    '\n'
    'Exam (complete the remaining content and maintain consistency with the format of the above examples):\n'
)


RE_TACRED_ORG_INCONTEXT = (
    'Task definition: change the relation between entities based on minimal context editing.\n'
    'Instruction: the process can be divided into the following six steps. (1) Identify causal words: find the'
    ' context words that are causally related to the relation. (2) Deconstruct entities: based on the attributes of'
    ' the entities, deconstruct the entities into several primary properties. (3) Reconstruct scenarios: based on the'
    ' deconstructed properties, reconstruct the scenarios that the entities may constitute. (4) Identify decisive'
    ' scenario: select a scenario that contribute the most to the relation. (5) Uncover potential relation: select'
    ' another scenario and match the most suitable relation from the candidate relations. (6) Replace causal words:'
    ' replace the identified causal words with suitable words to change the original relation to the potential one.\n'
    'Candidate relations: founded by, city of branch, website, top members/employees, number of employees/members,'
    ' members, country of branch, state or province of branch, political/religious affiliation, member of, dissolved,'
    ' shareholders, founded.\n'
    '\n'
    'Example 1:\n'
    'Input: <e1> Steve Jobs </e1> is the president of <e2> Apple Inc </e2>\n'
    'Entities: Steve Jobs-Apple Inc\n'
    'Relation: top members/employees\n'
    'Identify causal words: the context words "president of" are causally related to the relation'
    ' "top members/employees".\n'
    'Deconstruct entities: based on the attributes of the entities, "Steve Jobs" can be deconstructed into the several'
    ' primary properties: form: leading man, usage: finish work, purpose: create value; "Apple Inc" can be'
    ' deconstructed into the several primary properties: form: large company, usage: conduct production, purpose: make'
    ' money.\n'
    'Pair the properties between "Steve Jobs" and "Apple Inc" to reconstruct the following three scenarios:\n'
    'Reconstruct the first scenario: based on the "form: leading man" property of "Steve Jobs" and the "usage: conduct'
    ' production" property of "Apple Inc", "Steve Jobs" should lead employees to conduct production, hence we can'
    ' reconstruct the scenario: leadership purpose: Steve Jobs manages Apple Inc.\n'
    'Reconstruct the second scenario: based on the "usage: finish work" property of "Steve Jobs" and the "purpose:'
    ' make money" property of "Apple Inc", "Apple Inc" can employ "Steve Jobs" to help it make money, hence we can'
    ' reconstruct the scenario: employment purpose: Steve Jobs is employed by Apple Inc.\n'
    'Reconstruct the third scenario: based on the "purpose: create value" property of "Steve Jobs" and the "form: large'
    ' company" property of "Apple Inc", "Steve Jobs" founded the large company "Apple Inc" to create his value, hence'
    ' we can reconstruct the scenario: creation purpose: Steve Jobs founded Apple Inc.\n'
    'Identify decisive scenario: the scenario "leadership purpose: Steve Jobs manages Apple Inc" contribute the most to'
    ' the relation "top members/employees".\n'
    'Uncover potential relation: if we focus on another scenario "employment purpose: Steve Jobs is employed by Apple'
    ' Inc", in the scenario, "Steve Jobs" is a member of "Apple Inc", hence the commonsense relation is "member of".\n'
    'Replace causal words: to change the original relation to the potential one "member of", the identified causal'
    ' words can be replaced with "member of".\n'
    'Output: <e1> Steve Jobs </e1> is the member of <e2> Apple Inc </e2>\n'
    'New relation: member of\n'
    "\n"
    'Example 2:\n'
    'Input: <e1> Steve Jobs </e1> is the president of <e2> Apple Inc </e2>\n'
    'Entities: Steve Jobs-Apple Inc\n'
    'Relation: top members/employees\n'
    'Identify causal words: the context words "president of" are causally related to the relation'
    ' "top members/employees".\n'
    'Deconstruct entities: based on the attributes of the entities, "Steve Jobs" can be deconstructed into the several'
    ' primary properties: form: leading man, usage: finish work, purpose: create value; "Apple Inc" can be'
    ' deconstructed into the several primary properties: form: large company, usage: conduct production, purpose: make'
    ' money.\n'
    'Pair the properties between "Steve Jobs" and "Apple Inc" to reconstruct the following three scenarios:\n'
    'Reconstruct the first scenario: based on the "form: leading man" property of "Steve Jobs" and the "usage: conduct'
    ' production" property of "Apple Inc", "Steve Jobs" should lead employees to conduct production, hence we can'
    ' reconstruct the scenario: leadership purpose: Steve Jobs manages Apple Inc.\n'
    'Reconstruct the second scenario: based on the "usage: finish work" property of "Steve Jobs" and the "purpose:'
    ' make money" property of "Apple Inc", "Apple Inc" can employ "Steve Jobs" to help it make money, hence we can'
    ' reconstruct the scenario: employment purpose: Steve Jobs is employed by Apple Inc.\n'
    'Reconstruct the third scenario: based on the "purpose: create value" property of "Steve Jobs" and the "form: large'
    ' company" property of "Apple Inc", "Steve Jobs" founded the large company "Apple Inc" to create his value, hence'
    ' we can reconstruct the scenario: creation purpose: Steve Jobs founded Apple Inc.\n'
    'Identify decisive scenario: the scenario "leadership purpose: Steve Jobs manages Apple Inc" contribute the most to'
    ' the relation "top members/employees".\n'
    'Uncover potential relation: if we focus on another scenario "creation purpose: Steve Jobs founded Apple Inc", in'
    ' the scenario, "Steve Jobs" is the founder of "Apple Inc", hence the commonsense relation is "founded by".\n'
    'Replace causal words: to change the original relation to the potential one "founded by", the identified causal'
    ' words can be replaced with "founder of".\n'
    'Output: <e1> Steve Jobs </e1> is the founder of <e2> Apple Inc </e2>\n'
    'New relation: founded by\n'
    '\n'
    'Exam (complete the remaining content and maintain consistency with the format of the above examples):\n'
)


TASK_INCONTEXT_MAPPING = {"tacred_per": TACRED_PER_INCONTEXT,
                          "tacred_org": TACRED_ORG_INCONTEXT,
                          "re-tacred_per": RE_TACRED_PER_INCONTEXT,
                          "re-tacred_org": RE_TACRED_ORG_INCONTEXT}


TACRED_PER_RELATION_EXPLANATION = {
    "per:employee_of": "employee of",
    "per:cities_of_residence": "cities of residence",
    "per:children": "children",
    "per:title": "title",
    "per:siblings": "siblings",
    "per:religion": "religion",
    "per:age": "age",
    "per:stateorprovinces_of_residence": "state or provinces of residence",
    "per:countries_of_residence": "countries of residence",
    "per:spouse": "spouse",
    "per:origin": "origin",
    "per:stateorprovince_of_birth": "state or province of birth",
    "per:date_of_death": "date of death",
    "per:parents": "parents",
    "per:schools_attended": "schools attended",
    "per:cause_of_death": "cause of death",
    "per:city_of_death": "city of death",
    "per:stateorprovince_of_death": "state or province of death",
    "per:country_of_birth": "country of birth",
    "per:date_of_birth": "date of birth",
    "per:city_of_birth": "city of birth",
    "per:charges": "charges",
    "per:country_of_death": "country of death",
}


TACRED_ORG_RELATION_EXPLANATION = {
    "org:founded_by": "founded by",
    "org:website": "website",
    "org:member_of": "member of",
    "org:top_members/employees": "top members/employees",
    "org:city_of_headquarters": "city of headquarters",
    "org:members": "members",
    "org:country_of_headquarters": "country of headquarters",
    "org:stateorprovince_of_headquarters": "state or province of headquarters",
    "org:number_of_employees/members": "number of employees/members",
    "org:parents": "parents",
    "org:subsidiaries": "subsidiaries",
    "org:political/religious_affiliation": "political/religious affiliation",
    "org:dissolved": "dissolved",
    "org:shareholders": "shareholders",
    "org:founded": "founded"
}


RE_TACRED_PER_RELATION_EXPLANATION = {
    "per:children": "children",
    "per:origin": "origin",
    "per:countries_of_residence": "countries of residence",
    "per:employee_of": "employee of",
    "per:title": "title",
    "per:religion": "religion",
    "per:age": "age",
    "per:date_of_death": "date of death",
    "per:stateorprovinces_of_residence": "state or provinces of residence",
    "per:spouse": "spouse",
    "per:siblings": "siblings",
    "per:stateorprovince_of_birth": "state or province of birth",
    "per:parents": "parents",
    "per:charges": "charges",
    "per:schools_attended": "schools attended",
    "per:cause_of_death": "cause of death",
    "per:city_of_death": "city of death",
    "per:stateorprovince_of_death": "state or province of death",
    "per:country_of_death": "country of death",
    "per:country_of_birth": "country of birth",
    "per:date_of_birth": "date of birth",
    "per:cities_of_residence": "cities of residence",
    "per:city_of_birth": "city of birth"
}


RE_TACRED_ORG_RELATION_EXPLANATION = {
    "org:founded_by": "founded by",
    "org:city_of_branch": "city of branch",
    "org:website": "website",
    "org:top_members/employees": "top members/employees",
    "org:number_of_employees/members": "number of employees/members",
    "org:members": "members",
    "org:country_of_branch": "country of branch",
    "org:stateorprovince_of_branch": "state or province of branch",
    "org:political/religious_affiliation": "political/religious affiliation",
    "org:member_of": "member of",
    "org:dissolved": "dissolved",
    "org:shareholders": "shareholders",
    "org:founded": "founded"
}


TACRED_PER_EXPLANATION_RELATION = dict(zip(TACRED_PER_RELATION_EXPLANATION.values(),
                                           TACRED_PER_RELATION_EXPLANATION.keys()))


TACRED_ORG_EXPLANATION_RELATION = dict(zip(TACRED_ORG_RELATION_EXPLANATION.values(),
                                           TACRED_ORG_RELATION_EXPLANATION.keys()))


RE_TACRED_PER_EXPLANATION_RELATION = dict(zip(RE_TACRED_PER_RELATION_EXPLANATION.values(),
                                              RE_TACRED_PER_RELATION_EXPLANATION.keys()))


RE_TACRED_ORG_EXPLANATION_RELATION = dict(zip(RE_TACRED_ORG_RELATION_EXPLANATION.values(),
                                              RE_TACRED_ORG_RELATION_EXPLANATION.keys()))


TASK_RELATION_EXPLANATION_MAPPING = {"tacred_per": TACRED_PER_RELATION_EXPLANATION,
                                     "tacred_org": TACRED_ORG_RELATION_EXPLANATION,
                                     "re-tacred_per": RE_TACRED_PER_RELATION_EXPLANATION,
                                     "re-tacred_org": RE_TACRED_ORG_RELATION_EXPLANATION}


TASK_EXPLANATION_RELATION_MAPPING = {"tacred_per": TACRED_PER_EXPLANATION_RELATION,
                                     "tacred_org": TACRED_ORG_EXPLANATION_RELATION,
                                     "re-tacred_per": RE_TACRED_PER_EXPLANATION_RELATION,
                                     "re-tacred_org": RE_TACRED_ORG_EXPLANATION_RELATION}
