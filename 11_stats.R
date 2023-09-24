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
  mutate(
    paired_comm_score = (own_score + comm_score) / 2,
    learn_score_norm = (learn_score - min(learn_score, na.rm = TRUE)) / (max(learn_score, na.rm = TRUE) - min(learn_score, na.rm = TRUE)) ,
    alignment_norm = (alignment - min(alignment, na.rm = TRUE)) / (max(alignment, na.rm = TRUE) - min(alignment, na.rm = TRUE))
  )

d.comm <- read_csv(here('test_output/communication.zip'))


# relationship between learning and communication score

ggplot(d, aes(x = learn_score_norm, y = comm_score)) +
  geom_point(size = 4,
             alpha = 0.8,
             stroke = 0) +
  geom_smooth(
    method = 'lm',
    se = TRUE,
    fill = "lightblue",
    color = "black"
  ) +
  labs(title = "learning and communication score") +
  geom_hline(yintercept = 0.5,
             color = "red",
             linetype = "dashed") +
  theme(axis.ticks.x = element_blank(),
        axis.ticks.y = element_blank()) +
  ylim(0.35, 1)


ggsave(here("figures/learn_comm.pdf"),
       width = 5,
       height = 4.5)


mod <- lm(comm_score ~ 1 + learn_score_norm,
          data = d)

summary(mod)

# relationship between communication round and communication score
d.learn.comm <- d.comm %>%
  group_by(round) %>%
  tidyboot_mean(score, na.rm = T)

ggplot(d.learn.comm, aes(x = round, y = empirical_stat)) +
  geom_line() +
  geom_ribbon(aes(ymin = ci_lower, ymax = ci_upper), alpha = 0.2) +
  geom_hline(yintercept = 0.5,
             color = "red",
             linetype = "dashed") +
  labs(title = "improvement over rounds", y = "communication score") +
  theme(axis.ticks.x = element_blank(),
        axis.ticks.y = element_blank()) +
  ylim(0.35, 1)

ggsave(here("figures/comm_improvement.pdf"),
       width = 4,
       height = 4.5)

comm.score.mod <- gam(score ~ s(round, bs = "cs"),
                      data = d.comm)

summary(comm.score.mod)

# TODO: analysis for performance above chance

# Try linear model
comm.score.mod.linear <- lmer(score ~ 1 + round + (1 |
                                                     gameid),
                              data = d.comm)

summary(comm.score.mod.linear)


# relationship between discreteness and systematicity, and performance
ggplot(d, aes(x = systematicity, y = discreteness, col = comm_score)) +
  geom_point(size = 3.3) +
  labs(title = "discreteness and global systematicity") +
  theme(axis.ticks.x = element_blank(),
        axis.ticks.y = element_blank())

ggsave(here("figures/disc_sys_perf.pdf"),
       width = 6.5,
       height = 4.5)

# discrete systems are also systematic
disc.sys.mod <- lm(discreteness ~ 1 + systematicity,
                   data = d)

summary(disc.sys.mod)



# relationship between discreteness, systematicity, and performance
perf.mod <-
  lm(scale(comm_score) ~ 1 + scale(discreteness) * scale(systematicity),
     data = d)

summary(perf.mod)


# histogram and summary stats of discreteness and systematicity
ggplot(d, aes(x = systematicity)) +
  geom_histogram()

ggplot(d, aes(x = discreteness)) +
  geom_histogram()

d %>%
  summarise(mean = mean(systematicity),
            sd = sd(systematicity))

d %>%
  summarize(mean = mean(discreteness), sd = sd(discreteness))


# partner alignment for signals -- pairs that have better alignment do better
ggplot(
  d %>% distinct(alignment_norm, .keep_all = T),
  aes(x = alignment_norm, y = paired_comm_score)
) +
  geom_point(size = 2.5)

mod <-
  lm(paired_comm_score ~ alignment_norm,
     data = d %>% distinct(alignment_norm, .keep_all = T))
summary(mod)

ggplot(d, aes(x = alignment, y = comm_score)) +
  geom_point(size = 2.5)

mod <- lm(comm_score ~ alignment, data = d)
summary(mod)

# participants that had better learning scores were also better aligned
mod <- lm(alignment_norm ~ learn_score, data = d)
summary(mod)

ggplot(d, aes(x = alignment_norm, y = learn_score)) +
  geom_point(size = 2.5)
