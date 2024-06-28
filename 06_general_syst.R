library(here)
library(tidyverse)
library(energy)
library(jsonlite)

set.seed(111)  # For reproducibility

pairwise.dists <- as.matrix(read_table(here("test_output/pairwise_dists.txt"), col_names = FALSE))
signal.labels <- as.data.frame(read_json(here("test_output/all_signal_labels.json"), simplifyVector = TRUE))
wcs <- read_json(here("tools/wcs_row_F.json"))

euclidean <- function(a, b) sqrt(sum((a - b)^2))

# TODO: filter for speaker ids in init
speaker.ids <- unique(signal.labels[, 2])


systs <- matrix(ncol = 3, nrow = 0)


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


  ### Do permutation test
  # Initialize a vector to store the results of the permutation test
  permuted_dc <- numeric(1000)  # for 1000 permutations

  # Permutation test
  for(i in 1:1000) {
    # Shuffle the rows of the color_distances matrix
    shuffled.color.dists <- color.dists[sample(nrow(color.dists)), ]

    # Calculate and store the distance correlation
    permuted_dc[i] <- dcor(signal.dists, shuffled.color.dists)
  }

  # Assess significance
  observed_rank <- sum(permuted_dc >= systematicity) + 1
  p_value <- observed_rank / (length(permuted_dc) + 1)


  systs <- rbind(systs, c(id, systematicity, p_value))
}

colnames(systs) <- c('speaker', 'dcor', 'p')
systs <- as.data.frame(systs)

hist(as.numeric(systs[2:51, ]$p),
     breaks = 100, # Adjusts the number of bins
     col = "skyblue",
     main = "Histogram of P-values",
     xlab = "P-value",
     border = "black")

# Adding grid lines for better readability
grid(nx = NULL, ny = NULL, col = "gray", lty = "dotted")

# ggplot(as.data.frame(systs), aes(x = p)) +
#   geom_histogram(fill = "blue", color = "black", binwidth = 0.01, stat = "count") +
#   theme_minimal() +
#   ggtitle("Histogram of Values") +
#   xlab("Values") +
#   ylab("Frequency")

write.csv(systs, here('test_output/syst_v2.csv'), row.names = FALSE)

