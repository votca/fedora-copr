%global with_xtp 1
# libint2 used by xtp is broken on 32-bit archs
# https://github.com/evaleev/libint/issues/196
# https://github.com/votca/xtp/issues/652
%ifarch %ix86 %arm
%global with_xtp 0
%endif

%global uversion 2022-rc.2
%global sover 2022

%global votca_desc \
VOTCA is a software package which focuses on the analysis of molecular \
dynamics data, the development of systematic coarse-graining techniques as \
well as methods used for simulating microscopic charge (and exciton) transport \
in disordered semiconductors.

Name:           votca
Version:        2022~rc2
Release:        2%{?dist}
Summary:        Versatile Object-oriented Toolkit for Coarse-graining Applications
License:        ASL 2.0
URL:            http://www.votca.org
Source0:        https://github.com/votca/votca/archive/v%{uversion}.tar.gz#/%{name}-%{uversion}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  fdupes
BuildRequires:  cmake3
BuildRequires:  expat-devel
BuildRequires:  fftw-devel
BuildRequires:  eigen3-devel
BuildRequires:  boost-devel
BuildRequires:  gromacs-devel
BuildRequires:  perl-generators
BuildRequires:  hdf5-devel
BuildRequires:  python3
BuildRequires:  python3-lxml
BuildRequires:  python3-h5py
BuildRequires:  libxc-devel
BuildRequires:  libecpint-devel
BuildRequires:  libint2-devel
# mpi packages only used for testing
BuildRequires:  gromacs-openmpi
%ifnarch s390x
BuildRequires:  python3-espresso-openmpi
%endif
BuildRequires:  openmpi-devel

#used for testing only
BuildRequires:  gromacs
BuildRequires:  lammps
BuildRequires:  python3-cma
BuildRequires:  python3-pytest
BuildRequires:  gnuplot
BuildRequires:  psmisc


Requires:   %{name}-common = %{version}-%{release}
Requires:   %{name}-libs%{?_isa} = %{version}-%{release}
%if %{with_xtp}
Requires:   %{name}-common-xtp = %{version}-%{release}
%endif
Obsoletes:      votca-tools <= 2022~rc1
Provides:       votca-tools = %version-%release
Obsoletes:      votca-csg <= 2022~rc1
Provides:       votca-csg = %version-%release
Obsoletes:      votca-xtp <= 2022~rc1
Provides:       votca-xtp = %version-%release

%description
%{votca_desc}

%package devel
Summary:        Development headers and libraries for votca
Requires:       pkgconfig
Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       %{name}-libs%{?_isa} = %{version}-%{release}
# votca header include these headers
Requires:       boost-devel
Requires:       expat-devel
Requires:       fftw3-devel
Requires:       libxc-devel
Requires:       libint2-devel
Requires:       libecpint-devel
Requires:       hdf5-devel
Obsoletes:      votca-csg-devel <= 2022~rc1
Provides:       votca-csg-devel = %version-%release
Obsoletes:      votca-tools-devel <= 2022~rc1
Provides:       votca-tools-devel = %version-%release
Obsoletes:      votca-xtp-devel <= 2022~rc1
Provides:       votca-xtp-devel = %version-%release

%description devel
%{votca_desc}

This package contains development headers and libraries for the VOTCA
package.

%package libs
Summary:    Libraries for VOTCA coarse-graining engine
Obsoletes:  votca-csg-libs <= 2022~rc1
Provides:   votca-csg-libs = %version-%release
Obsoletes:  votca-xtp-libs <= 2022~rc1
Provides:   votca-xtp-libs = %version-%release

%description libs
%{votca_desc}

This package contains libraries for the VOTCA package.

%package common
Summary:    Architecture independent data files for VOTCA
BuildArch:  noarch
Obsoletes:  votca-csg-common <= 2022~rc1
Provides:   votca-csg-common = %version-%release

%description common
%{votca_desc}

This package contains architecture independent data files for the VOTCA
package.

%package csg-tutorials
Summary:    Architecture independent csg tutorial files for VOTCA
BuildArch:  noarch
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description csg-tutorials
%{votca_desc}

This package contains architecture independent csg tutorial files
for the VOTCA package.

# split off as some arch do not have xtp parts
%if %{with_xtp}
%package xtp-tutorials
Summary:    Architecture independent xtp tutorial files for VOTCA
BuildArch:  noarch
Requires:   %{name}%{?_isa} = %{version}-%{release}

%description xtp-tutorials
%{votca_desc}

This package contains architecture independent xtp tutorial files
for the VOTCA package.

%package common-xtp
Summary:    Architecture independent data files for xtp parts of VOTCA
BuildArch:  noarch
Obsoletes:  votca-xtp-common <= 2022~rc1
Provides:   votca-xtp-common = %version-%release

%description common-xtp
%{votca_desc}

This package contains architecture independent data files for the xtp
parts of the VOTCA package.
%endif

%package bash
Summary:    Bash completion for VOTCA
Requires:   %{name}%{?_isa} = %{version}-%{release}
Requires:   bash-completion
BuildArch:  noarch
Obsoletes:  votca-csg-bash <= 2022~rc1
Provides:   votca-csg-bash = %version-%release

%description bash
%{votca_desc}

This package contains bash completion support for the VOTCA package.

%prep
%setup -q -n %{name}-%{uversion}

%build
# load openmpi, so that cmake can find mdrun_openmpi for testing only
%_openmpi_load
# not a 100% sure why this is needed, but otherwise espressomd cannot be found
export PYTHONPATH="${MPI_PYTHON3_SITEARCH}${PYTHONPATH:+:}${PYTHONPATH}"

%{cmake} -DCMAKE_BUILD_TYPE=Release -DINSTALL_RC_FILES=OFF -DENABLE_TESTING=ON -DBUILD_CSGAPPS=ON \
 -DBUILD_XTP=%{with_xtp} \
  -DENABLE_REGRESSION_TESTING=ON -DHDF5_C_COMPILER_EXECUTABLE=/usr/bin/h5cc -DINJECT_MARCH_NATIVE=OFF
%cmake_build
%_openmpi_unload

%install
%cmake_install
# Install bash completion file
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
mv %{buildroot}%{_datadir}/votca/rc/csg-completion.bash %{buildroot}%{_datadir}/bash-completion/completions/votca

%fdupes %{buildroot}%{_prefix}

%check
%_openmpi_load
export PYTHONPATH="${MPI_PYTHON3_SITEARCH}${PYTHONPATH:+:}${PYTHONPATH}"
%ctest
%_openmpi_unload

%files
%{_bindir}/{votca,csg,xtp}_*
%{_mandir}/man1/{votca,csg,xtp}_*.1*
%{_mandir}/man7/votca-*.7*

%files common
%doc CHANGELOG.rst NOTICE.rst README.rst
%license LICENSE
%{_datadir}/votca/
%exclude %{_datadir}/votca/*-tutorials/
%exclude %{_datadir}/votca/xtp/

%files csg-tutorials
%{_datadir}/votca/csg-tutorials/

%if %{with_xtp}
%files xtp-tutorials
%{_datadir}/votca/xtp-tutorials/

%files common-xtp
%license LICENSE
%{_datadir}/votca/xtp/
%endif

%files libs
%license LICENSE
%{_libdir}/libvotca_*.so.%{sover}

%files devel
%{_includedir}/votca/
%{_libdir}/libvotca_*.so
%{_libdir}/cmake/VOTCA_*

%files bash
%{_datadir}/bash-completion/completions/votca

%changelog
* Wed Dec 29 2021 Christoph Junghans <junghans@votca.org> - 2022~rc2-2
- Incorporated changes from package review (bug #2032487#c7)

* Thu Dec 23 2021 Christoph Junghans <junghans@votca.org> - 2022~rc2-1
- initial import (bug #2032487)

