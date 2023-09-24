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
  # signals.speaker1 <-
  #   as.integer(unique(signal.labels$referent_id[signal.labels$speaker == game.speaker.ids[1]]))
  # signals.speaker2 <-
  #   as.integer(unique(signal.labels$referent_id[signal.labels$speaker == game.speaker.ids[2]]))

  n.signals <- 40


  # Make an empty vector of signal distances for each speaker
  game.signal.dists <- numeric(0)

  # For each signal for speaker 1, find the corresponding signal for speaker 2
  # Then find distance between those two signals
  for (i in 1:n.signals) {
    # find the referent id for the signal for speaker 1
    speaker1.signal.referent_id <-
      signal.labels$referent_id[speaker1.signal.indices[i]]
    # find the signal for speaker 2 that corresponds to the same referent
    speaker2.signal.index <-
      speaker2.signal.indices[signal.labels$referent_id[speaker2.signal.indices] == speaker1.signal.referent_id]


    # find the distance between the two signals
    speakers.signal.dist <-
      pairwise.dists[speaker1.signal.indices[i], speaker2.signal.index]


    # find the distance between the two signals
    # speakers.signal.dist <-
    #   pairwise.dists[speaker1.signal.indices[i], speaker2.signal.indices[i]]

    # add the distance to the vector of distances
    game.signal.dists <-
      c(game.signal.dists, speakers.signal.dist)


  }
  # Calculate the mean of the list of distances, make sure to exclude NaNs

  alignment <-
    mean(game.signal.dists, na.rm = TRUE)
  alignments <- rbind(alignments, c(id, alignment))
}

colnames(alignments) <- c("game", "dist")

# Normalize s.t. 0 is least aligned and 1 is most aligned



write.csv(alignments, here("test_output/alignments.csv"), row.names = FALSE)

