library(here)
library(tidyverse)
library(factoextra)
library(clustertend)
library(ggthemes)

d <- read.csv(here('output/embeddings_3d.csv'))
# TODO: get rid of X in first column of CSV

# Loop through participants
# Make a discreteness score for each participant 
# Save in eitehr csv or json file 

df = data.frame(matrix(ncol = 2, nrow = 0))


participants = unique(d$participant)

for (p in participants) {
  filtered_df = d %>% filter(participant == p) %>% 
    select(MDS_1, MDS_2, MDS_3)
  res = get_clust_tendency(
    data = filtered_df, 
    n = nrow(filtered_df) - 1, 
    graph = TRUE,
    seed = 123
  )
  output = c(p, res$hopkins_stat)
  df = rbind(df, output)
}

x <- c("participant", "hopkins_stat")
colnames(df) <- x

write.csv(df, here('output/hopkins_stat.csv'), row.names = FALSE)
