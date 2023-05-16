import csv
import numpy as np
from skbio.diversity import alpha_diversity
from random import sample
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from sklearn.cluster import KMeans
from scipy.spatial import ConvexHull

freq_data_file = open('species_freq_table_filtered.tsv')
sampling_data_file = open('species_freq_table_expanded.tsv')
freq_data_reader = csv.reader(freq_data_file, delimiter='\t')
sampling_data_reader = csv.reader(sampling_data_file, delimiter='\t')

sample_names = []
first_line = True
real_data_matrix = []
samples_indexes = slice(0)
sample_num = 0
species_count = 0
for line in freq_data_reader:
	if first_line:
		samples_indexes = slice(line.index('Species')+1, line.index('Kingdom'))
		sample_names = line[samples_indexes]
		sample_num = samples_indexes.stop - samples_indexes.start
		real_data_matrix = [[] for i in range(sample_num)]
		first_line = False
		continue
	line = line[samples_indexes]
	for i in range(sample_num):
		real_data_matrix[i].append(float(line[i]))
	species_count += 1

first_line = True
sample_data_list = []
samples_indexes = slice(0)
sample_num = 0
for line in sampling_data_reader:
	if first_line:
		samples_indexes = slice(line.index('Species')+1, line.index('Kingdom'))
		first_line = False
		continue
	line = line[samples_indexes]
	for num in line:
		sample_data_list.append(float(num))

margalef_of_real_data = list(alpha_diversity('margalef', real_data_matrix))

rep_num = 500
booted_margalefs = []
for i in range(rep_num):
	random_sample = sample(sample_data_list, species_count)
	random_margalef = alpha_diversity('margalef', random_sample)[0]
	booted_margalefs.append(random_margalef)

maxes_in_sample_data = [int(max(sample)) for sample in real_data_matrix]
simpson_of_real_data = list(alpha_diversity('simpson_e', real_data_matrix))
booted_simpsons = []
for i in range(rep_num):
	random_sample = sample(range(0, max(maxes_in_sample_data)), species_count)
	random_simpson = alpha_diversity('simpson_e', random_sample)[0]
	booted_simpsons.append(random_simpson)

all_margalef = margalef_of_real_data.copy()
all_margalef.extend(booted_margalefs)
all_simpson = simpson_of_real_data.copy()
all_simpson.extend(booted_simpsons)
plt.scatter(all_margalef, all_simpson)
plt.title('Alpha diversity')
plt.xlabel('Margalef index')
plt.ylabel('Simpson evenness index')
plt.show()

all_points = [tup for tup in zip(all_margalef, all_simpson)]
sample_points = np.array([tup for tup in zip(margalef_of_real_data, simpson_of_real_data)])
booted_points = np.array([tup for tup in zip(booted_margalefs, booted_simpsons)])
model = KMeans(n_clusters=2)
model.fit(all_points)
labels = model.predict(all_points)
plt.scatter(all_margalef, all_simpson, c=np.array(['green', 'pink', 'red', 'brown'])[np.array(labels)])
plt.scatter(model.cluster_centers_[:, 0], model.cluster_centers_[:, 1], marker='D', s=200, alpha=0.75)
sample_hull = ConvexHull(sample_points)
booted_hull = ConvexHull(booted_points)
sample_hull_x = np.append(sample_points[sample_hull.vertices, 0], sample_points[sample_hull.vertices, 0][0])
sample_hull_y = np.append(sample_points[sample_hull.vertices, 1], sample_points[sample_hull.vertices, 1][0])
booted_hull_x = np.append(booted_points[booted_hull.vertices, 0], booted_points[booted_hull.vertices, 0][0])
booted_hull_y = np.append(booted_points[booted_hull.vertices, 1], booted_points[booted_hull.vertices, 1][0])
plt.fill(booted_hull_x, booted_hull_y, alpha=0.3, c=np.array([0, 0.501, 0]))
plt.fill(sample_hull_x, sample_hull_y, alpha=0.3, c=np.array([1, 0.753, 0.796]))
legend_elements = [Line2D([0], [0], marker='o', color='w', label='Real data', markerfacecolor='pink', markersize=5),
				   Line2D([0], [0], marker='o', color='w', label='Boot data', markerfacecolor='green', markersize=5)]
plt.legend(handles=legend_elements, loc='upper right')
plt.title('Alpha diversity')
plt.xlabel('Margalef index')
plt.ylabel('Simpson evenness index')
plt.show()

model = KMeans(n_clusters=2)
model.fit(sample_points)
labels = model.predict(sample_points)
plt.scatter(margalef_of_real_data, simpson_of_real_data, c=np.array(['brown', 'black', 'red'])[np.array(labels)])
plt.scatter(model.cluster_centers_[:, 0], model.cluster_centers_[:, 1], marker='D', s=200, alpha=0.75)
plt.title('Alpha diversity of real data\n')
plt.xlabel('Margalef index')
plt.ylabel('Simpson evenness index')
plt.show()

print('----------------------')
cluster_list = {}
for (label, sample) in zip(labels, sample_names):
	sample_list = cluster_list.get(label, [])
	sample_list.append(sample)
	cluster_list[label] = sample_list

for key in cluster_list.keys():
	print(f'Cluster {key}:')
	for sample in cluster_list[key]:
		print(f' - {sample}')
	print('----------------------')
