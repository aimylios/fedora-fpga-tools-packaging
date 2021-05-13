%global snapdate @SNAPDATE@
%global commit0 @COMMIT0@
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           yosys
Version:        0.9
Release:        99.%{snapdate}git%{shortcommit0}%{?dist}
Summary:        Yosys Open SYnthesis Suite
License:        ISC and MIT
URL:            http://www.clifford.at/yosys/

Source0:        https://github.com/YosysHQ/yosys/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz
Source1:        https://github.com/mdaines/viz.js/releases/download/0.0.3/viz.js

# https://github.com/YosysHQ/yosys/issues/278
Source2:        http://http.debian.net/debian/pool/main/y/yosys/yosys_0.9-1.debian.tar.xz

Patch0:         https://src.fedoraproject.org/rpms/yosys/raw/rawhide/f/yosys-cfginc.patch

BuildRequires:  abc
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  gcc-c++
BuildRequires:  iverilog
BuildRequires:  libffi-devel
BuildRequires:  make
BuildRequires:  pkgconfig
BuildRequires:  python3
BuildRequires:  readline-devel
BuildRequires:  tcl-devel
BuildRequires:  txt2man

Requires:       %{name}-share = %{version}-%{release}
Requires:       abc
Requires:       graphviz
Requires:       python-xdot

# abc use broken on all Big Endian CPUs, specifically s390x (see BZ 1937362, 1937395):
ExcludeArch:    s390x

%description
Yosys is a framework for Verilog RTL synthesis. It currently has extensive
Verilog-2005 support and provides a basic set of synthesis algorithms for
various application domains.


%package share
Summary:        Architecture-independent Yosys files
BuildArch:      noarch

%description share
Architecture-independent Yosys files.


%package devel
Summary:        Development files to build Yosys synthesizer plugins
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       tcl-devel

%description devel
Development files to build Yosys synthesizer plugins.


%prep
%autosetup -p 1 -n %{name}-%{commit0}

# set GIT_REV to the correct value
sed -i 's/UNKNOWN/%{shortcommit0}/g' Makefile

# Ensure that Makefile doesn't wget viz.js
cp %{SOURCE1} .

# Get man pages from Debian
%setup -q -T -D -a 2 -n %{name}-%{commit0}

# Remove '/usr/bin/env', without changing timestamps, in all python shebangs:
for f in `find . -name \*.py`
do
    sed 's|/usr/bin/env python3|/usr/bin/python3|' $f >$f.new
    touch -r $f $f.new
    mv $f.new $f
done

make config-gcc


%build
%set_build_flags
%make_build PREFIX="%{_prefix}" ABCEXTERNAL=%{_bindir}/abc PRETTY=0 all

%global man_date "`stat -c %y debian/man/yosys-smtbmc.txt | awk '{ print $1 }'`"
txt2man -d %{man_date} -t YOSYS-SMTBMC debian/man/yosys-smtbmc.txt >yosys-smtbmc.1


%install
%make_install PREFIX="%{_prefix}" ABCEXTERNAL=%{_bindir}/abc STRIP=/bin/true

# move include files to includedir
install -d -m 0755 %{buildroot}%{_includedir}
mv %{buildroot}%{_datarootdir}/%{name}/include %{buildroot}%{_includedir}/%{name}

# install man mages
install -d -m 0755 %{buildroot}%{_mandir}/man1
install -m 0644 yosys-smtbmc.1 debian/yosys{,-config,-filterlib}.1 %{buildroot}%{_mandir}/man1


%files
%license COPYING
%doc README.md
%{_bindir}/%{name}
%{_bindir}/%{name}-filterlib
%{_bindir}/%{name}-smtbmc
%{_mandir}/man1/%{name}.1*
%{_mandir}/man1/%{name}-filterlib.1*
%{_mandir}/man1/%{name}-smtbmc.1*

%files share
%{_datarootdir}/%{name}

%files devel
%{_bindir}/%{name}-config
%{_includedir}/%{name}
%{_mandir}/man1/%{name}-config.1*


%changelog
* Thu May 13 2021 Aimylios <aimylios@xxx.xx> - 0.9-99.%{snapdate}git%{shortcommit0}
- Align some comments with upstream
- Download patch from Fedora servers instead of using local copy
- Add ExcludeArch for s390x

* Fri Feb 26 2021 Aimylios <aimylios@xxx.xx> - 0.9-99.%{snapdate}git%{shortcommit0}
- Manually set the git revision to the correct value

* Wed Feb 17 2021 Aimylios <aimylios@xxx.xx> - 0.9-99.%{snapdate}git%{shortcommit0}
- Add make as explicit build-time dependency

* Fri May 1 2020 Aimylios <aimylios@xxx.xx> - 0.9-99.%{snapdate}git%{shortcommit0}
- Initial version for nightly builds based on 0.9-4
