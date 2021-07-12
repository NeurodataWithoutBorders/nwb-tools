# nwbtools

## nwbls
Tool to print the contents of an NWB file

For example:
```bash
$ nwbls nwbfile.nwb
- acquisition: Group (1 members)
  - TimeSeries: Group (2 members)
    - data: Dataset (shape: (10000, 10), dtype: int32)
      > conversion: 1.0
      > resolution: -1.0
      > unit: unit
    - starting_time: Dataset (shape: (), dtype: float64)
      > rate: 1.0
      > unit: seconds
    > comments: no comments
    > description: no description
    > namespace: core
    > neurodata_type: TimeSeries
    > object_id: 5f9d991c-e106-4df3-bf8f-ce8fa174d52f
- analysis: Group (0 members)
- file_create_date: Dataset (shape: (1,), dtype: object)
- general: Group (0 members)
- identifier: Dataset (shape: (), dtype: object)
- processing: Group (0 members)
- session_description: Dataset (shape: (), dtype: object)
- session_start_time: Dataset (shape: (), dtype: object)
- specifications: Group (3 members)
  - core: Group (1 members)
    - 2.3.0: Group (13 members)
      - namespace: Dataset (shape: (), dtype: object)
      - nwb.base: Dataset (shape: (), dtype: object)
      - nwb.behavior: Dataset (shape: (), dtype: object)
      - nwb.device: Dataset (shape: (), dtype: object)
      - nwb.ecephys: Dataset (shape: (), dtype: object)
      - nwb.epoch: Dataset (shape: (), dtype: object)
      - nwb.file: Dataset (shape: (), dtype: object)
      - nwb.icephys: Dataset (shape: (), dtype: object)
      - nwb.image: Dataset (shape: (), dtype: object)
      - nwb.misc: Dataset (shape: (), dtype: object)
      - nwb.ogen: Dataset (shape: (), dtype: object)
      - nwb.ophys: Dataset (shape: (), dtype: object)
      - nwb.retinotopy: Dataset (shape: (), dtype: object)
  - hdmf-common: Group (1 members)
    - 1.5.0: Group (4 members)
      - base: Dataset (shape: (), dtype: object)
      - namespace: Dataset (shape: (), dtype: object)
      - sparse: Dataset (shape: (), dtype: object)
      - table: Dataset (shape: (), dtype: object)
  - hdmf-experimental: Group (1 members)
    - 0.1.0: Group (3 members)
      - experimental: Dataset (shape: (), dtype: object)
      - namespace: Dataset (shape: (), dtype: object)
      - resources: Dataset (shape: (), dtype: object)
- stimulus: Group (2 members)
  - presentation: Group (0 members)
  - templates: Group (0 members)
- timestamps_reference_time: Dataset (shape: (), dtype: object)
> .specloc: Reference to /specifications
> namespace: core
> neurodata_type: NWBFile
> nwb_version: 2.3.0
> object_id: 41284c57-659a-442f-aad8-a9f920a771a0
```

## nwbtrim
Tool to reduce the size of an NWB file for debugging and sharing
