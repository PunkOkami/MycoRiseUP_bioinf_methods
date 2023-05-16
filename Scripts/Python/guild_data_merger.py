import csv

# Opens file with OTU taxonomy, output of FUNGuild and creates file that will have merged data
otu_table = open('OTU_phylogenetic_table.tsv')
otu_reader = csv.reader(otu_table, delimiter='\t')
guild_table = open('OTUs_parsed_for_funguild.guilds.txt')
guild_reader = csv.reader(guild_table, delimiter='\t')
otus_with_guild_file = open('OTU_phylogenetic_table_with_guilds.tsv', mode='w')
otus_with_guild_writer = csv.writer(otus_with_guild_file, delimiter='\t')

# Reads both input files and merges rows knowing that nth row in taxonomy file corresponds to nth row in guild data file
otu_index = 0
taxonomy_indexes = ()
sample_indexes = ()
freq_index = 0
taxonomic_level_index = 0
guild = ''
guild_index = 0
first_row = True
for (otu_row, guild_row) in zip(otu_reader, guild_reader):
	if first_row:
		otu_index = otu_row.index('OTU')
		taxonomy_indexes = (otu_row.index('Kingdom'), otu_row.index('Species') + 1)
		taxonomy_levels = otu_row[taxonomy_indexes[0]: taxonomy_indexes[1]]
		sample_indexes = (otu_index + 1, taxonomy_indexes[0])
		sample_names = otu_row[sample_indexes[0]: sample_indexes[1]]
		freq_index = otu_row.index('Total abundance')
		guild_index = guild_row.index('guild')
		taxonomic_level_index = guild_row.index('taxonomicLevel')
		out_row = ['OTU']
		out_row.extend(sample_names)
		out_row.extend(taxonomy_levels)
		out_row.append(otu_row[freq_index])
		out_row.append('Guild')
		otus_with_guild_writer.writerow(out_row)
		first_row = False
		continue
	otu = otu_row[otu_index]
	taxonomy = otu_row[taxonomy_indexes[0]: taxonomy_indexes[1]]
	sample_data = otu_row[sample_indexes[0]: sample_indexes[1]]
	freq = otu_row[freq_index]
	taxonomic_level = guild_row[taxonomic_level_index]
    # taxonomic_level == '13' means that FUNGuild have data about genus, not higher and it coresponds to 'Highly Probable' flag
	if taxonomic_level == '13':
		guild = guild_row[guild_index]
		guild = guild.split('-')
		guild = ", ".join(guild)
	else:
		guild = 'NA'
	out_row = [otu]
	out_row.extend(sample_data)
	out_row.extend(taxonomy)
	out_row.append(freq)
	out_row.append(guild)
	otus_with_guild_writer.writerow(out_row)
