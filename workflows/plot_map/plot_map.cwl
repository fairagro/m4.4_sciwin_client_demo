#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: CommandLineTool

requirements:
- class: InitialWorkDirRequirement
  listing:
  - entryname: code/plot_map.py
    entry:
      $include: ../../code/plot_map.py
- class: DockerRequirement
  dockerFile:
    $include: ../../Dockerfile
  dockerImageId: pyplot
- class: NetworkAccess
  networkAccess: true

inputs:
- id: geojson
  type: File
  default:
    class: File
    location: ../../districts.geojson
  inputBinding:
    prefix: --geojson
- id: csv
  type: File
  default:
    class: File
    location: ../../data.csv
  inputBinding:
    prefix: --csv
- id: feature
  type: string
  default: F3
  inputBinding:
    prefix: --feature
- id: on
  type: string
  default: gebiet-nr:BEZNUM
  inputBinding:
    prefix: --on
- id: output_name
  type: string
  default: plot
  inputBinding:
    prefix: --output_name

outputs:
- id: plot
  type: File
  outputBinding:
    glob: plot.png

baseCommand:
- python
- code/plot_map.py
