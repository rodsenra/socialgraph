# -*- coding: utf-8 -*-

import os
from zipfile import ZipFile
from StringIO import StringIO
from socialgraph.converter import convert_tsv_into_graphml


dataset_path = os.path.join('..', 'datasets', 'wiki.txt.zip')
input_file = StringIO(ZipFile(dataset_path).read('wiki-Vote.txt'))

output_file = os.path.join('..', 'datasets', 'wiki.graphml')

topics = ['Athletics', 'Cultural Center', 'Dorms', 'Food', 'Groceries']

convert_tsv_into_graphml(input_file, output_file, topics)