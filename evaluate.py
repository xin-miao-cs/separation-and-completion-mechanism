from model import GPT

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
     'Input: <e1> man </e1> establishes the <e2> company </e2>\n'
     'Entities: man-company\n'
     'Relation: producer-product: producer creates product\n'
     'Identify causal words: the context words "establishes" are causally related to the relation "producer-product:'
     ' producer creates product".\n'
     'Uncover potential relation: apart from the original relation "producer-product: producer creates product", the entity 1'
     ' "man" and the entity 2 "company" can be "member-collection: member is member of collection".\n'
     'Replace causal words: to change the original relation to the potential one "member-collection: member is member of'
     ' collection", the identified causal words can be replaced with "becomes a member of".\n'
     'Output: <e1> man </e1> becomes a member of the <e2> company </e2>\n'
     'New relation: member-collection: member is member of collection\n'
     '\n'
     'Example 2:\n'
     'Input: <e1> man </e1> establishes the <e2> company </e2>\n'
     'Entities: man-company\n'
     'Relation: producer-product: producer creates product\n'
     'Identify causal words: the context words "establishes" are causally related to the relation "producer-product:'
     ' producer creates product".\n'
     'Uncover potential relation: apart from the original relation "producer-product: producer creates product", the entity 1'
     ' "man" and the entity 2 "company" can be "agency-instrument: agency uses instrument".\n'
     'Replace causal words: to change the original relation to the potential one "agency-instrument: agency uses instrument",'
     ' the identified causal words can be replaced with "utilizes".\n'
     'Output: <e1> man </e1> utilizes the <e2> company </e2>\n'
     'New relation: agency-instrument: agency uses instrument\n'
     '\n'
     'Exam (complete the remaining content and maintain consistency with the format of the above examples):\n'
     'Input: <e1> eggs </e1> are moved into a <e2> box </e2>\n'
     'Entities: eggs-box\n'
     'Relation: entity-destination: entity is moved into destination\n'
)

model = GPT("gpt-3.5-turbo-0613", 1000, 0)
answer = model.query(STANDARD_SEMEVAL_INCONTEXT)
print(answer)