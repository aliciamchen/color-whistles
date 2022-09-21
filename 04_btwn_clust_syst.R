library(here)
library(tidyverse)
library(energy)
library(jsonlite)

pairwise.dists <-
  as.matrix(read_table(here("test_output/pairwise_dists.txt"), col_names = FALSE))
signal.labels <-
  as.data.frame(read_json(here("test_output/all_signal_labels.json"), simplifyVector = TRUE))
cluster.info <- read_csv(here("test_output/embedding_viz.csv"))


wcs <- read_json(here("tools/wcs_row_F.json"))

euclidean <- function(a, b)
  sqrt(sum((a - b) ^ 2))



speaker.ids <- unique(signal.labels[, 2])
systs <- matrix(ncol = 2, nrow = 0)

# For each participant, extract their signal distances from big pairwise matrix
for (id in speaker.ids) {
  if (id == 'init') {
    next
  }
  
  color.centroids <- matrix(ncol = 3, nrow = 0)
  signal.centroids <- matrix(ncol = 2, nrow = 0)
  
  for (cluster.idx in unique(filter(cluster.info, speaker == id)$cluster_label)) {
    referents.ids.in.cluster <-
      filter(cluster.info, speaker == id, cluster_label == cluster.idx)$referent_id
    
    # calculate color centroid
    luv.coords <- matrix(nrow = 0, ncol = 3)
    for (ref.id in referents.ids.in.cluster) {
      luv.coords <- rbind(luv.coords, as.numeric(wcs$luv[[ref.id + 1]])) # because of zero-indexing
    }
    
    color.centroid <- colMeans(luv.coords)
    color.centroids <- rbind(color.centroids, color.centroid)
    
    # calculate signal centroid
    signal.centroid <-
      as.vector(colMeans(
        filter(cluster.info, speaker == id, cluster_label == cluster.idx)[c("mds_1", "mds_2")]
      ))
    
    signal.centroids <- rbind(signal.centroids, signal.centroid)
    
  }
  
  # Calculate distance correlation
  systematicity <- dcor(color.centroids, signal.centroids)
  systs <- rbind(systs, c(id, systematicity))
}

colnames(systs) <- c('speaker', 'dcor')

write.csv(systs,
          here('test/one2one_betwn_clust_syst.csv'),
          row.names = FALSE)

