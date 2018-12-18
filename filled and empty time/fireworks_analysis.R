# analysis of fireworks demo
true_duration <- 10
true_explosions <- 25

path_to_fireworks <- "/home/richard/Dropbox/PROMOTION WORKING FOLDER/Talks/Zeitwahrnehmung HU Berlin/demos/filled and empty time"
fireworks <- read.csv(file.path(path_to_fireworks, "Fireworks Demo 26.06.2018.csv"), header = TRUE)
colnames(fireworks) <- c("subj_id", "empty_dur", "filled_dur", "nr_explosions")
str(fireworks)

# convert to long format
library(tidyr)
fireworks_long <- gather_(data = fireworks, key_col = 'judgment', value_col = 'estimated', 
                          gather_cols = colnames(fireworks)[-1])
fireworks_long$judgment_f <- factor(fireworks_long$judgment)
levels(fireworks_long$judgment_f) <- c("Duration Empty", "Duration Fireworks", "Number of explosions")
fireworks_long$temporal_judgment <- fireworks_long$judgment_f!=levels(fireworks_long$judgment_f)[3]
fireworks_long$temporal_judgment_f <- factor(fireworks_long$temporal_judgment)
levels(fireworks_long$temporal_judgment_f) <- c("Number of explosions", "Perceived duration")

# aggregate
library(reshape)
#fireworks_long$estimated[fireworks_long$estimated<1] <- fireworks_long$estimated[fireworks_long$estimated<1] * 100
fire_agg <- cast(fireworks_long, value = "estimated", 
                 formula = temporal_judgment + temporal_judgment_f + judgment_f ~ ., function(x) {
  c(M = median(x), 
    SE = sd(x)/sqrt(length(x)))
}, subset = !is.na(estimated))
# add reference
fire_agg$reference <- NA
fire_agg$reference[fire_agg$temporal_judgment] <- true_duration
fire_agg$reference[!fire_agg$temporal_judgment] <- true_explosions

# now plot
to_plot <- fire_agg[fire_agg$temporal_judgment, ]

library(ggplot2)
fire_plot <- ggplot(to_plot, 
                    aes(x = judgment_f, y = M, fill = judgment_f)) + 
  geom_bar(stat = "identity") + geom_errorbar(aes(ymin = M - SE, ymax = M + SE)) + 
#  facet_wrap(~temporal_judgment_f, scales = "free_x") + 
  geom_hline(data = to_plot, aes(yintercept = reference), linetype = "dotted") +
  labs(fill = " ", x = " ", y = "Perceived Duration [s]") 
fire_plot + theme_bw(base_size = 20) + theme(legend.position = "top")
