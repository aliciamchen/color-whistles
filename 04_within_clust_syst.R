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
btwn.clust.systs <- matrix(ncol = 2, nrow = 0)
within.clust.systs <- matrix(ncol = 2, nrow = 0)

# For each participant, extract their signal distances from big pairwise matrix
for (id in speaker.ids) {
  if (id == 'init') {
    next
  }
  
  color.medoids <- matrix(ncol = 3, nrow = 0)
  signal.medoids <- matrix(ncol = 2, nrow = 0)
  
  # Loop through each cluster and calculate within-cluster systematicity
  cluster.systs <- c()
  for (cluster.idx in unique(filter(cluster.info, speaker == id)$cluster_label)) {
    referents.in.cluster <-
      filter(cluster.info, speaker == id, cluster_label == cluster.idx)$referent
    
    # if there's only one referent, ignore
    if (length(referents.in.cluster) == 1) {
      next
    }
    
      signal.indices <-
        which((signal.labels$V2 %in% id) &
                (signal.labels$V3 %in% referents.in.cluster)) # change later for informative column labels
      
      n.signals <- length((signal.indices))
      
      signal.dists <- matrix(NA, nrow = n.signals, ncol = n.signals)
      color.dists <- matrix(NA, nrow =
                              n.signals, ncol = n.signals)
      
      for (i in 1:n.signals) {
        for (j in 1:n.signals) {
          signal.dist <-
            pairwise.dists[signal.indices[i], signal.indices[j]]
          
          color.idx.i <-
            strtoi(signal.labels[signal.indices[i], 4]) + 1 # correct for zero-indexing
          color.idx.j <-
            strtoi(signal.labels[signal.indices[j], 4]) + 1
          color.dist = euclidean(unlist(wcs$luv[[color.idx.i]]), unlist(wcs$luv[[color.idx.j]]))
          
          signal.dists[i, j] <- signal.dist
          color.dists[i, j] <- color.dist
        }
      }
   
      # Within-cluster stuff
      this.cluster.syst <- dcor(signal.dists, color.dists)
      cluster.systs <- c(cluster.systs, this.cluster.syst)
      
      # Between-cluster stuff
      medoid.idx <- which.min(colSums(signal.dists))
      signal.medoid.label <- signal.labels[signal.indices[medoid.idx], ]
      signal.medoid <- filter(cluster.info, speaker == signal.medoid.label$V2, referent == signal.medoid.label$V3)[c("mds_1", "mds_2")]
      color.medoid <- wcs$luv[[strtoi(signal.medoid.label$V4) + 1]]
      
      signal.medoids <- rbind(signal.medoids, signal.medoid)
      color.medoids <- rbind(color.medoids, color.medoid)
    
  }
  
  # Within-cluster systematicity
  within.clust.syst <- mean(cluster.systs)
  within.clust.systs <- rbind(within.clust.systs, c(id, within.clust.syst))
  
  # Between-cluster systematicity
  btwn.clust.syst <- dcor(color.medoids, signal.medoids)
  btwn.clust.systs <- rbind(btwn.clust.systs, c(id, btwn.clust.syst))
}

colnames(btwn.clust.systs) <- c('speaker', 'dcor')
colnames(within.clust.systs) <- c('speaker', 'dcor')

write.csv(btwn.clust.systs, here('test/one2one_btwn_clust_syst_new.csv'), row.names = FALSE)
write.csv(within.clust.systs, here('test/one2one_within_clust_syst_new.csv'), row.names = FALSE)

