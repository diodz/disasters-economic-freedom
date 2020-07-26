library(haven)
library(readxl)


IfoGAME_balanced_panel <- read_dta("data/IfoGAME_balanced_panel.dta")
efw_2019_master_index_data_for_researchers <- read_excel(
    "data/efw-2019-master-index-data-for-researchers.xlsx",
    sheet = "EFW Panel Data 2019 Report")

