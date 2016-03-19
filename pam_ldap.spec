%bcond_with	dnsconfig

Summary:	NSS library and PAM module for LDAP
Name:		pam_ldap
Version:	186
Release:	12
License:	LGPLv2+
Group:		System/Libraries
Url:		http://www.padl.com/
Source0:	http://www.padl.com/download/%{name}-%{version}.tar.gz
Source1:	resolve.c
Source2:	resolve.h
Source3:	snprintf.h
Source4:	snprintf.c
Patch2:		pam_ldap-156-makefile.patch
Patch3:		pam_ldap-176-dnsconfig.patch
# http://bugzilla.padl.com/show_bug.cgi?id=324
Patch4:		pam_ldap-184-lockoutmsg.patch
Patch5:		pam_ldap-186-automake1.13-fix.patch
#BuildRequires:	db_nss-devel >= 4.2.52-5mdk
BuildRequires:	openldap-devel
BuildRequires:	pam-devel
Requires:	nss_ldap >= 217

%description
Pam_ldap is a module for Linux-PAM that supports password changes, V2
clients, Netscapes SSL, ypldapd, Netscape Directory Server password
policies, access authorization, crypted hashes, etc.

Install pam_ldap if you need to authenticate PAM-enabled services to
LDAP.
%if !%{with dnsconfig}
This package can be compiled with support for configuration
from DNS, by building with "--with dnsconfig"
%else
This package is built with DNS configuration support
%endif

%prep
%setup -q
%patch2 -p1 -b .pam_makefile~
%patch4 -p1 -b .lockoutmsg~

%if %{with dnsconfig}
%patch3 -p1 -b .dnsconfig
cp %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4}
%endif
%patch5 -p1 -b .am113~
autoreconf -fiv

%build
%serverbuild
%configure2_5x \
	--with-ldap-lib=openldap \
	--libdir=/%{_lib}
%make

%install
%makeinstall_std

# Remove unpackaged file
rm %{buildroot}%{_sysconfdir}/ldap.conf 

%files
%doc AUTHORS ChangeLog README pam.d chsh chfn ldap.conf
/%{_lib}/security/*so*
%{_mandir}/man?/*

