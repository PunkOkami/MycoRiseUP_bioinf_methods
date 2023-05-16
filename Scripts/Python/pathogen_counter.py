import csv

# Reads data and pulls out taxa in metacategory Pathogens
species_table = open('../../Data/species_freq_table_filtered.tsv')
species_reader = csv.reader(species_table, delimiter='\t')

plant_pathogen_dict = {}
for row in species_reader:
	if 'Pat' in row[-1]:
		plant_pathogen_dict[row[0]] = float(row[-3])

# Writes names and the abundance of all taxa pulled out
out_file = open('pathogen_list.txt', mode='w')
out_file.write(f'Liczba gatunków patogenów: {len(plant_pathogen_dict.items())}\n\n')
plant_pathogen_dict = sorted(plant_pathogen_dict.items(), key=lambda x: x[1], reverse=True)
for (pathogen, freq) in plant_pathogen_dict:
	out_file.write(f'{pathogen} - {freq}\n')
