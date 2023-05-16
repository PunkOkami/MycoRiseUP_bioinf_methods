# Opens log file with OTUs not found in database and FASTA file with all sequences to pull out those that are in log file
blast_log_file = open('blast-output-parser.log')
fasta_file = open('dna-sequences.fasta')

# Reads log file and pulls out set of indetifiers
first_line = True
seq_id_list = set()
for line in blast_log_file:
	if first_line:
		first_line = False
		continue
	line = line.rstrip().split(' --- ')
	if float(line[1]) >= 10:
		seq_id_list.add(line[0])
print(len(seq_id_list))

# Creates FASTA file with sequences of those OTUs from log file that have over 10 hits and are liekely to be real species not result of sequencing or isolation errors
dark_matter_fasta_file = open('dark_matter.fasta', mode='w')
seq_line = False
for line in fasta_file:
	line = line.rstrip()
	if seq_line:
		dark_matter_fasta_file.write(f'{line}\n')
		seq_line = False
	if line.startswith('>'):
		line = line.lstrip('>')
		if line in seq_id_list:
			dark_matter_fasta_file.write(f'>{line}\n')
			seq_line = True
