# SciWIn Client Demo
A basic Workflow using SciWIn Client (`s4n`) can be created with the commands hereafter. This guid assumes the usage of unix based operating systems, however Windows should work, too. If not please [open an issue](https://github.com/fairagro/m4.4_sciwin_client/issues/new).

## Installation
[![GitHub Release](https://img.shields.io/github/v/release/fairagro/m4.4_sciwin_client)](https://github.com/fairagro/m4.4_sciwin_client/releases/latest)

The latest Version of `s4n` can be installed using the following command:
```
curl --proto '=https' --tlsv1.2 -LsSf https://fairagro.github.io/m4.4_sciwin_client/get_s4n.sh | sh 
```

Specific Versions can be installed with the following command, by replacing the version tag with a version of choice.
```
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/fairagro/m4.4_sciwin_client/releases/download/v0.6.0/s4n-installer.sh | sh
```

The Installation can be verified using `s4n -V`.
SciWIn Client comes with a lot of commands. In this demo the `init`, `tool`, `workflow` and `execute` commands will be showcased.
```
 _____        _  _    _  _____         _____  _  _               _   
/  ___|      (_)| |  | ||_   _|       /  __ \| |(_)             | |   
\ `--.   ___  _ | |  | |  | |  _ __   | /  \/| | _   ___  _ __  | |_  
 `--. \ / __|| || |/\| |  | | | '_ \  | |    | || | / _ \| '_ \ | __|
/\__/ /| (__ | |\  /\  / _| |_| | | | | \__/\| || ||  __/| | | || |_  
\____/  \___||_| \/  \/  \___/|_| |_|  \____/|_||_| \___||_| |_| \__|

Client tool for Scientific Workflow Infrastructure (SciWIn)
Documentation: https://fairagro.github.io/m4.4_sciwin_client/

Version: 0.6.0

Usage: s4n <COMMAND>

Commands:
  init         Initializes project folder structure and repository
  tool         Provides commands to create and work with CWL CommandLineTools
  workflow     Provides commands to create and work with CWL Workflows
  annotate     Annotate CWL files
  execute      Execution of CWL Files locally or on remote servers [aliases: ex]
  sync         
  completions  Generate shell completions
  help         Print this message or the help of the given subcommand(s)

Options:
  -h, --help     Print help
  -V, --version  Print version
```

## Demo Repository
The [Demo Repository](https://github.com/fairagro/sciwin_client_demo) mainly contains two folders `data` and `code`. The result workflow will convert input data into a `geojson` file, download election data and maps it onto the `geojson` data resulting in a `choropleth` graph.

![result]()

## Creating the CommandLineTools
First of all, we start, by creating a new `s4n` project.
```
s4n init
```

CWL mainly describes processes in CommandLineTools which later can be connected into Workflows. CommandLineTools are essentially wrappers for commands that would usually be executed in the command line. CWL uses a special YAML structure to describe those processes.

```cwl
#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: CommandLineTool

requirements:
- class: DockerRequirement
  dockerPull: osgeo/gdal:ubuntu-full-3.6.3
- class: InlineJavascriptRequirement

inputs:
- id: districts_geojson
  type: string
  default: districts.geojson
  inputBinding:
    position: 0
- id: data_braunschweig
  type: Directory
  default:
    class: Directory
    location: ../../data/braunschweig
  inputBinding:
    position: 1
- id: lco
  type: string
  default: RFC7946=YES
  inputBinding:
    prefix: -lco

outputs:
- id: districts
  type: File
  outputBinding:
    glob: $(inputs.districts_geojson)

baseCommand: ogr2ogr
```

However it may is tedious to write those files by hand. That is where `s4n` comes to the rescue. A Command that would normally happen on the command line just needs to be prefixed with `s4n tool create`. Examples can be found at the [documentation](https://fairagro.github.io/m4.4_sciwin_client/examples/tool-creation/).

The first tool, we need to create uses [GDAL](https://de.wikipedia.org/wiki/Geospatial_Data_Abstraction_Library) to convert the shape file in `data/braunschweig` to a `geojson` file. The Command one would typically use would be
```bash
ogr2ogr districts.geojson data/braunschweig -lco RFC7946=YES
# s4n command
s4n tool create ogr2ogr districts.geojson data/braunschweig -lco RFC7946=YES
```

However we might not have gdal installed on our machine, so we request `s4n` to not run the command. Therefore `s4n` needs to be told what file will be written with `-o` and for later usage a docker image is specified using `-c`.
```bash
s4n tool create --name shp2geojson --no-run -o districts.geojson -c osgeo/gdal:ubuntu-full-3.6.3 ogr2ogr districts.geojson data/braunschweig -lco RFC7946=YES
```
This correct creation of the tool can be tested using 
```bash
s4n execute local workflows/shp2geojson/shp2geojson.cwl 
```

The outputted file now needs to be committed to move on
```bash
git add . && git commit -m "Execution of shp2geojson"
```

To create Tools based of the Python scripts in the `code` Directory a virtual environment needs to be created using 
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install plotly pandas kaleido
```

The next step is to download election data using a series of API calls for which luckily already a script exists. The script downloads the data from `votemanager.kdo.de` and writes the `csv` to stdout.
A tool can be created easily be prefixing the python call. However we also need to escape the `>` using a backslash for it to properly work
```bash
s4n tool create python code/download_election_data.py --ags 03101000 --election "Bundestagswahl 2025" \> election.csv
```

In the last step the plot tool needs to be created. In this tool `plotly` is used to create a `choropleth` graph based on the outputs of the preceeding steps. The packages installed to the virtual environment are needed here. A Dockerfile to use is already in the repo.
```bash
s4n tool create -c Dockerfile --container-tag pyplot --enable-network python code/plot_map.py --geojson districts.geojson --csv election.csv --feature F3 --on gebiet-nr:BEZNUM --output_name plot
```

## Combining the Tools into a workflow
The three CommandLineTools now will be combined into an automated pipeline. A barebones workflow can be generated by using the create command
```bash
s4n workflow create demo
```

The workflow we want to build looks like the graph represented in the following image
![the resulting workflow]()

Knowing that the plot tool needs the geojson, a connection from the geojson output to the corresponding input can be created.
```bash
s4n workflow connect demo --from shp2geojson/districts --to plot_map/geojson
```

To get the correct values for `--from` and `--to` the command `s4n tool ls -a` can be used. As the plot step also needs the election data, another connection can be created.
```bash
s4n workflow connect demo --from download_election_data/election --to plot_map/csv
```

Now we need to wire up the inputs. In all three tools there are a lot of inputs, but some have default values. That means only neccesary connections have to be made. For the creation of inputs the `--from` value neeeds to start with `@inputs`. The input connections for `ags`, `election`, `feature`and `shapes` will be created as follows:
```bash
s4n workflow connect demo --from @inputs/ags --to download_election_data/ags
s4n workflow connect demo --from @inputs/election --to download_election_data/election
s4n workflow connect demo --from @inputs/feature --to plot_map/feature
s4n workflow connect demo --from @inputs/shapes --to shp2geojson/data_braunschweig
```

The last step is to add the outputs to the workflow. Only the `png` file is desired, therefore a single output is created using
```bash
s4n workflow connect demo --from plot_map/plot --to @outputs/result
```

Saving the workflow is neccessary to have a clean git history for furhter creating CommandLineTools.

```bash
s4n workflow save demo
```

## Workflow Execution
We want to clean our workspace by deleting the outputs we created by creating the CommandLineTools. For the execution a parameter file will be created using the `s4n execute make-template` command.
```bash
s4n execute make-template workflows/demo/demo.cwl > inputs.yml
```

This needs to be updated using the correct input values:
```yaml
ags: "03101000"
election: Bundestagswahl 2025
shapes:
  class: Directory
  location: data/braunschweig
feature: F3
```

Execution of the Workflow is done by
```bash
s4n execute local workflows/demo/demo.cwl inputs.yml
```