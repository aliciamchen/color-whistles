library(here)
library(tidyverse)
library(factoextra)
library(clustertend)

args <- commandArgs(trailingOnly = TRUE)

embedding_file <- args[1]
output.dir <- args[2]

d <- read.csv(here(embedding_file))

speaker.ids = unique(d$speaker)

df = data.frame(matrix(ncol = 2, nrow = 0))

for (id in speaker.ids) {
  filtered.df = d %>%
    filter(speaker == id) %>%
    select(starts_with("mds"))

  res = get_clust_tendency(
    data = filtered.df,
    n = nrow(filtered.df) - 1,
    graph = TRUE,
    seed = 88
  )

  output = c(id, res$hopkins_stat)
  df = rbind(df, output)
}

colnames(df) <- c("speaker", "hopkins_stat")

write.csv(df, here(paste0(output.dir, "/hopkins.csv")), row.names = FALSE)

