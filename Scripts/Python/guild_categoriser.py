import csv

# Opens file with list of guilds and assigned categories and table file with species data
guild_rename_file = open('guild_list_rename.txt')
species_table = open('species_freq_table.tsv')
species_table_reader = csv.reader(species_table, delimiter='\t')
species_table_with_guild_category = open('species_freq_table_expanded.tsv', mode='w')
species_table_with_guild_category_writer = csv.writer(species_table_with_guild_category, delimiter='\t')

# Reads line after line to create dictionary of guilds and assigned metacategories
guild_category_dict = {}
for line in guild_rename_file:
	line = line.strip()
	if line.startswith('- '):
		line = line.lstrip(' - ').split('\t')
		line = [el for el in line if el != '']
		guild_category_dict[line[0]] = line[1]

# Special case of species that show some influence in lowering number of Pathogens in soil
biocontrol_list = {'Trichoderma_atroviride', 'Trichoderma_harzianum', 'Trichoderma_asperellum', 'Trichoderma_virens', 'Trichoderma_longibrachiatum', 'Trichoderma_viride'}

# Writes table with metacategory assigned
first_line = True
guild_row_index = 0
species_index = 0
for row in species_table_reader:
	if first_line:
		guild_row_index = row.index('Guild')
		species_index = row.index('Species')
		names = row
		names.append('Guild category')
		species_table_with_guild_category_writer.writerow(names)
		first_line = False
		continue
	guild = row[guild_row_index]
	guild_category = guild_category_dict[guild]
	if row[species_index] in biocontrol_list:
		guild_category = 'Bcn'
	new_row = row + [guild_category]
	species_table_with_guild_category_writer.writerow(new_row)
