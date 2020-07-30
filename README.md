## Replication code for: The Impact of Institutions in the Aftermath of Natural Disasters

GeoMet data comes from: 

Felbermayr, G., & Gröschl, J. (2014). Naturally negative: The growth effects of natural disasters. Journal of Development Economics, 111, 92-106. [View article.](https://www.sciencedirect.com/science/article/abs/pii/S0304387814000820) 

The data can be downloaded directly from the [Ifo Institute Website.](https://www.cesifo-group.de/de/dms/ifodoc/docs/IfoGAME/IfoGAME_balanced_panel.dta)

The data of Economic Freedom from the Fraser Institute can be downloaded directly from [their website.](https://www.fraserinstitute.org/economic-freedom/dataset?geozone=world&page=dataset&min-year=2&max-year=0&filter=0&sort-field=year&sort-reversed=0&year=1970)

A copy of both datasets is included in the data folder. 

# To replicate results:

Python file data_preparation.py creates the data used for the regression analysis in R, called econ_freedom_and_geomet.csv, which involves grouping, interpolating and merging. The R files replicate the results from table 1 and table 2 in the article.
