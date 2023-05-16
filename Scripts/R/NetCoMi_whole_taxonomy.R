library(NetCoMi)

# Reading data and preparing it for network costruction
data = read.delim('../../Data/species_freq_table_filtered.tsv', sep='\t')
otu_names = data[,1]
data = data[,-c(1, 19:30)]
data = as.matrix(data)
rownames(data) = otu_names
data = apply(t(data), 2, rev)

# Basic single network costruction and analysis to set it ready to plot. Values are set to keep around 120 species
# IMPORTANT: measurePar settiong is very high to make it easier for NetCoMi to create good networks with ~15 samples
net_spring <- netConstruct(data,
                           filtTax = "totalReads",
                           filtTaxPar = list(totalReads = 1000),
                           filtSamp = "totalReads",
                           filtSampPar = list(totalReads = 1000),
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

p <- plot(props_spring,
          nodeColor = "cluster",
          nodeSize = "eigenvector",
          title1 = "Species with over 1000 sequences found",
          showTitle = TRUE,
          cexTitle = 1.9,
          repulsion = 0.95,
          labelScale = FALSE,
          cexLabels = 0.7,
          cexHubLabels = 0.9)

legend(0.7, 1, cex = 1.1, title = "estimated association:",
       legend = c("+","-"), lty = 1, lwd = 3, col = c("#009900","red"),
       bty = "n")

