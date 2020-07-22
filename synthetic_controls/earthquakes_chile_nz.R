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
library("Synth")
library("tidyverse")
library("plm")
library("readr")
library("readxl")
library("broom")
library("RCurl")

#########################################################
#                 Optimization Results
#This section replicates the synthetic control for our case studies
#########################################################

#----------------------------------------------
# Earthquake: Canterbury, New Zealand  2011
# (Figure: 1. Bottom)
#----------------------------------------------
nz_2011 <- read_xlsx("data/scm_nz_2011.xlsx")
nz_2011$regionname <- as.character(nz_2011$regionname)
nz_2011 <- filter(nz_2011, year != 2016)
nz_2011$gdp_cap <- nz_2011$gdp_cap *1000
nz_2011 <- as.data.frame(nz_2011)

dataprep.out <-
  dataprep(foo = nz_2011,
           predictors = c('sec_agriculture', 'sec_adm', 'sec_construction', 'sec_education',
                          'sec_financial', 'sec_food', 'sec_health', 'sec_information',
                          'sec_manufacuring', 'sec_ocupation', 'sec_profesional', 'sec_public',
                          'sec_rental', 'sec_retail', 'sec_transport', 'sec_varios',
                          'sec_wholesale'),
           predictors.op = "mean",
           time.predictors.prior = 2005:2010,
           special.predictors = list(
             list("gdp_cap", 2005:2010, "mean"),
             list("tertiary_per", 2007:2010, "mean")),
           dependent = "gdp_cap",
           unit.variable = "regioncode",
           unit.names.variable = "regionname",
           time.variable = "year",
           treatment.identifier = 13,
           controls.identifier = c(1:12,14:15),
           time.optimize.ssr = 2000:2010,
           time.plot = 2000:2015
  )

synth.out <- synth(data.prep.obj = dataprep.out,
                   method = "BFGS")

synth.tables <- synth.tab(dataprep.res = dataprep.out,
                          synth.res = synth.out
)
par(mfrow=c(1, 2))
path.plot(synth.res = synth.out,
          dataprep.res = dataprep.out,
          Ylab = "Real per-capita GDP",
          Xlab = "Year",
          Ylim = c(20,60),
          Legend = c("Canterbury region","Synthetic Canterbury region"),
          Legend.position = "topleft", abline(v=2010, col = "red", lty = 2)
)

store <- matrix(NA,length(2000:2015),15)
colnames(store) <- unique(nz_2011$regionname)

# run placebo test
for(iter in 1:15) {
  dataprep.out <-
    dataprep(foo = nz_2011,
             predictors = c('sec_agriculture', 'sec_adm', 'sec_construction', 'sec_education',
                            'sec_financial', 'sec_food', 'sec_health', 'sec_information',
                            'sec_manufacuring', 'sec_ocupation', 'sec_profesional', 'sec_public',
                            'sec_rental', 'sec_retail', 'sec_transport', 'sec_varios',
                            'sec_wholesale') ,
             predictors.op = "mean" ,
             time.predictors.prior = 2005:2010 ,
             special.predictors = list(
               list("gdp_cap", 2005:2010, "mean"),
               list("tertiary_per", 2007:2010, "mean")),
             dependent = "gdp_cap",
             unit.variable = "regioncode",
             unit.names.variable = "regionname",
             time.variable = "year",
             treatment.identifier = iter,
             controls.identifier = c(1:15)[-iter],
             time.optimize.ssr = 2000:2010,
             time.plot = 2000:2015
    )
  # run synth
  synth.out <- synth(
    data.prep.obj = dataprep.out,
    method = "BFGS"
  )

  # store gaps
  store[,iter] <- dataprep.out$Y1plot - (dataprep.out$Y0plot %*% synth.out$solution.w)
}

# now do figure
data <- store
rownames(data) <- 2000:2015
length(data)

# Set bounds in gaps data
gap.start     <- 1
gap.end       <- nrow(data)
years         <- 2000:2015
gap.end.pre  <- which(rownames(data)=="2010")

#  MSPE Pre-Treatment
mse <- apply(data[ gap.start:gap.end.pre,]^2,2,mean)
canterbury.mse <- as.numeric(mse[13])
# Exclude states with 5 times higher MSPE than basque
data <- data[,mse<5*canterbury.mse]

plot(years,data[gap.start:gap.end,which(colnames(data)=="canterbury")],
     ylim=c(-6,6),xlab="year",
     xlim=c(2000,2015),ylab="gap in real per-capita GDP",
     type="l",lwd=2,col="black",
     xaxs="i",yaxs="i")

# Add lines for control states
for (i in 1:ncol(data)) { lines(years,data[gap.start:gap.end,i],col="grey") }

## Add Line
lines(years,data[gap.start:gap.end,which(colnames(data)=="canterbury")],lwd=2,col="black")

# Add grid
abline(v=2011,lty="dotted",lwd=2, col ='black')
abline(h=0,lwd=2)
legend("topleft",legend=c("Canterbury region","Control regions"),
       lty=c(1,1),col=c("black","gray"),lwd=c(2,1),cex=.8)



#----------------------------------------------
# Earthquake: Maule region, Chile 2010
# (Figure: 1. Top. and figure 2)
#----------------------------------------------
chile_2010 <- read_xlsx("data/scm_chile_2010.xlsx")
chile_2010$region_name <- as.character(chile_2010$region_name)
chile_2010$gdp_cap <- chile_2010$gdp_cap / 100000
names(chile_2010)[1] <- paste("year")
chile_2010 <- as.data.frame(chile_2010)

dataprep.out <-
  dataprep(foo = chile_2010,
           predictors = c("agropecuario" , "pesca" , "mineria" , "industria_m" , "electricidad" , "construccion","comercio","transporte","servicios_financieros", "vivienda","personales","publica") ,
           predictors.op = "mean" ,
           time.predictors.prior = 2005:2009 ,
           special.predictors = list(
             list("ed_superior_cap" , 2008:2009 , "mean"),
             list("gdp_cap", 2000:2009, "mean")),
           dependent = "gdp_cap",
           unit.variable = "id",
           unit.names.variable = "region_name",
           time.variable = "year",
           treatment.identifier = 8,
           controls.identifier = c(1:7,10:13),
           time.optimize.ssr = 1985:2009,
           time.plot = 1985:2015)

synth.out <- synth(data.prep.obj = dataprep.out,
                   method = "BFGS")

gaps <- dataprep.out$Y1plot - (dataprep.out$Y0plot %*% synth.out$solution.w)

synth.tables <- synth.tab(dataprep.res = dataprep.out,
                          synth.res = synth.out
)
par(mfrow=c(1, 2))
path.plot(synth.res = synth.out,
          dataprep.res = dataprep.out,
          Ylab = "Real per-capita GDP",
          Xlab = "Year",
          Ylim = c(5,80),
          Legend = c("Maule region","Synthetic Maule region"),
          Legend.position = "topleft",
          abline(v=2010, col = "red", lty = 2)
)


store <- matrix(NA,length(1985:2015),13)
colnames(store) <- unique(chile_2010$region_name)

# run placebo test
for(iter in 1:13) {
  if (iter == 9) next
  dataprep.out <-
    dataprep(foo = chile_2010,
             predictors = c("agropecuario" , "pesca" , "mineria" , "industria_m" ,
                            "electricidad" , "construccion","comercio","transporte",
                            "servicios_financieros", "vivienda","personales",
                            "publica") ,
             predictors.op = "mean" ,
             time.predictors.prior = 2005:2009 ,
             special.predictors = list(
               list("ed_superior_cap" , 2008:2009 , "mean"),
               list("gdp_cap", 2000:2009, "mean")),
             dependent = "gdp_cap",
             unit.variable = "id",
             unit.names.variable = "region_name",
             time.variable = "year",
             treatment.identifier = iter,
             controls.identifier = c(1:13)[-c(iter, 9)],
             time.optimize.ssr = 1985:2009,
             time.plot = 1985:2015
    )
  # run synth
  synth.out <- synth(
    data.prep.obj = dataprep.out,
    method = "BFGS")

  # store gaps
  store[,iter] <- dataprep.out$Y1plot - (dataprep.out$Y0plot %*% synth.out$solution.w)
}

# now do figure
data <- store
rownames(data) <- 1985:2015
length(data)

# Set bounds in gaps data
gap.start     <- 1
gap.end       <- nrow(data)
years         <- 1985:2015
gap.end.pre  <- which(rownames(data)=="2009")

#  MSPE Pre-Treatment
mse        <-             apply(data[ gap.start:gap.end.pre,]^2,2,mean)
maule.mse <- as.numeric(mse[8])
# Exclude states with 5 times higher MSPE than basque
data <- data[,mse<5*maule.mse]

# Plot
plot(years,data[gap.start:gap.end,which(colnames(data)=="VII Del Maule")],
     ylim=c(-4,4),
     xlab="Year",
     xlim=c(1985,2015),ylab="Gap in real per-capita GDP",
     type="l",lwd=2,col="black",
     xaxs="i",yaxs="i")

# Add lines for control states
for (i in 1:ncol(data)) { lines(years, data[gap.start:gap.end, i], col="grey") }

## Add  Line
lines(years, data[gap.start:gap.end,which(colnames(data)=="VII Del Maule")], lwd=2, col="black")

# Add grid
abline(v=2010,lty="dotted",lwd=2)
abline(h=0,lwd=2)
legend("topleft", legend=c("Maule Region","Control Regions"),
       lty=c(1,1), col=c("black","gray"), lwd=c(2,1),cex=.8)


#----------------------------------------------
# Eartquake: Valparaiso region, Chile 1985
# (Figure: 2)
#----------------------------------------------
chile_1985 <- read_xlsx("data/scm_chile_1985.xlsx")
chile_1985$regionname <- as.character(chile_1985$regionname)
chile_1985 <- chile_1985 %>%
  arrange(id)
#Eliminating zeros for readability
chile_1985$gdpcap <- chile_1985$gdpcap/100000
chile_1985 <- as.data.frame(chile_1985)

dataprep.out <-
  dataprep(foo = chile_1985,
           predictors = c("sec.agricultureper" , "sec.fishingper" , "sec.miningper" ,
                          "sec.industryper" , "sec.energyper" , "sec.constructionper","sec.retailper", "sec.transportper","sec.othersper") ,
           predictors.op = "mean" ,
           time.predictors.prior = 1975:1984 ,
           special.predictors = list(
             list("gdpcap" , 1975:1984 , "mean")),
           dependent = "gdpcap",
           unit.variable = "id",
           unit.names.variable = "regionname",
           time.variable = "year",
           treatment.identifier = 5,
           controls.identifier = c(1:4,6:13),
           time.optimize.ssr = 1960:1984,
           time.plot = 1960:2001
  )

synth.out <- synth(data.prep.obj = dataprep.out,
                   method = "BFGS")
gaps <- dataprep.out$Y1plot - (dataprep.out$Y0plot %*% synth.out$solution.w)

synth.tables <- synth.tab(dataprep.res = dataprep.out,
                          synth.res = synth.out
)
par(mfrow=c(1, 2))
path.plot(synth.res = synth.out,
          dataprep.res = dataprep.out,
          Ylab = "Real per-capita GDP",
          Xlab = "Year",
          Ylim = c(5, 30),
          Legend = c("Valparaíso region","Synthetic Valparaíso region"),
          Legend.position = "topleft", abline(v=1985, col = "red", lty = 2)
)

store <- matrix(NA,length(1960:2001),13)
colnames(store) <- unique(chile_1985$regionname)

# run placebo test
for(iter in 1:13) {
  dataprep.out <-
    dataprep(foo = chile_1985,
             predictors = c("sec.agricultureper" , "sec.fishingper" , "sec.miningper" ,
                            "sec.industryper" , "sec.energyper" , "sec.constructionper","sec.retailper", "sec.transportper","sec.othersper") ,
             predictors.op = "mean" ,
             time.predictors.prior = 1980:1984 ,
             special.predictors = list(
               list("gdpcap" , 1980:1984 , "mean")),
             dependent = "gdpcap",
             unit.variable = "id",
             unit.names.variable = "regionname",
             time.variable = "year",
             treatment.identifier = iter,
             controls.identifier = c(1:13)[-iter],
             time.optimize.ssr = 1960:1984,
             time.plot = 1960:2001
    )

  # run synth
  synth.out <- synth(
    data.prep.obj = dataprep.out,
    method = "BFGS"
  )

  # store gaps
  store[,iter] <- dataprep.out$Y1plot - (dataprep.out$Y0plot %*% synth.out$solution.w)
}
store
# now do figure
data <- store
rownames(data) <- 1960:2001
length(data)

# Set bounds in gaps data
gap.start     <- 1
gap.end       <- nrow(data)
years         <- 1960:2001
gap.end.pre  <- which(rownames(data)=="1984")

#  MSPE Pre-Treatment
mse        <-             apply(data[ gap.start:gap.end.pre,]^2,2,mean)
valparaiso.mse <- as.numeric(mse[5])

# Exclude states with 5 times higher MSPE than valparaiso
data <- data[,mse<5*valparaiso.mse]

plot(years,data[gap.start:gap.end, which(colnames(data) == "V De Valparaíso")],
     ylim=c(-6,6),
     xlab="Year",
     xlim=c(1960,2001),ylab="Gap in real per-capita GDP",
     type="l",lwd=2,col="black",
     xaxs="i",yaxs="i")

# Add lines for control states
for (i in 1:ncol(data)) { lines(years,data[gap.start:gap.end,i],col="grey") }

## Add Valparaiso Line
lines(years,data[gap.start:gap.end,which(colnames(data) == "V De Valparaíso")],lwd=2,col="black")

# Add grid
abline(v=1985,lty="dotted",lwd=2)
abline(h=0,lty="dashed",lwd=2)
legend("topleft",legend=c("Valparaíso region","Control regions"),
       lty=c(1,1),col=c("black","grey"),lwd=c(2,1),cex=.8)

