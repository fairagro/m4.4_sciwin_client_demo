#!/usr/bin/env cwl-runner

cwlVersion: v1.2
class: Workflow

inputs:
- id: ags
  type: string
- id: election
  type: string

outputs:
- id: bar
  type: File
  outputSource: plot_election/election

steps:
- id: download_election_data
  in:
  - id: ags
    source: ags
  - id: election
    source: election
  run: ../download_election_data/download_election_data.cwl
  out:
  - election
- id: get_feature_info
  in:
  - id: data
    source: download_election_data/election
  run: ../get_feature_info/get_feature_info.cwl
  out:
  - features
- id: plot_election
  in:
  - id: data
    source: download_election_data/election
  - id: features
    source: get_feature_info/features
  run: ../plot_election/plot_election.cwl
  out:
  - election
