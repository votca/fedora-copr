Name:           votca
Version:        1.6~rc1
%global         uversion 1.6_rc1
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
Patch0:         https://github.com/votca/tools/pull/196.patch
Patch1:         https://github.com/votca/tools/pull/197.patch
Patch2:         https://github.com/votca/tools/pull/199.patch
Patch3:         https://github.com/votca/csg/pull/473.patch
Patch4:         https://github.com/votca/xtp/pull/345.patch
Patch5:         https://github.com/votca/xtp/pull/347.patch
Patch6:         https://github.com/votca/csg-tutorials/pull/71.patch 

BuildRequires:  gcc-c++
BuildRequires:  cmake3
BuildRequires:  expat-devel
BuildRequires:  fftw-devel
BuildRequires:  eigen3-devel
BuildRequires:  boost-devel
BuildRequires:  gromacs-devel
BuildRequires:  perl-generators
BuildRequires:  txt2tags
BuildRequires:  texlive
BuildRequires:  texlive-appendix
BuildRequires:  texlive-wrapfig
BuildRequires:  texlive-a4wide
BuildRequires:  texlive-xstring
BuildRequires:  inkscape
BuildRequires:  transfig
BuildRequires:  texlive-bclogo
BuildRequires:  texlive-braket
BuildRequires:  texlive-mdframed
BuildRequires:  texlive-sidecap
BuildRequires:  texlive-units
BuildRequires:  texlive-type1cm
BuildRequires:  tex(latex)
BuildRequires:  graphviz
BuildRequires:  hdf5-devel
BuildRequires:  lammps
BuildRequires:  python3-espresso-openmpi
BuildRequires:  python3-cma
BuildRequires:  valgrind
BuildRequires:  libxc-devel
BuildRequires:  ImageMagick
BuildRequires:  /usr/bin/dvipdf
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
%patch0 -d tools -p1
%patch1 -d tools -p1
%patch2 -d tools -p1
%patch3 -d csg -p1
%patch4 -d xtp -p1
%patch5 -d xtp -p1
%patch6 -d csg-tutorials -p1

# create latex.fmt before manual generation does it in parallel and might have a raise condition
mktexfmt latex.fmt

%build
# for espresso module
# export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib64/python3.7/site-packages/openmpi/espressomd
# load openmpi, so that cmake can find mdrun_openmpi for testing
%_openmpi_load
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake3} .. -DCMAKE_BUILD_TYPE=Release -DWITH_RC_FILES=OFF -DENABLE_TESTING=ON -DBUILD_CSGAPPS=ON -DBUILD_CSG_MANUAL=ON -DBUILD_XTP=ON -DENABLE_REGRESSION_TESTING=ON -DREGRESSIONTEST_TOLERANCE="2e-5" -DHDF5_C_COMPILER_EXECUTABLE=/usr/bin/h5cc
%make_build
%_openmpi_unload

%install
%make_install -C %{_target_platform}
sed -i '1s@env @@' %{buildroot}/%{_datadir}/votca/scripts/inverse/*.py
sed -i -e '1s@env python@python2@'  %{buildroot}/%{_bindir}/xtp_*

%check
%_openmpi_load
make -C %{_target_platform} test CTEST_OUTPUT_ON_FAILURE=1 ARGS="-E \(spce_cma_simple\)"
%_openmpi_unload

%files
%license tools/LICENSE
%doc tools/NOTICE
%{_bindir}/votca_*
%{_bindir}/csg_*
%{_bindir}/xtp_*
%{_libdir}/libvotca_*.so.*
%{_mandir}/man1/votca_*.*
%{_mandir}/man1/csg_*.*
%{_mandir}/man1/xtp_*.*
%{_mandir}/man7/votca-*.7*
%{_datadir}/votca
%{_datadir}/doc/votca/*.pdf

%files devel
%{_includedir}/votca/
%{_libdir}/libvotca_*.so
%{_libdir}/cmake/VOTCA_*

%changelog
