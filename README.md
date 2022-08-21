This programs compares OSM walking route data to that of other data sets.


# Installation

Make sure to install python on your system. This program depends on the
following libraries:

- python geojson for package for importing geojson data
- pyside6 for the Qt GUI

Install with:
	
	pip install geojson pyside6

# Running

Open a terminal in this project's directory. The program can be run with the following command:

	python knooppunten.py [-h] --osmfile OSMFILE --importfile IMPORTFILE [--region REGION]

Where you replace the arguments in capital letters with your own arguments. For example:

	python knooppunten.py --osmfile data/groningen.osm --importfile 'data/Wandelknooppunten (wgs84).geojson' --region "Groningen"

Or for Windows users:

	python knooppunten.py --osmfile data\groningen.osm --importfile 'data\Wandelknooppunten (wgs84).geojson' --region "Groningen"


For more detail about the arguments, run:

	python knooppunten.py -h

# Results format

After running the script you can find the results in the results directory.
Results are exported to geojson format. Every geojson file contains a bunch of
points along with metadata about those points. Every point has the following
metadata:

- `rwn_ref`: Wandelknooppuntnummer
- `rcn_ref`: Fietsknooppuntnummer
- `distance closest node`: The distance in meters of the closest matching point in the other dataset.


After running the script the following files can be found in the results folder:

`non_matches.geojson`: De knooppunten van de routedatabank die niet binnen 100 meter liggen van een passend OSM knooppunt.

`poor_matches.geojson`: De knooppunten van de routedatabank die 10-100 meter liggen van een passend OSM knooppunt.

`good_matches.geojson`: De knooppunten van de routedatabank die 1-10 meter liggen van een passend OSM knooppunt.

`great_matches.geojson`: De knooppunten van de routedatabank die binnen 1 meter liggen van een passend OSM knooppunt.

`invalid_nodes_ext.geojson`: De knooppunten van de routedatabank die geen valide knooppuntnummer hebben.


`poor_matches_osm.geojson`: De bijpassende knooppunten die het dichts bij de punten van `poor_matches.geojson` liggen. Elk routedatabank punt heeft 1 bijpassend OSM knooppunt.

`good_matches_osm.geojson`: De bijpassende knooppunten die het dichts bij de punten van `good_matches.geojson` liggen. Elk routedatabank punt heeft 1 bijpassend OSM knooppunt.

`great_matches_osm.geojson`: De bijpassende knooppunten die het dichts bij de punten van `great_matches.geojson` liggen. Elk routedatabank punt heeft 1 bijpassend OSM knooppunt.

`osm_match_0.geojson`: OSM nodes die niet aan routedatabank nodes zijn gematcht.

`osm_match_2.geojson`: OSM nodes die aan 2 routedatabank nodes zijn gematcht.

`osm_match_gt_2.geojson`: OSM nodes die aan meer dan 2 routedatabank nodes zijn gematcht.

Passend betekent dat de wandelknooppuntnummers overeen komen.

These files can all be opened in JOSM.

# Data sources

- OpenStreetMap
- Routedatabank

# Getting the data

## OSM data

Below are the instructions to download the OSM data. This might be automated in
the future with an overpass query.

- Go to https://knooppuntnet.nl/nl/analysis/hiking
- Select "Explore by network" on the left.
- Navigate to the network you want to analyze
- Open JOSM with remote control enabled
- Click the edit button. The dataset will open in JOSM
- Click "file > save as" and save as .osm file

You now have succesfully created a dataset that can be used by this program.

## Routedatabank

This data is not downloadable without account, but you can make use of the data
in this repository (only for OSM purposes).
Contact Friso Smit (fw.smit01@gmail.com) if you need a more up-to-date version of the dataset.
