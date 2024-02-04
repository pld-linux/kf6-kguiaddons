#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeframever	5.249.0
%define		qtver		5.15.2
%define		kfname		kguiaddons

Summary:	Utilities for graphical user interfaces
Name:		kf6-%{kfname}
Version:	5.249.0
Release:	0.1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/unstable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	a3b79e48c2d8d03725794713c410d5ae
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6WaylandClient >= %{qtver}
BuildRequires:	Qt6WaylandClient-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf5-plasma-wayland-protocols-devel >= 1.7.0
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	libxcb-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	qt6-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	wayland-devel >= 1.9
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-proto-kbproto-devel
BuildRequires:	xz
Requires:	Qt6Gui >= %{qtver}
Requires:	Qt6WaylandClient >= %{qtver}
Requires:	kf6-dirs
Requires:	wayland >= 1.9
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
The KDE GUI addons provide utilities for graphical user interfaces in
the areas of colors, fonts, text, images, keyboard input.

%package devel
Summary:	Header files for %{kfname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kfname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Gui-devel >= %{qtver}
Requires:	cmake >= 3.16

%description devel
Header files for %{kfname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kfname}.

%prep
%setup -q -n %{kfname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
%ninja_build -C build test
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md
%ghost %{_libdir}/libKF6GuiAddons.so.6
%attr(755,root,root) %{_libdir}/libKF6GuiAddons.so.*.*
%{_datadir}/qlogging-categories6/kguiaddons.categories
%attr(755,root,root) %{_bindir}/kde-geo-uri-handler
%{_desktopdir}/google-maps-geo-handler.desktop
%{_desktopdir}/openstreetmap-geo-handler.desktop
%{_desktopdir}/qwant-maps-geo-handler.desktop
%{_desktopdir}/wheelmap-geo-handler.desktop

%files devel
%defattr(644,root,root,755)
%{_includedir}/KF6/KGuiAddons
%{_libdir}/cmake/KF6GuiAddons
%{_libdir}/libKF6GuiAddons.so
%{_pkgconfigdir}/KF6GuiAddons.pc
