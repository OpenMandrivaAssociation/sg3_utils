%define	major 2
%define libname	%mklibname sgutils %{major}
%define develname %mklibname sgutils -d

Summary:	Utils for Linux's SCSI generic driver devices + raw devices
Name:		sg3_utils
Version:	1.35
Release:	2
License:	GPL+
Group:		System/Kernel and hardware
URL:		http://sg.danny.cz/sg/sg3_utils.html
Source0:	http://sg.danny.cz/sg/p/%{name}-%{version}.tgz
BuildRequires:	libtool

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

%package -n %{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n %{libname}
This package contains the shared library for %{name}.

%package -n %{develname}
Summary:	Static library and header files for the sgutils library
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Provides:	libsgutils-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%{mklibname sgutils 1 -d} < 1.26

%description -n	%{develname}
This package contains the sgutils library and its header
files.

%define devel_name_static %mklibname %{name} -d -s
%package -n	%{devel_name_static}
Summary:	Static library and header files for the sgutils library
Group:		Development/C
Provides:	%{name}-static-devel = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Obsoletes:	%{mklibname sgutils 1 -d} < 1.26

%description -n	%{devel_name_static}
This package contains the static sgutils library and its header
files.

%prep
%setup -q

%build
%configure2_5x \
	--bindir=%{_sbindir}
%make

%install
%makeinstall_std 
find %{buildroot} -name \*.la|xargs rm -f


%files
%doc ChangeLog COVERAGE CREDITS README README.sg_start
%attr(0755,root,root) %{_sbindir}/*
%{_mandir}/man8/*

%files -n %{libname}
%{_libdir}/*.so.%{major}*

%files -n %{develname}
%{_includedir}/scsi/*.h
%{_libdir}/*.so

%files -n %{devel_name_static}
%{_libdir}/*.a
