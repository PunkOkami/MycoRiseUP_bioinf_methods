import csv

# Opens table of OTUs and merges the data of occurance for those OTUs that have the same species assigned
OTU_file = open('OTU_phylogenetic_table_with_guilds.tsv')
OTU_reader = csv.reader(OTU_file, delimiter='\t')
species_data = {}
first_row = True
taxonomy_indexes = ()
sample_indexes = ()
freq_index = 0
species_index = 0
guild_index = 0
sample_names = []
taxonomy_levels = []
for row in OTU_reader:
	if first_row:
		taxonomy_indexes = (row.index('Kingdom'), row.index('Species'))
		taxonomy_levels = row[taxonomy_indexes[0]: taxonomy_indexes[1] + 1]
		sample_indexes = (row.index('OTU') + 1, taxonomy_indexes[0])
		sample_names = row[sample_indexes[0]: sample_indexes[1]]
		freq_index = row.index('Total abundance')
		species_index = taxonomy_indexes[1]
		guild_index = row.index('Guild')
		first_row = False
		continue
	species = row[species_index]
	sample_data = row[sample_indexes[0]: sample_indexes[1]]
	sample_data = [float(num) for num in sample_data]
	taxonomy = row[taxonomy_indexes[0]: taxonomy_indexes[1] + 1]
	freq = float(row[freq_index])
	guild = row[guild_index]
	species_row = species_data.get(species, [[], [], 0, ''])
	main_sample_data = species_row[0]
	if len(main_sample_data) == 0:
		main_sample_data = sample_data.copy()
	else:
		main_sample_data = [main_sample_data[i] + sample_data[i] for i in range(len(sample_data))]
	species_row[0] = main_sample_data
	if len(species_row[1]) == 0:
		species_row[1] = taxonomy
	species_row[2] = species_row[2] + freq
	species_row[3] = guild
	species_data[species] = species_row
OTU_file.close()

# Creates and fills file table about species, not OTUs
species_freq_table_file = open('species_freq_table.tsv', mode='w')
species_freq_table_writer = csv.writer(species_freq_table_file, delimiter='\t')
fields_names = ['Species']
fields_names.extend(sample_names)
fields_names.extend(taxonomy_levels)
fields_names.append('Total abundance')
fields_names.append('Guild')
species_freq_table_writer.writerow(fields_names)

for (species, species_row) in species_data.items():
	row = [species]
	row.extend(species_row[0])
	row.extend(species_row[1])
	row.append(species_row[2])
	row.append(species_row[3])
	species_freq_table_writer.writerow(row)
