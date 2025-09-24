#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: CommandLineTool

requirements:
- class: InitialWorkDirRequirement
  listing:
  - entryname: code/download_election_data.py
    entry:
      $include: ../../code/download_election_data.py

inputs:
- id: ags
  type: string
  default: '03101000'
  inputBinding:
    prefix: --ags
- id: election
  type: string
  default: Bundestagswahl 2025
  inputBinding:
    prefix: --election

outputs:
- id: data
  type: File
  outputBinding:
    glob: data.csv
stdout: data.csv

baseCommand:
- python
- code/download_election_data.py
