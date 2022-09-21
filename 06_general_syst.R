library(here)
library(tidyverse)
library(energy)
library(jsonlite)

pairwise.dists <- as.matrix(read_table(here("test/one2many_pairwise_dists.txt"), col_names = FALSE))
signal.labels <- as.data.frame(read_json(here("test/one2many_signal_labels.json"), simplifyVector = TRUE))
wcs <- read_json(here("tools/wcs_row_F.json"))

euclidean <- function(a, b) sqrt(sum((a - b)^2))

# TODO: filter for speaker ids in init
speaker.ids <- unique(signal.labels[, 2])


systs <- matrix(ncol = 2, nrow = 0)

# For each participant, extract their signal distances from big pairwise matrix
for (id in speaker.ids) {

  signal.indices <- which(signal.labels$V2 %in% id) # change later
  n.signals <- length((signal.indices))

  signal.dists <- matrix(NA, nrow = n.signals, ncol = n.signals)
  color.dists <- matrix(NA, nrow = n.signals, ncol = n.signals)

  for (i in 1:n.signals) {
    for (j in 1:n.signals) {
      # print(signal.indices[i])
      # print(signal.indices[j])
      # print(pairwise.dists)
      signal.dist <- pairwise.dists[signal.indices[i], signal.indices[j]]

      color.idx.i <- strtoi(signal.labels[signal.indices[i], 4]) + 1 # correct for zero-indexing
      color.idx.j <- strtoi(signal.labels[signal.indices[j], 4]) + 1
      # TODO: index by actual data frame title

      # print(signal.labels[signal.indices[i], 3])
      # print(color.idx.i)
      # print(color.idx.j)
      color.dist = euclidean(unlist(wcs$luv[[color.idx.i]]), unlist(wcs$luv[[color.idx.j]]))

      signal.dists[i, j] <- signal.dist
      color.dists[i, j] <- color.dist
    }
  }

  # Calculate distance correlation
  systematicity <- dcor(signal.dists, color.dists)
  systs <- rbind(systs, c(id, systematicity))
}

colnames(systs) <- c('speaker', 'dcor')

write.csv(systs, here('test/one2many_systematicity.csv'), row.names = FALSE)

