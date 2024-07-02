library(here)
library(tidyverse)
library(energy)
library(jsonlite)

set.seed(111)

args <- commandArgs(trailingOnly = TRUE)

dists.file <- args[1]
labels.file <- args[2]
output.dir <- args[3]


pairwise.dists <- as.matrix(read_table(here(dists.file), col_names = FALSE))
wcs <- read_json(here("stim/wcs_row_F.json"))

# Read the JSON content as a character string, replace NaNs with "NaN" (as a string), and parse it
json_content <- readLines(here(labels.file), warn = FALSE)
json_text <- paste(json_content, collapse = "\n")
modified_json_text <- gsub("\\bNaN\\b", '"NaN"', json_text)
parsed_json <- fromJSON(modified_json_text, simplifyVector = TRUE)
signal.labels <- as.data.frame(parsed_json)
# signal.labels <- as.data.frame(read_json(here(labels.file), simplifyVector = TRUE))

euclidean <- function(a, b) sqrt(sum((a - b)^2))

# TODO: filter for speaker ids in init
speaker.ids <- unique(signal.labels[, 2])


systs <- matrix(ncol = 3, nrow = 0)

print("Calculating systematicity...")
# For each participant, extract their signal distances from big pairwise matrix
for (id in speaker.ids) {
  print(id)

  signal.indices <- which(signal.labels$V2 %in% id) # change later
  n.signals <- length((signal.indices))

  signal.dists <- matrix(NA, nrow = n.signals, ncol = n.signals)
  color.dists <- matrix(NA, nrow = n.signals, ncol = n.signals)

  for (i in 1:n.signals) {
    for (j in 1:n.signals) {

      signal.dist <- pairwise.dists[signal.indices[i], signal.indices[j]]

      color.idx.i <- strtoi(signal.labels[signal.indices[i], 4]) + 1 # correct for zero-indexing
      color.idx.j <- strtoi(signal.labels[signal.indices[j], 4]) + 1

      color.dist = euclidean(unlist(wcs$luv[[color.idx.i]]), unlist(wcs$luv[[color.idx.j]]))

      signal.dists[i, j] <- signal.dist
      color.dists[i, j] <- color.dist
    }
  }

  # Calculate distance correlation
  systematicity <- dcor(signal.dists, color.dists)


  ### Do permutation test
  permuted_dc <- numeric(10000)
  for(i in 1:10000) {
    shuffled.color.dists <- color.dists[sample(nrow(color.dists)), ]

    permuted_dc[i] <- dcor(signal.dists, shuffled.color.dists)
  }

  # Assess significance
  observed_rank <- sum(permuted_dc >= systematicity) + 1
  p_value <- observed_rank / (length(permuted_dc) + 1)


  systs <- rbind(systs, c(id, systematicity, p_value))
}

colnames(systs) <- c('speaker', 'dcor', 'p')
systs <- as.data.frame(systs)

print("Systematicity calculations complete")

# hist(as.numeric(systs[2:51, ]$p),
#      breaks = 100, # Adjusts the number of bins
#      col = "skyblue",
#      main = "Histogram of P-values",
#      xlab = "P-value",
#      border = "black")

# # Adding grid lines for better readability
# grid(nx = NULL, ny = NULL, col = "gray", lty = "dotted")



write.csv(systs, here(paste0(output.dir, "/systematicity.csv")), row.names = FALSE)

