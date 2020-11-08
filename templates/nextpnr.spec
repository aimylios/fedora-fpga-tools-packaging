%global snapdate @SNAPDATE@
%global commit0 @COMMIT0@
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           nextpnr
Version:        0
Release:        0.99.%{snapdate}git%{shortcommit0}%{?dist}
Summary:        FPGA place and route tool
License:        ISC and BSD and MIT and (MIT or Public Domain)
URL:            https://github.com/YosysHQ/nextpnr

Source0:        https://github.com/YosysHQ/nextpnr/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  boost-filesystem
BuildRequires:  boost-iostreams
BuildRequires:  boost-program-options
BuildRequires:  boost-python3-devel
BuildRequires:  boost-thread
BuildRequires:  cmake
BuildRequires:  cmake(QtConfiguration)
BuildRequires:  eigen3-devel
BuildRequires:  gcc-c++
BuildRequires:  icestorm
BuildRequires:  libglvnd-devel
BuildRequires:  make
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  qt5-qtconfiguration-devel
BuildRequires:  trellis-devel

# License: ISC
Provides:       bundled(qtimgui)

# Qt5 enabled fork of QtPropertyBrowser
# License: BSD
Provides:       bundled(QtPropertyBrowser)

# License: MIT
Provides:       bundled(python-console)

# License: (MIT or Public Domain)
Provides:       bundled(imgui) = 1.66-wip

%description
nextpnr aims to be a vendor neutral, timing driven, FOSS FPGA place and route
tool.


%prep
%autosetup -n %{name}-%{commit0}
cp 3rdparty/imgui/LICENSE.txt LICENSE-imgui.txt
cp 3rdparty/qtimgui/LICENSE LICENSE-qtimgui.txt
cp 3rdparty/python-console/LICENSE LICENSE-python-console.txt


%build
%cmake . \
    -DARCH=all \
    -DICEBOX_DATADIR=%{_datadir}/icestorm \
    -DTRELLIS_LIBDIR=%{_libdir}/trellis \
    -DCURRENT_GIT_VERSION=%{shortcommit0}
%cmake_build
# prepare examples doc. directory:
mkdir -p examples/ice40
cp -r ice40/examples/* examples/ice40


%install
%cmake_install


%files
%license COPYING
%license LICENSE-imgui.txt LICENSE-qtimgui.txt LICENSE-python-console.txt
%doc README.md docs examples
%{_bindir}/nextpnr-generic
%{_bindir}/nextpnr-ice40
%{_bindir}/nextpnr-ecp5


%changelog
* Sun Nov 8 2020 Aimylios <aimylios@xxx.xx> - 0-0.99.%{snapdate}git%{shortcommit0}
- Fix usage of cmake macros
- Add python3-setuptools as build-time requirement

* Sat Aug 8 2020 Aimylios <aimylios@xxx.xx> - 0-0.99.%{snapdate}git%{shortcommit0}
- Explicitly set ICEBOX_DATADIR instead of ICESTORM_INSTALL_PREFIX
- Explicitly set TRELLIS_LIBDIR instead of TRELLIS_INSTALL_PREFIX

* Sat Aug 1 2020 Aimylios <aimylios@xxx.xx> - 0-0.99.%{snapdate}git%{shortcommit0}
- Update CMake variables

* Fri May 1 2020 Aimylios <aimylios@xxx.xx> - 0-0.99.%{snapdate}git%{shortcommit0}
- Initial version for nightly builds based on 0-0.10.20200129git85f4452
