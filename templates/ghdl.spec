%global snapdate @SNAPDATE@
%global commit0 @COMMIT0@
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

%ifarch %{ix86} x86_64
%bcond_without mcode
%else
%bcond_with mcode
%endif

%ifarch x86_64 ppc64le
%bcond_without llvm
%else
%bcond_with llvm
%endif

%bcond_with gnatwae

%global DATE 20200826
%global gitrev c59c8927f43fb78d6a72a0ff93a47b36e43282d5
%global gcc_version 10.2.1
%global gcc_major 10
# Note, gcc_release must be integer, if you want to add suffixes to
# %%{release}, append them after %%{gcc_release} on Release: line.
%global gcc_release 3
# Hardening slows the compiler way too much.
%undefine _hardened_build
# Until annobin is fixed (#1519165).
%undefine _annotated_build
%global build_isl 1

Name:           ghdl
Version:        2.0.0~dev
Release:        99.%{snapdate}git%{shortcommit0}%{?dist}
Summary:        A VHDL simulator, using the GCC technology
License:        GPLv2+ and GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions and LGPLv2+ and BSD
URL:            http://ghdl.free.fr/

# The source for this package was pulled from upstream's vcs.  Use the
# following commands to generate the tarball:
# git clone --depth 1 git://gcc.gnu.org/git/gcc.git gcc-dir.tmp
# git --git-dir=gcc-dir.tmp/.git fetch --depth 1 origin %%{gitrev}
# git --git-dir=gcc-dir.tmp/.git archive --prefix=%%{name}-%%{version}-%%{DATE}/ %%{gitrev} | xz -9e > %%{name}-%%{version}-%%{DATE}.tar.xz
# rm -rf gcc-dir.tmp
Source0:         gcc-%{gcc_version}-%{DATE}.tar.xz
%global isl_version 0.16.1

Patch0:         https://src.fedoraproject.org/rpms/ghdl/raw/master/f/gcc10-hack.patch#/ghdl-gcc10-hack.patch
Patch1:         https://src.fedoraproject.org/rpms/ghdl/raw/master/f/gcc10-i386-libgomp.patch#/ghdl-gcc10-i386-libgomp.patch
Patch3:         https://src.fedoraproject.org/rpms/ghdl/raw/master/f/gcc10-libgomp-omp_h-multilib.patch#/ghdl-gcc10-libgomp-omp_h-multilib.patch
Patch4:         https://src.fedoraproject.org/rpms/ghdl/raw/master/f/gcc10-libtool-no-rpath.patch#/ghdl-gcc10-libtool-no-rpath.patch
Patch5:         https://src.fedoraproject.org/rpms/ghdl/raw/master/f/gcc10-isl-dl.patch#/ghdl-gcc10-isl-dl.patch
Patch7:         https://src.fedoraproject.org/rpms/ghdl/raw/master/f/gcc10-no-add-needed.patch#/ghdl-gcc10-no-add-needed.patch
Patch8:         https://src.fedoraproject.org/rpms/ghdl/raw/master/f/gcc10-foffload-default.patch#/ghdl-gcc10-foffload-default.patch
Patch9:         https://src.fedoraproject.org/rpms/ghdl/raw/master/f/gcc10-Wno-format-security.patch#/ghdl-gcc10-Wno-format-security.patch
Patch10:        https://src.fedoraproject.org/rpms/ghdl/raw/master/f/gcc10-rh1574936.patch#/ghdl-gcc10-rh1574936.patch
Patch11:        https://src.fedoraproject.org/rpms/ghdl/raw/master/f/gcc10-pr96383.patch#/ghdl-gcc10-pr96383.patch
Patch12:        https://src.fedoraproject.org/rpms/ghdl/raw/master/f/gcc10-pr96385.patch#/ghdl-gcc10-pr96385.patch
Patch13:        https://src.fedoraproject.org/rpms/ghdl/raw/master/f/gcc10-pr96690.patch#/ghdl-gcc10-pr96690.patch

Source100:      https://github.com/ghdl/ghdl/archive/%{commit0}/%{name}-%{shortcommit0}.tar.gz

Patch100:       https://src.fedoraproject.org/rpms/ghdl/raw/master/f/ghdl-llvmflags.patch
# From: Thomas Sailer <t.sailer@alumni.ethz.ch>
# To: ghdl-discuss@gna.org
# Date: Thu, 02 Apr 2009 15:36:00 +0200
# https://gna.org/bugs/index.php?13390
Patch106:       https://src.fedoraproject.org/rpms/ghdl/raw/master/f/ghdl-ppc64abort.patch

Requires:       gcc

Patch200:       https://src.fedoraproject.org/rpms/ghdl/raw/master/f/gcc-config.patch#/ghdl-gcc-config.patch

BuildRequires:  binutils
BuildRequires:  zlib-devel
BuildRequires:  gettext
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  texinfo
BuildRequires:  gmp-devel
BuildRequires:  mpfr-devel
BuildRequires:  libmpc-devel
BuildRequires:  python2-devel, python3-devel
BuildRequires:  gcc
BuildRequires:  gcc-c++
# Make sure pthread.h doesn't contain __thread tokens
# Make sure glibc supports stack protector
# Make sure glibc supports DT_GNU_HASH
BuildRequires:  glibc-devel
BuildRequires:  elfutils-devel
BuildRequires:  elfutils-libelf-devel
%if %{build_isl}
BuildRequires:  isl = %{isl_version}
BuildRequires:  isl-devel = %{isl_version}
%if 0%{?__isa_bits} == 64
Requires:       libisl.so.15()(64bit)
%else
Requires:       libisl.so.15
%endif
%endif
Requires:       binutils
Requires:       libgcc >= %{gcc_version}

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  libtool
BuildRequires:  gcc-gnat
# for x86, we also build the mcode version; if on x86_64, we need some 32bit libraries
%if %{with llvm}
BuildRequires:  libedit-devel
BuildRequires:  clang
BuildRequires:  llvm
BuildRequires:  llvm-devel
BuildRequires:  llvm-static
%endif
BuildRequires:  make

Requires: ghdl-grt = %{version}-%{release}

Provides: bundled(libiberty)

# gcc-gnat only available on these:
ExclusiveArch: %{GNAT_arches}

# the following arches are not supported by the base compiler:
ExcludeArch: armv7hl

# Make sure we don't use clashing namespaces
%global _vendor fedora_ghdl

%global _gnu %{nil}
%global gcc_target_platform %{_target_platform}

# do not strip libgrt.a -- makes debugging tedious otherwise
%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's#/usr/lib/rpm/redhat/brp-strip-static-archive .*##g')

%description
GHDL is the open-source analyzer, compiler, simulator and (experimental)
synthesizer for VHDL, a Hardware Description Language (HDL). GHDL implements
the VHDL language according to the 1987, 1993 and 2002 versions of the IEEE
1076 VHDL standard, and partial for 2008. It compiles VHDL files and creates
a binary that simulates (or executes) your design. GHDL can also translate
a design into a VHDL 1993 netlist, or it can be plugged into Yosys for
open-source synthesis.

Since GHDL is a compiler (i.e., it generates object files), you can call
functions or procedures written in a foreign language, such as C, C++, Ada95
or Python.


%package grt
Summary: GHDL runtime libraries
# rhbz #316311
Requires: zlib-devel, libgnat >= 4.3

%description grt
This package contains the runtime libraries needed to link ghdl-compiled
object files into simulator executables. grt contains the simulator kernel
that tracks signal updates and schedules processes.


%ifarch %{ix86} x86_64
%if %{with mcode}
%package mcode
Summary: GHDL with mcode backend
Requires: ghdl-mcode-grt = %{version}-%{release}

%description mcode
This package contains the ghdl compiler with the mcode backend. The mcode
backend provides for faster compile time at the expense of longer run time.


%package mcode-grt
Summary: GHDL mcode runtime libraries

%description mcode-grt
This package contains the runtime libraries needed to link ghdl-mcode-compiled
object files into simulator executables. mcode-grt contains the simulator kernel
that tracks signal updates and schedules processes.
%endif
%endif


%if %{with llvm}
%package llvm
Summary: GHDL with LLVM backend
Requires: ghdl-llvm-grt = %{version}-%{release}

%description llvm
This package contains the ghdl compiler with the LLVM backend. The LLVM
backend is experimental.


%package llvm-grt
Summary: GHDL LLVM runtime libraries

%description llvm-grt
This package contains the runtime libraries needed to link ghdl-llvm-compiled
object files into simulator executables. llvm-grt contains the simulator kernel
that tracks signal updates and schedules processes.
%endif


%prep
%setup -q -n gcc-%{gcc_version}-%{DATE} -a 100
%patch0 -p0 -b .hack~
%patch1 -p0 -b .i386-libgomp~
%patch3 -p0 -b .libgomp-omp_h-multilib~
%patch4 -p0 -b .libtool-no-rpath~
%if %{build_isl}
%patch5 -p0 -b .isl-dl~
%endif
%patch7 -p0 -b .no-add-needed~
%patch8 -p0 -b .foffload-default~
%patch9 -p0 -b .Wno-format-security~
%patch10 -p0 -b .rh1574936~
%patch11 -p0 -b .pr96383~
%patch12 -p0 -b .pr96385~
%patch13 -p0 -b .pr96690~

%patch200 -p1
pushd libiberty
autoconf -f
popd
pushd intl
autoconf -f
popd

echo 'Red Hat %{version}-%{gcc_release}' > gcc/DEV-PHASE

cp -a libstdc++-v3/config/cpu/i{4,3}86/atomicity.h

./contrib/gcc_update --touch

LC_ALL=C sed -i -e 's/\xa0/ /' gcc/doc/options.texi

sed -i -e 's/Common Driver Var(flag_report_bug)/& Init(1)/' gcc/common.opt

# This test causes fork failures, because it spawns way too many threads
rm -f gcc/testsuite/go.test/test/chan/goroutines.go

# ghdl
mv ghdl-%{commit0} ghdl
%patch100 -p0 -b .llvmflags~

# fix library and include path
pushd ghdl
sed -i.orig -e 's|\"lib\"|\"%{_lib}\"|' -e 's|\"include\"|\"include/ghdl\"|' src/ghdldrv/ghdlsynth.adb
sed -i.orig -e 's|\"lib\"|\"%{_lib}\"|' -e 's|\"include\"|\"include/ghdl\"|' src/ghdldrv/ghdlvpi.adb
popd

%if %{without gnatwae}
perl -i -pe 's,-gnatwae,,' ghdl/dist/gcc/Make-lang.in
%endif

%if %{with mcode}
cp -r ghdl ghdl-mcode
pushd ghdl-mcode
perl -i -pe 's,^libdirsuffix=.*$,libdirsuffix=%{_lib}/ghdl/mcode,' configure
perl -i -pe 's,^libdirreverse=.*$,libdirreverse=../../..,' configure
popd
%endif

%if %{with llvm}
cp -r ghdl ghdl-llvm
pushd ghdl-llvm
perl -i -pe 's,^libdirsuffix=.*$,libdirsuffix=%{_lib}/ghdl/llvm,' configure
perl -i -pe 's,^libdirreverse=.*$,libdirreverse=../../..,' configure
popd
%endif

echo 'Red Hat %{version}-%{gcc_release}' > gcc/DEV-PHASE

pushd ghdl
./configure --prefix=/usr --with-gcc=.. --enable-libghdl --enable-synth
make copy-sources
popd

%patch106 -p0 -b .ppc64abort


%build

# build mcode on x86
%if %{with mcode}
pushd ghdl-mcode
./configure \
%if %{without gnatwae}
    --disable-werror \
%endif
    --prefix=/usr --enable-libghdl --enable-synth
make %{?_smp_mflags}
popd
%endif

%if %{with llvm}
pushd ghdl-llvm
./configure --prefix=/usr \
%if %{without gnatwae}
    --disable-werror \
%endif
    --with-llvm-config=/usr/bin/llvm-config --enable-libghdl --enable-synth
make %{?_smp_mflags} LDFLAGS=-Wl,--build-id
popd
%endif

# Undo the broken autoconf change in recent Fedora versions
export CONFIG_SITE=NONE

CC=gcc
CXX=g++
OPT_FLAGS=`echo %{optflags}|sed -e 's/\(-Wp,\)\?-D_FORTIFY_SOURCE=[12]//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-flto=auto//g;s/-flto//g;s/-ffat-lto-objects//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-m64//g;s/-m32//g;s/-m31//g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-mfpmath=sse/-mfpmath=sse -msse2/g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/ -pipe / /g'`
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-Werror=format-security/-Wformat-security/g'`
%ifarch %{ix86}
OPT_FLAGS=`echo $OPT_FLAGS|sed -e 's/-march=i.86//g'`
%endif
OPT_FLAGS=`echo "$OPT_FLAGS" | sed -e 's/[[:blank:]]\+/ /g'`
case "$OPT_FLAGS" in
  *-fasynchronous-unwind-tables*)
    sed -i -e 's/-fno-exceptions /-fno-exceptions -fno-asynchronous-unwind-tables /' \
      libgcc/Makefile.in
    ;;
esac

rm -rf obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
pushd obj-%{gcc_target_platform}

CONFIGURE_OPTS="\
    --prefix=%{_prefix} --mandir=%{_mandir} --infodir=%{_infodir} \
    --with-bugurl=http://bugzilla.redhat.com/bugzilla \
    --enable-shared --enable-threads=posix --enable-checking=release \
%ifarch ppc64le
    --enable-targets=powerpcle-linux \
%endif
    --disable-multilib \
    --with-system-zlib --enable-__cxa_atexit --disable-libunwind-exceptions \
    --enable-gnu-unique-object --enable-linker-build-id --with-gcc-major-version-only \
    --with-linker-hash-style=gnu \
    --enable-plugin --enable-initfini-array \
%if %{build_isl}
    --with-isl \
%else
    --without-isl \
%endif
%ifarch %{arm}
    --disable-sjlj-exceptions \
%endif
%ifarch ppc64le
    --enable-secureplt \
%endif
%ifarch ppc64le s390x
    --with-long-double-128 \
%endif
%ifarch ppc64le
    --with-cpu-32=power8 --with-tune-32=power8 --with-cpu-64=power8 --with-tune-64=power8 \
%endif
%ifarch %{ix86} x86_64
    --enable-cet \
    --with-tune=generic \
%endif
%if 0%{?rhel} >= 7
%ifarch %{ix86}
    --with-arch=x86-64 \
%endif
%ifarch x86_64
    --with-arch_32=x86-64 \
%endif
%else
%ifarch %{ix86}
    --with-arch=i686 \
%endif
%ifarch x86_64
    --with-arch_32=i686 \
%endif
%endif
%ifarch s390 s390x
%if 0%{?rhel} >= 7
%if 0%{?rhel} > 7
    --with-arch=zEC12 --with-tune=z13 \
%else
    --with-arch=z196 --with-tune=zEC12 \
%endif
%else
%if 0%{?fedora} >= 26
    --with-arch=zEC12 --with-tune=z13 \
%else
    --with-arch=z9-109 --with-tune=z10 \
%endif
%endif
    --enable-decimal-float \
%endif
%ifarch armv7hl
    --with-tune=generic-armv7-a --with-arch=armv7-a \
    --with-float=hard --with-fpu=vfpv3-d16 --with-abi=aapcs-linux \
%endif
    --build=%{gcc_target_platform} \
    "

CC="$CC" \
CXX="$CXX" \
CFLAGS="$OPT_FLAGS" \
CXXFLAGS="`echo " $OPT_FLAGS " | sed 's/ -Wall / /g;s/ -fexceptions / /g' \
    | sed 's/ -Wformat-security / -Wformat -Wformat-security /'`" \
XCFLAGS="$OPT_FLAGS" \
TCFLAGS="$OPT_FLAGS" \
../configure \
    --enable-bootstrap=no \
    --enable-languages=vhdl \
    $CONFIGURE_OPTS

make %{?_smp_mflags}
pushd gcc/vhdl
gnatmake -c -aI%{_builddir}/gcc-%{gcc_version}-%{DATE}/gcc/vhdl ortho_gcc-main \
    -cargs -g -Wall -fexceptions -fstack-protector-strong --param=ssp-buffer-size=4 -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 \
%ifarch %{ix86} x86_64
  -mtune=generic \
%endif
%ifarch ppc64le
  -mcpu=power8 -mtune=power8 \
%endif
  -gnata -gnat05 -gnaty3befhkmr
popd

make %{?_smp_mflags}

popd


%install
# install mcode on x86
%if %{with mcode}
pushd ghdl-mcode
make DESTDIR=%{buildroot} install
mv %{buildroot}/%{_bindir}/ghdl %{buildroot}/%{_bindir}/ghdl-mcode
popd
%endif

# install llvm
%if %{with llvm}
pushd ghdl-llvm
%make_install
mv %{buildroot}/%{_bindir}/ghdl %{buildroot}/%{_bindir}/ghdl-llvm
popd
%endif

# install gcc
%make_install -C obj-%{gcc_target_platform}

PBINDIR=`pwd`/obj-%{gcc_target_platform}/gcc/

pushd ghdl
make bindir=${PBINDIR} GHDL1_GCC_BIN="--GHDL1=${PBINDIR}/ghdl1" ghdllib
%make_install
popd

# Add additional libraries to link
(
echo "-lgnat-`gnatmake --version| sed -n 's/^GNATMAKE \([^.]*\)\..*$/\1/p'`"
) >> %{buildroot}%{_prefix}/lib/ghdl/grt.lst

# Remove files not to be packaged
pushd %{buildroot}
rm -f \
    .%{_bindir}/{cpp,gcc,gccbug,gcov,gcov-dump,gcov-tool,lto-dump} \
    .%{_bindir}/%{gcc_target_platform}-gcc{,-%{gcc_major}} \
    .%{_bindir}/{,%{gcc_target_platform}-}gcc-{ar,nm,ranlib} \
    .%{_includedir}/mf-runtime.h \
    .%{_libdir}/lib{atomic,cc1,gcc_s,gomp,quadmath,ssp}* \
    .%{_infodir}/dir \
    .%{_infodir}/{cpp,cppinternals,gcc,gccinstall,gccint}.info* \
    .%{_infodir}/{libgomp,libquadmath}.info* \
    .%{_datadir}/locale/*/LC_MESSAGES/{gcc,cpplib}.mo \
    .%{_mandir}/man1/{cpp,gcc,gcov,gcov-dump,gcov-tool,lto-dump}.1* \
    .%{_mandir}/man7/{fsf-funding,gfdl,gpl}.7* \
    .%{_prefix}/lib/libgcc_s.* \
    .%{_prefix}/lib/libmudflap.* \
    .%{_prefix}/lib/libmudflapth.* \
    .%{_prefix}/lib/lib{atomic,gomp,quadmath,ssp}* \
    .%{_libdir}/32/libiberty.a

# Remove crt/libgcc, as ghdl invokes the native gcc to perform the linking
rm -f \
    .%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/*crt* \
    .%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/libgc* \
    .%{_libexecdir}/gcc/%{gcc_target_platform}/%{gcc_major}/{cc1,collect2} \
    .%{_libexecdir}/gcc/%{gcc_target_platform}/%{gcc_major}/*lto*

# Remove directory hierarchies not to be packaged
rm -rf \
    .%{_prefix}/lib/gcc/%{gcc_target_platform}/%{gcc_major}/{include,include-fixed,plugin,install-tools} \
    .%{_libexecdir}/gcc/%{gcc_target_platform}/%{gcc_major}/install-tools \
    .%{_libexecdir}/gcc/%{gcc_target_platform}/%{gcc_major}/plugin \

popd

install -d %{buildroot}%{_includedir}/ghdl
mv %{buildroot}%{_includedir}/vpi_user.h %{buildroot}%{_includedir}/ghdl
mv %{buildroot}%{_includedir}/ghdlsynth*.h %{buildroot}%{_includedir}/ghdl
%if "%{_lib}" != "lib"
mv %{buildroot}/usr/lib/libghdlvpi.so %{buildroot}%{_libdir}/
mv %{buildroot}/usr/lib/libghdl-*.so %{buildroot}%{_libdir}/
%endif
# remove static libghdl
rm %{buildroot}/usr/lib/libghdl.{a,link}


%files
%license ghdl/COPYING.md
%{_bindir}/ghdl
%{_infodir}/ghdl.info.*
# Need to own directory %%{_libexecdir}/gcc even though we only want the
# %%{gcc_target_platform}/%%{gcc_version} subdirectory
%{_libexecdir}/gcc/
%{_mandir}/man1/*
%{_includedir}/ghdl/vpi_user.h
%{_includedir}/ghdl/ghdlsynth*.h
%{_libdir}/libghdl*.so

%files grt
# Need to own directory %%{_libdir}/gcc even though we only want the
# %%{gcc_target_platform}/%%{gcc_version} subdirectory
%{_prefix}/lib/gcc/
%{_prefix}/lib/ghdl/

%if %{with mcode}
%files mcode
%{_bindir}/ghdl-mcode

%files mcode-grt
%dir %{_libdir}/ghdl
%{_libdir}/ghdl/mcode
%endif

%if %{with llvm}
%files llvm
%{_bindir}/ghdl-llvm
%{_bindir}/ghdl1-llvm

%files llvm-grt
%dir %{_libdir}/ghdl
%{_libdir}/ghdl/llvm
%endif


%changelog
* Wed Feb 17 2021 Aimylios <aimylios@xxx.xx> - 2.0.0~dev-99.%{snapdate}git%{shortcommit0}
- Add make as explicit build-time dependency

* Sun Nov 8 2020 Aimylios <aimylios@xxx.xx> - 0.38~dev-99.%{snapdate}git%{shortcommit0}
- Backport updates from Fedora upstream

* Sun May 31 2020 Aimylios <aimylios@xxx.xx> - 0.38~dev-99.%{snapdate}git%{shortcommit0}
- Do not package static library

* Fri May 1 2020 Aimylios <aimylios@xxx.xx> - 0.38~dev-99.%{snapdate}git%{shortcommit0}
- Initial version for nightly builds based on 0.38~dev-2.20200428gitad4e2f3
