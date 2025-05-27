#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: CommandLineTool

requirements:
- class: InitialWorkDirRequirement
  listing:
  - entryname: code/get_feature_info.py
    entry:
      $include: ../../code/get_feature_info.py

inputs:
- id: data
  type: File
  default:
    class: File
    location: ../../data.csv
  inputBinding:
    prefix: --data

outputs:
- id: features
  type: File
  outputBinding:
    glob: features.json

baseCommand:
- python
- code/get_feature_info.py
