library(NetCoMi)

# Reading data and preparing it for network costruction with filtering out all taxa not found in set metacategories
data = read.delim('../../Data/species_freq_table_filtered.tsv', sep='\t')
guild_we_want = c('Sap', 'Myc')
data = data[data$Guild.category %in% guild_we_want,]
otu_names = data[,1]
data = data[,-c(1, 19:30)]
data = as.matrix(data)
rownames(data) = otu_names
data = apply(t(data), 2, rev)

# Basic single network costruction and analysis to set it ready to plot. Values are set to keep around 100 species
# IMPORTANT: measurePar settiong is very high to make it easier for NetCoMi to create good networks with ~15 samples
net_spring <- netConstruct(data,
                           filtTax = "totalReads",
                           filtTaxPar = list(totalReads = 150),
                           filtSamp = "totalReads",
                           filtSampPar = list(totalReads = 100),
                           measure = "spring",
                           measurePar = list(nlambda=100,
                                             rep.num=10),
                           normMethod = "none",
                           zeroMethod = "none",
                           sparsMethod = "none",
                           dissFunc = "signed",
                           verbose = 3,
                           seed = 123456)

props_spring <- netAnalyze(net_spring,
                           centrLCC = TRUE,
                           clustMethod = "cluster_fast_greedy",
                           hubPar = "eigenvector",
                           weightDeg = FALSE, normDeg = FALSE)

# Simple title pasting to make it look nice and easy to change guilds used
network_title = paste('Species in guilds:', paste(guild_we_want, collapse = ', '), 'over 150 reads')
p <- plot(props_spring,
          nodeColor = "cluster",
          nodeSize = "eigenvector",
          title1 = network_title,
          showTitle = TRUE,
          cexTitle = 1.9,
          repulsion = 0.95,
          labelScale = FALSE,
          cexLabels = 0.7,
          cexHubLabels = 0.9)

legend(0.6, 1.09, cex = 1.5, title = "estimated association:",
       legend = c("+","-"), lty = 1, lwd = 3, col = c("#009900","red"),
       bty = "n")
