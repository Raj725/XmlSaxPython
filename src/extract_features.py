#!/usr/bin/env python3

import sys
from itertools import combinations
import logging as log
from src.drugbase import parse
# from features import feature_config
# from similarity import *
# from lda import create_model, load_model
import optparse
from os.path import isfile

DEFAULT_LDA = 'lda.model'
DEFAULT_DICTIONARY = 'lda.dict'
DEFAULT_OUTFILE = "pairs.tsv"

log.basicConfig(format='%(levelname)s: %(message)s', level=log.DEBUG)

parser = optparse.OptionParser()

parser.add_option('-d', '--database',
                  dest="database_file")
parser.add_option('-m', '--lda-model',
                  dest="lda_model_file")
parser.add_option('-i', '--dictionary',
                  dest="dictionary_file")
parser.add_option('-o', '--output-file',
                  dest="output_file")

options, remainder = parser.parse_args()

if not options.database_file:
    log.error("Please specify a database file.")
    sys.exit(1)
if not isfile(options.database_file):
    log.error("Database file {0} does not exist, exiting.".format(options.database_file))
    sys.exit(1)
if not options.output_file:
    output_file = DEFAULT_OUTFILE
else:
    output_file = options.output_file

# read the database
drugs = parse(options.database_file, feature_config)

# load or create the LDA model
if options.lda_model_file == None or options.dictionary_file == None:
    if not isfile(DEFAULT_LDA) or not isfile(DEFAULT_DICTIONARY):
        log.info('creating LDA model...')
        texts = []
        for drug, features in drugs.items():
            for feature in features:
                if feature_config[feature]['type'] == 'text':
                    texts.append(features[feature])
        lda, dictionary = create_model(texts)
    else:
        log.info('loading LDA model from default file {0} and dictionary from default file {1}'.format(DEFAULT_LDA, DEFAULT_DICTIONARY))
        lda, dictionary = load_model(DEFAULT_LDA, DEFAULT_DICTIONARY)
else:
    log.info('loading LDA model from file {0} and dictionary from file {1}'.format(options.lda_model_file, options.dictionary_file))
    lda, dictionary = load_model(options.lda_model_file,sys.argv[3])


log.info('computing pairs...')
features = ['name', 'description', 'indication', 'synonyms', 'forms']
with open(output_file, 'w') as fo:
    fo.write("drug1\tdrug2\t")
    fo.write("name.levenhstein\tname.hamming\tname.jaccard\tname.soundex\tname.match_rating\tname.metaphone\tname.nysiis\t")
    fo.write("synonyms.levenhstein\tsynonyms.hamming\tsynonyms.jaccard\tsynonyms.soundex\tsynonyms.match_rating\tsynonyms.metaphone\tsynonyms.nysiis\t")
    fo.write("forms.jaccard_index\n")
    for (drug1, features1), (drug2, features2) in combinations(drugs.items(), 2):
        fo.write("{0}\t{1}\t".format(drug1, drug2))
        fo.write("{0}\t".format(similarity_levenshtein(features1['name'], features2['name'])))
        fo.write("{0}\t".format(similarity_hamming(features1['name'], features2['name'])))
        fo.write("{0}\t".format(similarity_jaccard(features1['name'], features2['name'])))
        fo.write("{0}\t".format(similarity_soundex(features1['name'], features2['name'])))
        fo.write("{0}\t".format(similarity_match_rating(features1['name'], features2['name'])))
        fo.write("{0}\t".format(similarity_metaphone(features1['name'], features2['name'])))
        fo.write("{0}\t".format(similarity_nysiis(features1['name'], features2['name'])))

        if not 'synonyms' in features1:
            synonyms1 = set()
        else:
            synonyms1 = features1['synonyms']
        if not 'synonyms' in features2:
            synonyms2 = set()
        else:
            synonyms2 = features2['synonyms']
        fo.write("{0}\t".format(set_similarity(synonyms1, synonyms2, similarity_levenshtein)))
        fo.write("{0}\t".format(set_similarity(synonyms1, synonyms2, similarity_hamming)))
        fo.write("{0}\t".format(set_similarity(synonyms1, synonyms2, similarity_jaccard)))
        fo.write("{0}\t".format(set_similarity(synonyms1, synonyms2, similarity_soundex)))
        fo.write("{0}\t".format(set_similarity(synonyms1, synonyms2, similarity_match_rating)))
        fo.write("{0}\t".format(set_similarity(synonyms1, synonyms2, similarity_metaphone)))
        fo.write("{0}\t".format(set_similarity(synonyms1, synonyms2, similarity_nysiis)))

        # uncomment these lines to compute the semantic similarities (warning: slow!)
        #fo.write("{0}\t".format(similarity_semantic(features1['indication'], features2['indication'], lda, dictionary)))
        #fo.write("{0}\t".format(similarity_semantic(features1['description'], features2['description'], lda, dictionary)))

        if not 'forms' in features1:
            forms1 = set()
        else:
            forms1 = features1['forms']
        if not 'forms' in features2:
            forms2 = set()
        else:
            forms2 = features2['forms']
        fo.write("{0}\n".format(jaccard_index(forms1, forms2)))
