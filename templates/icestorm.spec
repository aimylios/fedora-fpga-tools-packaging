%global snapdate @SNAPDATE@
%global commit0 @COMMIT0@
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           icestorm
Version:        0
Release:        0.99.%{snapdate}git%{shortcommit0}%{?dist}
Summary:        Lattice iCE40 FPGA bitstream creation/analysis/programming tools
License:        ISC
URL:            http://www.clifford.at/icestorm/

Source0:        https://github.com/cliffordwolf/icestorm/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

#Patch1:         %%{name}-datadir.patch

BuildRequires:  gcc-c++
BuildRequires:  libftdi-devel
BuildRequires:  python3

%description
Project IceStorm aims at documenting the bitstream format of Lattice iCE40
FPGAs and providing simple tools for analyzing and creating bitstream files.


%prep
%autosetup -n %{name}-%{commit0}

# fix shebang lines in Python scripts
find . -name \*.py -exec sed -i 's|/usr/bin/env python3|/usr/bin/python3|' {} \;
# get rid of .gitignore files in examples
find . -name \.gitignore -delete


%build
%global moreflags -I/usr/include/libftdi1
%make_build \
    CFLAGS="%{optflags} %{moreflags}" \
    CXXFLAGS="%{optflags} %{moreflags}" \
    PREFIX="%{_prefix}" \
    CHIPDB_SUBDIR="%{name}" \
    LDFLAGS="$RPM_LD_FLAGS"


%install
%make_install PREFIX="%{_prefix}"
chmod +x %{buildroot}%{_bindir}/icebox.py
mv %{buildroot}%{_datarootdir}/icebox %{buildroot}%{_datarootdir}/%{name}
install -p -m 644 icefuzz/timings_*.txt %{buildroot}%{_datarootdir}/%{name}


%files
%license COPYING
%doc README examples
%{_bindir}/*
%{_datarootdir}/%{name}/


%changelog
* Fri May 1 2020 Aimylios <aimylios@xxx.xx> - 0-0.99.%{snapdate}git%{shortcommit0}
- Initial version for nightly builds based on 0-0.11.20190823git9594931
