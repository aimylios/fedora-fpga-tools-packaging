# fedora-fpga-tools-packaging

## Packaging nightly builds of open source FPGA tools for Fedora

Different to most other Linux distributions, Fedora tends to package the latest available version of an application, and sometimes even snapshots of unreleased versions. But updates typically happen every couple of months, and sometimes they are only pushed to Rawhide. This is not a satisfying situation in the quickly evolving world of open source tools for FPGA development, where important bug fixes and interesting new features get added on a daily basis, but official releases happen rarely (or even never at all).

To improve this situation, I've decided to provide nightly builds for Fedora of all the open source FPGA tools I personally use:
* [OpenOCD](http://openocd.org/)
* [Icarus Verilog](http://iverilog.icarus.com/)
* [Yosys](https://yosyshq.net/yosys/) (currently not built as part of the nightlies)
* [GHDL](http://ghdl.free.fr/)
* [ghdl-yosys-plugin](https://github.com/ghdl/ghdl-yosys-plugin)
* [Project IceStorm](https://clifford.at/icestorm/)
* [Project Trellis](https://github.com/SymbiFlow/prjtrellis)
* [arachne-pnr](https://github.com/YosysHQ/arachne-pnr)
* [nextpnr](https://github.com/YosysHQ/nextpnr)

This repository only includes the SPEC description files for the RPMs and the packaging scripts. The ready-made RPMs are available via my personal [aimylios/fpga-tools-nightly](https://copr.fedorainfracloud.org/coprs/aimylios/fpga-tools-nightly/) Copr repository. They are rebuilt automatically on a regular basis in case new commits have been added since the last build.
