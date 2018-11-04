#
# Conditional build:
%bcond_with	lua		# build without tests

Summary:	Alpine Package Keeper - package manager for alpine
Name:		apk-tools
Version:	2.10.1
Release:	1
License:	GPL v2
Group:		Base
Source0:	https://dev.alpinelinux.org/archive/apk-tools/%{name}-%{version}.tar.xz
# Source0-md5:	d14969082e880bd056644f73ac3b3eb2
Patch0:		0001-fix-strncpy-bounds-errors.patch
Patch1:		0002-include-sys-sysmacros.h-for-makedev-definition.patch
Patch2:		0001-add-support-for-openssl-1.1.patch
URL:		https://git.alpinelinux.org/cgit/apk-tools/
%{?with_lua:BuildRequires:	lua52-devel}
BuildRequires:	openssl-devel
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir /sbin

%description
Package manager for Alpine Linux.

%package lua
Summary:	Lua module for apk-tools
Group:		Base

%description lua
Lua module for apk-tools.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
generate_config() {
cat <<-EOF
	FULL_VERSION=%{version}-%{release}
	LUAAPK=%{?with_lua:YesPlease}
	export LUAAPK
EOF
}
generate_config > config.mk
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

# empty file
%{__rm} $RPM_BUILD_ROOT%{_docdir}/apk/README

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_sbindir}/apk

%if %{with lua}
%files lua
%defattr(644,root,root,755)
# XXX: parent dir not packaged
%{_prefix}/lib/lua/5.2/apk.so
%endif
