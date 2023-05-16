import csv
from tqdm import tqdm

# Opens data file outputed by Qiime
OTU_freq_file = open('feature-table.tsv')
OTU_freq_reader = csv.reader(OTU_freq_file, delimiter='\t')
taxonomic_levels = ['Kingdom', 'Phylum', 'Class', 'Order', 'Family', 'Genus', 'Species']

# Reads file and makes two lists that have synced indexes, also counts all OTUs to give total in tqdm pbar
OTU_ids = []
OTU_freqs = []
num_of_queries = 0
sample_names = []
for row in OTU_freq_reader:
	if row[0] == '#OTU ID':
		sample_names = row[1:20]
		continue
	OTU_ids.append(row[0])
	freqs = [float(num) for num in row[1:20]]
	OTU_freqs.append(freqs)
	num_of_queries += 1

# Opens BLAST output file, file to write table to, log file to log OTUs not found in database and tsv file to write query for FUNGuild
blast_file = open('sequences_aligned.tsv')
blast_file_reader = csv.reader(blast_file, delimiter='\t')
otu_file = open('OTU_phylogenetic_table.tsv', mode='w')
otu_file_writer = csv.writer(otu_file, delimiter='\t')
taxa_file_fields = ['OTU']
taxa_file_fields.extend(sample_names)
taxa_file_fields.extend(taxonomic_levels)
taxa_file_fields.append('Total abundance')
otu_file_writer.writerow(taxa_file_fields)
log_file = open('blast-output-parser.log', mode='w')
funguild_input_file = open('OTUs_parsed_for_funguild.tsv', mode='w')
funguild_input_writer = csv.writer(funguild_input_file, delimiter='\t')
funguild_name_row = ['OTU_ID']
funguild_name_row.extend(taxonomic_levels)
funguild_input_writer.writerow(funguild_name_row)

# Creates pbar, initiales all varieables used in loop and parses data into all 3 output files, however it does not write log file as there is num of all OTUs not found in UNITE database
pbar = tqdm(total=num_of_queries)
not_first_record = False
query = ''
freqs = []
fields = []
hit = []
not_found_seqs = []
for line in blast_file_reader:
	if line[0].startswith('# BLAST'):
		if not_first_record:
			if len(hit) == 0:
				not_found_seqs.append(query)
				continue
			freqs = OTU_freqs[OTU_ids.index(query)]
			total_freq = sum(freqs)
			row = [query]
			row.extend(freqs)
			row.extend(hit)
			row.append(total_freq)
			otu_file_writer.writerow(row)
			funguild_row = [query]
			funguild_row.extend(hit)
			funguild_input_writer.writerow(funguild_row)
			query = ''
			fields = []
			hit = []
			pbar.update(1)
		not_first_record = True
	elif line[0].startswith('# Query'):
		query = line[0].split(' ')[2]
	elif line[0].startswith('# Fields'):
		fields = line[0].split(': ')[1].split(', ')
	elif len(hit) == 0 and line[0] == query:
		subject_field_index = fields.index("subject acc.ver")
		hit = line[subject_field_index]
		hit = hit.split('|')[-1]
		hit = [phylo.split('__')[1] for phylo in hit.split(';')]
blast_file.close()

# Writes data to log file, but only if there are any OTUs not found in database
freq = 0
if len(not_found_seqs) != 0:
	log_file.write(f"There are {len(not_found_seqs)} sequences in query that were not found in databases:\n")
	for seq in not_found_seqs:
		freq = OTU_freqs[OTU_ids.index(seq)]
		log_file.write(f'{seq} --- {sum(freq)}\n')
log_file.close()
otu_file.close()

# phylogenetic_translation = {'k': 'kingdom', 'p': 'phylum', 'c': 'class', 'o': 'order', 'f': 'family', 'g': 'genus', 's': 'species'}
