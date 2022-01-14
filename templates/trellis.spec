%global snapdate @SNAPDATE@
%global commit0 @COMMIT0@
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global commit1 @COMMIT1@
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})

Name:           trellis
Version:        1.1
Release:        99.%{snapdate}git%{shortcommit0}%{?dist}
Summary:        Lattice ECP5 FPGA bitstream creation/analysis/programming tools
License:        ISC
URL:            https://github.com/YosysHQ/prjtrellis

Source0:        https://github.com/YosysHQ/prjtrellis/archive/%{commit0}/prjtrellis-%{shortcommit0}.tar.gz
Source1:        https://github.com/YosysHQ/prjtrellis-db/archive/%{commit1}/prjtrellis-db-%{shortcommit1}.tar.gz

BuildRequires:  boost-python3-devel
BuildRequires:  cmake
BuildRequires:  gcc-c++
BuildRequires:  make
BuildRequires:  python3-devel
# for building manpages:
BuildRequires:  help2man

Requires:       %{name}-data = %{version}-%{release}

%description
Project Trellis enables a fully open-source flow for ECP5 FPGAs using Yosys for
Verilog synthesis and nextpnr for place and route. Project Trellis provides the
device database and tools for bitstream creation.


%package devel
Summary:        Development files for Project Trellis
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-data = %{version}-%{release}

%description devel
Development files to build packages using Project Trellis


%package data
Summary:        Project Trellis - Lattice ECP5 Bitstream Database
BuildArch:      noarch

%description data
This package contains the bitstream documentation database for Lattice ECP5 FPGA
devices.


%prep
%setup -q -n prj%{name}-%{commit0} -a 1
rm -rf database
mv prj%{name}-db-%{commit1} database
# add "-fPIC -g1" to CMAKE_CXX_FLAGS:
# (NOTE: "-g1" reduces debuginfo verbosity over "-g", which helps on armv7hl)
sed -i '/CMAKE_CXX_FLAGS/s/-O3/-O3 -fPIC -g1/' libtrellis/CMakeLists.txt
# prevent "lib64" false positive (e.g., on i386):
sed -i 's/"lib64"/"lib${LIB_SUFFIX}"/' libtrellis/CMakeLists.txt
# fix shebang lines in Python scripts:
find . -name \*.py -exec sed -i 's|/usr/bin/env python3|/usr/bin/python3|' {} \;
# remove .gitignore files in examples:
find . -name \.gitignore -delete


%build
# building manpages requires in-source build:
%define __cmake_in_source_build 1
%cmake libtrellis -DCURRENT_GIT_VERSION=%{version}-%{release}
%cmake_build
# build manpages:
mkdir man1
for f in ecp*
do
    [ -x $f ] || continue
    LD_PRELOAD=./libtrellis.so \
        help2man --no-discard-stderr --version-string %{version} -N \
            -o man1/$f.1 ./$f
    sed -i '/required but missing/d' man1/$f.1
done


%install
%cmake_install
install -D -p -m 644 -t %{buildroot}%{_mandir}/man1 man1/*


%files
%license COPYING
%doc README.md
%doc examples
%{_bindir}/*
%dir %{_libdir}/%{name}/
%{_libdir}/%{name}/libtrellis.so
%{_datadir}/%{name}/misc/
%{_mandir}/man1/ecp*.1*

%files devel
%doc libtrellis/examples
%{_libdir}/%{name}/pytrellis.so
%{_datadir}/%{name}/timing
%{_datadir}/%{name}/util

%files data
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/database


%changelog
* Fri Jan 14 2022 Aimylios <aimylios@xxx.xx> - 1.1-99.%{snapdate}git%{shortcommit0}
- Bump version to 1.1
- Remove python3-setuptools from build-time requirements

* Thu May 13 2021 Aimylios <aimylios@xxx.xx> - 1.0-99.%{snapdate}git%{shortcommit0}
- Add python3-setuptools as build-time requirement

* Wed Feb 17 2021 Aimylios <aimylios@xxx.xx> - 1.0-99.%{snapdate}git%{shortcommit0}
- Update source URLs
- Add make as explicit build-time dependency
- Re-enable LTO

* Sun Nov 8 2020 Aimylios <aimylios@xxx.xx> - 1.0-99.%{snapdate}git%{shortcommit0}
- Fix usage of cmake macros
- Disable LTO for now (RHBZ 1865586)

* Fri May 1 2020 Aimylios <aimylios@xxx.xx> - 1.0-99.%{snapdate}git%{shortcommit0}
- Initial version for nightly builds based on 1.0-0.7.20200127git30ee6f2
