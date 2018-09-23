import xml.sax
import logging as log

class DrugBaseContentHandler(xml.sax.ContentHandler):
    def __init__(self, feature_config):
        xml.sax.ContentHandler.__init__(self)
        self.path = []
        self.primary_id = False
        self.current_id = None
        self.buffer = ""
        self.drugs = dict()
        self.feature_config = feature_config

    def startElement(self, name, attrs):
        self.path.append(name)
        if name == "drugbank-id":
            self.primary_id = 'primary' in attrs and attrs['primary'] == 'true'

    def endElement(self, name):
        for feature_name, feature in self.feature_config.items():
            if feature['pattern'] == tuple(self.path):
                #print ("\t".join((self.current_id, self.path[-1], self.buffer.strip())))
                if feature['cardinality'] == 'single':
                    self.drugs[self.current_id][feature_name] = self.buffer.strip()
                elif  feature['cardinality'] == 'set':
                    if not feature_name in self.drugs[self.current_id]:
                        self.drugs[self.current_id][feature_name] = set()
                    self.drugs[self.current_id][feature_name].add(self.buffer.strip())

        if self.path == ['drugbank', 'drug', 'drugbank-id'] and self.primary_id:
            self.current_id = self.buffer.strip()
            self.drugs[self.current_id] = dict()
            l = len(self.drugs.keys())
            if l % 100 == 0:
                log.info("parsed {0} drugs...".format(l))

        self.buffer = ""
        self.path.pop()

    def characters(self, content):
        self.buffer += content

def parse(database_file, feature_config):
    source = open(database_file, encoding="utf-8")
    parser = DrugBaseContentHandler(feature_config)
    xml.sax.parse(source, parser)
    return parser.drugs
