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
