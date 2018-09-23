import os
from xml.etree import ElementTree

filename = 'database.xml'

tree = ElementTree.parse(filename)
drugbank_tag = tree.getroot()
# print(drugbank_tag.tag, drugbank_tag.attrib)

drugs = dict()

for drug_tag in drugbank_tag:
    # print(drug_tag.tag, drug_tag.attrib)

    drug = dict()

    primary_id_tag = drug_tag.find("{http://www.drugbank.ca}drugbank-id[@primary='true']")
    primary_id = primary_id_tag.text

    name_tag = drug_tag.find("{http://www.drugbank.ca}name")
    name = name_tag.text

    description_tag = drug_tag.find("{http://www.drugbank.ca}description")
    description = description_tag.text

    indication_tag = drug_tag.find("{http://www.drugbank.ca}indication")
    indication = indication_tag.text

    # synonyms_tag = drug_tag.find("{http://www.drugbank.ca}synonyms")
    # synonyms=set()
    # for synonym_tag in synonyms_tag:
    #     synonym = synonym_tag.text
    #     synonyms.add(synonym)

    synonym_tags = drug_tag.findall("{http://www.drugbank.ca}synonyms/{http://www.drugbank.ca}synonym")
    synonyms = set()
    for synonym_tag in synonym_tags:
        synonym = synonym_tag.text
        synonyms.add(synonym)

    form_tags = drug_tag.findall(
        "{http://www.drugbank.ca}dosages/{http://www.drugbank.ca}dosage/{http://www.drugbank.ca}form")
    forms = set()
    for form_tag in form_tags:
        form = form_tag.text
        forms.add(form)

    drug['name'] = name
    drug['description'] = description
    drug['indication'] = indication
    drug['synonyms'] = synonyms
    drug['form'] = form

    drugs[primary_id] = drug


print(drugs)
# for drug in drugs.items():
#     print('Drug:', drug)

