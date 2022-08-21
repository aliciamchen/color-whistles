library(here)
library(tidyverse)
library(lme4)
library(lmerTest)
library(ggthemes)
library(tidyboot)


d <- read.csv(here('output/sys_disc_final.csv'))
d.comm <- read.csv(here('output/comm_cleaned.csv'))

d <- d %>% mutate(paired_comm_score = (own_comm_score + partner_comm_score) / 2)

# relationship between learning and communication score
mod <- lm(
  paired_comm_score ~ 1 + learn_score,
  data = d
)

summary(mod)

# TODO: make per-observation csv, per-participant stuff

# relationship between communication round and communication score
comm.score.mod <- lmer(
  score ~ 1 + round + (1 + round | gameid/speakerid), 
  data = d.comm
)

summary(comm.score.mod)

# relationship between discreteness and systematicity
disc.sys.mod <- lm(
  hopkins_stat_norm ~ 1 + colorsignal_corr, 
  data = d
)

summary(disc.sys.mod)

# relationship between discreteness, systematicity, and performance
perf.mod <- lm(
  paired_comm_score ~ 1 + hopkins_stat_norm * colorsignal_corr,
  data = d
)

summary(perf.mod)

