This programs compares OSM walking route data to that of other data sets.


# Dependencies

This program depends on python-geojson for importing geojson data.

Run with

        python knooppunten.py

# Results format

Results are exported to geojson format. The points are tagged with their node number. The number -1 means the node doesn't have a number of this type.

After running the script the following files can be found in the results folder:

`non_matches.geojson`: De knooppunten van de routedatabank die niet binnen 100 meter liggen van een passend OSM knooppunt.

`poor_matches.geojson`: De knooppunten van de routedatabank die 10-100 meter liggen van een passend OSM knooppunt.

`good_matches.geojson`: De knooppunten van de routedatabank die 1-10 meter liggen van een passend OSM knooppunt.

`great_matches.geojson`: De knooppunten van de routedatabank die binnen 1 meter liggen van een passend OSM knooppunt.


`poor_matches_osm.geojson`: De bijpassende knooppunten die het dichts bij de punten van `poor_matches.geojson` liggen. Elk routedatabank punt heeft 1 bijpassend OSM knooppunt.

`good_matches_osm.geojson`: De bijpassende knooppunten die het dichts bij de punten van `good_matches.geojson` liggen. Elk routedatabank punt heeft 1 bijpassend OSM knooppunt.

`great_matches_osm.geojson`: De bijpassende knooppunten die het dichts bij de punten van `great_matches.geojson` liggen. Elk routedatabank punt heeft 1 bijpassend OSM knooppunt.

`osm_match_2.geojson`: OSM nodes die aan 2 routedatabank nodes zijn gematcht.

`osm_match_gt_2.geojson`: OSM nodes die aan meer dan 2 routedatabank nodes zijn gematcht.

Passend betekent dat de wandelknooppuntnummers overeen komen.

These files can all be opened in JOSM.

# Data sources

OSM data: https://knooppuntnet.nl/nl/analysis/hiking
Routedatabank

# Converting data

## OSM data

The OSM data can be imported in JOSM and exported to the .osm (XML) data format.

## WFS data

Take a look at: https://docs.qgis.org/2.18/en/docs/training_manual/online_resources/wfs.html
for importing WFS data.

To get the data in the right format, export them to GEOJSON in QGIS.
