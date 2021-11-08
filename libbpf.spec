#
# Conditional build:
%bcond_without	apidocs	# API documentation

Summary:	Libbpf library
Summary(pl.UTF-8):	Biblioteka libbpf
Name:		libbpf
Version:	0.5.0
Release:	1
License:	LGPL v2.1 or BSD
Group:		Libraries
#Source0Download: https://github.com/libbpf/libbpf/releases
Source0:	https://github.com/libbpf/libbpf/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	ba0a514d2775f033c24a6fec37e587bc
URL:		https://github.com/libbpf/libbpf
BuildRequires:	elfutils-devel
BuildRequires:	linux-libc-headers >= 7:5.4.0
BuildRequires:	pkgconfig
BuildRequires:	rpm-build >= 4.6
BuildRequires:	zlib-devel
%if %{with apidocs}
BuildRequires:	doxygen
BuildRequires:	python3-breathe
BuildRequires:	sphinx-pdg-3
%endif
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A mirror of bpf-next Linux tree bpf-next/tools/lib/bpf directory plus
its supporting header files. The version of the package reflects the
version of ABI.

%description -l pl.UTF-8
Kopia lustrzana katalogu bpf-next/tools/lib/bpf ze źródeł Linuksa, z
drzewka bpf-next wraz ze wspierającymi plikami nagłówkowymi. Wersja
pakietu odzwierciedla wersję ABI.

%package devel
Summary:	Development files for libbpf library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libbpf
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	elfutils-devel
Requires:	linux-libc-headers >= 7:5.4.0
Requires:	zlib-devel

%description devel
This package contains header files for developing applications that
use libbpf.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe do tworzenia aplikacji
wykorzystujących libbpf.

%package static
Summary:	Static libbpf library
Summary(pl.UTF-8):	Statyczna biblioteka libbpf
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
This package contains static library for developing applications that
use libbpf.

%description static -l pl.UTF-8
Ten pakiet zawiera bibliotekę statyczną do tworzenia aplikacji
wykorzystujących libbpf.

%package apidocs
Summary:	API documentation for libbpf library
Summary(pl.UTF-8):	Dokumentacja API biblioteki libbpf
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for libbpf library.

%description apidocs -l pl.UTF-8
Dokumentacja API biblioteki libbpf.

%prep
%setup -q

%build
# use NO_PKG_CONFIG to link with -lelf -lz, not $(pkg-config --libs libelf) which doesn't contain -lz
%{__make} -C src \
	CC="%{__cc}" \
	CFLAGS="%{rpmcflags} %{rpmcppflags} -fPIC" \
	LDFLAGS="%{rpmldflags}" \
	NO_PKG_CONFIG=1 \
	V=1

%if %{with apidocs}
READTHEDOCS=True \
%{__make} -C docs -f sphinx/Makefile html \
	SOURCEDIR=. \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C src install \
	DESTDIR=$RPM_BUILD_ROOT \
	LIBSUBDIR=%{_lib}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE LICENSE.BSD-2-Clause README.md
%attr(755,root,root) %{_libdir}/libbpf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libbpf.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libbpf.so
%{_includedir}/bpf
%{_pkgconfigdir}/libbpf.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libbpf.a

%if %{with apidocs}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,*.html,*.js}
%endif
