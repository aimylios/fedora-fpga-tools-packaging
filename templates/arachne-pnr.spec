%global snapdate @SNAPDATE@
%global commit0 @COMMIT0@
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

# The upstream makefile gets version information by invoking git. We can't
# do that. We can still use what the Makefile calls GIT_REV, because that's
# our shortcommit0 variable extracted from commit0 below.  We have to
# hard-code VER and VER_HASH here, as ver0 and verhash0.  When updating this
# package spec for a new git snapshot, clone the git repo, run make in it,
# and inspect the generated version_(has).cc to determine the correct values.
%global ver0 0.1+328+0
%global verhash0 34321

Name:           arachne-pnr
Version:        0.1
Release:        0.99.%{snapdate}git%{shortcommit0}%{?dist}
Summary:        Place and route for FPGA compilation
License:        GPLv2
URL:            https://github.com/YosysHQ/arachne-pnr

Source0:        https://github.com/YosysHQ/arachne-pnr/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

# https://github.com/YosysHQ/arachne-pnr/issues/126
Patch0:         https://github.com/YosysHQ/%{name}/commit/8843f4d861c739db8c428d5a24d1e97490d4f6df.patch
Patch1:         https://github.com/YosysHQ/arachne-pnr/commit/885b45007d3ea11f8c02f86a92180dd0d60fafe5.patch

BuildRequires:  gcc-c++
BuildRequires:  icestorm

%description
Arachne-pnr implements the place and route step of the hardware compilation
process for FPGAs. It accepts as input a technology-mapped netlist in BLIF
format, as output by the Yosys synthesis suite for example. It currently targets
the Lattice Semiconductor iCE40 family of FPGAs. Its output is a textual
bitstream representation for assembly by the IceStorm icepack command. The
output of icepack is a binary bitstream which can be uploaded to a hardware
device.

Together, Yosys, arachne-pnr and IceStorm provide a fully open-source
Verilog-to-bistream toolchain for iCE40 1K and 8K FPGA development.


%prep
%autosetup -n %{name}-%{commit0} -p1

# can't use git from Makefile to extract version information
sed -i 's/^VER =.*/VER = %{ver0}/' Makefile
sed -i 's/^GIT_REV =.*/GIT_REV = %{shortcommit0}/' Makefile
sed -i 's/^VER_HASH =.*/VER_HASH = %{verhash0}/' Makefile


%build
%make_build \
    CXXFLAGS="%{optflags}" \
    PREFIX="%{_prefix}" \
    ICEBOX="%{_datadir}/icestorm"


%install
%make_install PREFIX="%{_prefix}" \
    DESTDIR="%{buildroot}" \
    ICEBOX="%{_datadir}/icestorm"


%files
%license COPYING
%doc README.md
%{_bindir}/*
%{_datadir}/%{name}


%changelog
* Fri May 1 2020 Aimylios <aimylios@xxx.xx> - 0.1-0.99.%{snapdate}git%{shortcommit0}
- Initial version for nightly builds based on 0.1-0.8.20190729gitc40fb22
