import seaborn
import matplotlib.pyplot as plt
import csv
import statistics
import copy
seaborn.set(font_scale=0.6)

# Opens data file and reads all data
file = open("../../Data/species_freq_table.tsv")
data_file = csv.reader(file, delimiter="\t")
freq_data = {}
taxonomy_data = {}
first_row = True
names = []
sample_names = []
for line in data_file:
	if first_row:
		names = line[0:18]
		names.extend(line[20:])
		sample_names = names[1:18]
		first_row = False
		continue
	name = line[0]
	nums = [float(num) for num in line[1:18]]
	nums.append(sum(nums))
	freq_data[name] = nums
	taxonomy = line[20:]
	taxonomy_data[name] = taxonomy


# Starts to change data format to match input for seaborn and filters taxa by occurance. With cuf-off 100 we are left with 99.26%
seq_num_before_filtering = sum([seq[-1] for seq in freq_data.values()])
print(f"Number of hits before filtering: {seq_num_before_filtering}")
heatmap_data = {}
otu_names = list(freq_data.keys())
otu_names = [tup[1] for tup in enumerate(names) if tup[0] % 4 == 0]
for seq, hits in freq_data.items():
	if hits[-1] >= 100:
		heatmap_data[seq] = hits[:-1]
print(f"Number of species after filtering: {len(heatmap_data)}")
seq_num_after_filtering = [sum(seq) for seq in heatmap_data.values()]
print(f"Number of hits after filterin: {sum(seq_num_after_filtering)}")
print(f'Percentage of hits after filtering: {round((sum(seq_num_after_filtering)/seq_num_before_filtering)*100, 2)}%')
print(f"Mean frequency: {round(statistics.mean(seq_num_after_filtering), 2)}")
print(f"Median frequency: {round(statistics.median(seq_num_after_filtering), 2)}")
print(f"Minimal freq of taxa after filtering: {min(seq_num_after_filtering)}")

# Finalises changing data format to fit seaborn and changes it to be percentile table, so heatmap has normalised data. Log scale and other nornmalisation methods show less success
heatmap_data_values = copy.deepcopy(list(heatmap_data.values()))
heatmap_data_flattened = []
for el in heatmap_data_values:
	heatmap_data_flattened.extend(el)
heatmap_data_flattened.sort()
percentile_dict = {num: round((heatmap_data_flattened.index(num) + 1) / len(heatmap_data_flattened) * 100, 2) for num in heatmap_data_flattened}
for i in range(len(heatmap_data_values)):
	seq = heatmap_data_values[i]
	for j in range(len(seq)):
		num = seq[j]
		perc = percentile_dict[num]
		seq[j] = perc
	heatmap_data_values[i] = seq

# Plots heatmap of taxa occurance and clusters pair-wise samples
otu_heat_map = seaborn.clustermap(heatmap_data_values, cmap="crest", row_cluster=False, cbar_pos=(0.1, 0.07, 0.05, 0.735),
								method='ward', xticklabels=sample_names, yticklabels=False)
plt.show()

# Asks if data is accaptable (as this script also filters data) and if 'Y' writes filtered data. I gave it option to not be accaptable so that user can experiment with different cut-offs
ask = input("Is this data acceptable? [Y/N]\n>>>")
if ask == "Y":
	filtered_file = open("../../Data/species_freq_table_filtered.tsv", mode="w")
	filtered_file_writer = csv.writer(filtered_file, delimiter="\t")
	filtered_file_writer.writerow(names)
	for seq, hits in heatmap_data.items():
		row = [seq]
		row.extend(hits)
		taxonomy = taxonomy_data[seq]
		row.extend(taxonomy)
		filtered_file_writer.writerow(row)
