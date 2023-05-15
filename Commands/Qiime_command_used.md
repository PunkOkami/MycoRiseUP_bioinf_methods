# Qiime2 commads used to filter reads and cluster them into OTUs

1. `qiime tools import  --type 'SampleData[SequencesWithQuality]'  --input-format CasavaOneEightLanelessPerSampleDirFmt  --input-path Raw_Data  --output-path raw_data.qza`
2. `qiime quality-filter q-score --i-demux raw_data.qza \\n--o-filtered-sequences filtered.qza --o-filter-stats filtered_stats.qza`
3. `qiime metadata tabulate --m-input-file filtered_stats.qza --o-visualization filtered_stats_v.qzv`
4. `qiime vsearch dereplicate-sequences --i-sequences filtered.qza --o-dereplicated-table table.qza --o-dereplicated-sequences rep-seqs.qza`
5. `qiime vsearch cluster-features-de-novo  --i-table table.qza  --i-sequences rep-seqs.qza  --p-perc-identity 0.97  --o-clustered-table clust-table-dn-97.qza  --o-clustered-sequences clust-seqs-dn-97.qza`
6. `qiime feature-table summarize  --i-table clust-table-dn-97.qza  --o-visualization table.qzv`
7. `qiime feature-table tabulate-seqs  --i-data clust-seqs-dn-97.qza  --o-visualization clust-seqs.qzv`
8. `qiime tools export --input-path clust-table-dn-97.qza --output-path OTU_data`
9. `qiime tools export --input-path clust-seqs-dn-97.qza --output-path OTU_data`
