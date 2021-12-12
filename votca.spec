Name:           votca
Version:        2022~rc1
%global         uversion 2022-rc.1
Release:        1%{?dist}
Summary:        VOTCA tools library
Group:          Applications/Engineering
License:        ASL 2.0
URL:            http://www.votca.org
Source0:        https://github.com/votca/votca/archive/v%{uversion}.tar.gz#/%{name}-%{uversion}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake3
BuildRequires:  expat-devel
BuildRequires:  fftw-devel
BuildRequires:  eigen3-devel
BuildRequires:  boost-devel
BuildRequires:  gromacs-devel
BuildRequires:  perl-generators
BuildRequires:  hdf5-devel
BuildRequires:  lammps
BuildRequires:  python3
BuildRequires:  libxc-devel
BuildRequires:  libecpint-devel
BuildRequires:  libint2-devel
BuildRequires:  valgrind
BuildRequires:  gromacs
BuildRequires:  gromacs-openmpi
BuildRequires:  openmpi-devel
BuildRequires:  gnuplot
BuildRequires:  psmisc

%description
Versatile Object-oriented Toolkit for Coarse-graining Applications (VOTCA) is
a package intended to reduce the amount of routine work when doing systematic
coarse-graining of various systems. The core is written in C++.

%package devel
Summary:        Development headers and libraries for votca-tools
Group:          Development/Libraries
Requires:       pkgconfig
Requires:       %{name} = %{version}-%{release}
# Programs that build against votca need also these
Requires:       boost-devel
Requires:       expat-devel
Requires:       fftw3-devel

%description devel
Versatile Object-oriented Toolkit for Coarse-graining Applications (VOTCA) is
a package intended to reduce the amount of routine work when doing systematic
coarse-graining of various systems. The core is written in C++.

%prep
%setup -q -n %{name}-%{uversion}

%build

# load openmpi, so that cmake can find mdrun_openmpi for testing
%_openmpi_load
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake} -DCMAKE_BUILD_TYPE=Release -DWITH_RC_FILES=OFF -DENABLE_TESTING=ON -DBUILD_CSGAPPS=ON -DBUILD_XTP=ON -DENABLE_REGRESSION_TESTING=ON -DHDF5_C_COMPILER_EXECUTABLE=/usr/bin/h5cc
%make_build
%_openmpi_unload

%install
%make_install -C %{_target_platform}

%check
%_openmpi_load
make -C %{_target_platform} test CTEST_OUTPUT_ON_FAILURE=1 %{?testargs}
%_openmpi_unload

%files
%license tools/LICENSE
%doc tools/NOTICE
%{_bindir}/votca_*
%{_bindir}/csg_*
%{_libdir}/libvotca_*.so.*
%{_mandir}/man1/votca_*.*
%{_mandir}/man1/csg_*.*
%{_mandir}/man7/votca-*.7*
%{_datadir}/votca
%{_bindir}/xtp_*
%{_mandir}/man1/xtp_*.*

%files devel
%{_includedir}/votca/
%{_libdir}/libvotca_*.so
%{_libdir}/cmake/VOTCA_*

%changelog
