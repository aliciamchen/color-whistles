library(here)
library(tidyverse)
library(ggplot2)
library(ggthemes)

theme_set(theme_classic(base_size = 15))
d <- read.csv(here("test_output/embedding_viz_new.csv"))
d.metrics <- read.csv((here("test/one2one_sys_disc_agg_new.csv")))


# Make color mapping vector
col <- unique(d$referent)
names(col) <- col

# Make list of systematicity, discreteness, communication scores (otherwise labeling doesn't work)
comm_list <- split(d.metrics$comm_score, d.metrics$speaker)
disc_list <- split(d.metrics$discreteness, d.metrics$speaker)
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
      "disc ",
      round(as.numeric(unlist(disc_list[string])), 3),
      "\n",
      "sys ",
      round(as.numeric(unlist(sys_list[string])), 3),
      "\n",
      "al ",
      round(as.numeric(unlist(align_list[string])), 3)
    )
    
  }


# TODO: make outliers a diff shape?? 


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


# Big plot

f = ggplot(d, aes(x = mds_1, y = mds_2)) +
  geom_point(
    aes(color = referent),
    size = 2.7,
    alpha = 0.5,
    stroke = 0
  ) +
  geom_point(
    data = d %>% filter(speaker == 'init'),
    aes(fill = referent),
    size = 4,
    shape = 22,
    stroke = 1.5
  ) +
  scale_color_manual(values = col) +
  scale_fill_manual(values = col) +
  theme(legend.position = "none") +
  coord_fixed()

# +
#   theme(axis.text.x=element_blank(),
#         axis.ticks.x=element_blank(),
#         axis.text.y=element_blank(),
#         axis.ticks.y=element_blank())
# lims(x = c(-7, 6), y = c(-5, 5))

f

ggsave(here("figures/mds_all_init.pdf"),
       f,
       width = 4,
       height = 6)



# filter df for values of mds_1 between 0.5 and 1.5
# and values of mds_2 between 0.5 and 2

# filter for yellow colors: referent_id between 7 and 12
# to pull out for systematicity calculation

df.filtered <-
  d %>% filter(mds_1 > 0.5 &
                 mds_1 < 1.5 &
                 mds_2 > 0.5 & mds_2 < 2 & referent_id > 6 & referent_id < 13)
