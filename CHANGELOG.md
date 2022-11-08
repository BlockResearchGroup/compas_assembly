# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.6.0] 2022-11-09

### Added

* Added basic "dome" template: `compas_assembly.geometry.Dome`.
* Added resultant visualisation to `compas_assembly.viewer.app.DEMViewer`.
* Added `compas_assembly.datastructures.Assembly.add_block_from_mesh`.
* Added `compas_assembly.datastructures.Assembly.number_of_nodes`.
* Added `compas_assembly.datastructures.Assembly.number_of_edges`.
* Added `compas_assembly.datastructures.Assembly.number_of_blocks`.
* Added `compas_assembly.datastructures.Assembly.number_of_interfaces`.
* Added `compas_assembly.datastructures.Assembly.unset_boundary_conditions`.
* Added `compas_assembly.datastructures.Assembly.set_boundary_condition`.
* Added `compas_assembly.datastructures.Assembly.set_boundary_conditions`.

### Changed

* Fixed bug in `compas_assembly.algorithms.assembly_interfaces`.
* Changed `compas_assembly.algorithms.assembly_interfaces` to return modified assembly for RPC.
* Changed `compas_assembly.algorithms.assembly_interfaces_numpy` to return modified assembly for RPC.

### Removed


## [0.5.0] 2022-10-10

### Added

* Added `compas_assembly.viewer.app.DEMViewer`.
* Added `compas_assembly.viewer.app.DEMController`.
* Added `compas_assembly.viewer.config.json`.
* Added `compas_assembly.datastructures.interface.Interface.polygon`.
* Added `compas_assembly.datastructures.interface.Interface.contactforces`.
* Added `compas_assembly.datastructures.interface.Interface.compressionforces`.
* Added `compas_assembly.datastructures.interface.Interface.tensionforces`.
* Added `compas_assembly.datastructures.interface.Interface.frictionforces`.
* Added `compas_assembly.datastructures.interface.Interface.resultantforce`.

### Changed

### Removed


## [0.4.3] 2022-09-01

### Added

* Added `compas_assembly.algorithms.assembly_interfaces`.
* Added `compas_assembly.datastructures.Interface`.
* Added `compas_assembly.datastructures.Assembly.default_node_attributes['mesh_size']`.
* Added `compas_assembly.datastructures.Assembly.default_node_attributes['section']`.
* Added `compas_assembly.datastructures.Interface.interaction`.

### Changed

* Changed `compas_assembly.algorithms.assembly_interfaces_numpy` to find all interfaces between two blocks.
* Changed `compas_assembly.datastructures.Assembly` do manage multiple interfaces per edge.

### Removed

## 0.1.7

### Added

### Changed

### Removed
