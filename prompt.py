

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


STANDARD_SEMEVAL_INCONTEXT = (
     'Task definition: change the relation between entities based on minimal context editing.\n'
     'Instruction: the process can be divided into the following three steps. (1) Identify causal words: find the context'
     ' words that are causally related to the relation. (2) Uncover potential relation: select another commonsense relation'
     ' for the entities from the candidate relations. (3) Replace causal words: replace the identified causal words with'
     ' suitable words to change the original relation to the potential one.\n'
     'Candidate relations:'
     ' message-topic: message describes topic,'
     ' topic-message: topic is reflected in message,'
     ' entity-origin: entity comes from origin,'
     ' origin-entity: origin is source of entity,'
     ' entity-destination: entity is moved into destination,'
     ' destination-entity: destination is destination of entity,'
     ' content-container: content is contained in container,'
     ' container-content: container contains content,'
     ' cause-effect: cause causes effect,'
     ' effect-cause: effect is cased by cause,'
     ' component-whole: component is part of whole,'
     ' whole-component: whole comprises component,'
     ' member-collection: member is member of collection,'
     ' collection-member: collection consists of member,'
     ' instrument-agency: instrument is used by agency,'
     ' agency-instrument: agency uses instrument,'
     ' product-producer: product is produced by producer,'
     ' producer-product: producer creates product.\n'
     '\n'
     'Example 1:\n'
     'Input: <e1> eggs </e1> are moved into a <e2> box </e2>\n'
     'Entities: eggs-box\n'
     'Relation: entity-destination: entity is moved into destination\n'
     'Identify causal words: the context words "moved into" are causally related to the relation "entity-destination: entity'
     ' is moved into destination".\n'
     'Uncover potential relation: apart from the original relation "entity-destination: entity is moved into destination",'
     ' the entity 1 "eggs" can be "content", hence the relation should start with "content-", the entity 2 "box" can be'
     ' "container", hence the relation should be supplemented as "content-container", hence another commonsense relation is'
     ' "content-container: content is contained in container".\n'
     'Replace causal words: to change the original relation to the potential one "content-container: content is contained in'
     ' container", the identified causal words can be replaced with "stored in".\n'
     'Output: <e1> eggs </e1> are stored in a <e2> box </e2>\n'
     'New relation: content-container: content is contained in container\n'
     '\n'
     'Example 2:\n'
     'Input: <e1> eggs </e1> are moved into a <e2> box </e2>\n'
     'Entities: eggs-box\n'
     'Relation: entity-destination: entity is moved into destination\n'
     'Identify causal words: the context words "moved into" are causally related to the relation "entity-destination: entity'
     ' is moved into destination".\n'
     'Uncover potential relation: apart from the original relation "entity-destination: entity is moved into destination",'
     ' the entity 1 "eggs" can be "entity", hence the relation should start with "entity-", the entity 2 "box" can be "origin",'
     ' hence the relation should be supplemented as "entity-origin", hence another commonsense relation is "entity-origin:'
     ' entity comes from origin".\n'
     'Replace causal words: to change the original relation to the potential one "entity-origin: entity comes from origin",'
     ' the identified causal words can be replaced with "from".\n'
     'Output: <e1> eggs </e1> are from a <e2> box </e2>\n'
     'New relation: entity-origin: entity comes from origin\n'
     '\n'
     'Exam (complete the remaining content and maintain consistency with the format of the above examples, if no another'
     ' commonsense relation exists, use the original relation as the potential one):\n'
)


EPISODIC_SEMEVAL_INCONTEXT = (
    'Task definition: change the relation between entities based on minimal context editing.\n'
    'Instruction: the process can be divided into the following six steps. (1) Identify causal words: find the context words'
    ' that are causally related to the relation. (2) Deconstruct entities: based on the attributes of the entities, deconstruct'
    ' the entities into several primary properties. (3) Reconstruct scenarios: based on the deconstructed properties, reconstruct'
    ' the scenarios that the entities may constitute. (4) Identify decisive scenario: select a scenario that contribute the most'
    ' to the relation. (5) Uncover potential relation: select another scenario and match the most suitable relation from the'
    ' candidate relations. (6) Replace causal words: replace the identified causal words with suitable words to change the'
    ' original relation to the potential one.\n'
    'Candidate relations:'
    ' message-topic: message describes topic, topic-message: topic is reflected in message, entity-origin: entity comes'
    ' from origin, origin-entity: origin is source of entity, entity-destination: entity is moved into destination,'
    ' destination-entity: destination is destination of entity, content-container: content is contained in container,'
    ' container-content: container contains content, cause-effect: cause causes effect, effect-cause: effect is cased by'
    ' cause, component-whole: component is part of whole, whole-component: whole comprises component, member-collection:'
    ' member is member of collection, collection-member: collection consists of member, instrument-agency: instrument'
    ' is used by agency, agency-instrument: agency uses instrument, product-producer: product is produced by producer,'
    ' producer-product: producer creates product.\n'
    '\n'
    'Example 1:\n'
    'Input: <e1> eggs </e1> are moved into a <e2> box </e2>\n'
    'Entities: eggs-box\n'
    'Relation: entity-destination: entity is moved into destination\n'
    'Identify causal words: the context words "moved into" are causally related to the relation "entity-destination: entity'
    ' is moved into destination".\n'
    'Deconstruct entities: based on the attributes of the entities, "eggs" can be deconstructed into the several primary'
    ' properties: form: fragile entity, usage: as food, purpose: farm product; "box" can be deconstructed into the several'
    ' primary properties: form: a container, usage: package something, purpose: preserve product.\n'
    'Pair the properties between "eggs" and "box" to reconstruct the following three scenarios:\n'
    'Reconstruct the first scenario: based on the "form: fragile entity" property of "eggs" and the "usage: package something"'
    ' property of "box", "eggs" should be moved into "box" to prevent them from breaking, hence we can reconstruct the scenario:'
    ' protective purpose: put eggs into box.\n'
    'Reconstruct the second scenario: based on the "purpose: farm product" property of "eggs" and the "form: a container"'
    ' property of "box", "eggs" should be contained in "box" for preservation, hence we can reconstruct the scenario:'
    ' preservation purpose: eggs are kept in box.\n'
    'Reconstruct the third scenario: based on the "usage: as food" property of "eggs" and the "purpose: preserve product"'
    ' property of "box", "eggs" should be taken out from "box" before making food, hence we can reconstruct the scenario:'
    ' consumption purpose: take out eggs from box.\n'
    'Identify decisive scenario: the scenario "protective purpose: put eggs into box" contribute the most to the relation'
    ' "entity-destination: entity is moved into destination".\n'
    'Uncover potential relation: if we focus on another scenario "preservation purpose: eggs are kept in box", in the scenario,'
    ' the entity 1 "eggs" is "content", hence the relation should start with "content-", the entity 2 "box" is "container",'
    ' hence the relation should be supplemented as "content-container", hence the commonsense relation is "content-container:'
    ' content is contained in container".\n'
    'Replace causal words: to change the original relation to the potential one "content-container: content is contained in'
    ' container", the identified causal words can be replaced with "stored in".\n'
    'Output: <e1> eggs </e1> are stored in a <e2> box </e2>\n'
    'New relation: content-container: content is contained in container\n'
    '\n'
    'Example 2:\n'
    'Input: <e1> eggs </e1> are moved into a <e2> box </e2>\n'
    'Entities: eggs-box\n'
    'Relation: entity-destination: entity is moved into destination\n'
    'Identify causal words: the context words "moved into" are causally related to the relation "entity-destination: entity'
    ' is moved into destination".\n'
    'Deconstruct entities: based on the attributes of the entities, "eggs" can be deconstructed into the several primary'
    ' properties: form: fragile entity, usage: as food, purpose: farm product; "box" can be deconstructed into the several'
    ' primary properties: form: a container, usage: package something, purpose: preserve product.\n'
    'Pair the properties between "eggs" and "box" to reconstruct the following three scenarios:\n'
    'Reconstruct the first scenario: based on the "form: fragile entity" property of "eggs" and the "usage: package something"'
    ' property of "box", "eggs" should be moved into "box" to prevent them from breaking, hence we can reconstruct the scenario:'
    ' protective purpose: put eggs into box.\n'
    'Reconstruct the second scenario: based on the "purpose: farm product" property of "eggs" and the "form: a container"'
    ' property of "box", "eggs" should be contained in "box" for preservation, hence we can reconstruct the scenario:'
    ' preservation purpose: eggs are kept in box.\n'
    'Reconstruct the third scenario: based on the "usage: as food" property of "eggs" and the "purpose: preserve product"'
    ' property of "box", "eggs" should be taken out from "box" before making food, hence we can reconstruct the scenario:'
    ' consumption purpose: take out eggs from box.\n'
    'Identify decisive scenario: the scenario "protective purpose: put eggs into box" contribute the most to the relation'
    ' "entity-destination: entity is moved into destination".\n'
    'Uncover potential relation: if we focus on another scenario "consumption purpose: take out eggs from box", in the'
    ' scenario, the entity 1 "eggs" is "entity", hence the relation should start with "entity-", the entity 2 "box" is'
    ' "origin", hence the relation should be supplemented as "entity-origin", hence the commonsense relation is'
    ' "entity-origin: entity comes from origin".\n'
    'Replace causal words: to change the original relation to the potential one "entity-origin: entity comes from origin",'
    ' the identified causal words can be replaced with "from".\n'
    'Output: <e1> eggs </e1> are from a <e2> box </e2>\n'
    'New relation: entity-origin: entity comes from origin\n'
    '\n'
    'Exam (complete the remaining content and maintain consistency with the format of the above examples):\n'
)


ACE2005_INCONTEXT = (
    'Task definition: change the relation between entities based on minimal context editing.\n'
    'Instruction: the process can be divided into the following six steps. (1) Identify causal words: find the context'
    ' words that are causally related to the relation. (2) Deconstruct entities: based on the attributes of the entities,'
    ' deconstruct the entities into several primary properties. (3) Reconstruct scenarios: based on the deconstructed'
    ' properties, reconstruct the scenarios that the entities may constitute. (4) Identify decisive scenario: select a'
    ' scenario that contribute the most to the relation. (5) Uncover potential relation: select another scenario and match'
    ' the most suitable relation from the candidate relations. (6) Replace causal words: replace the identified causal'
    ' words with suitable words to change the original relation to the potential one.\n'
    'Candidate relations:'
    ' ORG-AFF: person for organization,'
    ' GEN-AFF: object from region'
    ' ART: person use artifact,'
    ' PHYS: person near location.\n'
    '\n'
    'Example 1:\n'
    'Input: <e1> man </e1> went to the <e2> company </e2>\n'
    'Entities: man-company\n'
    'Relation: PHYS: person near location\n'
    'Identify causal words: the context words "went to" are causally related to the relation "PHYS: person near location".\n'
    'Deconstruct entities: based on the attributes of the entities, "man" can be deconstructed into the several primary'
    ' properties: form: social member, usage: go to work, purpose: create value; "company" can be deconstructed into the'
    ' several primary properties: form: profit organization, usage: hire employee, purpose: make money.\n'
    'Pair the properties between "man" and "company" to reconstruct the following three scenarios:\n'
    'Reconstruct the first scenario: based on the "usage: go to work" property of "man" and the "purpose: make money"'
    ' property of "company", "man" can go to "company" to work for making money, hence we can reconstruct the scenario:'
    ' work purpose: man go to the company.\n'
    'Reconstruct the second scenario: based on the "form: social member" property of "man" and the "usage: hire employee"'
    ' property of "company", "man" as a social member, can be employed by "company", hence we can reconstruct the scenario:'
    ' employment purpose: man is employed by the company.\n'
    'Reconstruct the third scenario: based on the "purpose: create value" property of "man" and the "form: profit organization"'
    ' property of "company", "man" can buy profit-making "company" to create value, hence we can reconstruct the scenario:'
    ' purchase purpose: man buy the company.\n'
    'Identify decisive scenario: the scenario "work purpose: man go to the company" contribute the most to the relation'
    ' "PHYS: person near location".\n'
    'Uncover potential relation: if we focus on another scenario "employment purpose: man is employed by the company", in'
    ' the scenario, "man" is person, "company" is organization, hence the relation between "man" and "company" is "ORG-AFF:'
    ' person for organization".\n'
    'Replace causal words: to change the original relation to the potential one "ORG-AFF: person for organization", the'
    ' identified causal words can be replaced with "for".\n'
    'Output: <e1> man </e1> for the <e2> company </e2>\n'
    'New relation: ORG-AFF: person for organization\n'
    '\n'
    'Example 2:\n'
    'Input: <e1> man </e1> went to the <e2> company </e2>\n'
    'Entities: man-company\n'
    'Relation: PHYS: person near location\n'
    'Identify causal words: the context words "went to" are causally related to the relation "PHYS: person near location".\n'
    'Deconstruct entities: based on the attributes of the entities, "man" can be deconstructed into the several primary'
    ' properties: form: social member, usage: go to work, purpose: create value; "company" can be deconstructed into the'
    ' several primary properties: form: profit organization, usage: hire employee, purpose: make money.\n'
    'Pair the properties between "man" and "company" to reconstruct the following three scenarios:\n'
    'Reconstruct the first scenario: based on the "usage: go to work" property of "man" and the "purpose: make money"'
    ' property of "company", "man" can go to "company" to work for making money, hence we can reconstruct the scenario:'
    ' work purpose: man go to the company.\n'
    'Reconstruct the second scenario: based on the "form: social member" property of "man" and the "usage: hire employee"'
    ' property of "company", "man" as a social member, can be employed by "company", hence we can reconstruct the scenario:'
    ' employment purpose: man is employed by the company.\n'
    'Reconstruct the third scenario: based on the "purpose: create value" property of "man" and the "form: profit organization"'
    ' property of "company", "man" can buy profit-making "company" to create value, hence we can reconstruct the scenario:'
    ' purchase purpose: man buy the company.\n'
    'Identify decisive scenario: the scenario "work purpose: man go to the company" contribute the most to the relation'
    ' "PHYS: person near location".\n'
    'Uncover potential relation: if we focus on another scenario "purchase purpose: man buy the company", in the scenario,'
    ' "man" is person, "company" is artifact, hence the relation between "man" and "company" is "ART: person use artifact"\n'
    'Replace causal words: to change the original relation to the potential one "ART: person use artifact", the identified'
    ' causal words can be replaced with "use".\n'
    'Output: <e1> man </e1> use the <e2> company </e2>\n'
    'New relation: ART: person use artifact\n'
    '\n'
    'Exam (complete the remaining content and maintain consistency with the format of the above examples):\n'
)


TACRED_PER_INCONTEXT = (
    'Task definition: change the relation between entities based on minimal context editing.\n'
    'Instruction: the process can be divided into the following six steps. (1) Identify causal words: find the context'
    ' words that are causally related to the relation. (2) Deconstruct entities: based on the attributes of the entities,'
    ' deconstruct the entities into several primary properties. (3) Reconstruct scenarios: based on the deconstructed'
    ' properties, reconstruct the scenarios that the entities may constitute. (4) Identify decisive scenario: select a'
    ' scenario that contribute the most to the relation. (5) Uncover potential relation: select another scenario and match'
    ' the most suitable relation from the candidate relations. (6) Replace causal words: replace the identified causal'
    ' words with suitable words to change the original relation to the potential one.\n'
    'Candidate relations: employee of, cities of residence, children, title, siblings, religion, age, state or provinces'
    ' of residence, countries of residence, spouse, origin, state or province of birth, date of death, parents, schools'
    ' attended, cause of death, city of death, state or province of death, country of birth, date of birth, city of birth,'
    ' charges, country of death.\n'
    '\n'
    'Example 1:\n'
    'Input: <e1> Jack </e1> is a famous movie director, died at <e2> Los Angeles </e2>\n'
    'Entities: Jack-Los Angeles\n'
    'Relation: city of death\n'
    'Identify causal words: the context words "died at" are causally related to the relation "city of death".\n'
    'Deconstruct entities: based on the attributes of the entities, "Jack" can be deconstructed into the several primary'
    ' properties: form: normal person, usage: learn skills, purpose: raise family; "Los Angeles" can be deconstructed into'
    ' the several primary properties: form: large city, usage: provide shelter, purpose: nurture human.\n'
    'Pair the properties between "Jack" and "Los Angeles" to reconstruct the following three scenarios:\n'
    'Reconstruct the first scenario: based on the "form: normal person" property of "Jack" and the "usage: provide shelter"'
    ' property of "Los Angeles", "Jack" can spend his entire life peacefully in "Los Angeles", hence we can reconstruct the'
    ' scenario: retirement purpose: Jack spend his final moments in Los Angeles.\n'
    'Reconstruct the second scenario: based on the "usage: learn skills" property of "Jack" and the "purpose: nurture human"'
    ' property of "Los Angeles", "Jack" can lean skills and grow up in "Los Angeles", hence we can reconstruct the scenario:'
    ' growth purpose: Jack grow up in Los Angeles.\n'
    'Reconstruct the third scenario: based on the "purpose: raise family" property of "Jack" and the "form: large city"'
    ' property of "Los Angeles", "Jack" can live in "Los Angeles" to make money to raise his family, hence we can reconstruct'
    ' the scenario: survival purpose: Jack live in Los Angeles.\n'
    'Identify decisive scenario: the scenario "retirement purpose: Jack spend his final moments in Los Angeles" contribute'
    ' the most to the relation "city of death".\n'
    'Uncover potential relation: if we focus on another scenario "growth purpose: Jack grow up in Los Angeles", in the'
    ' scenario, "Los Angeles" is the birth city of "Jack", hence the commonsense relation is "city of birth".\n'
    'Replace causal words: to change the original relation to the potential one "city of birth", the identified causal words'
    ' can be replaced with "born in".\n'
    'Output: <e1> Jack </e1> is a famous movie director, born in <e2> Los Angeles </e2>\n'
    'New relation: city of birth\n'
    '\n'
    'Example 2:\n'
    'Input: <e1> Jack </e1> is a famous movie director, died at <e2> Los Angeles </e2>\n'
    'Entities: Jack-Los Angeles\n'
    'Relation: city of death\n'
    'Identify causal words: the context words "died at" are causally related to the relation "city of death".\n'
    'Deconstruct entities: based on the attributes of the entities, "Jack" can be deconstructed into the several primary'
    ' properties: form: normal person, usage: learn skills, purpose: raise family; "Los Angeles" can be deconstructed into'
    ' the several primary properties: form: large city, usage: provide shelter, purpose: nurture human.\n'
    'Pair the properties between "Jack" and "Los Angeles" to reconstruct the following three scenarios:\n'
    'Reconstruct the first scenario: based on the "form: normal person" property of "Jack" and the "usage: provide shelter"'
    ' property of "Los Angeles", "Jack" can spend his entire life peacefully in "Los Angeles", hence we can reconstruct the'
    ' scenario: retirement purpose: Jack spend his final moments in Los Angeles.\n'
    'Reconstruct the second scenario: based on the "usage: learn skills" property of "Jack" and the "purpose: nurture human"'
    ' property of "Los Angeles", "Jack" can lean skills and grow up in "Los Angeles", hence we can reconstruct the scenario:'
    ' growth purpose: Jack grow up in Los Angeles.\n'
    'Reconstruct the third scenario: based on the "purpose: raise family" property of "Jack" and the "form: large city"'
    ' property of "Los Angeles", "Jack" can live in "Los Angeles" to make money to raise his family, hence we can reconstruct'
    ' the scenario: survival purpose: Jack live in Los Angeles.\n'
    'Identify decisive scenario: the scenario "retirement purpose: Jack spend his final moments in Los Angeles" contribute'
    ' the most to the relation "city of death".\n'
    'Uncover potential relation: if we focus on another scenario "survival purpose: Jack live in Los Angeles", in the scenario,'
    ' "Los Angeles" is the residence city of "Jack", hence the commonsense relation is "cities of residence".\n'
    'Replace causal words: to change the original relation to the potential one "cities of residence", the identified causal'
    ' words can be replaced with "reside in".\n'
    'Output: <e1> Jack </e1> is a famous movie director, reside in <e2> Los Angeles </e2>\n'
    'New relation: cities of residence\n'
    '\n'
    'Exam (complete the remaining content and maintain consistency with the format of the above examples):\n'
)


TACRED_ORG_INCONTEXT = (
    'Task definition: change the relation between entities based on minimal context editing.\n'
    'Instruction: the process can be divided into the following six steps. (1) Identify causal words: find the context'
    ' words that are causally related to the relation. (2) Deconstruct entities: based on the attributes of the entities,'
    ' deconstruct the entities into several primary properties. (3) Reconstruct scenarios: based on the deconstructed'
    ' properties, reconstruct the scenarios that the entities may constitute. (4) Identify decisive scenario: select a'
    ' scenario that contribute the most to the relation. (5) Uncover potential relation: select another scenario and match'
    ' the most suitable relation from the candidate relations. (6) Replace causal words: replace the identified causal'
    ' words with suitable words to change the original relation to the potential one.\n'
    'Candidate relations: founded by, website, member of, top members/employees, city of headquarters, members, country of'
    ' headquarters, state or province of headquarters, number of employees/members, parents, subsidiaries, political/religious'
    ' affiliation, dissolved, shareholders, founded.\n'
    '\n'
    'Example 1:\n'
    'Input: <e1> Steve Jobs </e1> is the president of <e2> Apple Inc </e2>\n'
    'Entities: Steve Jobs-Apple Inc\n'
    'Relation: top members/employees\n'
    'Identify causal words: the context words "president of" are causally related to the relation "top members/employees".\n'
    'Deconstruct entities: based on the attributes of the entities, "Steve Jobs" can be deconstructed into the several primary'
    ' properties: form: leading man, usage: complete work, purpose: create value; "Apple Inc" can be deconstructed into the'
    ' several primary properties: form: large company, usage: conduct production, purpose: make money.\n'
    'Pair the properties between "Steve Jobs" and "Apple Inc" to reconstruct the following three scenarios:\n'
    'Reconstruct the first scenario: based on the "form: leading man" property of "Steve Jobs" and the "usage: conduct'
    ' production" property of "Apple Inc", "Steve Jobs" should lead employees to conduct production, hence we can reconstruct'
    ' the scenario: leadership purpose: Steve Jobs manages Apple Inc.\n'
    'Reconstruct the second scenario: based on the "usage: finish work" property of "Steve Jobs" and the "purpose: make'
    ' money" property of "Apple Inc", "Apple Inc" can employ "Steve Jobs" to help it make money, hence we can reconstruct' 
    ' the scenario: employment purpose: Steve Jobs is employed by Apple Inc.\n'
    'Reconstruct the third scenario: based on the "purpose: create value" property of "Steve Jobs" and the "form: large'
    ' company" property of "Apple Inc", "Steve Jobs" founded the large company "Apple Inc" to create his value, hence we'
    ' can reconstruct the scenario: creation purpose: Steve Jobs founded Apple Inc.\n'
    'Identify decisive scenario: the scenario "leadership purpose: Steve Jobs manages Apple Inc" contribute the most to the'
    ' relation "top members/employees".\n'
    'Uncover potential relation: if we focus on another scenario "employment purpose: Steve Jobs is employed by Apple Inc",'
    ' in the scenario, "Steve Jobs" is a member of "Apple Inc", hence the commonsense relation is "member of".\n'
    'Replace causal words: to change the original relation to the potential one "member of",'
    ' the identified causal words can be replaced with "member of".\n'
    'Output: <e1> Steve Jobs </e1> is the member of <e2> Apple Inc </e2>\n'
    'New relation: member of\n'
    '\n'
    'Example 2:\n'
    'Input: <e1> Steve Jobs </e1> is the president of <e2> Apple Inc </e2>\n'
    'Entities: Steve Jobs-Apple Inc\n'
    'Relation: top members/employees\n'
    'Identify causal words: the context words "president of" are causally related to the relation "top members/employees".\n'
    'Deconstruct entities: based on the attributes of the entities, "Steve Jobs" can be deconstructed into the several primary'
    ' properties: form: leading man, usage: complete work, purpose: create value; "Apple Inc" can be deconstructed into the'
    ' several primary properties: form: large company, usage: conduct production, purpose: make money.\n'
    'Pair the properties between "Steve Jobs" and "Apple Inc" to reconstruct the following three scenarios:\n'
    'Reconstruct the first scenario: based on the "form: leading man" property of "Steve Jobs" and the "usage: conduct'
    ' production" property of "Apple Inc", "Steve Jobs" should lead employees to conduct production, hence we can reconstruct'
    ' the scenario: leadership purpose: Steve Jobs manages Apple Inc.\n'
    'Reconstruct the second scenario: based on the "usage: finish work" property of "Steve Jobs" and the "purpose: make'
    ' money" property of "Apple Inc", "Apple Inc" can employ "Steve Jobs" to help it make money, hence we can reconstruct' 
    ' the scenario: employment purpose: Steve Jobs is employed by Apple Inc.\n'
    'Reconstruct the third scenario: based on the "purpose: create value" property of "Steve Jobs" and the "form: large'
    ' company" property of "Apple Inc", "Steve Jobs" founded the large company "Apple Inc" to create his value, hence we'
    ' can reconstruct the scenario: creation purpose: Steve Jobs founded Apple Inc.\n'
    'Identify decisive scenario: the scenario "leadership purpose: Steve Jobs manages Apple Inc" contribute the most to the'
    ' relation "top members/employees".\n'
    'Uncover potential relation: if we focus on another scenario "creation purpose: Steve Jobs founded Apple Inc", in the'
    ' scenario, "Steve Jobs" is the founder of "Apple Inc", hence the commonsense relation is "founded by".\n'
    'Replace causal words: to change the original relation to the potential one "founded by", the identified causal words'
    ' can be replaced with "founder of".\n'
    'Output: <e1> Steve Jobs </e1> is the founder of <e2> Apple Inc </e2>\n'
    'New relation: founded by\n'
    '\n'
    'Exam (complete the remaining content and maintain consistency with the format of the above examples):\n'
)


TASK_INCONTEXT_MAPPING = {"episodic_semeval": EPISODIC_SEMEVAL_INCONTEXT,
                          "ace2005": ACE2005_INCONTEXT,
                          "tacred_per": TACRED_PER_INCONTEXT,
                          "tacred_org": TACRED_ORG_INCONTEXT}


SEMEVAL_RELATION_EXPLANATION = {
    "Message-Topic(e1,e2)": "message-topic: message describes topic",
    "Message-Topic(e2,e1)": "topic-message: topic is reflected in message",
    "Entity-Origin(e1,e2)": "entity-origin: entity comes from origin",
    "Entity-Origin(e2,e1)": "origin-entity: origin is source of entity",
    "Entity-Destination(e1,e2)": "entity-destination: entity is moved into destination",
    "Entity-Destination(e2,e1)": "destination-entity: destination is destination of entity",
    "Content-Container(e1,e2)": "content-container: content is contained in container",
    "Content-Container(e2,e1)": "container-content: container contains content",
    "Cause-Effect(e1,e2)": "cause-effect: cause causes effect",
    "Cause-Effect(e2,e1)": "effect-cause: effect is cased by cause",
    "Component-Whole(e1,e2)": "component-whole: component is part of whole",
    "Component-Whole(e2,e1)": "whole-component: whole comprises component",
    "Member-Collection(e1,e2)": "member-collection: member is member of collection",
    "Member-Collection(e2,e1)": "collection-member: collection consists of member",
    "Instrument-Agency(e1,e2)": "instrument-agency: instrument is used by agency",
    "Instrument-Agency(e2,e1)": "agency-instrument: agency uses instrument",
    "Product-Producer(e1,e2)": "product-producer: product is produced by producer",
    "Product-Producer(e2,e1)": "producer-product: producer creates product"
}


ACE2005_RELATION_EXPLANATION = {
    "ORG-AFF": "ORG-AFF: person for organization",
    "GEN-AFF": "GEN-AFF: object from region",
    "ART": "ART: person use artifact",
    "PHYS": "PHYS: person near location"
}


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


TASK_RELATION_EXPLANATION_MAPPING = {"episodic_semeval": SEMEVAL_RELATION_EXPLANATION,
                                     "ace2005": ACE2005_RELATION_EXPLANATION,
                                     "tacred_per": TACRED_PER_RELATION_EXPLANATION,
                                     "tacred_org": TACRED_ORG_RELATION_EXPLANATION}


SEMEVAL_EXPLANATION_RELATION = dict(zip(SEMEVAL_RELATION_EXPLANATION.values(),
                                        SEMEVAL_RELATION_EXPLANATION.keys()))


ACE2005_EXPLANATION_RELATION = dict(zip(ACE2005_RELATION_EXPLANATION.values(),
                                        ACE2005_RELATION_EXPLANATION.keys()))


TACRED_PER_EXPLANATION_RELATION = dict(zip(TACRED_PER_RELATION_EXPLANATION.values(),
                                           TACRED_PER_RELATION_EXPLANATION.keys()))


TACRED_ORG_EXPLANATION_RELATION = dict(zip(TACRED_ORG_RELATION_EXPLANATION.values(),
                                           TACRED_ORG_RELATION_EXPLANATION.keys()))


TASK_EXPLANATION_RELATION_MAPPING = {"episodic_semeval": SEMEVAL_EXPLANATION_RELATION,
                                     "ace2005": ACE2005_EXPLANATION_RELATION,
                                     "tacred_per": TACRED_PER_EXPLANATION_RELATION,
                                     "tacred_org": TACRED_ORG_EXPLANATION_RELATION}
