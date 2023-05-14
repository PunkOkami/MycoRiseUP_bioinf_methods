# MycoRiseUP bioinformatical methodology
This is a repo of bioinformatical methods and tools used in "Microbiomes of deciduous trees prospective for the forests on the example of small-leaved linden (Tilia cordata, L.) - bioinformatic-phenomic study of seedlings. " and presented at MycoRiseUP! conferance in 2023.


## Overview and description
Pipeline in this repo is a pipeline used in afermntioned student grant project. The project aimed to profile mycobiomes of small-leaved linden (Tilia cordata, L.). However data presented in this repo is a training set from Morasko Meteoryt NR. Main methodolody consists of metabarcoding, OTU clustering, taxonomy assignment, ecological role assignment, pairwise and k-means clustering of samples, computational statistical validation and trophic network construction.

### Sampling
Data used here comes from soil samples of two groups of trees from Morasko Meteoryt NR. 

### Sequencing
Sequencing was perfomed using IONTorrent platform and ITS marker region. 

### Quality filtering and OTU clustering
Quality filtering and OTU clustering was achieved using Qiime2 tool and used commands are listed in file (wpisać nazwę).

### Taxonomic assigment
Taxonomic assigment was done using local BLASTN searching against fungal UNITE database. OTUs that were not found in fungal databse were filtered by count with cut off 10 occurences and then searched for in UNITE databse of all genomes. Next we combined abundance of OTUs assigned to the same species into one record. That gave us 820 species of fungi not counting singletons.

### Guilds and ecological metacategories
Using taxonomic information obtained from UNITE database FUNGuild tool was used to assign guilds. To assure confidence in guild information we kept only data labeled as 'Highly Probable". Later we proposed metacategories based on hierarchical order based on ecological effect on plants: Myc (mycorrhizal of all kinds), Pat (plant pathogen), Sap (saprotrophs of all kinds), End (endophytes), Bcn (biocontrol) and Nop (non-plant specific). Except those 6 we named the rest as ENA (ecologically not assigned)

### Occurance filtering
At this stage we used an abundance filter. We kept only the species that togther constitute over 99% of all hits. The filter left us woth 217 taxa that make up 99.26% of all hits and limited ecological metacategories present to %: Myc, Pat, Sap, Nop and ENA. The make up of taxa and groups can be found in Krona charts: XXX and heatmaps 

### Clustering
Parallel to occurance filtering our pipeline perfomes pair-wise clustering of samples and produces a clustermap showing the pairwise clustering and biodiversity of samples. K-means clustering is based on two biodiversity indexes: Margalef richness index and Simpson eveness index. Both indexes are also validated using boostrap method.

### Network construction
To construct trophic networks we usee NetCoMi R package. When we constructed networks made up of taxa from all metacategories we limit taxa to those that have over 1k hits. We also construct networks of pairs of metacategories and compare taxonomic profile of two sets of samples.

## Authors
Sampling and sequncing: Mikołaj Charchuta - mikcha1@st.amu.edu.pl\
Bioinformatics work: Maksymilian Chmielewski - makchm@st.amu.edu.pl\
Supervisor: Prof. UAM dr hab. Władysław Polcyn - polcyn@amu.edu.pl

## Affiliations
Bioinformatics Section of Natural Sciences Club\
Adam Mickiwicz University in Poznań
