library(here)
library(tidyverse)
library(lme4)
library(lmerTest)
library(ggthemes)
library(tidyboot)
library(mgcv)
library(readr)

theme_set(theme_few(base_size = 15))

d <- read.csv(here('test/one2one_sys_disc_agg_new.csv')) %>%
  mutate(paired_comm_score = (own_score + comm_score) / 2)

d.comm <- read_csv(here('test_output/communication.zip'))


# relationship between learning and communication score
ggplot(d, aes(x = learn_score, y = comm_score)) +
  geom_point() +
  geom_smooth(method = 'lm') + 
  labs(title = "learning and communication score")

mod <- lm(comm_score ~ 1 + learn_score,
          data = d)

summary(mod)

# store learning/comm residuals
learn_comm_resid <- rstandard(mod)
d.with.resid <- cbind(na.omit(d), learn_comm_resid)

# relationship between communication round and communication score
ggplot(d.comm, aes(x = round, y = score)) +
  geom_smooth() +
  labs(title = "one to one initialization")

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
  geom_point(size = 2.5) + 
  labs(title = "discreteness and global systematicity")

disc.sys.mod <- lm(discreteness ~ 1 + systematicity,
                   data = d)

summary(disc.sys.mod)

# relationship between discreteness and within- / between-cluster systematicity
ggplot(d, aes(x = btwn_clust_sys, y = discreteness, col = comm_score)) +
  geom_point(size = 2.5) + 
  labs(title = "discreteness and between-cluster systematicity")

ggplot(d, aes(x = within_clust_sys, y = discreteness, col = comm_score)) +
  geom_point(size = 2.5) + 
  labs(title = "discreteness and within-cluster systematicity")


ggplot(d, aes(x = within_clust_sys, y = btwn_clust_sys, col = comm_score)) + 
  geom_point(size = 2.5) + 
  labs(title = "within- and between-cluster systematicity")


ggplot(d, aes(x = within_clust_sys, y = btwn_clust_sys, col = systematicity)) + 
  geom_point(size = 2.5) + 
  labs(title = "within- and between-cluster systematicity vs. global systematicity")


# no relationship between between- and within-cluster systematicity
perf.mod <- lm(within_clust_sys ~ 1 + btwn_clust_sys,
               data = d)

summary(perf.mod)

# diff between between and within-cluster systematicity and performance
ggplot(d, aes(x = within_clust_sys - btwn_clust_sys, y = comm_score)) + 
  geom_point(size = 2.5) + 
  geom_smooth(method = "lm") + 
  labs(title = "diff between within- and between-cluster systematicities vs. performance")

perf.mod <- lm(comm_score ~ 1 + abs(within_clust_sys - btwn_clust_sys),
               data = d)

summary(perf.mod)


# relationship between discreteness, systematicity, and performance
perf.mod <- lm(scale(comm_score) ~ 1 + scale(discreteness) * scale(systematicity),
               data = d)

summary(perf.mod)

perf.mod <- lm(scale(comm_score) ~ 1 + scale(discreteness) + scale(systematicity) * scale(within_clust_sys) * scale(btwn_clust_sys),
               data = d)

summary(perf.mod)

bmod <- brm(comm_score ~ discreteness + systematicity * within_clust_sys * btwn_clust_sys,
    family = Beta(),
    data = d,
    chains=4,
    cores=4,
    iter = 8000,
    warmup=2000,
    control = list(adapt_delta = .95, max_treedepth=15))

bmod
describe_posterior(bmod)
pp_check(bmod, ndraws=100)

?betareg
fmod <- betareg(comm_score ~ btwn_clust_sys * within_clust_sys,
                link="logit", data=d)
summary(fmod)

fmod_simple <- lm(comm_score ~ systematicity + discreteness, data=d)
summary(fmod_simple)

ggplot(d, aes(y=btwn_clust_sys, x=systematicity, col=comm_score)) + geom_smooth() + geom_point() +
  scale_color_continuous()

perf.mod <- lm(scale(comm_score) ~ 1  + scale(systematicity) + scale(btwn_clust_sys),
               data = d)

summary(perf.mod)

perf.mod <- lm(scale(comm_score) ~ 1 + scale(discreteness) * scale(within_clust_sys),
               data = d)

summary(perf.mod)

perf.mod <- lm(scale(comm_score) ~ 1 + scale(discreteness) * scale(btwn_clust_sys),
               data = d)

summary(perf.mod)

# try with paired comm score

perf.mod.paired <- lm(paired_comm_score ~ 1 + discreteness * systematicity,
                      data = d)

summary(perf.mod.paired)

# break down plots into individual systematicity and discreteness vs. performance
ggplot(d, aes(x = systematicity, y = comm_score, col = game)) +
  geom_point(size = 2.5) +
  geom_smooth(method = "lm") + 
  theme(legend.position = "none") + 
  labs(title = "global sys and performance, colored by game")

ggplot(d, aes(x = within_clust_sys, y = comm_score, col = game)) +
  geom_point(size = 2.5) +
  geom_smooth(method = "lm") + 
  theme(legend.position = "none") + 
  labs(title = "within-clust sys and performance, colored by game")

ggplot(d, aes(x = btwn_clust_sys, y = comm_score, col = game)) +
  geom_point(size = 2.5) +
  geom_smooth(method = "lm") + 
  theme(legend.position = "none") + 
  labs(title = "between-clust sys and performance, colored by game")

ggplot(d, aes(x = discreteness, y = comm_score, col = game)) +
  geom_point(size = 2.5) +
  theme(legend.position = "none") + 
  labs(title = "Discreteness and performance, colored by game")


ggplot(d, aes(x = btwn_clust_sys, y = comm_score, col = within_clust_sys)) +
  geom_point(size = 2.5) +
  geom_smooth(method = "lm") + 
  labs(title = "between cluster systematicity and performance")

ggplot(d, aes(x = within_clust_sys, y = comm_score, col = btwn_clust_sys)) +
  geom_point(size = 2.5) +
  geom_smooth(method = "lm") + 
  labs(title = "within cluster systematicity and performance")

ggplot(d, aes(x = btwn_clust_sys + within_clust_sys, y = systematicity)) +
  geom_point(size = 2.5) +
  geom_smooth(method = "lm") + 
  labs(title = "breaking down systematicity")
# Some other plots 

# look at histograms of systematicity and discreteness

ggplot(d, aes(x = systematicity)) +
  geom_histogram(bins = 10) + 
  theme(legend.position = "none")

ggplot(d, aes(x = discreteness)) +
  geom_histogram(bins = 10) + 
  theme(legend.position = "none")

# add in residuals to linear model
perf.mod.resid <- lm(scale(comm_score) ~ 1 + scale(discreteness) * scale(systematicity) + scale(learn_comm_resid),
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

