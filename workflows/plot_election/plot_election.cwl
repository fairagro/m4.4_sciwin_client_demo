#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: CommandLineTool

requirements:
- class: InitialWorkDirRequirement
  listing:
  - entryname: code/plot_election.py
    entry:
      $include: ../../code/plot_election.py
- class: DockerRequirement
  dockerFile:
    $include: ../../Dockerfile
  dockerImageId: pyplot
- class: NetworkAccess
  networkAccess: true

inputs:
- id: data
  type: File
  default:
    class: File
    location: ../../data.csv
  inputBinding:
    prefix: --data
- id: features
  type: File
  default:
    class: File
    location: ../../features.json
  inputBinding:
    prefix: --features

outputs:
- id: election
  type: File
  outputBinding:
    glob: election.png

baseCommand:
- python
- code/plot_election.py
