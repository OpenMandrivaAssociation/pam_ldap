# conditionally define %mkrel
%{?!mkrel:%define mkrel(c:) %{-c:0.%{-c*}.}%{!?_with_unstable:%(perl -e '$_="%{1}";m/(.\*\\D\+)?(\\d+)$/;$rel=${2}-1;re;print "$1$rel";').%{?subrel:%subrel}%{!?subrel:1}.%{?distversion:%distversion}%{?!distversion:%(echo $[%{mdkversion}/10])}}%{?_with_unstable:%{1}}%{?distsuffix:%distsuffix}%{?!distsuffix:mdk}}

Summary:	NSS library and PAM module for LDAP
Name: 		pam_ldap
Version: 	185
Release: 	%mkrel 1
License:	LGPL
Group:		System/Libraries
URL: 		http://www.padl.com/
#BuildRequires:	db_nss-devel >= 4.2.52-5mdk
BuildRequires:	libldap-devel >= 2.0.7-7.1mdk
BuildRequires:	pam-devel
BuildRequires:	automake1.4
Source0: 	http://www.padl.com/download/%{name}-%{version}.tar.gz
Source1:	resolve.c
Source2:	resolve.h
Source3:	snprintf.h
Source4:	snprintf.c
Patch1:     pam_ldap-185-fix-script-invocation.patch
Patch2:		pam_ldap-156-makefile.patch
Patch3:		pam_ldap-176-dnsconfig.patch
# http://bugzilla.padl.com/show_bug.cgi?id=324
Patch4:		pam_ldap-184-lockoutmsg.patch
Requires:	nss_ldap >= 217
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Pam_ldap is a module for Linux-PAM that supports password changes, V2
clients, Netscapes SSL, ypldapd, Netscape Directory Server password
policies, access authorization, crypted hashes, etc.

Install pam_ldap if you need to authenticate PAM-enabled services to
LDAP.
%{?!_with_dnsconfig:This package can be compiled with support for configuration}
%{?!_with_dnsconfig:from DNS, by building with "--with dnsconfig"}
%{?_with_dnsconfig:This package is built with DNS configuration support}

%prep
%setup -q
%patch1 -p1
%patch2 -p1 -b .pam_makefile
%patch4 -p1 -b .lockoutmsg

%if %{?_with_dnsconfig:1}%{!?_with_dnsconfig:0}
%patch3 -p1 -b .dnsconfig
for i in %SOURCE1 %SOURCE2 %SOURCE3 %SOURCE4
do cp $i .
done
%endif

%build
%serverbuild
#aclocal && automake && autoheader && autoconf
#autoreconf --force

rm -f configure
libtoolize --copy --force; aclocal; autoconf; automake

export CFLAGS="$CFLAGS -fno-strict-aliasing"
%configure2_5x --with-ldap-lib=openldap --libdir=/%{_lib}
%__make

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_mandir}/man5

install -d %{buildroot}/%{_sysconfdir}
install -d %{buildroot}/%{_lib}/security

# Install the module for PAM.
%make install DESTDIR="%{buildroot}" libdir=/%{_lib}

# Remove unpackaged file
rm -rf	%{buildroot}%{_sysconfdir}/ldap.conf 

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog COPYING COPYING.LIB README pam.d chsh chfn ldap.conf
/%{_lib}/security/*so*
%{_mandir}/man?/*
