import seaborn
import matplotlib.pyplot as plt
import csv
import copy
seaborn.set(font_scale=0.6)

# Open data file and reads all metacategories present
data_file = open('../../Data/species_freq_table_filtered.tsv')
data_reader = csv.reader(data_file, delimiter='\t')
guild_set = set()
guild_category_index = 0
first_line = True
for row in data_reader:
	if first_line:
		guild_category_index = row.index('Guild category')
		first_line = False
		continue
	guild_set.add(row[guild_category_index])
guild_set.remove('ENA')

# Prints all cats present and asks user what should be present on
print('Guild categories present in the file, write what categories you want in the heatmap[guild1, guild2, ...]:')
print(', '.join(guild_set))
chosen_guilds = input('>>>').split(', ')
guild_set.intersection_update(chosen_guilds)

# Moves to begining of the file and reads all rows from set categories and sorts rows based on the category
data_file.seek(0)
most_common_dict = {}
freq_data = {}
sample_names = []
sample_indexes = (0, 0)
species_index = 0
total_freq_index = 0
first_line = True
for row in data_reader:
	if first_line:
		total_freq_index = row.index('Total abundance')
		species_index = row.index('Species')
		sample_indexes = (species_index+1, row.index('Kingdom'))
		sample_names = row[sample_indexes[0]:sample_indexes[1]]
		first_line = False
		continue
	guild_category = row[guild_category_index]
	if guild_category in guild_set:
		species = row[species_index]
		total_freq = float(row[total_freq_index])
		nums = [float(num) for num in row[sample_indexes[0]:sample_indexes[1]]]
		guild_data = freq_data.get(guild_category, [])
		guild_data.append(nums)
		freq_data[guild_category] = guild_data
		highest_in_guild = most_common_dict.get(guild_category, ('', 0))

		if highest_in_guild[1] < total_freq:
			highest_in_guild = (species, total_freq)
			most_common_dict[guild_category] = highest_in_guild

# order_on_heatmap is used as a hint on the heatmap to show what is where
order_on_heatmap = list(freq_data.keys())
# This provides statistics for each category selected, helps to understand heatmap and data
guild_population_num = {}
for guild, species in freq_data.items():
	species_num = len(species)
	total_abundance = sum([sum(row) for row in species])
	highest_in_guild = most_common_dict[guild]
	population_data = [species_num, total_abundance]
	population_data.extend(highest_in_guild)
	guild_population_num[guild] = population_data

# Nice table printing of data
print('Guild	-	Number of species	-	Total abundance	-	Most common species	-	Their population')
for guild, population_data in guild_population_num.items():
	output = [str(item) for item in population_data]
	output.insert(0, guild)
	output = '	-	'.join(output)
	print(output)

# Reverse is needed as the first category in data will be on top and in legend would be on the bottom without reversing
order_on_heatmap.reverse()
# Changes data format to fir seaborn and to make it percentile normalisation
heatmap_data = []
for value in freq_data.values():
	copyied = copy.deepcopy(value)
	heatmap_data.extend(copyied)
heatmap_data_flattened = []
for row in heatmap_data:
	heatmap_data_flattened.extend(row)
heatmap_data_flattened.sort()
percentile_dict = {num: round((heatmap_data_flattened.index(num) + 1) / len(heatmap_data_flattened) * 100, 2) for num in heatmap_data_flattened}
for i in range(len(heatmap_data)):
	seq = heatmap_data[i]
	for j in range(len(seq)):
		num = seq[j]
		perc = percentile_dict[num]
		seq[j] = perc
	heatmap_data[i] = seq

# Makes heatmap, adds all labels, titles and shows it
species_guilds_heatmap = seaborn.heatmap(heatmap_data, cmap="crest", yticklabels=False)
species_guilds_heatmap.set_xticklabels(sample_names)
species_guilds_heatmap.set_ylabel('                      '.join(order_on_heatmap), fontsize=10, weight='bold')
species_guilds_heatmap.set_xlabel('Samples', fontsize=15, weight='bold')
plt.xticks(rotation=90)
plt.title(f'Abundance of species in guilds: {", ".join(order_on_heatmap)}\n', fontsize=20)
plt.show()
