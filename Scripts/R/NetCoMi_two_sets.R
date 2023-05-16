library(NetCoMi)

# Reading data and prepraring it for network costruction with spliting samples into two sets coresponding to two sets of trees
data = read.delim('../../Data/species_freq_table_filtered.tsv', sep='\t')
otu_names = data[,1]
data = data[,-c(1, 19:30)]
data = as.matrix(data)
rownames(data) = otu_names
col_names = colnames(data)
set_A = which(grepl('A', col_names, fixed = TRUE))
set_B = which(grepl('B', col_names, fixed = TRUE))
data = apply(t(data), 2, rev)
set_A = data[set_A,]
set_B = data[set_B,]

# Basic network comparision construction, analysis and plotting with settings that leave 55 species for plot radability
# IMPORTANT: measurePar settiong is very high to make it easier for NetCoMi to create good networks with ~15 samples
net_spring <- netConstruct(data = set_A,
                           data2 = set_B,
                           filtTax = "totalReads",
                           filtTaxPar = list(totalReads = 500),
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
                           centrLCC = FALSE,
                           avDissIgnoreInf = TRUE,
                           sPathNorm = FALSE,
                           clustMethod = "cluster_fast_greedy",
                           hubPar = c("degree", "eigenvector"),
                           hubQuant = 0.9,
                           lnormFit = TRUE,
                           normDeg = FALSE,
                           normBetw = FALSE,
                           normClose = FALSE,
                           normEigen = FALSE)

p <- plot(props_spring,
          sameLayout = TRUE,
          layoutGroup = 'union',
          nodeColor = "cluster",
          nodeSize = "mclr",
          cexTitle = 2,
          repulsion = 0.95,
          labelScale = FALSE,
          cexLabels = 0.7,
          cexHubLabels = 0.7,
          hubBorderCol = "darkgray",
          groupNames = c("Set A", "Set B"),)

legend(-0.25, 1.05, cex = 1.2, title = "estimated association:",
       legend = c("+","-"), lty = 1, lwd = 3, col = c("#009900","red"),
       bty = "n")

