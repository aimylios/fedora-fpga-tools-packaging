%global snapdate @SNAPDATE@
%global commit0 @COMMIT0@
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           iverilog
Version:        12.0
Release:        0.1.%{snapdate}git%{shortcommit0}%{?dist}
Summary:        Icarus Verilog is a verilog compiler and simulator
License:        GPLv2
URL:            http://iverilog.icarus.com

Source0:        https://github.com/steveicarus/iverilog/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  autoconf
BuildRequires:  bison
BuildRequires:  bzip2-devel
BuildRequires:  flex
BuildRequires:  gcc-c++
BuildRequires:  gperf
BuildRequires:  make
BuildRequires:  readline-devel
BuildRequires:  zlib-devel

%description
Icarus Verilog is a Verilog compiler that generates a variety of engineering
formats, including simulation. It strives to be true to the IEEE-1364 standard.


%prep
%autosetup -n %{name}-%{commit0}
find . -type f -name ".git" -exec rm '{}' \;
rm -rf `find . -type d -name "autom4te.cache" -exec echo '{}' \;`

# set VERSION_TAG to the correct value
sed -i 's/VERSION_TAG ""/VERSION_TAG "%{shortcommit0}"/g' Makefile.in


%build
chmod +x autoconf.sh
sh autoconf.sh
export CPPFLAGS="$CPPFLAGS -fcommon"
%configure

# avoid use V=1 due https://github.com/steveicarus/iverilog/issues/262
make %{?_smp_mflags}


%install
make \
    prefix=%{buildroot}%{_prefix} \
    bindir=%{buildroot}%{_bindir} \
    libdir=%{buildroot}%{_libdir} \
    libdir64=%{buildroot}%{_libdir} \
    includedir=%{buildroot}%{_includedir} \
    mandir=%{buildroot}%{_mandir}  \
    vpidir=%{buildroot}%{_libdir}/ivl/ \
    INSTALL="install -p" \
    install


%check
make check


%files
%license COPYING
%doc BUGS.txt README.txt QUICK_START.txt
%doc ieee1364-notes.txt mingw.txt swift.txt netlist.txt
%doc t-dll.txt vpi.txt cadpli/cadpli.txt
%doc xilinx-hint.txt examples/
%doc va_math.txt tgt-fpga/fpga.txt extensions.txt glossary.txt attributes.txt
%{_bindir}/*
%{_libdir}/ivl
%{_mandir}/man1/*
# headers for PLI: This is intended to be used by the user.
%{_includedir}/*.h
# RHBZ 480531
%{_libdir}/*.a


%changelog
* Fri Feb 26 2021 Aimylios <aimylios@xxx.xx> - 12.0-0.1.%{snapdate}git%{shortcommit0}
- Manually set the git revision to the correct value

* Wed Feb 17 2021 Aimylios <aimylios@xxx.xx> - 12.0-0.1.%{snapdate}git%{shortcommit0}
- Add make as explicit build-time dependency

* Fri May 1 2020 Aimylios <aimylios@xxx.xx> - 11.0-0.1.%{snapdate}git%{shortcommit0}
- Initial version for nightly builds based on 10.3-3
