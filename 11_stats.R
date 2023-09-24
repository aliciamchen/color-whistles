library(here)
library(tidyverse)
library(lme4)
library(lmerTest)
library(ggthemes)
library(tidyboot)
library(mgcv)
library(readr)

theme_set(theme_classic(base_size = 20))

d <- read.csv(here('test/one2one_sys_disc_agg_new.csv')) %>%
  mutate(paired_comm_score = (own_score + comm_score) / 2, 
         learn_score_norm = (learn_score - min(learn_score, na.rm = TRUE)) / (max(learn_score, na.rm = TRUE) - min(learn_score, na.rm = TRUE)) ,
         alignment_norm = (alignment - min(alignment, na.rm = TRUE)) / (max(alignment, na.rm = TRUE) - min(alignment, na.rm = TRUE)))

d.comm <- read_csv(here('test_output/communication.zip'))


# relationship between learning and communication score

  
ggplot(d, aes(x = learn_score_norm, y = comm_score)) +
  geom_point(size = 4, alpha = 0.8, stroke = 0) +
  geom_smooth(method = 'lm', se = TRUE, fill = "lightblue", color = "black") +
  labs(title = "learning and communication score") +
  geom_hline(yintercept=0.5, color="red", linetype="dashed") +
  theme(axis.ticks.x=element_blank(),
        axis.ticks.y=element_blank()) + 
  ylim(0.35, 1)


ggsave(here("figures/learn_comm.pdf"),
       width = 5,
       height = 4.5)


mod <- lm(comm_score ~ 1 + learn_score_norm,
          data = d)

summary(mod)

# store learning/comm residuals
learn_comm_resid <- rstandard(mod)
d.with.resid <- cbind(na.omit(d), learn_comm_resid)

# relationship between communication round and communication score
d.learn.comm <- d.comm %>% 
  group_by(round) %>% 
  tidyboot_mean(score, na.rm = T)

ggplot(d.learn.comm, aes(x = round, y = empirical_stat)) +
  geom_line() +
  geom_ribbon(aes(ymin=ci_lower, ymax=ci_upper), alpha=0.2) +
  geom_hline(yintercept=0.5, color="red", linetype="dashed") +
  labs(title = "improvement over rounds", y = "communication score") +
  theme(axis.ticks.x=element_blank(),
        axis.ticks.y=element_blank()) +
  ylim(0.35, 1)

ggsave(here("figures/comm_improvement.pdf"),
       width = 4,
       height = 4.5)

comm.score.mod <- gam(score ~ s(round, bs = "cs"),
                      data = d.comm)

summary(comm.score.mod)

# Try linear model (note: doesn't converge)
comm.score.mod.linear <- lmer(score ~ 1 + round + (1 |
                                                     gameid),
                              data = d.comm)

summary(comm.score.mod.linear)


# relationship between discreteness and systematicity
ggplot(d, aes(x = systematicity, y = discreteness, col = comm_score)) +
  geom_point(size = 3.3) + 
  labs(title = "discreteness and global systematicity") +
  theme(axis.ticks.x=element_blank(),
        axis.ticks.y=element_blank())

ggsave(here("figures/disc_sys_perf.pdf"),
       width = 6.5,
       height = 4.5)

disc.sys.mod <- lm(discreteness ~ 1 + systematicity,
                   data = d)

summary(disc.sys.mod)

# histogram of discreteness and systematicity
ggplot(d, aes(x = systematicity)) + 
  geom_histogram()

d %>% 
  summarise(mean = mean(systematicity), sd = sd(systematicity))

d %>% 
  summarize(mean = mean(discreteness), sd = sd(discreteness))

ggplot(d, aes(x = discreteness)) + 
  geom_histogram()

# cut off discreteness and systematicity at median
d.blah <- d %>% 
  mutate(is_discrete = ifelse(discreteness > 0.75, T, F), 
         is_systematic = ifelse(systematicity > 0.5, T, F))

# how many discrete and systematic? 
d.blah %>% 
  group_by(is_discrete, is_systematic) %>% 
  count()

# bar plot
d.bar <- d.blah %>% 
  group_by(is_discrete, is_systematic) %>% 
  tidyboot_mean(comm_score, na.rm = T) %>% 
  mutate(category = case_when(
    is_discrete & is_systematic ~ "D+S+",
    is_discrete & !is_systematic ~ "D+S-",
    !is_discrete & is_systematic ~ "D-S+",
    !is_discrete & !is_systematic ~ "D-S-",
    TRUE ~ "UNKNOWN"
  ))



ggplot(d.bar, aes(x = category, y = empirical_stat)) +
  geom_point(mapping = aes(x = category, y = empirical_stat),
                 size = 2.3,
                 alpha = 1,
                 position = position_dodge(width = 0.8)) +
  geom_errorbar(mapping = aes(x = category, ymin = ci_lower, ymax = ci_upper),
                    position = position_dodge(width = 0.8),
                    size = 1.5,
                    width = 0.09) +
  labs(y = "communication score")

# relationship between discreteness and within- / between-cluster systematicity
ggplot(d, aes(x = btwn_clust_sys, y = discreteness, col = comm_score)) +
  geom_point(size = 2.5) + 
  labs(title = "discreteness and between-cluster systematicity")

ggplot(d, aes(x = within_clust_sys, y = discreteness, col = comm_score)) +
  geom_point(size = 2.5) + 
  labs(title = "discreteness and within-cluster systematicity")

ggplot(d, aes(x = systematicity, y = discreteness, col = comm_score)) +
  geom_point(size = 2.5) + 
  labs(title = "discreteness and systematicity")

ggplot(d, aes(x = within_clust_sys, y = btwn_clust_sys, col = comm_score)) + 
  geom_point(size = 2.5) + 
  labs(title = "within- and between-cluster systematicity")


ggplot(d, aes(x = within_clust_sys, y = btwn_clust_sys, col = systematicity)) + 
  geom_point(size = 2.5) + 
  labs(title = "within- and between-cluster systematicity vs. global systematicity")

ggplot(d, aes(x = systematicity, y = btwn_clust_sys, col = discreteness)) + 
  geom_point(size = 2.5) + 
  labs(title = "")


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
perf.mod <- lmer(scale(comm_score) ~ 1 + scale(discreteness) + scale(systematicity) + (1 | game),
               data = d)

summary(perf.mod)

perf.mod <- lmer(scale(comm_score) ~ 1 + scale(discreteness) + scale(systematicity) * scale(within_clust_sys) * scale(btwn_clust_sys) + (1 | game),
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


# does partner alignment for either discreteness or systematicity predicts better communication? NO

d.alignment <- d %>% 
  group_by(game, paired_comm_score) %>% 
  summarise(
    abs_diff_systematicity = abs(diff(systematicity)),
    abs_diff_discreteness = abs(diff(discreteness)) 
  )

ggplot(d.alignment, aes(x = abs_diff_systematicity, y = abs_diff_discreteness, col = paired_comm_score)) +
  geom_point(size = 2.5)

ggplot(d.alignment, aes(x = abs_diff_systematicity, y = paired_comm_score)) +
  geom_point(size = 2.5)

ggplot(d.alignment, aes(x = abs_diff_discreteness, y = paired_comm_score)) +
  geom_point(size = 2.5)

ggplot(d.alignment, aes(x = alignment, y = paired_comm_score)) +
  geom_point(size = 2.5)

mod <- lm(paired_comm_score ~ 1 + abs_diff_discreteness * abs_diff_systematicity,
                 data = d.alignment)

summary(mod)

# partner alignment for signals 
ggplot(d %>% distinct(alignment_norm, .keep_all = T), aes(x = alignment_norm, y = paired_comm_score)) + 
  geom_point(size = 2.5) 

mod <- lm(paired_comm_score ~ alignment_norm, data = d %>% distinct(alignment_norm, .keep_all = T))
summary(mod) 

ggplot(d, aes(x = alignment, y = comm_score)) + 
  geom_point(size = 2.5)

mod <- lm(comm_score ~ alignment, data = d)
summary(mod)

# there isnt an effect. 
# what about learning score and partner alignment? 
mod <- lm(alignment ~ learn_score, data = d)
summary(mod)

ggplot(d, aes(x = alignment, y = learn_score)) + 
  geom_point(size = 2.5)
