# -*- coding: utf-8 -*-


semeval_prompt = "Task definition: explain the relation based on the known basic information.\n" \
                 "Instruction: a detailed explanation consisting of subject-verb-object structure," \
                 " the subject and object are already known, please add the appropriate verb phrase.\n" \
                 "Notation: maintain the order of entities in the explanation.\n" \
                 "\n" \
                 "Example 1:\n" \
                 "Relation: message-topic\n" \
                 "Explanation: message describes topic\n" \
                 "\n" \
                 "Example 2:\n" \
                 "Relation: topic-message\n" \
                 "Explanation: topic is reflected in message\n" \
                 "\n" \
                 "Example 3:\n" \
                 "Relation: entity-origin\n" \
                 "Explanation: entity comes from origin\n" \
                 "\n" \
                 "Example 4:\n" \
                 "Relation: origin-entity\n" \
                 "Explanation: origin is source of entity\n" \
                 "\n" \
                 "Example 5:\n" \
                 "Relation: entity-destination\n" \
                 "Explanation: entity is moved into destination\n" \
                 "\n" \
                 "Example 6:\n" \
                 "Relation: destination-entity\n" \
                 "Explanation: destination is destination of entity\n" \
                 "\n" \
                 "Exam (complete the remaining content and maintain consistency with the format of the above" \
                 " examples):\n"


tacred_prompt = ""

