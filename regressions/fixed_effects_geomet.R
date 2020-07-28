#---------------------------------------------------------------
# The following script replicates the results in the article
# "The importance of formal institutions after a natural disaster"
# All data used is provided along this script.
# Any problem with the execution please contact Diego D?az H. at diegodiaz@udd.cl

# System information from R.version is the following:
# platform       x86_64-w64-mingw32
# arch           x86_64
# os             mingw32
# system         x86_64, mingw32
# status
# major          4
# minor          0.2
# year           2020
# month          06
# day            22
# svn rev        78730
# language       R
# version.string R version 4.0.2 (2020-06-22)
# nickname       Taking Off Again

#---------------------------------------------------------------
rm(list = ls())
library("tidyverse")
library("plm")
library("readr")
library("readxl")
library("broom")
library("RCurl")


#########################################################
#                   Regression Results
# The regression results from Table 1 are replicated in this section
#########################################################

#the following code obtains a function for estimating robust standard errors
url_robust <- "https://raw.githubusercontent.com/IsidoreBeautrelet/economictheoryblog/master/robust_summary.R"
eval(parse(text = getURL(url_robust, ssl.verifypeer = FALSE)),
     envir=.GlobalEnv)
########

geomet_ECindex <- read.csv("data/econ_freedom_and_geomet.csv")
geomet_ECindex <- as.data.frame(geomet_ECindex)
geomet_ECindex$cpi <- as.numeric(geomet_ECindex$cpi)
geomet_ECindex$lcpi <- log(geomet_ECindex$cpi)
GeoMet_panel <- pdata.frame(geomet_ECindex, index = c("id", "year"))

# creating lagged variables
GeoMet_panel$L.lcgdp <- lag(GeoMet_panel$lcgdp, 1)
GeoMet_panel$L.lpop <- lag(GeoMet_panel$lpop, 1)
GeoMet_panel$L.polity <- lag(GeoMet_panel$polity, 1)
GeoMet_panel$L.open <- lag(GeoMet_panel$open, 1)
GeoMet_panel$L.interest <- lag(GeoMet_panel$interest, 1)
GeoMet_panel$L.credit <- lag(GeoMet_panel$credit, 1)
GeoMet_panel$L.gross <- lag(GeoMet_panel$gross, 1)
GeoMet_panel$L.fdi <- lag(GeoMet_panel$fdi, 1)
GeoMet_panel$L.lcpi <- lag(GeoMet_panel$lcpi, 1)
GeoMet_panel$L.balance <- lag(GeoMet_panel$balance, 1)
GeoMet_panel$L.EFW <- lag(GeoMet_panel$EFW, 1)

# creating first difference
GeoMet_panel$D.lcgdp <- diff(GeoMet_panel$lcgdp, 1)

# lagging sub indexes from economic freedom
GeoMet_panel$L.size_gov <- lag(GeoMet_panel$size_gov, 1)
GeoMet_panel$L.property_rights <- lag(GeoMet_panel$prop_rights, 1)
GeoMet_panel$L.sound <- lag(GeoMet_panel$sound_money, 1)
GeoMet_panel$L.freedom_to_trade <- lag(GeoMet_panel$freedom_to_trade, 1)
GeoMet_panel$L.regulation <- lag(GeoMet_panel$regulation, 1)

columns <- c('D.lcgdp', 'indexla', 'L.EFW', 'L.lcgdp', 'L.lpop',
             'L.polity', 'L.open', 'L.interest', 'L.credit', 'L.gross', 'L.fdi',
             'L.lcpi', 'L.balance', 'year', 'L.size_gov', 'L.property_rights',
             'L.sound', 'L.freedom_to_trade', 'L.regulation')

GeoMet_panel <- GeoMet_panel[c(columns, 'country')]
for (col in columns){
  GeoMet_panel[[col]] <- as.numeric(GeoMet_panel[[col]])
}

#----------------------------------------------
# Fixed effects regression with ECI
# (Table: 1)
#----------------------------------------------
fixed <- plm(D.lcgdp ~ indexla+L.EFW+L.lcgdp+L.lpop+L.polity+L.open+
               L.interest+L.credit+L.gross+L.fdi+L.lcpi+L.balance+factor(year),
               data=GeoMet_panel, index=c("country", "year"), model="within")

summary(fixed)
reg <- tidy(fixed)
print(summary(fixed, robust=TRUE))
#----------------------------------------------
# Fixed effects regression with ECI subindexes
# (Table: 1)
#----------------------------------------------
fixed <- plm(D.lcgdp ~ indexla+L.size_gov+L.property_rights+L.sound+
             L.freedom_to_trade+L.regulation+L.lcgdp+L.lpop+L.polity+L.open+
             L.interest+L.credit+L.gross+L.fdi++L.lcpi+L.balance+factor(year),
             data=GeoMet_panel, index=c("country", "year"), model="within")
summary(fixed)
reg2 <- tidy(fixed)
print(summary(fixed, robust=TRUE))

#----------------------------------------------
# Fixed effects regression with ECI subindexes and time trend
# (Table: Extra)
#----------------------------------------------
fixed <- plm(D.lcgdp ~ indexla+year+L.size_gov+L.property_rights+L.sound+
                 L.freedom_to_trade+L.regulation+L.lcgdp+L.lpop+L.polity+L.open+
                 L.interest+L.credit+L.gross+L.fdi+L.lcpi+L.balance+factor(year),
             data=GeoMet_panel, index=c("country", "year"), model="within")
summary(fixed)
reg2 <- tidy(fixed)
print(summary(fixed, robust=TRUE))




