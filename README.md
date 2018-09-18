# data-tx-nhd

This repo contains a set of experimental processes for extracting and caching data from the National Hydrography Dataset (different versions) that we set up within the Biogeographic Information System to run various types of analyses. These are considered data-building codes in our architecture - codes that are used to provide a transparent and buildable process for data that end up in our system for use.

This code built on work started by Daniel Wieferich [here](https://github.com/dwief-usgs/BCB_Ipython_Notebooks/blob/master/NHDPlusV1_Into_SB.ipynb) for NHDPlusV1. Sky took it a somewhat different direction, using the [ScienceBase Items](https://www.sciencebase.gov/catalog/items?parentId=5644f3c1e4b0aafbcd0188f1&filter=tags%3DNHDPlusV1) to serve as manually configured starting/connecting points to the FTP repository location for the files. Core logic used in packaging the files was put into a new NHD module in the [pybis package](https://github.com/usgs-bis/pybis).

## Primary Contents

* cacheNHDRepoCatalogs.py - This script reads the indicated Horizon Systems FTP URL from the collection of ScienceBase Items (parentId and tag filtered), grabs the directory listing, and builds a catalog of the contents for later reference and processing. The catalog contains details on the location of the data and interprets the file name (based on documentation for the file naming conventions used) to produce a set of more usable attributes.
* cacheFlowlineData.py - Using the previously cached catalogs for each NHDPlusV1 processing area, this script retrieves the "NHD" zip file, extracts just the flowline shapefile components, builds a new "FlowlineExtract" zip file, and uploads the file to the corresponding ScienceBase Item. These files are then pulled through another pipeline where they are integrated together into a National NHDPlusV1 flow line dataset for our use.

## Next Steps
We will continue building on this idea for processing NHDPlusV2 and other aspects of the NHD that we need for our purposes. This also serves as a pattern for other similar data-building processes we need to get in place where we are working on the following principles:
* Use ScienceBase where it makes sense as a caching location for forms of data that we need to use, that we may manipulate with code in various ways to transform for our use, and that we treat as a semi-permanent repository that helps us sustain our system and show where everything comes from.
* Build core logic for these processes into the pybis Python package or some other applicable codebase as a cohesive point of management and versioning over time.
* Build the actual data-building code workflows with the ability to be re-run at any time to build our data for use - perhaps on a different platform or with slight variation in processing logic.
