This programs compares OSM walking route data to that of other data sets.

# Data sources

OSM data: https://knooppuntnet.nl/nl/analysis/hiking

Groningen wandelnetwerk: https://data.overheid.nl/dataset/7289-wandelnetwerk-groningen--routenetwerk-

# Converting data

## OSM data

The OSM data can be imported in JOSM and exported to the .osm (XML) data format.

## WFS data

The data from the Groningen walking routes are in OGS:WFS format. These need to
be imported. I used QGIS for this.
Take a look at: https://docs.qgis.org/2.18/en/docs/training_manual/online_resources/wfs.html
for importing WFS data.

To get the data in the right format, export them to GEOJSON in QGIS.
