#Replicates descriptive statistics for table 1
library(pastecs)
rm(list = ls())
columns <- c('EFW', 'size_gov', 'prop_rights', 'sound_money', 'freedom_to_trade',
             'regulation', 'lcgdp', 'lpop', 'polity', 'open', 'interest',
             'credit', 'gross', 'fdi', 'cpi', 'balance',
             'indexla')

geomet_ECindex <- read.csv("data/econ_freedom_and_geomet.csv")
geomet_ECindex <- as.data.frame(geomet_ECindex)
table1_vars <- geomet_ECindex[columns]

stat.desc(table1_vars, basic = FALSE)
