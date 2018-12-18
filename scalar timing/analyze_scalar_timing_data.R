# analysis of the scalar timing demo
interval_durations = c(0, 4, 13, 6, 10, 2, 8, 16, 19)
colnames <- paste("Dur", (interval_durations), sep = "_")
dat_scalar <- read.csv('/home/richard/Dropbox/PROMOTION WORKING FOLDER/Talks/Zeitwahrnehmung HU Berlin/demos/scalar timing/Scalar Timing Demo 26.06.2018.csv', 
                       sep = ",", stringsAsFactors = FALSE, header = TRUE)
# dat_scalar_previous <- read.csv('/home/richard/Dropbox/PROMOTION WORKING FOLDER/Talks/time perception lecture/demos/scalar timing/scalar_timing_data_25102016.csv')

colnames(dat_scalar) <- c("subj", colnames)
for (c in 2:ncol(dat_scalar)) {
  # check whether people used commas as decimal specifiers
  # if so, convert , to .
  if (typeof(dat_scalar[ ,c])=="character") {
    dat_scalar[ ,c] <- gsub(x = dat_scalar[ ,c], pattern = ",", replacement = ".")
  }
  # convert to numeric by force
  dat_scalar[ ,c] <- as.numeric(dat_scalar[ ,c])
}

# simulate data with scalar property
n <- 12
cols <- cbind((1:n))
for (i in interval_durations) {
  col <- rnorm(n = n, mean = i, sd = i/4)
  cols <- cbind(cols, col)
}
dat_scalar_test <- data.frame(cols)
colnames(dat_scalar_test) <- c("subj", colnames)

# convert from wide format to long format
library(tidyr)
dat_scalar_long <- gather_(data = dat_scalar, key_col = 'duration', value_col = 'estimated', gather_cols = colnames)

# create factor duration
for (d in 1:length(dat_scalar_long$duration)) {
  dat_scalar_long$duration[d] <- strsplit(x = dat_scalar_long$duration[d], split = "_")[[1]][2]
}
dat_scalar_long$duration <- as.numeric(dat_scalar_long$duration)

# remove test interval and NAs
dat_scalar_long <- dat_scalar_long[!is.na(dat_scalar_long$estimated) & dat_scalar_long$estimated!=0, ]
str(dat_scalar_long)

# aggregate data
library(reshape)
dat_2 <- cast(dat_scalar_long, value="estimated", duration ~ ., 
              function(x) c( M = mean(x),
                             SE = signif(sd(x)/sqrt(length(x)), 2) ))
dat_2

library(ggplot2)
# compute relative temporal judgments
dat_scalar_long$relative <- dat_scalar_long$estimated/dat_scalar_long$duration

plot_3 <- ggplot(dat_scalar_long[dat_scalar_long$duration!=0, ], 
                 aes(x = relative, fill = duration)) + facet_grid(duration ~ . ) +
  labs(x = "Estimated Duration / Physical Duration [s]", y = "Response frequency") + theme_bw(base_size = 20)
#plot_3 + geom_histogram()
plot_3 + geom_density(adjust=2) + scale_x_continuous(limits = c(0,2))

# plot as histogram
plot_2 <- ggplot(dat_scalar_long[!is.na(dat_scalar_long$estimated) & dat_scalar_long$estimated!=0, ], 
                 aes(x = estimated, fill = duration)) + facet_grid(duration ~ . ) +
                 labs(x = "Estimated Duration [s]", y = "Response frequency") + theme_bw(base_size = 20)
#plot_2 + geom_histogram()
plot_2 + geom_density(adjust=2)

# plot data: as a boxplot
plot_1 <- ggplot(dat_2, aes(x = duration, y = M)) 
plot_1 <- plot_1 + geom_point() + geom_errorbar(aes(ymax = M + SE, ymin= M - SE), width=.25) + 
  labs(x ="Physical Duration [s]", y ="Estimated Duration [s]") + geom_abline(intercept=0, slope = 1, linetype = "dotted")
plot_1 + theme_bw(base_size=20) 

