%global snapdate @SNAPDATE@
%global commit0 @COMMIT0@
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           openocd
Version:        0.10.0
Release:        99.%{snapdate}git%{shortcommit0}%{?dist}
Summary:        Debugging, in-system programming and boundary-scan testing for embedded devices
License:        GPLv2
URL:            https://sourceforge.net/projects/openocd

Source0:        %{name}-%{shortcommit0}.tar.xz

BuildRequires:  chrpath
BuildRequires:  gcc
BuildRequires:  hidapi-devel
BuildRequires:  jimtcl-devel
BuildRequires:  libftdi-devel
BuildRequires:  libjaylink-devel
BuildRequires:  libusb-devel
BuildRequires:  libusbx-devel
BuildRequires:  sdcc
BuildRequires:  texinfo

%description
OpenOCD provides on-chip programming and debugging support with a layered
architecture of JTAG interface and TAP support including:

- (X)SVF playback to facilitate automated boundary scan and FPGA/CPLD
programming;

- debug target support (e.g. ARM, MIPS): single-stepping,
breakpoints/watchpoints, gprof profiling, etc;

- flash chip drivers (e.g. CFI, NAND, internal flash);

- embedded TCL interpreter for easy scripting.

Several network interfaces are available for interacting with OpenOCD: telnet,
TCL, and GDB. The GDB server enables OpenOCD to function as a"remote target" for
source-level debugging of embedded systems using the GNU GDB program (and the
others who talk GDB protocol, e.g. IDA Pro).


%prep
%autosetup -n %{name}-%{commit0}
rm -rf jimtcl
rm -f src/jtag/drivers/OpenULINK/ulink_firmware.hex


%build
pushd src/jtag/drivers/OpenULINK
%make_build PREFIX=sdcc hex
popd

%configure \
    --disable-werror \
    --enable-static \
    --disable-shared \
    --enable-dummy \
    --enable-ftdi \
    --enable-stlink \
    --enable-ti-icdi \
    --enable-ulink \
    --enable-usb-blaster-2 \
    --enable-ft232r \
    --enable-vsllink \
    --enable-xds110 \
    --enable-osbdm \
    --enable-opendous \
    --enable-aice \
    --enable-usbprog \
    --enable-rlink \
    --enable-armjtagew \
    --enable-cmsis-dap \
    --enable-kitprog \
    --enable-usb-blaster \
    --enable-presto \
    --enable-openjtag \
    --enable-jlink \
    --enable-parport \
    --enable-parport_ppdev \
    --enable-jtag_vpi \
    --enable-amtjtagaccel \
    --enable-ep39xx \
    --enable-at91rm9200 \
    --enable-gw16012 \
    --enable-buspirate \
    --enable-sysfsgpio \
    --enable-xlnx-pcie-xvc \
    --enable-remote-bitbang \
    --disable-internal-jimtcl \
    --disable-doxygen-html
%make_build


%install
%make_install
rm -f %{buildroot}/%{_infodir}/dir
rm -f %{buildroot}/%{_libdir}/libopenocd.*
rm -rf %{buildroot}/%{_datadir}/%{name}/contrib
mkdir -p %{buildroot}/%{_prefix}/lib/udev/rules.d/
install -p -m 644 contrib/60-openocd.rules %{buildroot}/%{_prefix}/lib/udev/rules.d/60-openocd.rules
chrpath --delete %{buildroot}/%{_bindir}/openocd


%files
%license COPYING
%doc README AUTHORS
%{_bindir}/%{name}
%{_datadir}/%{name}
%{_infodir}/%{name}.info*.gz
%{_mandir}/man1/*
%{_prefix}/lib/udev/rules.d/60-openocd.rules


%changelog
* Fri May 1 2020 Aimylios <aimylios@xxx.xx> - 0.10.0-99.%{snapdate}git%{shortcommit0}
- Initial version for nightly builds based on 0.10.0-15
