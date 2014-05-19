%define rescan_version 1.56
%define rescan_script rescan-scsi-bus.sh

%define	major	2
%define	libname	%mklibname sgutils %{major}
%define	devname	%mklibname sgutils -d
%define	static	%mklibname sgutils -d -s

%bcond_without	uclibc

Summary:	Utils for Linux's SCSI generic driver devices + raw devices
Name:		sg3_utils
Version:	1.38
Release:	1
License:	GPL+
Group:		System/Kernel and hardware
URL:		http://sg.danny.cz/sg/sg3_utils.html
Source0:	http://sg.danny.cz/sg/p/%{name}-%{version}.tgz
#Source1:	http://www.garloff.de/kurt/linux/%{rescan_script}-%{rescan_version}
Source2:	scsi-rescan.8
Patch0:		sg3_utils-1.38-fix-out-of-source-build-includes.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=920687
Patch1:		sg3_utils-1.37-dont-open-dev-snapshot.patch
# update configure for ppc64le (#1079542)
Patch2:		sg3_utils-1.38-ppc64le.patch
%if %{with uclibc}
BuildRequires:	uClibc-devel
%endif

%description
Collection of tools for SCSI devices that use the Linux SCSI
generic (sg) interface. Includes utilities to copy data based on
"dd" syntax and semantics (called sg_dd, sgp_dd and sgm_dd); check
INQUIRY data and associated pages (sg_inq); check mode and log
pages (sg_modes and sg_logs); spin up and down disks (sg_start);
do self tests (sg_senddiag); and various other functions. See the
README and CHANGELOG files. Requires the lk 2.4 series or better.
[In the lk 2.5 development series many of these utilities can be
used on the primary block device name (e.g. /dev/sda).]

Warning: Some of these tools access the internals of your system
and the incorrect usage of them may render your system inoperable.

%package -n	uclibc-%{name}
Summary:	Utils for Linux's SCSI generic driver devices + raw devices (uClibc build)
Group:		System/Kernel and hardware

%description -n	uclibc-%{name}
Collection of tools for SCSI devices that use the Linux SCSI
generic (sg) interface. Includes utilities to copy data based on
"dd" syntax and semantics (called sg_dd, sgp_dd and sgm_dd); check
INQUIRY data and associated pages (sg_inq); check mode and log
pages (sg_modes and sg_logs); spin up and down disks (sg_start);
do self tests (sg_senddiag); and various other functions. See the
README and CHANGELOG files. Requires the lk 2.4 series or better.
[In the lk 2.5 development series many of these utilities can be
used on the primary block device name (e.g. /dev/sda).]

Warning: Some of these tools access the internals of your system
and the incorrect usage of them may render your system inoperable.

%package -n	%{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n	%{libname}
This package contains the shared library for %{name}.

%package -n	uclibc-%{libname}
Summary:	Shared library for %{name} (uClibc build)
Group:		System/Libraries

%description -n	uclibc-%{libname}
This package contains the shared library for %{name}.

%package -n	%{devname}
Summary:	Static library and header files for the sgutils library
Group:		Development/C
Provides:	%{name}-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}
%if %{with uclibc}
Requires:	uclibc-%{libname} = %{EVRD}
%endif
Obsoletes:	%{mklibname sgutils 1 -d} < 1.26

%description -n	%{devname}
This package contains the sgutils library and its header
files.

%package -n	%{static}
Summary:	Static library and header files for the sgutils library
Group:		Development/C
Provides:	%{name}-static-devel = %{EVRD}
Requires:	%{libname} = %{EVRD}
Obsoletes:	%{mklibname sgutils 1 -d} < 1.26

%description -n	%{static}
This package contains the static sgutils library and its header
files.

%prep
%setup -q
%patch0 -p1 -b .include~
%patch1 -p1 -b .dev-snapshot
%patch2 -p1 -b .ppc64le
autoreconf -fi

%build
export CONFIGURE_TOP="$PWD"
%if %{with uclibc}
mkdir -p uclibc
pushd uclibc
%uclibc_configure \
	--bindir=%{uclibc_root}/%{_sbindir}
%make
popd
%endif

mkdir -p glibc
pushd glibc
%configure2_5x \
	--bindir=%{_sbindir} \
	--enable-static
%make
popd

%install
%if %{with uclibc}
%makeinstall_std -C uclibc
%endif
%makeinstall_std -C glibc

install -p -m755 scripts/%{rescan_script} -D %{buildroot}%{_bindir}/%{rescan_script}
ln -s %{rescan_script} %{buildroot}%{_bindir}/scsi-rescan
install -p -m644 %{SOURCE2} -D %{buildroot}%{_mandir}/man8/scsi-rescan.8

%files
%doc ChangeLog COVERAGE CREDITS README README.sg_start
%{_bindir}/*
%{_sbindir}/*
%{_mandir}/man8/*

%if %{with uclibc}
%files -n uclibc-%{name}
%{uclibc_root}%{_sbindir}/*
%endif

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n uclibc-%{libname}
%if %{with uclibc}
%{uclibc_root}%{_libdir}/*.so.%{major}*
%endif

%files -n %{devname}
%{_includedir}/scsi/*.h
%{_libdir}/*.so
%if %{with uclibc}
%{uclibc_root}%{_libdir}/*.so
%endif

%files -n %{static}
%{_libdir}/*.a
