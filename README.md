This programs compares OSM walking route data to that of other data sets.


# Installation

Make sure to install python on your system. This program depends on the
following libraries:

- python geojson for package for importing geojson data
- pyside6 for the Qt GUI

Open a command prompt and install with:
	
	pip install geojson pyside6

Then download the code repository from github. You can dowload the latest
release (recommended) or the latest git version.

To download the latest release, go to
https://github.com/fwsmit/osm-knooppunten/releases/latest and download the
source code (zip). Unzip this to a directory of your choice. Then you can
proceed to running it.

# Running (GUI)

It's easy to run this program with it's graphical interface. Simply run the
file `knooppunten.py` that you just unzipped in python. To do this, right click
the file in your file manager and select "Run with" and choose python. The
application should open.

## Selecting data

The proram needs two data files to compare. In the section "Getting the data"
you can learn more about how to aquire the data. There are
some example data files provided for the region Groningen.
Let's move on, assuming you have the right data.

The first step is selecting the OSM data. Press the "Select button" to select
an OSM data file (.osm).

Then you can select a data file to compare against. This file has to be of the
geojson format.

Lastly you can filter the import data by region. This is strongly recommended
to make the computing time reasonable. Also make sure the OSM data is also of
the same region to minimize the number of false positives.

## Running analysis

If you're done selecting the data, click the "run" button to start the
analysis. This will open a new window that will eventually display the results.

## Interpreting results

The results window shows a table of different node categories. All nodes from
the import dataset have been categorized in one of the following categories:

- `Renamed`: Node is still in the same place, but has a different number
- `Removed`: Node is not present in import dataset, but is in OSM
- `Added`: Node is not present in OSM, but is in the import dataset
- `No change`: Nothing is different between the OSM and import node
- `Moved short distance`: Node moved a distance of <100m
- `Moved long distance`: Node moved a distance of 100-1000m
- `Other`: Could not be determined to be in one of the above categories

All results are exported to geojson. You can open them in JOSM to analyze them
further and make changes to OSM. All nodes in the export have metadata tagged
to thme with their node numbers in the import dataset.

# Data sources

This tool is written for comparing the data from OpenStreetMap and Routedatabank in mind.

## OSM data

Below are the instructions to download the OSM data. This might be automated in
the future with an overpass query.

- Open JOSM with remote control enabled
- Go to https://knooppuntnet.nl/nl/analysis/hiking
- Select "Explore by network" on the left.
- Navigate to the network you want to analyze
- Click the edit button. The dataset will open in JOSM
- Click "file > save as" and save as .osm file

You now have succesfully created a dataset that can be used by this program.

## Routedatabank

This data is not downloadable without account, but you can make use of the data
in this repository (only for OSM purposes).
Contact Friso Smit (fw.smit01@gmail.com) if you need a more up-to-date version of the dataset.

# Command line interface

You can also run the analyzer using a command line interface. This currently has
the similar functionality to the graphical application. Instructions for running
it are below.

Open a terminal in this project's directory. The program can be run
with the following command:

	python knooppunten-cli.py [-h] --osmfile OSMFILE --importfile IMPORTFILE [--region REGION]

Where you replace the arguments in capital letters with your own arguments. For example:

	python knooppunten-cli.py --osmfile data/groningen.osm --importfile 'data/Wandelknooppunten (wgs84).geojson' --region "Groningen"

Or for Windows users:

	python knooppunten-cli.py --osmfile data\groningen.osm --importfile 'data\Wandelknooppunten (wgs84).geojson' --region "Groningen"


For more detail about the arguments, run:

	python knooppunten-cli.py -h
