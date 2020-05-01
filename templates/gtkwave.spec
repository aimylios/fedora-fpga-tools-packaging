%global snapdate @SNAPDATE@
%global commit0 @COMMIT0@
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           gtkwave
Version:        3.3.105
Release:        0.1.%{snapdate}git%{shortcommit0}%{?dist}
Summary:        Waveform Viewer
License:        GPLv2+
URL:            http://gtkwave.sourceforge.net/

Source0:        https://github.com/gtkwave/gtkwave/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

BuildRequires:  bzip2-devel
BuildRequires:  coreutils
BuildRequires:  desktop-file-utils
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  flex
BuildRequires:  gedit
BuildRequires:  gnome-icon-theme
BuildRequires:  gperf
BuildRequires:  gtk2-devel
BuildRequires:  hicolor-icon-theme
BuildRequires:  Judy-devel
BuildRequires:  libappstream-glib
BuildRequires:  libtirpc-devel
BuildRequires:  make
BuildRequires:  pkgconfig(gio-unix-2.0) >= 2.0
BuildRequires:  shared-mime-info
BuildRequires:  tcl-devel >= 8.4
BuildRequires:  tk-devel
BuildRequires:  xz-devel
BuildRequires:  zlib-devel

Recommends:     gedit
Requires:       gnome-icon-theme
Requires:       hicolor-icon-theme
Requires:       shared-mime-info

%description
GTKWave is a waveform viewer that can view VCD files produced by most Verilog
simulation tools, as well as LXT files produced by certain Verilog simulation
tools.


%prep
%autosetup -n %{name}-%{commit0}


%build
cd gtkwave3/
%configure \
    --disable-dependency-tracking \
    --disable-mime-update \
    --enable-judy \
    --with-gsettings \
    --with-tirpc
%make_build


%install
cd gtkwave3/
%make_install

# Icons and desktop entry
desktop-file-install --vendor "" --dir %{buildroot}%{_datadir}/applications \
    share/applications/gtkwave.desktop
install -D -m 644 -p share/icons/gnome/16x16/mimetypes/gtkwave.png \
    %{buildroot}%{_datadir}/icons/hicolor/16x16/apps/gtkwave.png
install -D -m 644 -p share/icons/gnome/32x32/mimetypes/gtkwave.png \
    %{buildroot}%{_datadir}/icons/hicolor/32x32/apps/gtkwave.png
install -D -m 644 -p share/icons/gnome/48x48/mimetypes/gtkwave.png \
    %{buildroot}%{_datadir}/icons/hicolor/48x48/apps/gtkwave.png
install -D -m 644 -p share/icons/gtkwave_256x256x32.png \
    %{buildroot}%{_datadir}/icons/hicolor/256x256/apps/gtkwave.png

# Appdata
install -D -m 644 -p share/appdata/gtkwave.appdata.xml \
    %{buildroot}%{_datadir}/appdata/gtkwave.appdata.xml


%check
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/gtkwave.appdata.xml


%files
%license gtkwave3/COPYING gtkwave3/LICENSE.TXT
%doc gtkwave3/AUTHORS gtkwave3/ChangeLog
%{_bindir}/evcd2vcd
%{_bindir}/fst2vcd
%{_bindir}/fstminer
%{_bindir}/ghwdump
%{_bindir}/gtkwave
%{_bindir}/lxt2miner
%{_bindir}/lxt2vcd
%{_bindir}/rtlbrowse
%{_bindir}/shmidcat
%{_bindir}/twinwave
%{_bindir}/vcd2fst
%{_bindir}/vcd2lxt
%{_bindir}/vcd2lxt2
%{_bindir}/vcd2vzt
%{_bindir}/vzt2vcd
%{_bindir}/vztminer
%{_bindir}/xml2stems
%{_datadir}/%{name}/
%{_datadir}/appdata/gtkwave.appdata.xml
%{_datadir}/applications/gtkwave.desktop
%{_datadir}/glib-2.0/schemas/com.geda.gtkwave.gschema.xml
%{_datadir}/icons/gnome/16x16/mimetypes/gnome-mime-application-vnd.gtkwave-ae2.png
%{_datadir}/icons/gnome/16x16/mimetypes/gnome-mime-application-vnd.gtkwave-aet.png
%{_datadir}/icons/gnome/16x16/mimetypes/gnome-mime-application-vnd.gtkwave-evcd.png
%{_datadir}/icons/gnome/16x16/mimetypes/gnome-mime-application-vnd.gtkwave-fst.png
%{_datadir}/icons/gnome/16x16/mimetypes/gnome-mime-application-vnd.gtkwave-ghw.png
%{_datadir}/icons/gnome/16x16/mimetypes/gnome-mime-application-vnd.gtkwave-gtkw.png
%{_datadir}/icons/gnome/16x16/mimetypes/gnome-mime-application-vnd.gtkwave-lx2.png
%{_datadir}/icons/gnome/16x16/mimetypes/gnome-mime-application-vnd.gtkwave-lxt.png
%{_datadir}/icons/gnome/16x16/mimetypes/gnome-mime-application-vnd.gtkwave-lxt2.png
%{_datadir}/icons/gnome/16x16/mimetypes/gnome-mime-application-vnd.gtkwave-vcd.png
%{_datadir}/icons/gnome/16x16/mimetypes/gnome-mime-application-vnd.gtkwave-vzt.png
%{_datadir}/icons/gnome/16x16/mimetypes/gtkwave.png
%{_datadir}/icons/gnome/32x32/mimetypes/gnome-mime-application-vnd.gtkwave-ae2.png
%{_datadir}/icons/gnome/32x32/mimetypes/gnome-mime-application-vnd.gtkwave-aet.png
%{_datadir}/icons/gnome/32x32/mimetypes/gnome-mime-application-vnd.gtkwave-evcd.png
%{_datadir}/icons/gnome/32x32/mimetypes/gnome-mime-application-vnd.gtkwave-fst.png
%{_datadir}/icons/gnome/32x32/mimetypes/gnome-mime-application-vnd.gtkwave-ghw.png
%{_datadir}/icons/gnome/32x32/mimetypes/gnome-mime-application-vnd.gtkwave-gtkw.png
%{_datadir}/icons/gnome/32x32/mimetypes/gnome-mime-application-vnd.gtkwave-lx2.png
%{_datadir}/icons/gnome/32x32/mimetypes/gnome-mime-application-vnd.gtkwave-lxt.png
%{_datadir}/icons/gnome/32x32/mimetypes/gnome-mime-application-vnd.gtkwave-lxt2.png
%{_datadir}/icons/gnome/32x32/mimetypes/gnome-mime-application-vnd.gtkwave-vcd.png
%{_datadir}/icons/gnome/32x32/mimetypes/gnome-mime-application-vnd.gtkwave-vzt.png
%{_datadir}/icons/gnome/32x32/mimetypes/gtkwave.png
%{_datadir}/icons/gnome/48x48/mimetypes/gnome-mime-application-vnd.gtkwave-ae2.png
%{_datadir}/icons/gnome/48x48/mimetypes/gnome-mime-application-vnd.gtkwave-aet.png
%{_datadir}/icons/gnome/48x48/mimetypes/gnome-mime-application-vnd.gtkwave-evcd.png
%{_datadir}/icons/gnome/48x48/mimetypes/gnome-mime-application-vnd.gtkwave-fst.png
%{_datadir}/icons/gnome/48x48/mimetypes/gnome-mime-application-vnd.gtkwave-ghw.png
%{_datadir}/icons/gnome/48x48/mimetypes/gnome-mime-application-vnd.gtkwave-gtkw.png
%{_datadir}/icons/gnome/48x48/mimetypes/gnome-mime-application-vnd.gtkwave-lx2.png
%{_datadir}/icons/gnome/48x48/mimetypes/gnome-mime-application-vnd.gtkwave-lxt.png
%{_datadir}/icons/gnome/48x48/mimetypes/gnome-mime-application-vnd.gtkwave-lxt2.png
%{_datadir}/icons/gnome/48x48/mimetypes/gnome-mime-application-vnd.gtkwave-vcd.png
%{_datadir}/icons/gnome/48x48/mimetypes/gnome-mime-application-vnd.gtkwave-vzt.png
%{_datadir}/icons/gnome/48x48/mimetypes/gtkwave.png
%{_datadir}/icons/gtkwave_256x256x32.png
%{_datadir}/icons/gtkwave_files_256x256x32.png
%{_datadir}/icons/gtkwave_savefiles_256x256x32.png
%{_datadir}/icons/hicolor/16x16/apps/gtkwave.png
%{_datadir}/icons/hicolor/32x32/apps/gtkwave.png
%{_datadir}/icons/hicolor/48x48/apps/gtkwave.png
%{_datadir}/icons/hicolor/256x256/apps/gtkwave.png
%{_datadir}/icons/hicolor/scalable/apps/gtkwave.svg
%{_datadir}/mime/packages/x-gtkwave-extension-ae2.xml
%{_datadir}/mime/packages/x-gtkwave-extension-aet.xml
%{_datadir}/mime/packages/x-gtkwave-extension-evcd.xml
%{_datadir}/mime/packages/x-gtkwave-extension-fst.xml
%{_datadir}/mime/packages/x-gtkwave-extension-ghw.xml
%{_datadir}/mime/packages/x-gtkwave-extension-gtkw.xml
%{_datadir}/mime/packages/x-gtkwave-extension-lx2.xml
%{_datadir}/mime/packages/x-gtkwave-extension-lxt.xml
%{_datadir}/mime/packages/x-gtkwave-extension-lxt2.xml
%{_datadir}/mime/packages/x-gtkwave-extension-vcd.xml
%{_datadir}/mime/packages/x-gtkwave-extension-vzt.xml
%{_mandir}/man1/evcd2vcd.1*
%{_mandir}/man1/fst2vcd.1*
%{_mandir}/man1/fstminer.1*
%{_mandir}/man1/ghwdump.1*
%{_mandir}/man1/gtkwave.1*
%{_mandir}/man1/lxt2miner.1*
%{_mandir}/man1/lxt2vcd.1*
%{_mandir}/man1/rtlbrowse.1*
%{_mandir}/man1/shmidcat.1*
%{_mandir}/man1/twinwave.1*
%{_mandir}/man1/vcd2fst.1*
%{_mandir}/man1/vcd2lxt.1*
%{_mandir}/man1/vcd2lxt2.1*
%{_mandir}/man1/vcd2vzt.1*
%{_mandir}/man1/vzt2vcd.1*
%{_mandir}/man1/vztminer.1*
%{_mandir}/man1/xml2stems.1*
%{_mandir}/man5/gtkwaverc.5*


%changelog
* Fri May 1 2020 Aimylios <aimylios@xxx.xx> - 3.3.105-0.1.%{snapdate}git%{shortcommit0}
- Initial version for nightly builds based on 3.3.104-1
