Name:           votca
Version:        1.6
%global         uversion %{version}
Release:        1%{?dist}
Summary:        VOTCA tools library
Group:          Applications/Engineering
License:        ASL 2.0
URL:            http://www.votca.org
Source0:        https://github.com/votca/votca/archive/v%{uversion}.tar.gz#/%{name}-%{uversion}.tar.gz
Source1:        https://github.com/votca/tools/archive/v%{uversion}.tar.gz#/%{name}-tools-%{uversion}.tar.gz
Source2:        https://github.com/votca/csg/archive/v%{uversion}.tar.gz#/%{name}-csg-%{uversion}.tar.gz
Source3:        https://github.com/votca/csg-tutorials/archive/v%{uversion}.tar.gz#/%{name}-csg-tutorials-%{uversion}.tar.gz
Source4:        https://github.com/votca/csg-manual/archive/v%{uversion}.tar.gz#/%{name}-csg-manual-%{uversion}.tar.gz
Source5:        https://github.com/votca/csgapps/archive/v%{uversion}.tar.gz#/%{name}-csgapps-%{uversion}.tar.gz
Source6:        https://github.com/votca/xtp/archive/v%{uversion}.tar.gz#/%{name}-xtp-%{uversion}.tar.gz
Source7:        https://github.com/votca/xtp-tutorials/archive/v%{uversion}.tar.gz#/%{name}-xtp-tutorials-%{uversion}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  cmake3
BuildRequires:  expat-devel
BuildRequires:  fftw-devel
BuildRequires:  eigen3-devel
BuildRequires:  boost-devel
BuildRequires:  gromacs-devel
BuildRequires:  perl-generators
BuildRequires:  txt2tags
BuildRequires:  hdf5-devel
BuildRequires:  lammps
BuildRequires:  python3
%if 0%{?fedora}
BuildRequires:  python3-espresso-openmpi
BuildRequires:  python3-cma
BuildRequires:  texlive
BuildRequires:  texlive-appendix
BuildRequires:  texlive-wrapfig
BuildRequires:  texlive-xstring
BuildRequires:  texlive-a4wide
BuildRequires:  texlive-bclogo
BuildRequires:  texlive-braket
BuildRequires:  texlive-mdframed
BuildRequires:  texlive-sidecap
BuildRequires:  texlive-units
BuildRequires:  texlive-type1cm
BuildRequires:  transfig
BuildRequires:  tex(latex)
BuildRequires:  graphviz
BuildRequires:  ImageMagick
BuildRequires:  /usr/bin/dvipdf
%endif
BuildRequires:  libxc-devel
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
%setup -q -a 1 -a 2 -a 3 -a 4 -a 5 -a 6 -a 7 -n %{name}-%{uversion}
for i in tools csg csg-tutorials csg-manual csgapps xtp xtp-tutorials; do
  rmdir $i && mv $i-%{uversion} $i;
done

%if 0%{?fedora}
# create latex.fmt before manual generation does it in parallel and might have a raise condition
mktexfmt latex.fmt
%endif

%build
# save some memory
%ifarch %ix86 %arm aarch64
%global _smp_mflags -j1
%global extra_cmake_opts -DENABLE_HIGH_MEMORY_TESTS=OFF
%endif

# load openmpi, so that cmake can find mdrun_openmpi for testing
%_openmpi_load
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake3} .. -DCMAKE_BUILD_TYPE=Release -DWITH_RC_FILES=OFF -DENABLE_TESTING=ON -DBUILD_CSGAPPS=ON -DBUILD_CSG_MANUAL=ON -DBUILD_XTP=ON -DENABLE_REGRESSION_TESTING=ON -DREGRESSIONTEST_TOLERANCE="3e-5" -DHDF5_C_COMPILER_EXECUTABLE=/usr/bin/h5cc %{?extra_cmake_opts} %{?rhel:-DBUILD_CSG_MANUAL=OFF -DCMAKE_DISABLE_FIND_PACKAGE_MDRUN_MPI=ON}
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
%if 0%{?fedora}
%{_datadir}/doc/votca/*.pdf
%endif

%files devel
%{_includedir}/votca/
%{_libdir}/libvotca_*.so
%{_libdir}/cmake/VOTCA_*

%changelog
