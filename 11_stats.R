library(here)
library(tidyverse)
library(lme4)
library(lmerTest)
library(ggthemes)
library(tidyboot)
library(mgcv)
library(readr)

theme_set(theme_few(base_size = 15))

d <- read.csv(here('test_output/sys_disc_agg.csv')) %>%
  mutate(paired_comm_score = (own_score + comm_score) / 2)

d.comm <- read_csv(here('test_output/communication.zip'))


# relationship between learning and communication score
ggplot(d, aes(x = learn_score, y = comm_score)) +
  geom_point() +
  geom_smooth(method = 'lm')

mod <- lm(comm_score ~ 1 + learn_score,
          data = d)

summary(mod)

# store learning/comm residuals
learn_comm_resid <- rstandard(mod)
d.with.resid <- cbind(na.omit(d), learn_comm_resid)

# relationship between communication round and communication score
ggplot(d.comm, aes(x = round, y = score)) +
  geom_smooth() 

comm.score.mod <- gam(score ~ s(round, bs = "cs"),
                      data = d.comm)

summary(comm.score.mod)

# Try linear model (note: doesn't converge)
comm.score.mod.linear <- lmer(score ~ 1 + round + (1 + round |
                                                     gameid / speakerid),
                              data = d.comm)

summary(comm.score.mod.linear)


# relationship between discreteness and systematicity
ggplot(d, aes(x = systematicity, y = discreteness, col = comm_score)) +
  geom_point(size = 2.5)

disc.sys.mod <- lm(discreteness ~ 1 + systematicity,
                   data = d)

summary(disc.sys.mod)

# relationship between discreteness, systematicity, and performance
perf.mod <- lm(comm_score ~ 1 + discreteness * systematicity,
               data = d)

summary(perf.mod)

# try with paired comm score

perf.mod.paired <- lm(paired_comm_score ~ 1 + discreteness * systematicity,
                      data = d)

summary(perf.mod.paired)

# break down plots into individual systematicity and discreteness vs. performance
ggplot(d, aes(x = systematicity, y = comm_score, col = game)) +
  geom_point(size = 2.5) +
  theme(legend.position = "none") + 
  labs(title = "Systematicity and performance, colored by game")

ggplot(d, aes(x = discreteness, y = comm_score, col = game)) +
  geom_point(size = 2.5) +
  theme(legend.position = "none") + 
  labs(title = "Discreteness and performance, colored by game")

# look at histograms of systematicity and discreteness

ggplot(d, aes(x = systematicity)) +
  geom_histogram(bins = 10) + 
  theme(legend.position = "none")

ggplot(d, aes(x = discreteness)) +
  geom_histogram(bins = 10) + 
  theme(legend.position = "none")

# add in residuals to linear model
perf.mod.resid <- lm(comm_score ~ 1 + discreteness * systematicity + learn_comm_resid,
                     data = d.with.resid)

summary(perf.mod.resid)

# plot residuals vs. performance
ggplot(d.with.resid, aes(x = learn_comm_resid, y = comm_score, col = game)) +
  geom_point(size = 2.5) +
  theme(legend.position = "none") + 
  labs(title = "Residuals and performance, colored by game")

# does this mean htat participants who do better incommunication vs. learning communicate better?

ggplot(d.with.resid,
       aes(x = learn_comm_resid, y = systematicity, col = game)) +
  geom_point(size = 2.5) +
  theme(legend.position = "none")

ggplot(d.with.resid,
       aes(x = learn_comm_resid, y = discreteness, col = game)) +
  geom_point(size = 2.5) +
  theme(legend.position = "none")
