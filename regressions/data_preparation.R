library(haven)
library(readxl)
library(tidyverse)
library(zoo)
library(dplyr)


IfoGAME_balanced_panel <- read_dta("data/IfoGAME_balanced_panel.dta")
efw_2019_master_index_data_for_researchers <- read_excel(
    "data/efw-2019-master-index-data-for-researchers.xlsx",
    sheet = "EFW Panel Data 2019 Report")

merged <- merge(IfoGAME_balanced_panel,
                efw_2019_master_index_data_for_researchers)

add_1979 <- function(df_fraser){
    countries <- unique(df_fraser$ISO_Code)
    for (country in countries){
        df_fraser <- rbind(df_fraser, c(1979, country, NA, NA, NA, NA, NA, NA,
                                        NA))
    }
    return(df_fraser)
}

rename_fraser_data <- function(df){
    df %>%
        rename(
            year = Year,
            iso = ISO_Code,
            size_gov = "1  Size of Government",
            prop_rights = "2  Legal System & Property Rights",
            sound_money = "3  Sound Money",
            freedom_to_trade = "4  Freedom to trade internationally",
            regulation = "5  Regulation"
        )
}

read_fraser_institute_data <- function(){
    fraser <- read_excel(
        "data/efw-2019-master-index-data-for-researchers.xlsx",
        sheet = "EFW Panel Data 2019 Report")
    fraser <- add_1979(fraser)
    fraser <- rename_fraser_data(fraser)
    fraser <- select(fraser, -c(Countries))
    fraser$year <- as.numeric(fraser$year)
    return(fraser)
}

fraser <- read_fraser_institute_data()

fraser_inter <- fraser %>%
    group_by(iso) %>%
    mutate(EFW = na.approx(EFW, na.rm=FALSE)) %>%
    mutate(size_gov = na.approx(size_gov , na.rm=FALSE)) %>%
    mutate(prop_rights = na.approx(prop_rights, na.rm=FALSE)) %>%
    mutate(sound_money = na.approx(sound_money , na.rm=FALSE)) %>%
    mutate(freedom_to_trade = na.approx(freedom_to_trade, na.rm=FALSE)) %>%
    mutate(regulation = na.approx(regulation  , na.rm=FALSE))
