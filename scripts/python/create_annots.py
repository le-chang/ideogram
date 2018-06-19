''' Creates simulated genome annotation data

Data is currently simulated single-nucleotide variations (SNVs).

TODO:
- Add handling for non-human organisms
- Enhance with more data than simply position, e.g.:
    - Variant type (use Sequence Ontology ID)
    - Molecular consequence (use SO ID)
    - Clinical significance
    - Transcript accession
    - HGVS expression
'''

import json
import random
import argparse

parser = argparse.ArgumentParser(
	description=__doc__,
	formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('--output_dir',
					help='Directory to send output data to',
					default='../../data/annotations/')
parser.add_argument('--num_annots',
					help='Number of annotations to create',
					type=int,
					default=1000)
parser.add_argument('--assembly',
                    help='Genome assembly reference to use: GRCh38 or GRCh37',
                    default='GRCh38')


args = parser.parse_args()
output_dir = args.output_dir
num_annots = args.num_annots
assembly = args.assembly

annots = []

chrs = [
    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10",
    "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
    "21", "22", "X", "Y"
]

lengths_GRCh38 = {
    "1": 248956422, "2": 242193529, "3": 198295559,
    "4": 190214555, "5": 181538259, "6": 170805979,
    "7": 159345973, "8": 145138636, "9": 138394717,
    "10": 133797422, "11": 135086622, "12": 133275309,
    "13": 114364328, "14": 107043718, "15": 101991189,
    "16": 90338345,    "17": 83257441, "18": 80373285,
    "19": 58617616, "20": 64444167, "21": 46709983,
    "22": 50818468, "X": 156040895, "Y": 57227415
}

lengths_GRCh37 = {
    "1": 249250621, "2": 243199373, "3": 198022430,
    "4": 191154276, "5": 180915260, "6": 171115067,
    "7": 159138663, "8": 146364022, "9": 141213431,
    "10": 135534747, "11": 135006516, "12": 133851895,
    "13": 115169878, "14": 107349540, "15": 102531392,
    "16": 90354753, "17": 81195210, "18": 78077248,
    "19": 59128983, "20": 63025520, "21": 48129895,
    "22": 51304566, "X": 155270560, "Y": 59373566
}

if assembly == 'GRCh38':
    chr_lengths = lengths_GRCh38
else:
    chr_lengths = lengths_GRCh37

for chr in chrs:
    annots.append({"chr": chr, "annots": []});

#
trackIndexPool = [0]*5 + [1]*80 + [2]*15
poolSize = len(trackIndexPool)

i = 0
while i < num_annots:
    j = str(i + 1)
    chr = i % 24

    start = int((i * chr_lengths[chrs[chr]])/1000 + 1)
    length = 0

    annot = [
        "rs" + j,
        start,
        length,
        trackIndexPool[random.randrange(0, poolSize - 1)]
    ]

    annots[chr]["annots"].append(annot)

    i += 1

top_annots = {}
top_annots["keys"] = ["name", "start", "length", "trackIndex"]
top_annots["annots"] = annots
annots = json.dumps(top_annots)

num_annots = str(num_annots)
output_path = output_dir + "/" + num_annots + "_virtual_snvs.json"

open(output_path, "w").write(annots)
print(
    'Output ' + num_annots + ' annotations ' +
    'on assembly ' + assembly + ' ' +
    'to ' + output_path
)
