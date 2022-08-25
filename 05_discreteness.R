library(here)
library(tidyverse)
library(factoextra)
library(clustertend)


d <- read.csv(here('test/one2many_embedding_disc.csv'))

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

write.csv(df, here('test/one2many_discreteness.csv'), row.names = FALSE)

