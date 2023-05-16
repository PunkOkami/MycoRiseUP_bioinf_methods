import csv
from pathlib import Path as P
import subprocess

data_file = open('species_freq_table_filtered.tsv')
column_names = data_file.readline().rstrip().split('\t')
data_file.close()
freq_index = column_names.index("Total abundance")
dir_path = P('../Kronas')
dir_path.mkdir(exist_ok=True)

krona_columns = {}
krona_columns["Taxonomy"] = [index for index in range(column_names.index("Kingdom"), column_names.index("Species", 1)+1)]
krona_columns["Guild"] = [column_names.index("Kingdom"), column_names.index("Guild category"), column_names.index("Genus"), column_names.index("Species")]
krona_columns["Custom set"] = [index for index in range(column_names.index("Kingdom"), column_names.index("Guild category")+1)]
krona_columns["Custom set"].remove(freq_index)
for key, value in krona_columns.items():
	new_value = [column_names[index] for index in value]
	krona_columns[key] = new_value
number_of_kronas = int(input('How many Krona charts would you like to generate?\n>>>'))
i = 0
while i < number_of_kronas:
	print(f'Choose one of the following types of Krona charts: {", ".join(krona_columns)}')
	krona_format = input('>>>').strip()
	if krona_format == "Custom set":
		selected_columns = krona_columns[krona_format]
		print('Choose one or more of these available columns, by typing their number separated by coma. Example: "1, 2, 3"')
		for num, col in enumerate(selected_columns):
			print(f'{num} --- {col}')
		col_nums = input(">>>").split(", ")
		col_nums.sort()
		selected_columns = [selected_columns[int(num)] for num in col_nums]
		if 'Guild' in selected_columns:
			selected_columns.remove('Guild')
			if 'Genus' in selected_columns:
				selected_columns.insert(selected_columns.index('Genus'), 'Guild')
			elif 'Species' in selected_columns:
				selected_columns.insert(selected_columns.index('Species'), 'Guild')
			else:
				selected_columns.append('Guild')
		i += 1
	elif krona_format in krona_columns.keys():
		selected_columns = krona_columns[krona_format]
		i += 1
	else:
		print('Please choose one of available options')
		continue
	krona_format = krona_format.lower().replace(" ", "_")
	selected_columns = [column_names.index(col) for col in selected_columns]
	selected_columns.insert(0, freq_index)
	data_file = open('species_freq_table_filtered.tsv')
	data_reader = csv.reader(data_file, delimiter="\t")
	krona_input_file_path = f'krona_input_{krona_format}.tsv'
	krona_input_file_path = P(dir_path, krona_input_file_path)
	krona_input_file = open(krona_input_file_path, mode="w")
	krona_input_writer = csv.writer(krona_input_file, delimiter='\t')
	first_row = True
	for data_row in data_reader:
		if first_row:
			first_row = False
			continue
		krona_row = [data_row[index] for index in selected_columns]
		krona_input_writer.writerow(krona_row)
	data_file.close()
	krona_input_file.close()
	krona_chart_path = P(krona_input_file_path.parent, f'{krona_format}_krona.html')
	subprocess_command = f"ktImportText {krona_input_file_path} -o {krona_chart_path}".split(" ")
	subprocess.run(subprocess_command)
	print(f'Krona chart number {i} generated')
