library(here)
library(tidyverse)
library(energy)
library(jsonlite)

pairwise.dists <-
  as.matrix(read_table(here("test_output/pairwise_dists.txt"), col_names = FALSE))
signal.labels <-
  as.data.frame(read_json(here("test_output/all_signal_labels.json"), simplifyVector = TRUE)) %>%
  rename(
    game = V1,
    speaker = V2,
    referent = V3,
    referent_id = V4
  )
wcs <- read_json(here("tools/wcs_row_F.json"))

speaker.ids <- unique(signal.labels$speaker)
game.ids <- unique(signal.labels$game)

alignments <- matrix(ncol = 2, nrow = 0)

remove_all_na_rows_and_columns <- function(mat1, mat2) {
  # Identify rows where all values are NA in either matrix
  all_na_rows1 <- apply(mat1, 1, function(row) all(is.na(row)))
  all_na_rows2 <- apply(mat2, 1, function(row) all(is.na(row)))
  all_na_rows <- all_na_rows1 | all_na_rows2

  # Identify columns where all values are NA in either matrix
  all_na_cols1 <- apply(mat1, 2, function(col) all(is.na(col)))
  all_na_cols2 <- apply(mat2, 2, function(col) all(is.na(col)))
  all_na_cols <- all_na_cols1 | all_na_cols2

  # Remove those rows and columns from both matrices
  mat1_filtered <- mat1[!all_na_rows, !all_na_cols]
  mat2_filtered <- mat2[!all_na_rows, !all_na_cols]

  return(list(mat1_filtered = mat1_filtered, mat2_filtered = mat2_filtered))
}

# Calculate how similar the signal distances are between the two speakers in each game
# Loop through each game. For each speaker in the game, make one matrix of signal distances
# Then, calculate distance correlation between the matrices
for (id in game.ids) {

  if (id == "NaN") {
    next
  }

  # Find the speaker ids for this game
  game.speaker.ids <-
    unique(signal.labels$speaker[signal.labels$game == id])

  speaker1.signal.indices <-
    which(signal.labels$speaker %in% game.speaker.ids[1])

  speaker2.signal.indices <-
    which(signal.labels$speaker %in% game.speaker.ids[2])

  # make array of available signal indices for each speaker
  signals.speaker1 <- as.integer(unique(signal.labels$referent_id[signal.labels$speaker == game.speaker.ids[1]]))
  signals.speaker2 <- as.integer(unique(signal.labels$referent_id[signal.labels$speaker == game.speaker.ids[2]]))

  n.signals <- 40


  # Make a matrix of signal distances for each speaker
  game.signal.dists.speaker1 <-
    matrix(NA,
           nrow = 40,
           ncol = 40)
  game.signal.dists.speaker2 <-
    matrix(NA,
           nrow = 40,
           ncol = 40)


  for (i in signals.speaker1) {
    for (j in signals.speaker1) {
      speaker1.signal.dist <-
        pairwise.dists[speaker1.signal.indices[i + 1], speaker1.signal.indices[j + 1]]

      game.signal.dists.speaker1[i + 1, j + 1] <- speaker1.signal.dist
    }
  }

  for (i in signals.speaker2) {
    for (j in signals.speaker2) {
      speaker2.signal.dist <-
        pairwise.dists[speaker2.signal.indices[i + 1], speaker2.signal.indices[j + 1]]

      game.signal.dists.speaker2[i+ 1, j + 1] <- speaker2.signal.dist
    }
  }


  # remove rows and columns that are completely comprised of missing values
  result <- remove_all_na_rows_and_columns(game.signal.dists.speaker1, game.signal.dists.speaker2)
  game.signal.dists.speaker1 <- result$mat1_filtered
  game.signal.dists.speaker2 <- result$mat2_filtered



  # Calculate distance correlation between the two matrices
  alignment <-
    dcor(game.signal.dists.speaker1, game.signal.dists.speaker2)
  alignments <- rbind(alignments, c(id, alignment))
}

colnames(alignments) <- c("game", "dcor")


write.csv(alignments, here("test/one2one_alignments.csv"), row.names = FALSE)
