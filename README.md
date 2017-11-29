# sar2watermask

A project for automatic download and processing sentinel-1 SAR files. It calibrates, filters, extracts watermask, writes to GeoTiff, polygonizes and simplifies polygon.

The scripts are suited to work on a cluster. In the future, they should run parallel.

Right now the workflow is as follows

## Query the [Copernicus Open Access Hub](https://scihub.copernicus.eu/)

`sar2watermask/modules/getRecentScenes.py` will 

Downloadand process several scenes once a week.

Check wiki in this repo for details and some preliminary results.
