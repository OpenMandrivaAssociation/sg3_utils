%define	major 1
%define libname	%mklibname sgutils %{major}

Summary:	Utils for Linux's SCSI generic driver devices + raw devices
Name:		sg3_utils
Version:	1.23
Release:	%mkrel 1
License:	GPL
Group:		System/Kernel and hardware
URL:		http://www.torque.net/sg/u_index.html
Source0:	http://www.torque.net/sg/p/%{name}-%{version}.tgz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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

%package -n	%{libname}
Summary:	Shared library for %{name}
Group:		System/Libraries

%description -n	%{libname}
This package contains the shared library for %{name}.

%package -n	%{libname}-devel
Summary:	Static library and header files for the sgutils library
Group:		Development/C
Obsoletes:	%{name}-devel
Provides:	%{name}-devel = %{version}
Provides:	libsgutils-devel = %{version}
Requires:	%{libname} = %{version}

%description -n	%{libname}-devel
This package contains the static sgutils library and its header
files.

%prep
%setup -q

%build
%make CFLAGS="%{optflags}" LIBDIR="%{_libdir}"

%install
rm -rf %{buildroot}

%makeinstall_std \
	PREFIX=%{_prefix} \
	LIBDIR=%{buildroot}%{_libdir} \
	INSTDIR=%{buildroot}%{_sbindir} \
	MANDIR=%{buildroot}%{_mandir} \
	INCLUDEDIR=%{buildroot}%{_includedir}

%post -n %{libname} -p /sbin/ldconfig

%postun -n %{libname} -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc CHANGELOG COVERAGE CREDITS README README.sg_start
%attr(0755,root,root) %{_sbindir}/*
%{_mandir}/man8/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/*.so.*

%files -n %{libname}-devel
%defattr(-,root,root)
%{_includedir}/scsi/*.h
%{_libdir}/*.so
%{_libdir}/*.a
%{_libdir}/*.la


