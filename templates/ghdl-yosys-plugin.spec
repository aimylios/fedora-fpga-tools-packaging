%global snapdate @SNAPDATE@
%global commit0 @COMMIT0@
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           ghdl-yosys-plugin
Version:        0
Release:        0.1.%{snapdate}git%{shortcommit0}%{?dist}
Summary:        GHDL plugin for Yosys
License:        GPLv3
URL:            https://github.com/ghdl/ghdl-yosys-plugin

Source0:        https://github.com/ghdl/ghdl-yosys-plugin/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  ghdl
BuildRequires:  libffi-devel
BuildRequires:  readline-devel
BuildRequires:  yosys-devel

Requires:       yosys

%description
VHDL synthesis based on GHDL and Yosys.


%prep
%autosetup -n %{name}-%{commit0}


%build
%make_build


%install
mkdir -p %{buildroot}%{_datadir}/yosys/plugins/
install -p ghdl.so %{buildroot}%{_datadir}/yosys/plugins/


%files
%license LICENSE
%doc README.md
%{_datadir}/yosys/plugins/ghdl.so


%changelog
* Fri May 1 2020 Aimylios <aimylios@xxx.xx> - 0-0.1.%{snapdate}git%{shortcommit0}
- Initial version for nightly builds
