# -*- coding: utf-8 -*-


semeval_prompt = (
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
    "Candidate relations:"
    " message-topic: message describes topic,"
    " topic-message: topic is reflected in message,"
    " entity-origin: entity comes from origin,"
    " origin-entity: origin is source of entity,"
    " entity-destination: entity is moved into destination,"
    " destination-entity: destination is destination of entity,"
    " content-container: content is contained in container,"
    " container-content: container contains content,"
    " cause-effect: cause causes effect,"
    " effect-cause: effect is cased by cause,"
    " component-whole: component is part of whole,"
    " whole-component: whole comprises component,"
    " member-collection: member is member of collection,"
    " collection-member: collection consists of member,"
    " instrument-agency: instrument is used by agency,"
    " agency-instrument: agency uses instrument,"
    " product-producer: product is produced by producer,"
    " producer-product: producer creates product.\n"
    "\n"
    "Example 1:\n"
    "Input: <e1> eggs </e1> are moved into a <e2> box </e2>\n"
    "Entities: eggs-box\n"
    "Relation: entity-destination: entity is moved into destination\n"
    'Identify causal words: the context words "moved into" are causally related to the relation'
    ' "entity-destination: entity is moved into destination".\n'
    'Deconstruct entities: based on the attributes of the entities, "eggs" can be deconstructed'
    " into the several primary properties: form: fragile entity, usage: as food, purpose: farm"
    ' product; "box" can be deconstructed into the several primary properties: form: a container,'
    " usage: package something, purpose: preserve product.\n"
    'Pair the properties between "eggs" and "box" to reconstruct the following three scenarios:\n'
    'Reconstruct the first scenario: based on the "form: fragile entity" property of "eggs" and'
    ' the "usage: package something" property of "box", "eggs" should be moved into "box" to'
    " prevent them from breaking, hence we can reconstruct the scenario: protective purpose: put"
    " eggs into box.\n"
    'Reconstruct the second scenario: based on the "purpose: farm product" property of "eggs"'
    ' and the "form: a container" property of "box", "eggs" should be contained in "box" for'
    " preservation, hence we can reconstruct the scenario: preservation purpose: eggs are kept"
    " in box.\n"
    'Reconstruct the third scenario: based on the "usage: as food" property of "eggs" and'
    ' the "purpose: preserve product" property of "box", "eggs" should be taken out from "box"'
    " before making food, hence we can reconstruct the scenario: consumption purpose: take out"
    " eggs from box.\n"
    'Identify decisive scenario: the scenario "protective purpose: put eggs into box" contribute'
    ' the most to the relation "entity-destination: entity is moved into destination".\n'
    'Uncover potential relation: if we focus on another scenario "preservation purpose: eggs are'
    ' kept in box", in the scenario, the entity 1 "eggs" is "content", hence the relation should'
    ' start with "content-", the entity 2 "box" is "container", hence the relation should be'
    ' supplemented as "content-container", hence the commonsense relation is "content-container:'
    ' content is contained in container".\n'
    'Replace causal words: to change the original relation to the potential one "content-container:'
    ' content is contained in container", the identified causal words can be replaced with "stored'
    ' in".\n'
    "Output: <e1> eggs </e1> are stored in a <e2> box </e2>\n"
    "New relation: content-container: content is contained in container\n"
    "\n"
    "Example 2:\n"
    "Input: <e1> eggs </e1> are moved into a <e2> box </e2>\n"
    "Entities: eggs-box\n"
    "Relation: entity-destination: entity is moved into destination\n"
    'Identify causal words: the context words "moved into" are causally related to the relation'
    ' "entity-destination: entity is moved into destination".\n'
    'Deconstruct entities: based on the attributes of the entities, "eggs" can be deconstructed'
    " into the several primary properties: form: fragile entity, usage: as food, purpose: farm"
    ' product; "box" can be deconstructed into the several primary properties: form: a container,'
    " usage: package something, purpose: preserve product.\n"
    'Pair the properties between "eggs" and "box" to reconstruct the following three scenarios:\n'
    'Reconstruct the first scenario: based on the "form: fragile entity" property of "eggs" and'
    ' the "usage: package something" property of "box", "eggs" should be moved into "box" to'
    " prevent them from breaking, hence we can reconstruct the scenario: protective purpose: put"
    " eggs into box.\n"
    'Reconstruct the second scenario: based on the "purpose: farm product" property of "eggs"'
    ' and the "form: a container" property of "box", "eggs" should be contained in "box" for'
    " preservation, hence we can reconstruct the scenario: preservation purpose: eggs are kept"
    " in box.\n"
    'Reconstruct the third scenario: based on the "usage: as food" property of "eggs" and'
    ' the "purpose: preserve product" property of "box", "eggs" should be taken out from "box"'
    " before making food, hence we can reconstruct the scenario: consumption purpose: take out"
    " eggs from box.\n"
    'Identify decisive scenario: the scenario "protective purpose: put eggs into box" contribute'
    ' the most to the relation "entity-destination: entity is moved into destination".\n'
    'Uncover potential relation: if we focus on another scenario "consumption purpose: take out'
    ' eggs from box", in the scenario, the entity 1 "eggs" is "entity", hence the relation should'
    ' start with "entity-", the entity 2 "box" is "origin", hence the relation should be'
    ' supplemented as "entity-origin", hence the commonsense relation is "entity-origin: entity'
    ' comes from origin".\n'
    'Replace causal words: to change the original relation to the potential one "entity-origin:'
    ' entity comes from origin", the identified causal words can be replaced with "from".\n'
    "Output: <e1> eggs </e1> are from a <e2> box </e2>\n"
    "New relation: entity-origin: entity comes from origin\n"
    "\n"
    "Exam (complete the remaining content and maintain consistency with the format of the above"
    " examples):\n"
)