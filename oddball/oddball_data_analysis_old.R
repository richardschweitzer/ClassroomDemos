## analysis of the oddball demo ##


# read file
dat_1 <- read.csv('/home/richard/Dropbox/PROMOTION WORKING FOLDER/Talks/time perception lecture/demos/oddball/oddball_data_24102017.csv')
#dat_1 <- read.csv('/home/richard/Dropbox/PROMOTION WORKING FOLDER/Talks/time perception lecture/demos/oddball/oddball_data_25102016.csv')
# compute probabilities
dat_1$p <- dat_1$longer/(dat_1$longer + dat_1$shorter)

# make curve
compute_curve <- function(p, xmin, xmax, comparison_durs, shorters, longers) {
  # round xmin and xmax and add 1 ms
  xmin <- signif(xmin, 3)-0.001
  xmax <- signif(xmax, 3)+0.001
  # create x-values
  xseq <- seq(xmin, xmax, len = length((xmin*1000):(xmax*1000))) # one value per ms
  # use logistic model
  model <- glm(cbind(longers, shorters) ~ comparison_durs, 
               family = binomial(link = "logit"))
  coef(model)
  # let the model predict
  yseq <- predict(model, data.frame(comparison_durs = xseq), type = "response")
  # compute difference limen / JND
  (m_model <- -coef(model)[[1]]/coef(model)[[2]])
  (sd_model <- 1/coef(model)[[2]])
  p_25 <- qnorm(0.25, m_model, sd_model) # see http://www.dlinares.org/psychopract.html
  p_75 <- qnorm(0.75, m_model, sd_model) 
  jnd <- (p_75 - p_25) / 2
  # see: http://www.nature.com/neuro/journal/v17/n5/fig_tab/nn.3689_SF2.html
  # compute pse and slope
  library(modelfree)
  thres <- threshold_slope(yseq, xseq, p)
  pse <- as.numeric(thres[1])
  slope <- as.numeric(thres[2])
  # output predicted data
  curve <- data.frame(xseq,yseq,pse,slope,jnd)
  colnames(curve) <- c("comparison_dur","p","pse","slope","jnd")
  curve
}
curve_overall <- compute_curve(p = 0.5, xmin = 0.3, xmax = 0.7, 
                               comparison_durs = dat_1$comparison_dur, 
                               shorters = dat_1$shorter, longers = dat_1$longer)
pse <- unique(curve_overall$pse)

# plot curve
library(ggplot2)
p1 <- ggplot(data = dat_1, aes(x = comparison_dur, y = p)) + 
  geom_point(size=3) + labs(x ="Comparison Duration [s]", y ="Relative frequency (longer)") 
p1 <- p1 + geom_line(data = curve_overall, aes(x = comparison_dur, y = p)) + # add curve
  geom_vline(xintercept = pse, linetype="dotted", color = "red", size = 1)
p1 + theme_bw(base_size=20) + geom_abline(intercept = 0.5, slope = 0, linetype="dotted") + 
  geom_vline(xintercept = 0.5, linetype="dotted")

# output of PSE
pse
