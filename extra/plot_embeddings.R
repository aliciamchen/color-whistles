library(here)
library(tidyverse)
library(ggplot2)
library(ggthemes)

theme_set(theme_classic(base_size = 15))
d <- read.csv(here("outputs/embedding_2d.csv"))
cluster.info <- read.csv(here("outputs/cluster_output.csv"))
d.metrics <- read.csv((here("outputs/all_calculations.csv")))

d <- merge(d, cluster.info %>% filter(min_cluster_size == 2), by = c("game", "speaker", "referent", "referent_id"))

# Make color mapping vector
col <- unique(d$referent)
names(col) <- col

# Make list of systematicity, discreteness, communication scores (otherwise labeling doesn't work)
comm_list <- split(d.metrics$comm_score, d.metrics$speaker)
disc_list <- split(d.metrics$hopkins, d.metrics$speaker)
sys_list <- split(d.metrics$systematicity, d.metrics$speaker)
align_list <- split(d.metrics$alignment, d.metrics$speaker)

# Plot
facet_titler <-
  function(string) {
    paste0(
      "speaker ",
      string,
      "\n",
      "comm score ",
      round(as.numeric(unlist(comm_list[string])), 3),
      # Jank but doesn't work otherwise
      "\n",
      "hop ",
      round(as.numeric(unlist(disc_list[string])), 3),
      "\n",
      "sys ",
      round(as.numeric(unlist(sys_list[string])), 3),
      "\n",
      "al ",
      round(as.numeric(unlist(align_list[string])), 3)
    )

  }


for (g in unique(d$game)) {
  d.this.game = d %>% filter(game == g)

  plot = ggplot(d.this.game, aes(x = mds_1, y = mds_2)) +
    geom_point(aes(color = referent, shape = factor(cluster_label)),
               size = 2,
               alpha = 0.8) +
    scale_fill_manual(values = col) +
    scale_color_manual(values = col) +
    theme(legend.position = "none") +
    lims(x = c(-7, 6), y = c(-5, 5)) +
    facet_wrap( ~ factor(speaker), labeller = as_labeller(facet_titler))

  print(plot)
}


# filter df for values of mds_1 between 0.5 and 1.5
# and values of mds_2 between 0.5 and 2

# filter for yellow colors: referent_id between 7 and 12
# to pull out for systematicity calculation

df.filtered <-
  d %>% filter(mds_1 > 0.5 &
                 mds_1 < 1.5 &
                 mds_2 > 0.5 & mds_2 < 2 & referent_id > 6 & referent_id < 13)
