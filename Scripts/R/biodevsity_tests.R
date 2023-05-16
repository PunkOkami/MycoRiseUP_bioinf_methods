library(pbapply)
library(parallel)
library(abdiv)

# Number of cores is set to work on my personal machine, remember to set it below number of cores you have
ncores = 12

# Reading two sets of data: sampling_data is data with control samples kept and before taxa filtering and using it as referance set to sample from makes data look less like biological data so it's a good referance if data is random or not
sampling_data = read.delim('../../Data/species_freq_table.tsv', sep='\t')
real_data = read.delim('../../Data/species_freq_table_filtered.tsv', sep = '\t')
real_data = real_data[,-c(1, 19:30)]
sampling_data = sampling_data[, -c(1, 21:30)]
real_data = as.matrix(real_data)
row_num = nrow(real_data)
sampling_data = as.matrix(sampling_data)

# Calculating Margalef richness index for both real and boostrap data
col_num = ncol(real_data)
margelef_vector = c()
for (i in 1:col_num) {
  sample = real_data[,i]
  margalef_index = margalef(sample)
  margelef_vector = c(margelef_vector, margalef_index)
}

cl = makeCluster(ncores)
clusterExport(cl=cl, c('sampling_data', 'row_num', 'margalef', 'simpson_e', 'real_data'))
rep_num = 10000
booted_margalef = pbreplicate(rep_num, {
  random_sample = sample(sampling_data, row_num)
  booted_index = margalef(random_sample)
}, cl=cl)

# Finding limits for x to plot all data neatly
x_min = min(c(min(booted_margalef), min(margelef_vector)))
x_max = max(c(max(booted_margalef), max(margelef_vector)))

# Plotting both real data and combined booted and real data
hist(margelef_vector, xlab = 'Margalef index', main = 'Sample data from Morasko')
hist(booted_margalef, xlim = c(x_min, x_max), xlab = 'Margalef index', main = 'Morasko data')
abline(v = margelef_vector, col = "red")
abline(v = max(booted_margalef, na.rm = TRUE), col = "blue")

# Same thing as with Margalef index but for Simpson eveness index
simpson_e_vector = c()
for (i in 1:col_num) {
  sample = real_data[,i]
  simpson_e_index = simpson_e(sample)
  simpson_e_vector = c(simpson_e_vector, simpson_e_index)
}

rep_num = 10000
booted_simpson = pbreplicate(rep_num, {
  random_sample = sample(1:max(real_data), row_num)
  # random_sample = runif(row_num, 0, max(real_data))
  booted_index = simpson_e(random_sample)
}, cl=cl)

# Finding new limits for ploting
x_min = min(c(min(booted_simpson), min(simpson_e_vector)))
x_max = max(c(max(booted_simpson), max(simpson_e_vector)))

# Ploting both real data and combined booted and real data
hist(simpson_e_vector, xlab = 'Simpson index', main = 'Sample data from Morasko')
hist(booted_simpson, xlim = c(x_min, x_max), xlab = 'Simpson index', main = 'Morasko data')
abline(v = simpson_e_vector, col = "red")
abline(v = min(booted_simpson, na.rm = TRUE), col = "blue")
