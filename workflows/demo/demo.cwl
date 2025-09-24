#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: Workflow

inputs:
- id: election
  type: string
- id: ags
  type: string

outputs:
- id: bar
  type: File
  outputSource: plot_election/election

steps:
- id: download_election_data
  in:
  - id: election
    source: election
  - id: ags
    source: ags
  run: ../download_election_data/download_election_data.cwl
  out:
  - data
- id: get_feature_info
  in:
  - id: data
    source: download_election_data/data
  run: ../get_feature_info/get_feature_info.cwl
  out:
  - features
- id: plot_election
  in:
  - id: data
    source: download_election_data/data
  - id: features
    source: get_feature_info/features
  run: ../plot_election/plot_election.cwl
  out:
  - election
