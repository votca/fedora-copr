#global _rcname rc3
#global _rc _%%_rcname

Name:           votca
Version:        1.5
Release:        0.1%{?_rcname}%{?dist}
Summary:        VOTCA tools library
Group:          Applications/Engineering
License:        ASL 2.0
URL:            http://www.votca.org
Source0:        https://github.com/votca/votca/archive/v%{version}%{?_rc}.tar.gz#/%{name}-%{version}%{?_rc}.tar.gz
Source1:        https://github.com/votca/tools/archive/v%{version}%{?_rc}.tar.gz#/%{name}-tools-%{version}%{?_rc}.tar.gz
Source2:        https://github.com/votca/csg/archive/v%{version}%{?_rc}.tar.gz#/%{name}-csg-%{version}%{?_rc}.tar.gz
Source3:        https://github.com/votca/csg-tutorials/archive/v%{version}%{?_rc}.tar.gz#/%{name}-csg-tutorials-%{version}%{?_rc}.tar.gz
Source4:        https://github.com/votca/csg-manual/archive/v%{version}%{?_rc}.tar.gz#/%{name}-csg-manual-%{version}%{?_rc}.tar.gz
Source5:        https://github.com/votca/csgapps/archive/v%{version}%{?_rc}.tar.gz#/%{name}-csgapps-%{version}%{?_rc}.tar.gz
Source6:        https://github.com/votca/xtp/archive/v%{version}%{?_rc}.tar.gz#/%{name}-xtp-%{version}%{?_rc}.tar.gz
Source7:        https://github.com/votca/ctp/archive/v%{version}%{?_rc}.tar.gz#/%{name}-ctp-%{version}%{?_rc}.tar.gz
Patch0:         https://github.com/votca/csgapps/pull/18.diff

BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  expat-devel
BuildRequires:  fftw-devel
BuildRequires:  eigen3-devel
BuildRequires:  boost-devel
BuildRequires:  gromacs-devel
BuildRequires:  perl-generators
BuildRequires:  txt2tags
BuildRequires:  sqlite-devel
BuildRequires:  texlive
BuildRequires:  texlive-appendix
BuildRequires:  texlive-wrapfig
BuildRequires:  texlive-a4wide
BuildRequires:  texlive-xstring 
BuildRequires:  inkscape
BuildRequires:  transfig
BuildRequires:  texlive-units
BuildRequires:  texlive-sidecap
BuildRequires:  texlive-bclogo
BuildRequires:  texlive-mdframed
BuildRequires:  texlive-braket
BuildRequires:  tex(latex)
BuildRequires:  graphviz
BuildRequires:  hdf5-devel
BuildRequires:  lammps
BuildRequires:  libxc-devel
BuildRequires:  ceres-solver-devel
BuildRequires:  ImageMagick
BuildRequires:  ghostscript-tools-dvipdf
BuildRequires:  gromacs
BuildRequires:  gromacs-openmpi
BuildRequires:  openmpi-devel
BuildRequires:  python2
%if 0%{?fedora} >= 29
BuildRequires:  python-unversioned-command
%endif
BuildRequires:  gnuplot
BuildRequires:  octave

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
Requires:       sqlite-devel

%description devel
Versatile Object-oriented Toolkit for Coarse-graining Applications (VOTCA) is
a package intended to reduce the amount of routine work when doing systematic
coarse-graining of various systems. The core is written in C++.

%prep
%setup -q -a 1 -a 2 -a 3 -a 4 -a 5 -a 6 -a 7 -n %{name}-%{version}%{?_rc}
for i in tools csg csg-tutorials csg-manual csgapps xtp ctp; do
  rmdir $i && mv $i-%{version}%{?_rc} $i;
done
sed -i -e '1s@env python@python3@' tools/scripts/votca_compare.in
%patch0 -d csgapps -p1

# create latex.fmt before manual generation does it in parallel and might have a raise condition
mktexfmt latex.fmt

%build
# load openmpi, so that cmake can find mdrun_openmpi for testing
%_openmpi_load
mkdir %{_target_platform}
pushd %{_target_platform}
%{cmake3} .. -DCMAKE_BUILD_TYPE=Release -DWITH_RC_FILES=OFF -DENABLE_TESTING=ON -DBUILD_CSGAPPS=ON -DBUILD_CSG_MANUAL=ON -DBUILD_XTP=ON -DENABLE_REGRESSION_TESTING=ON -DBUILD_XTP_MANUAL=ON -DBUILD_CTP=ON -DBUILD_CTP_MANUAL=ON -DREGRESSIONTEST_TOLERANCE="2e-5"
%make_build
%_openmpi_unload

%install
%make_install -C %{_target_platform}
sed -i '1s@env @@' %{buildroot}/%{_datadir}/votca/scripts/inverse/*.py
sed -i -e '1s@env python@python2@'  %{buildroot}/%{_bindir}/xtp_*

%check
%_openmpi_load
make -C %{_target_platform} test CTEST_OUTPUT_ON_FAILURE=1 ARGS="-E \(imc\|cma\|multi\)"
%_openmpi_unload

%files
%license tools/LICENSE
%doc tools/NOTICE
%{_bindir}/votca_*
%{_bindir}/csg_*
%{_bindir}/xtp_*
%{_bindir}/ctp_*
%{_bindir}/moo_*
%{_bindir}/kmc_*
%{_libdir}/libvotca_*.so.*
%{_mandir}/man1/votca_*.*
%{_mandir}/man1/csg_*.*
%{_mandir}/man1/xtp_*.*
%{_mandir}/man1/ctp_*.*
%{_mandir}/man1/moo_*.*
%{_mandir}/man1/kmc_*.*
%{_mandir}/man7/votca-*.7*
%{_datadir}/votca
%{_datadir}/doc/votca/*.pdf

%files devel
%{_includedir}/votca/
%{_libdir}/libvotca_*.so
%{_libdir}/pkgconfig/libvotca_*.pc

%changelog
