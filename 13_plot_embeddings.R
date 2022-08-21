library(here)
library(tidyverse)
library(ggplot2)
library(ggthemes)

theme_set(theme_few(base_size = 15))
d <- read.csv(here("test_output/embedding_viz.csv"))

# Make color mapping vector
col <- unique(d$referent)
names(col) <- col

# todo: savecommunication score, discreteness, systematicity per participant

# Plot
for (g in unique(d$game)) {
  d.this.game = d %>% filter(game == g)
  
  plot = ggplot(d.this.game, aes(x = mds_1, y = mds_2)) +
    geom_point(aes(color = referent), size = 1.5, alpha = 0.6) +
    scale_fill_manual(values = col) + 
    scale_color_manual(values = col) + 
    theme(legend.position = "none") + 
    lims(x = c(-7, 6), y = c(-5, 5)) + 
    facet_wrap(~speaker)
  # TODO: set consistent x and y axes
  
  print(plot)
}


# Big plot

ggplot(d, aes(x = mds_1, y = mds_2)) +
  geom_point(aes(color = referent), size = 1.5, alpha = 0.6) +
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
  # coord_fixed() + 
  lims(x = c(-7, 6), y = c(-5, 5))
