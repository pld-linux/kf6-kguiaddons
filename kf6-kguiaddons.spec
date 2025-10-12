#
# Conditional build:
%bcond_with	tests		# test suite

%define		kdeframever	6.19
%define		qtver		6.5.0
%define		kfname		kguiaddons

Summary:	Utilities for graphical user interfaces
Summary(pl.UTF-8):	Narzędzia do graficznych interfejsów użytkownika
Name:		kf6-%{kfname}
Version:	6.19.0
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/frameworks/%{kdeframever}/%{kfname}-%{version}.tar.xz
# Source0-md5:	0ff2052c895371c9999eca831f389e5c
URL:		https://kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6DBus-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= %{qtver}
BuildRequires:	Qt6WaylandClient-devel >= %{qtver}
BuildRequires:	cmake >= 3.16
BuildRequires:	kf6-extra-cmake-modules >= %{version}
BuildRequires:	libxcb-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	plasma-wayland-protocols-devel >= 1.15.0
BuildRequires:	qt6-linguist >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	wayland-devel >= 1.9
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-proto-kbproto-devel
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
Requires:	Qt6Core >= %{qtver}
Requires:	Qt6DBus >= %{qtver}
Requires:	Qt6Gui >= %{qtver}
Requires:	Qt6WaylandClient >= %{qtver}
Requires:	kf6-dirs
Requires:	wayland >= 1.9
# will serve also for parallelly installed kf5-kguiaddons
Provides:	kf5-kguiaddons-geo-handler = %{version}-%{release}
Obsoletes:	kf5-kguiaddons-geo-handler < 6
%requires_eq_to Qt6Core Qt6Core-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The KDE GUI addons provide utilities for graphical user interfaces in
the areas of colors, fonts, text, images, keyboard input.

%description -l pl.UTF-8
Pakiet dodatków KDE GUI zapewnia narzędzia do graficznych interfejsów
użytkownika w obszarze kolorów, fontów, tekstu, obrazów i wejścia z
klawiatury.

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
	-DBUILD_PYTHON_BINDINGS=OFF \
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

%post
/sbin/ldconfig
%update_desktop_database_post

%postun
/sbin/ldconfig
%update_desktop_database_postun

%files
%defattr(644,root,root,755)
%doc README.md
%{_libdir}/libKF6GuiAddons.so.*.*.*
%ghost %{_libdir}/libKF6GuiAddons.so.6
%dir %{_libdir}/qt6/qml/org/kde/guiaddons
%{_libdir}/qt6/qml/org/kde/guiaddons/libkguiaddonsqml.so
%{_libdir}/qt6/qml/org/kde/guiaddons/kde-qmlmodule.version
%{_libdir}/qt6/qml/org/kde/guiaddons/kguiaddonsqml.qmltypes
%{_libdir}/qt6/qml/org/kde/guiaddons/qmldir
%{_datadir}/qlogging-categories6/kguiaddons.categories

# geo-handler (common for kf5 and kf6)
%attr(755,root,root) %{_bindir}/kde-geo-uri-handler
%{_desktopdir}/google-maps-geo-handler.desktop
%{_desktopdir}/openstreetmap-geo-handler.desktop
##%{_desktopdir}/qwant-maps-geo-handler.desktop
%{_desktopdir}/wheelmap-geo-handler.desktop

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKF6GuiAddons.so
%{_includedir}/KF6/KGuiAddons
%{_libdir}/cmake/KF6GuiAddons
%{_pkgconfigdir}/KF6GuiAddons.pc
