# analysis for the AWH
# Richard, 11/2018

library(data.table)
library(reshape)
library(ggplot2)
library(ez)

path_to_data <- "~/Dropbox/STUDIUM_MIND_BRAIN/Active Vision/PRESENTATION/demo exp"

###### read design #####
design_data <- read.csv(file.path(path_to_data, "design.csv"), header = TRUE)
design_agg <- cast(design_data, value = "target_ori", formula = trial_nr + color_swap + SoA ~ ., unique)
colnames(design_agg)[length(colnames(design_agg))] <- "target_ori"
table(design_agg$target_ori)
str(design_agg)

###### read responses ######
resp_data <- read.csv(file.path(path_to_data, "Active Vision 13.11.2018.csv"), header = TRUE, sep = ",", 
                      stringsAsFactors = FALSE)
resp_data <- resp_data[ ,-2]
colnames(resp_data)[1] <- "ID"
str(resp_data)
resp_agg <- melt(data = resp_data, id.vars = "ID", variable_name = "trial_nr")
str(resp_agg)
colnames(resp_agg)[length(colnames(resp_agg))] <- "resp_raw"
resp_agg$trial_nr <- as.character(resp_agg$trial_nr)
resp_agg$trial_nr <- as.numeric(gsub(x = resp_agg$trial_nr, pattern = "Trial.", replacement = ""))
# code responses
resp_agg$resp <- NA
resp_agg$resp[resp_agg$resp_raw=="/ (CW)"] <- 45
resp_agg$resp[resp_agg$resp_raw=="\\ (CCW)"] <- (-1)*45
table(resp_agg$resp, resp_agg$resp_raw)

##### merge design and responses #####
awh_data <- merge(design_agg, resp_agg, by = "trial_nr")
str(awh_data)

##### compute correct responses #####
awh_data$correct <- awh_data$target_ori == awh_data$resp
awh_data$correct_num <- as.numeric(awh_data$correct)
awh_data$color_swap_f <- factor(awh_data$color_swap)
levels(awh_data$color_swap_f) <- c("color same", "color swapped")
awh_data$SoA_f <- ordered(awh_data$SoA)

# tables
table(awh_data$correct, awh_data$SoA, awh_data$color_swap, useNA = "ifany")
table(awh_data$correct, awh_data$SoA, awh_data$ID, useNA = "ifany")

# aggregation
awh_agg <- cast(data = awh_data, value = "correct_num", 
                formula = color_swap_f + SoA ~ .,
                function(x) c( corrects = sum(x),
                               N = length(x) ) )
awh_agg$p.correct <- awh_agg$corrects / awh_agg$N
str(awh_agg)

# plot
awh_plot <- ggplot(data = awh_agg, aes(x = SoA, y = p.correct, color = color_swap_f)) + 
  geom_point() + geom_line() + theme_bw(base_size = 15) + 
  labs(x = "Stimulus Mask Asynchrony [s]", y = "Proportion correct", color = " ") + 
  geom_hline(yintercept = 0.5, linetype = "dotted")
awh_plot
ggsave(filename = file.path(path_to_data, "results.png"), plot = awh_plot)

# 
