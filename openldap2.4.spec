%define pkg_name	openldap
%define version	2.4.5
%define rel 2
%global	beta beta

%{?!mklibname:%{error:You are missing macros, build will fail, see http://qa.mandriva.com/twiki/bin/view/Main/BackPorting}}

%{?!distsuffix:%define distsuffix mdk}
%{?!distversion:%define distversion %(echo $[%{mdkversion}/10])}
%{?!mkrel:%define mkrel(c:) %{-c:0.%{-c*}.}%{!?_with_unstable:%(perl -e '$_="%{1}";m/(.\*\\D\+)?(\\d+)$/;$rel=${2}-1;re;print "$1$rel";').%{?subrel:%subrel}%{!?subrel:1}.%{distversion}%{?_with_unstable:%{1}}%{distsuffix}}}

%define release %mkrel %rel

#defaults
%define build_system 0
%define build_alternatives 0
%define build_modules 1
%define build_modpacks 0
%define build_slp 0
%global build_migration 0

%if %{?mdkversion:0}%{?!mdkversion:1}
# OK, we're not on a Mandriva box ... set this to the lowest we support
# and define a new macro we can use to know we're not in Mandriva
%define mdkversion 1000
%global notmdk 1
%endif

%if %mdkversion >= 200900
%define build_system 1
%else
%global build_migration 1
%define _with_migration 1
%endif

%{?_with_system: %global build_system 1}
%{?_without_system: %global build_system 0}
%{?_with_modules: %global build_modules 1}
%{?_without_modules: %global build_modules 0}
%{?_with_slp: %global build_slp 1}
%{?_without_slp: %global build_slp 0}

%define major 		2.4_2
%define fname ldap
%define libname %mklibname %fname %major
%define migtools_ver 	45
# we want db42 with 4.2.52.5 and Howard's patch (2008.0)
%if %mdkversion >= 200800
%global db4_internal 0
%else
%global db4_internal 1
%global __libtoolize /bin/true
%endif
%{?_with_db4internal: %global db4_internal 1}
%{?_without_db4internal: %global db4_internal 0}
%define dbver 4.2.52
%define dbname %(a=%dbver;echo ${a%.*})

%define ol_ver_major 2.4
%if %build_system
%define ol_major %{nil}
%define ol_suffix %nil
%else
%define ol_major 2.4
%define ol_suffix 24
%endif

%if %build_alternatives || !%build_system
%define alternative_major 2.4
%else
%define alternatives_major %{nil}
%endif

%global clientbin	ldapadd,ldapcompare,ldapdelete,ldapmodify,ldapmodrdn,ldappasswd,ldapsearch,ldapwhoami
%if %db4_internal
%global serverbin	slapd_db_archive,slapd_db_checkpoint,slapd_db_deadlock,slapd_db_dump,slapd_db_load,slapd_db_printlog,slapd_db_recover,slapd_db_stat,slapd_db_upgrade,slapd_db_verify,slapd-addel,slapd-bind,slapd-modify,slapd-modrdn,slapd-read,slapd-search,slapd-tester
%else
%global serverbin	slapd-addel,slapd-bind,slapd-modify,slapd-modrdn,slapd-read,slapd-search,slapd-tester
%endif
%define serversbin	slapadd,slapcat,slapd,slapdn,slapindex,slappasswd,slaptest,slurpd,slapacl,slapauth

#localstatedir is passed directly to configure, and we want it to be /var/lib
#define _localstatedir %{_var}/run
%define	_libexecdir	%{_sbindir}

# Allow --with[out] SASL at rpm command line build
%{?_without_SASL: %{expand: %%define _without_cyrussasl --without-cyrus-sasl}}
%{?_with_SASL: %{expand: %%define _with_cyrussasl --with-cyrus-sasl}}
%{!?_with_cyrussasl: %{!?_without_cyrussasl: %global _with_cyrussasl --with-cyrus-sasl}}
%{?_with_cyrussasl: %define _with_cyrussasl --with-cyrus-sasl}
%{?_without_cyrussasl: %define _without_cyrussasl --without-cyrus-sasl}
%{?_with_gdbm: %global db_conv dbb}
%{!?_with_gdbm: %global db_conv gdbm}
%global sql 1
%{?_without_sql: %global sql 0}
%global back_perl 0

Summary: 	LDAP servers and sample clients
Name: 		%{pkg_name}%{ol_major}
Version: 	%{version}
Release: 	%{release}
License: 	Artistic
Group: 		System/Servers
URL: 		http://www.openldap.org

# Openldap source
Source0: 	ftp://ftp.openldap.org/pub/OpenLDAP/openldap-release/%{pkg_name}-%{version}%{beta}.tgz


## To generate ths tarball, check the docs out of CVS:
# cvs -d :pserver:anonymous@cvs.OpenLDAP.org:/repo/OpenLDAP co \
# -r OPENLDAP_REL_ENG_2_4 guide
## patch the docs:
# cd guide/admin
# patch -p0 < `rpm --eval %_sourcedir`/openldap-2.4-admin-guide-add-vendor-doc.patch
# cp -p `rpm --eval %_sourcedir`/vendor*.sdf .
## build the docs
# make guide.html
## tar them up
# mkdir openldap-guide
# cp *.html *.gif *.png ../images/LDAPlogo.gif openldap-guide
# tar cjvf `rpm --eval %_sourcedir`/openldap-guide-2.4.tar.bz2 openldap-guide
## To update the README-openldap2.4.mdv as well:
# sdf -2txt_ vendor-standalone.sdf
# cp vendor-standalone.txt `rpm --eval %_sourcedir`/README-openldap2.4.mdv
## ensure your changes get back into the package:
# cvs diff | bzip2 -c > \
# `rpm --eval %_sourcedir`/openldap-2.4-admin-guide-add-vendor-doc.patch.bz2
# tar cjvf `rpm --eval %_sourcedir`/openldap-2.4-vendor-docs.tar.bz2 vendor*.sdf

Source12:	openldap-guide-2.4.tar.bz2
Source13:	README-openldap2.4.mdv

# Specific source
Source1: 	ldap.init
Source2: 	%{pkg_name}.sysconfig
Source19:	gencert.sh
Source20:	ldap.logrotate
Source21:	slapd.conf
Source22:	DB_CONFIG
Source23:	ldap.conf
Source24:	slapd.access.conf
Source25:	ldap-hot-db-backup
Source26:	ldap-reinitialise-slave
Source27:	ldap-common

# Migration tools
Source11:	http://www.padl.com/download/MigrationTools-%{migtools_ver}.tar.bz2
Source3: 	migration-tools.txt
Source4: 	migrate_automount.pl

%if %db4_internal
Source30: http://www.sleepycat.com/update/snapshot/db-%{dbver}.tar.bz2
%endif

# Extended Schema 
Source50: 	rfc822-MailMember.schema
Source51: 	autofs.schema
Source52: 	kerberosobject.schema
# Get from qmail-ldap patch (http://www.nrg4u.com/qmail/)
Source53: 	qmail.schema
Source54: 	mull.schema
# Get from samba source, examples/LDAP/samba.schema
Source55: 	samba.schema
Source56: 	http://debian.jones.dk/debian/local/honda/pool-ldapv3/woody-jones/openldap2/schemas/netscape-profile.schema
Source57: 	http://debian.jones.dk/debian/local/honda/pool-ldapv3/woody-jones/openldap2/schemas/trust.schema
Source58: 	http://debian.jones.dk/debian/local/honda/pool-ldapv3/woody-jones/openldap2/schemas/dns.schema
Source59: 	http://debian.jones.dk/debian/local/honda/pool-ldapv3/woody-jones/openldap2/schemas/cron.schema
Source60:	http://debian.jones.dk/debian/local/honda/pool-ldapv3/woody-jones/openldap2/schemas/qmailControl.schema
Source61:	krb5-kdc.schema
Source62:	kolab.schema
# from evolution package
Source63:	evolutionperson.schema
# from rfc2739, updated for schema correctness, used by evo for calendar attrs 
Source64:	calendar.schema
# from README.LDAP in sudo (pre-1.6.8) CVS:
Source65:	sudo.schema
# from bind sdb_ldap page:http://www.venaas.no/ldap/bind-sdb/dnszone-schema.txt
Source66:	dnszone.schema
# from http://cvs.pld.org.pl/SOURCES/openldap-dhcp.schema
Source67: 	dhcp.schema
# from pam_ldap source
Source68: 	ldapns.schema

# Doc sources, used to build SOURCE12 and SOURCE13 above
Source100:	openldap-2.4-admin-guide-add-vendor-doc.patch
Source101:	vendor.sdf
Source100:	vendor-standalone.sdf

# Chris Patches
Patch0: 	%{pkg_name}-2.3.4-config.patch
Patch1:		%{pkg_name}-2.0.7-module.patch

# For now, only build support for SMB (no krb5) changing support in smbk5passwd
# overlay:
Patch2:		openldap-2.3.4-smbk5passwd-only-smb.patch

# RH + PLD Patches
Patch15:	%{pkg_name}-cldap.patch

# Migration tools Patch
Patch40: 	MigrationTools-34-instdir.patch
Patch41: 	MigrationTools-36-mktemp.patch
Patch42: 	MigrationTools-27-simple.patch
Patch43: 	MigrationTools-26-suffix.patch
Patch45:	MigrationTools-45-i18n.patch
# schema patch
Patch46: 	openldap-2.0.21-schema.patch
# http://qa.mandriva.com/show_bug.cgi?id=15499
Patch48:	MigrationTools-45-structural.patch

# http://www.oracle.com/technology/software/products/berkeley-db/db/
# http://www.oracle.com/technology/products/berkeley-db/db/update/4.2.52/patch.4.2.52.html
Patch50: http://www.oracle.com/technology/products/berkeley-db/db/update/4.2.52/patch.4.2.52.1
Patch51: http://www.oracle.com/technology/products/berkeley-db/db/update/4.2.52/patch.4.2.52.2
Patch52: db-4.2.52-amd64-mutexes.patch
Patch55: http://www.oracle.com/technology/products/berkeley-db/db/update/4.2.52/patch.4.2.52.3
Patch56: http://www.oracle.com/technology/products/berkeley-db/db/update/4.2.52/patch.4.2.52.4
Patch57: http://www.oracle.com/technology/products/berkeley-db/db/update/4.2.52/patch.4.2.52.5
Patch58: http://www.stanford.edu/services/directory/openldap/configuration/patches/db/4252-region-fix.diff
Patch60: db-4.2.52-libtool-fixes.patch
%if %db4_internal
# used by s_config, which is required by above patch:
BuildRequires:	ed autoconf%{?notmdk: >= 2.5}
%else
# txn_nolog added in 4.2.52-6mdk
BuildRequires: 	db4-devel = %{dbver}
%endif

Patch53: %pkg_name-2.2.19-ntlm.patch
# preserves the temp file used to import data if an error occured
Patch54: MigrationTools-40-preserveldif.patch

#patches in CVS
# see http://www.stanford.edu/services/directory/openldap/configuration/openldap-build.html
# for other possibly interesting patches
Patch100:	openldap-2.4-dont-write-outside-testdir.patch


%{?_with_cyrussasl:BuildRequires: 	%{?!notmdk:libsasl-devel}%{?notmdk:cyrus-sasl-devel}}
%{?_with_kerberos:BuildRequires:	krb5-devel}
BuildRequires:	openssl-devel, perl
%if %build_slp
BuildRequires: openslp-devel
%endif
#BuildRequires: libgdbm1-devel
%if %sql
BuildRequires: 	unixODBC-devel
%endif
%if %back_perl
BuildRequires:	perl-devel
%endif
BuildRequires:  ncurses-devel >= 5.0
BuildRequires: tcp_wrappers%{?!notmdk:-devel} libtool%{?!notmdk:-devel}
BuildRequires:  krb5-devel
BuildRequires:	groff
# for make test:
BuildRequires:	diffutils
BuildRoot: 	%{_tmppath}/%{name}-%{version}-root
Requires: 	%libname = %{version}-%{release}
Requires:	shadow-utils, setup >= 2.2.0-6mdk
#%{mklibname db 4.3}

%description
OpenLDAP is an open source suite of LDAP (Lightweight Directory Access
Protocol) applications and development tools.  The suite includes a
stand-alone LDAP server (slapd) which is in the -servers package, libraries for
implementing the LDAP protocol (in the lib packages), and utilities, tools, and 
sample clients (in the -clients package). The openldap binary package includes
only configuration files used by the libraries.

Install openldap if you need LDAP applications and tools.

%package servers
Summary: 	OpenLDAP servers and related files
Group: 		System/Servers
Requires(pre):	%{?!notmdk:rpm-helper}%{?notmdk:/usr/sbin/useradd} coreutils
%if !%build_modpacks
Provides:	%{name}-back_dnssrv = %{version}-%{release}
Provides:	%{name}-back_ldap = %{version}-%{release}
Provides:	%{name}-back_passwd = %{version}-%{release}
Provides:	%{name}-back_sql = %{version}-%{release}
Obsoletes:	%{name}-back_dnssrv < %{version}-%{release}
Obsoletes:	%{name}-back_ldap < %{version}-%{release}
Obsoletes:	%{name}-back_passwd < %{version}-%{release}
Obsoletes:	%{name}-back_sql < %{version}-%{release}
%endif
%if !%db4_internal
Requires(pre):	db4-utils
Requires(post):	db4-utils
Requires:	db4-utils
%endif
%if %{?_with_cyrussasl:1}%{!?_with_cyrussasl:0}
%define saslver %([ -f "%{_includedir}/sasl/sasl.h" ] && echo -e "#include <sasl/sasl.h>\\nSASL_VERSION_MAJOR SASL_VERSION_MINOR SASL_VERSION_STEP"|cpp|awk 'END {printf "%s.%s.%s",$1,$2,$3}' || echo "2.1.22")
%define sasllib %mklibname sasl 2
#Ensure we have the sasl library we compiled against available in post so
#slapadd etc works
Requires(post):	%{?!notmdk:%sasllib}%{?notmdk:cyrus-sasl} = %saslver
%endif
Requires: 	%libname = %{version}-%{release}
Conflicts:	kolab < 1.9.5-0.20050801.4mdk

%description servers
OpenLDAP Servers

This package contains the OpenLDAP server, slapd (LDAP server), additional 
backends, configuration files, schema definitions required for operation, and 
database maintenance tools

This server package was compiled with support for the %{?_with_gdbm:gdbm}%{!?_with_gdbm:berkeley}
database library.

%package clients
Summary: 	OpenLDAP clients and related files
Group: 		System/Servers
Requires: 	%libname = %{version}-%{release}

%description clients
OpenLDAP clients

This package contains command-line ldap clients (ldapsearch, ldapadd etc)

%if %build_migration
%package migration
Summary: 	Set of scripts for migration of a nis domain to a ldap directory
Group: 		System/Configuration/Other
Requires: 	%{name}-servers = %{version}
Requires: 	%{name}-clients = %{version}
Requires: 	perl-MIME-Base64

%description migration
This package contains a set of scripts for migrating data from local files
(ie /etc/passwd) or a nis domain to an ldap directory.
%endif

%package -n %libname
Summary: 	OpenLDAP libraries
Group: 		System/Libraries
Provides:       lib%fname = %version-%release
# This is needed so all libldap2 applications get /etc/openldap/ldap.conf
# which was moved from openldap-clients to openldap in 2.1.25-4mdk
Requires:	%{name} >= 2.1.25-4mdk

%description -n %libname
This package includes the libraries needed by ldap applications.


%package -n %libname-devel
Summary: 	OpenLDAP development libraries and header files
Group: 		Development/C
Requires: 	%libname = %{version}-%release
Provides:       %{name}-devel = %{version}-%{release}
%if %build_system
Provides: 	lib%fname-devel = %version-%release
Provides:	openldap2-devel = %{version}-%{release}
Obsoletes: 	openldap-devel
%endif
Conflicts:	libldap1-devel
Conflicts:	%mklibname -d ldap 2
Conflicts:	%mklibname -d ldap 2.3_0

%description -n %libname-devel
This package includes the development libraries and header files
needed for compiling applications that use LDAP internals.  Install
this package only if you plan to develop or will need to compile
LDAP clients.


%package -n %{libname}-static-devel
Summary: 	OpenLDAP development static libraries
Group: 		Development/C
Requires: 	%libname-devel = %{version}-%release
%if %build_system
Provides: 	lib%fname-devel-static = %version-%release
Provides: 	lib%fname-static-devel = %version-%release
Provides:	openldap-devel-static = %{version}-%{release}
Provides:	openldap-static-devel = %{version}-%{release}
Obsoletes: 	openldap-devel-static
%endif
Conflicts:	libldap1-devel


%description -n %libname-static-devel
OpenLDAP development static libraries

%if %build_modpacks
%package back_dnssrv
Summary: 	Module dnssrv for OpenLDAP 
Group: 		System/Libraries
Requires: 	%libname = %{version}-%{release}
Requires: 	openldap-servers = %{version}-%{release}

%description back_dnssrv
The dnssrv daabase backend module for OpenLDAP daemon

%package back_ldap
Summary: 	Module ldap for OpenLDAP 
Group: 		System/Libraries
Requires: 	%libname = %{version}-%{release}
Requires: 	openldap-servers = %{version}-%{release}

%description back_ldap
The ldap database backend module for OpenLDAP daemon


%package back_passwd
Summary: 	Module passwd for OpenLDAP 
Group: 		System/Libraries
Requires: 	%libname = %{version}-%release
Requires: 	openldap-servers = %{version}-%release

%description back_passwd
The passwd database backend module for OpenLDAP daemon
%endif
%if %sql && %build_modpacks
%package back_sql
Summary: 	Module sql for OpenLDAP 
Group: 		System/Libraries
Requires: 	%libname = %{version}-%{release}
Requires: 	openldap-servers = %{version}-%{release}

%description back_sql
The sql database backend module for OpenLDAP daemon
%endif

%package doc
Summary: 	OpenLDAP documentation and administration guide
Group: 		Books/Computer books
Requires: 	openldap
Provides:	openldap-guide
Obsoletes:	openldap-guide

%description doc
OpenLDAP documentation, incuding RFCs and the adminitration guide

%package tests
Summary:	OpenLDAP Test Suite - tests and data
Group:		Development/Other
Requires:	%{name}-servers %{name}-clients %{name}-testprogs

%description tests
OpenLDAP now has a substantial test suite, which includes sample configurations
and data for a large number of scenarios and features. These are useful for
testing the installed server, and seeing examples of how to use the features.

The intention is that it should be possible to run the entire test suite on
the installed server using this package.


%package testprogs
Summary:	OpenLDAP Test Suite - simple testing client binaries
Group:		Development/Other

%description testprogs
Programs shipped with the test suite which are used by the test suite, and may
also be useful as load generators etc.

%prep
%if %db4_internal
%setup -q -n %{pkg_name}-%{version}%{beta} %{?_with_migration:-a 11} -a 30 
pushd db-%{dbver} >/dev/null
#upstream patches
%patch50
%patch51
%patch55
%patch56
%patch57
%patch58 -p1

%ifnarch %ix86
%patch52 -p1 -b .amd64-mutexes
%patch60 -p1 -b .libtool-fixes

(cd dist && ./s_config)
%endif
popd >/dev/null
%else
%setup -q  -n %{pkg_name}-%{version}%{beta} %{?_with_migration:-a 11}
%endif

%patch0 -p1 -b .config
perl -pi -e 's/^(#define\s+DEFAULT_SLURPD_REPLICA_DIR.*)ldap(.*)/${1}ldap%{ol_major}${2}/' servers/slurpd/slurp.h
perl -pi -e 's/LDAP_DIRSEP "run" //g' include/ldap_defaults.h
%patch1 -p1 -b .module
%patch2 -p1 -b .only-smb

%patch15 -p1 -b .cldap 


%if %build_migration
pushd MigrationTools-%{migtools_ver}
%patch40 -p1 -b .instdir
%patch41 -p1 -b .mktemp
%patch42 -p1 -b .simple
%patch43 -p1 -b .suffix
%patch45 -p2 -b .i18n
%patch48 -p2 -b .account
%patch54 -p1 -b .preserve
popd
%endif

%patch46 -p1 -b .mdk
#bgmilne %patch47 -p1 -b .maildropschema
# FIXME
#%patch53 -p1 -b .ntlm

# patches from CVS
#%patch100 -p1
#-b .dont-write-to-testdir

# README:
cp %{SOURCE13} README.mdk

# test049 not ready for not writing to testdir ...
mv tests/scripts/{,broken}test049*

%build
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
#disable icecream:
PATH=`echo $PATH|perl -pe 's,:[\/\w]+icecream[\/\w]+:,:,g'`
%serverbuild

%if %db4_internal
dbdir=`pwd`/db-instroot
pushd db-%{dbver}/build_unix
CONFIGURE_TOP="../dist" %configure2_5x \
        --enable-shared --disable-static \
        --with-uniquename=_openldap_slapd%{ol_suffix}_mdk \
	--program-prefix=slapd%{ol_major}_ \
%ifarch %{ix86}
	--disable-posixmutexes --with-mutex=x86/gcc-assembly
%endif
%ifarch alpha
	--disable-posixmutexes --with-mutex=ALPHA/gcc-assembly
%endif
%ifarch ia64
	--disable-posixmutexes --with-mutex=ia64/gcc-assembly
%endif
%ifarch ppc
	--disable-posixmutexes --with-mutex=PPC/gcc-assembly
%endif
%ifarch sparc
	--disable-posixmutexes --with-mutex=Sparc/gcc-assembly
%endif

#--with-mutex=POSIX/pthreads/library
#JMD: use --disable-posixmutexes so it works on a non-NPTL kernel, and use
#assembler mutexes since they're *way* faster and correctly implemented.

perl -pi -e 's/^(libdb_base=\s+)\w+/\1libslapd%{ol_suffix}_db/g' Makefile
#Fix soname and libname in libtool:
#perl -pi -e 's/shared_ext/shrext/g' libtool
make
rm -Rf $dbdir
mkdir -p $dbdir
make DESTDIR=$dbdir install
ln -sf ${dbdir}/%{_libdir}/libslapd%{ol_suffix}_db-%{dbname}.so ${dbdir}/%{_libdir}/libdb-%{dbname}.so
popd
export CPPFLAGS="-I${dbdir}/%{_includedir} $CPPFLAGS"
export LDFLAGS="-L${dbdir}/%{_libdir} $LDFLAGS"
export LD_LIBRARY_PATH="${dbdir}/%{_libdir}"
%endif

unset CONFIGURE_TOP

#FIXME: Some script backends should not be used with threads, mostly shell/perl

%if !%build_system
perl -pi -e 's,(progname = "\w+)",${1}%{ol_major}",g' servers/slapd/*.c
perl -pi -e 's,({"slap\w+)",${1}%{ol_major}",g' servers/slapd/main.c
%endif

# don't choose db4.3 even if it is available
export ol_cv_db_db_4_dot_3=no
# try and miss linuxthreads, so we get a threading lib on glibc2.4:
%if %mdkversion > 200600
export ol_cv_header_linux_threads=no
%endif
#rh only:
export CPPFLAGS="-I%{_prefix}/kerberos/include $CPPFLAGS"
%if %{?openldap_fd_setsize:1}%{!?openldap_fd_setsize:0}
CPPFLAGS="$CPPFLAGS -DOPENLDAP_FD_SETSIZE=%{openldap_fd_setsize}"
%endif
export LDFLAGS="-L%{_prefix}/kerberos/%{_lib} $LDFLAGS"
# building for systems with kernel < 2.6 requires building without epoll support
%if %{mdkversion} < 1000 || %{?_without_epoll:1}%{!?_without_epoll:0}
export ac_cv_header_sys_epoll_h=no
%endif

%configure2_5x \
	--with-subdir=%{name} \
%if !%build_system
	--program-suffix=%{ol_major} \
%endif
	--localstatedir=/var/run/ldap%{ol_major} \
	--enable-dynamic \
	--enable-syslog \
	--enable-proctitle \
	--enable-ipv6 \
	--enable-local \
	%{?_with_cyrussasl} %{?_without_cyrussasl} \
	%{?_with_kerberos} %{?_without_kerberos} \
	--with-threads \
	--with-tls \
	--enable-slapd \
	--enable-aci \
	--enable-cleartext \
	--enable-crypt \
	--enable-lmpasswd \
	%{?_with_kerberos:--enable-kpasswd} \
	%{?_with_cyrussasl:--enable-spasswd} \
%if %build_modules
	--enable-modules \
%endif
	--enable-rewrite \
	--enable-rlookups \
%if %build_slp
	--enable-slp \
%endif
	--enable-wrappers \
	--enable-bdb=yes \
	--enable-dnssrv=mod \
	--enable-hdb=yes \
	--enable-ldap=mod \
	--enable-ldbm=yes \
	--enable-meta=mod \
	--enable-monitor=mod \
	--enable-passwd=mod \
%if %back_perl
	--enable-perl=mod \
%endif
	--enable-relay=mod \
%if %sql
	--enable-sql=mod \
%endif
	--enable-overlays=mod \
	--enable-shared

# These options are no longer available
#	--enable-cldap \
#	--enable-multimaster \

%if !%build_system
perl -pi -e 's/^(ldap_subdir\s+=\s+.*)%{pkg_name}/$1%{name}/g' Makefile
%endif

# (oe) amd64 fix
perl -pi -e "s|^AC_CFLAGS.*|AC_CFLAGS = $CFLAGS -fPIC|g" libraries/librewrite/Makefile

make depend 

make 
make -C contrib/slapd-modules/smbk5pwd
pushd contrib/slapd-modules/acl
#gcc -shared -fPIC -I../../../include -I../../../servers/slapd -Wall -g \
#        -o acl-posixgroup.so posixgroup.c
popd
pushd contrib/slapd-modules/passwd
gcc -shared -fPIC -I../../../include -Wall -g -o pw-netscape.so netscape.c
gcc -shared -fPIC -I../../../include -I /usr/kerberos/include -Wall -g -DHAVE_KRB5 -o pw-kerberos.so kerberos.c
popd

%check
%if %{!?_without_test:1}%{?_without_test:0}
%if !%{build_system}
pushd clients/tools
for OLD in {%{clientbin}}
do
    NEW=`echo ${OLD}%{alternative_major}`
    ln -sf $OLD $NEW
    #mv -f $OLD $NEW ||:
    #if [ -L $NEW ]
    #then ln -sf `readlink $NEW`%{alternative_major} $NEW
    #fi
done
popd
%endif
#disable icecream:
#PATH=`echo $PATH|perl -pe 's,:[\/\w]+icecream[\/\w]+:,:,g'`
%if %db4_internal
dbdir=`pwd`/db-instroot
export LD_LIBRARY_PATH="${dbdir}/%{_libdir}"
%endif
# meta test seems to timeout on the Mandriva cluster:
#export TEST_META=no
make -C tests %{!?tests:bdb}%{?tests:%tests}
%endif

%install
#disable icecream:
#PATH=`echo $PATH|perl -pe 's,:[\/\w]+icecream[\/\w]+:,:,g'`
export DONT_GPRINTIFY=1
cp -af contrib/slapd-modules/smbk5pwd/README{,.smbk5passwd}
cp -af contrib/slapd-modules/passwd/README{,.passwd}
cp -af contrib/slapd-modules/acl/README{,.acl}
rm -Rf %{buildroot}

%if %db4_internal
pushd db-%{dbver}/build_unix
%makeinstall_std
for i in %{buildroot}/%{_bindir}/db_*;do mv $i ${i/db_/slapd_db_};done
popd
%endif

%makeinstall_std

cp  contrib/slapd-modules/smbk5pwd/.libs/smbk5pwd.so* %{buildroot}/%{_libdir}/%{name}
#cp contrib/slapd-modules/acl/acl-posixgroup.so %{buildroot}/%{_libdir}/%{name}
cp contrib/slapd-modules/passwd/pw-netscape.so %{buildroot}/%{_libdir}/%{name}
cp contrib/slapd-modules/passwd/pw-kerberos.so %{buildroot}/%{_libdir}/%{name}

# try and ship the tests such that they will run properly

install -d %{buildroot}/%{_datadir}/%{name}/tests
cp -a tests/{data,scripts,Makefile,run} %{buildroot}/%{_datadir}/%{name}/tests
ln -s %{_datadir}/%{name}/schema %{buildroot}/%{_datadir}/%{name}/tests
find %{buildroot}/%{_datadir}/%{name}/tests -type f -name '*.conf' -exec perl -pi -e 's,\.\.\/servers\/slapd\/back-.*,%{_libdir}/%{name},g;s,\.\.\/servers\/slapd\/overlays,%{_libdir}/%{name},g' {} \;
perl -pi -e 's,(\`pwd\`\/)?\.\.\/servers\/(slapd|slurpd)\/(slapd|slurpd),%{_sbindir}/${2}%{ol_major},g;s,^PROGDIR=.*,PROGDIR=%{_bindir},g;s,^CLIENTDIR=.*,CLIENTDIR=%{_bindir},g;s,^TESTDIR=.*,TESTDIR=\${USER_TESTDIR-\$TMPDIR/openldap-testrun},g;s,^SHTOOL=.*,. scripts/defines.sh,g;s/ldap(search|add|delete|modify|whoami|compare|passwd)/ldap${1}%{ol_major}/g' %{buildroot}/%{_datadir}/%{name}/tests/scripts/defines.sh %{buildroot}/%{_datadir}/%{name}/tests/run
perl -pi -e 's/testrun/\$TESTDIR/g;s,^SHTOOL=.*,. scripts/defines.sh,g' %{buildroot}/%{_datadir}/%{name}/tests/scripts/all
perl -pi -e 's/^(Makefile|SUBDIRS)/#$1/g' %{buildroot}/%{_datadir}/%{name}/tests/Makefile
echo 'SHTOOL="./scripts/shtool"' >> %{buildroot}/%{_datadir}/%{name}/tests/scripts/defines.sh
install -m755 build/shtool %{buildroot}/%{_datadir}/%{name}/tests/scripts

install -m755 tests/progs/.libs/slapd-* %{buildroot}/%{_bindir}

### some hack
perl -pi -e "s| -L../liblber/.libs||g" %{buildroot}%{_libdir}/libldap.la

perl -pi -e  "s,-L$RPM_BUILD_DIR\S+%{_libdir},,g" %{buildroot}/%{_libdir}/lib*.la
#sed -i -e "s|-L$RPM_BUILD_DIR/%{name}-%{version}/db-instroot/%{_libdir}||g" %{buildroot}/%{_libdir}/*la
#%{buildroot}/%{_libdir}/%{name}/*.la 

### Init scripts
install -d %{buildroot}%{_initrddir}
install -m 755 %{SOURCE1} %{buildroot}%{_initrddir}/ldap%{ol_major}

install -d %{buildroot}%{_sysconfdir}/sysconfig
install -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/sysconfig/ldap%{ol_major}

install -m 640 %{SOURCE21} %{SOURCE23} %{SOURCE24} %{buildroot}%{_sysconfdir}/%{name}
#install -d %{_buildroot}/%{_sysconfdir}/%{name}/slapd.d

### repository dir
install -d %{buildroot}%{_var}/lib/ldap%{ol_major}

### DB_CONFIG for bdb backend
install -m644 %{SOURCE22} %{buildroot}%{_var}/lib/ldap%{ol_major}

### run dir
install -d %{buildroot}%{_var}/run/ldap%{ol_major}

### Server defaults
echo "localhost" > %{buildroot}%{_sysconfdir}/%{name}/ldapserver

### we don't need the default files 
rm -f %{buildroot}/etc/%{name}/*.default 
rm -f %{buildroot}/etc/%{name}/schema/*.default 


### Standard schemas should not be changed by users
install -d %{buildroot}%{_datadir}/%{name}/schema
mv -f %{buildroot}%{_sysconfdir}/%{name}/schema/* %{buildroot}%{_datadir}/%{name}/schema/

### install additional schemas
for i in %{SOURCE50} %{SOURCE51} %{SOURCE52} %{SOURCE53} %{SOURCE54} \
	%{SOURCE55} %{SOURCE56} %{SOURCE57} %{SOURCE58} %{SOURCE59} \
	%{SOURCE60} %{SOURCE61} %{SOURCE62} %{SOURCE63} %{SOURCE64} \
	%{SOURCE65} %{SOURCE66} %{SOURCE67} %{SOURCE68}; do
install -m 644 $i %{buildroot}%{_datadir}/%{name}/schema/
done

install -d %{buildroot}/%{_datadir}/%{name}/scripts
install -m 755 %{SOURCE25} %{SOURCE26} %{SOURCE27} %{buildroot}/%{_datadir}/%{name}/scripts/
for i in hourly daily weekly monthly yearly
do
	install -d %{buildroot}/%{_sysconfdir}/cron.${i}
	ln -s %{_datadir}/%{name}/scripts/ldap-hot-db-backup %{buildroot}/%{_sysconfdir}/cron.${i}/ldap-hot-db-backup%{ol_major}
done

### create local.schema
echo "# This is a good place to put your schema definitions " > %{buildroot}%{_sysconfdir}/%{name}/schema/local.schema
chmod 644 %{buildroot}%{_sysconfdir}/%{name}/schema/local.schema

### deal with the migration tools
%if %build_migration
install -d %{buildroot}%{_datadir}/%{name}/migration
install -m 755 MigrationTools-%{migtools_ver}/{*.pl,*.sh,*.txt,*.ph} %{buildroot}%{_datadir}/%{name}/migration
install -m 644 MigrationTools-%{migtools_ver}/README %{SOURCE3} %{buildroot}%{_datadir}/%{name}/migration
install -m 755 %{SOURCE4} %{buildroot}%{_datadir}/%{name}/migration

cp MigrationTools-%{migtools_ver}/README README.migration
cp %{SOURCE3} TOOLS.migration
%endif

### Guide
mkdir -p %{buildroot}/%{_docdir}/
tar xvjf %{SOURCE12} -C %{buildroot}/%{_docdir}/
mv %{buildroot}/%{_docdir}/{%{pkg_name},%{name}}-guide ||:

### gencert.sh
install -m 755 %{SOURCE19} %{buildroot}/%{_datadir}/%{name}

### log repository
install -m 700 -d %{buildroot}/var/log/ldap%{ol_major}
install -d %{buildroot}%{_sysconfdir}/logrotate.d
install -m 644 %{SOURCE20} %{buildroot}%{_sysconfdir}/logrotate.d/ldap%{ol_major}


# get the buildroot out of the man pages
perl -pi -e "s|%{buildroot}||g" %{buildroot}%{_mandir}/*/*.*

mkdir -p %{buildroot}%{_sysconfdir}/ssl/%{name}

#rename binaries
%if !%{build_system} || %build_alternatives
for OLD in %{buildroot}/%{_bindir}/{%{clientbin}}
do
    NEW=`echo ${OLD}%{alternative_major}`
    mv -f $OLD $NEW ||:
    if [ -L $NEW ]
    then ln -sf `readlink $NEW`%{alternative_major} $NEW
    fi
done
for OLD in %{buildroot}/%{_mandir}/man?/{%{clientbin},ldap.conf,ldif}*
do
    if [ -e $OLD ]
    then
        BASE=`perl -e '$_="'${OLD}'"; m,(%buildroot)(.*?)(\.[0-9]),;print "$1$2\n";'`
        EXT=`echo $OLD|sed -e 's,'${BASE}',,g'`
        NEW=`echo ${BASE}%{alternative_major}${EXT}`
        mv $OLD $NEW
    fi
done
%endif
%if !%build_system
for OLD in %{buildroot}/%{_bindir}/{%{serverbin}} %{buildroot}/%{_sbindir}/{%{serversbin}}
do
    NEW=`echo ${OLD}%{ol_major}`
    mv $OLD $NEW -f ||:
    if [ -L $NEW ]
        then ln -sf `readlink $NEW`%{ol_major} $NEW
    fi
done
# And the man pages too:
%if %db4_internal
for OLD in %{buildroot}/%{_mandir}/man?/{%{serverbin},%{serversbin},slapo}*
%else
for OLD in %{buildroot}/%{_mandir}/man?/{%{serversbin},slapo}*
%endif
do
    if [ -e $OLD ]
    then
        BASE=`perl -e '$_="'${OLD}'"; m,(%buildroot)(.*?)(\.[0-9]),;print "$1$2\n";'`
#        BASE=`perl -e '$name="'${OLD}'"; print "",($name =~ /(.*?)\.[0-9]/), "\n";'`
	EXT=`echo $OLD|sed -e 's,'${BASE}',,g'`
	NEW=`echo ${BASE}%{ol_major}${EXT}`
	mv $OLD $NEW
    fi
done
%endif

#Fix binary names and config paths in scripts/configs
perl -pi -e 's,/%{pkg_name}/,/%{name}/,g;s,(/ldap\w?)\b,${1}%{ol_major},g;s,(%{_bindir}/slapd_db_\w+),${1}%{ol_major},g;s,(%{_sbindir}/sl(apd|urpd|aptest))\b,${1}%{ol_major},g;s/ldap%{ol_major}-common/ldap-common/g;s,ldap%{ol_major}.pem,ldap.pem,g;s,/usr/lib,%{_libdir},g' %{buildroot}/{%{_sysconfdir}/%{name}/slapd.conf,%{_initrddir}/ldap%{ol_major},%{_datadir}/%{name}/scripts/*}
perl -pi -e 's/ldap/ldap%{ol_major}/' %{buildroot}/%{_sysconfdir}/logrotate.d/ldap%{ol_major}

mv %{buildroot}/var/run/ldap%{ol_major}/openldap-data/DB_CONFIG.example %{buildroot}/%{_var}/lib/ldap%{ol_major}/

%clean 
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}
#rm -rf $RPM_BUILD_DIR/%{name}-%{version}


%pre servers
%_pre_useradd ldap %{_var}/lib/ldap /bin/false
# allowing slapd to read hosts.allow and hosts.deny
%{_bindir}/gpasswd -a ldap adm 1>&2 > /dev/null || :

%if build_system
LDAPUSER=ldap
LDAPGROUP=ldap
[ -e "/etc/sysconfig/%{name}" ] && . "/etc/sysconfig/%{name}"
SLAPDCONF=${SLAPDCONF:-/etc/%{name}/slapd.conf}

#decide whether we need to migrate at all:
MIGRATE=`%{_sbindir}/slapd%{ol_major} -VV 2>&1|while read a b c d e;do case $d in (2.4.*) echo nomigrate;;(2.*) echo migrate;;esac;done`

if [ "$1" -ne 1 -a -e "$SLAPDCONF" -a "$MIGRATE" != "nomigrate" ]
then 
SLAPD_STATUS=`LANG=C LC_ALL=C NOLOCALE=1 service ldap%{ol_major} status 2>/dev/null|grep -q stopped;echo $?`
[ $SLAPD_STATUS -eq 1 ] && service ldap%{ol_major} stop
#`awk '/^[:space:]*directory[:space:]*\w*/ {print $2}' /etc/%{name}/slapd.conf`
dbs=`awk 'BEGIN {OFS=":"} /[:space:]*^database[:space:]*\w*/ {db=$2;suf="";dir=""}; /^[:space:]*suffix[:space:]*\w*/ {suf=$2;if((db=="bdb"||db=="ldbm"||db=="hdb")&&(suf!=""&&dir!="")) print dir,suf};/^[:space:]*directory[:space:]*\w*/ {dir=$2; if((db=="bdb"||db=="ldbm"||db="hdb")&&(suf!=""&&dir!="")) print dir,suf};' "$SLAPDCONF" $(awk  '/^[[:blank:]]*include[[:blank:]]*/ {print $2}' "$SLAPDCONF")|sed -e 's/"//g'`
for db in $dbs
do
	dbdir=${db/:*/}
	dbsuffix=${db/*:/}
	[ -e /etc/sysconfig/ldap%{ol_major} ] && . /etc/sysconfig/ldap%{ol_major}
# data migration between incompatible versions
# openldap >= 2.2.x have slapcat as a link to slapd, older releases do not
	if [ "${AUTOMIGRATE:-yes}" == "yes" -a -f %{_sbindir}/slapcat ]
	then
		ldiffile="rpm-migrate-to-%{ol_ver_major}.ldif"
		# dont do backups more than onc
		if [ ! -e "${dbdir}/${ldiffile}-imported" -a ! -e "${dbdir}/${ldiffile}-import-failed" ];then
		echo "Migrating pre-OpenLDAP-%{ol_ver_major} data"
		echo "Making a backup of $dbsuffix to ldif file ${dbdir}/$ldiffile"
		# For some reason, slapcat works in the shell when slapd is
		# running but not via rpm ...
		slapcat -b "$dbsuffix" -l ${dbdir}/${ldiffile} ||:
		fi
	fi
done
[ $SLAPD_STATUS -eq 1 ] && service ldap%{ol_major} start || :
fi
%endif

%post servers
/sbin/ldconfig
SLAPD_STATUS=`LANG=C LC_ALL=C NOLOCALE=1 service ldap%{ol_major} status 2>/dev/null|grep -q stopped;echo $?`
[ $SLAPD_STATUS -eq 1 ] && service ldap%{ol_major} stop
# bgmilne: part 2 of gdbm->dbb conversion for data created with 
# original package for 9.1:
dbnum=1
LDAPUSER=ldap
LDAPGROUP=ldap
[ -e "/etc/sysconfig/%{name}" ] && . "/etc/sysconfig/%{name}"
SLAPDCONF=${SLAPDCONF:-/etc/%{name}/slapd.conf}
if [ -e "$SLAPDCONF" ] 
then
dbs=`awk 'BEGIN {OFS=":"} /[:space:]*^database[:space:]*\w*/ {db=$2;suf="";dir=""}; /^[:space:]*suffix[:space:]*\w*/ {suf=$2;if((db=="bdb"||db=="ldbm")&&(suf!=""&&dir!="")) print dir,suf};/^[:space:]*directory[:space:]*\w*/ {dir=$2; if((db=="bdb"||db=="ldbm")&&(suf!=""&&dir!="")) print dir,suf};' "$SLAPDCONF" $(awk  '/^[[:blank:]]*include[[:blank:]]*/ {print $2}' "$SLAPDCONF")|sed -e 's/"//g'`
for db in $dbs
do	
	dbdir=${db/:*/}
	dbsuffix=${db/*:/}
	ldiffile="rpm-migrate-to-%{ol_ver_major}.ldif"
	if [ -e "${dbdir}/${ldiffile}" ]
	then
		echo -e "\n\nImporting $dbsuffix"
		if [ -e ${dbdir}/ldap-rpm-backup ]
		then 
			echo "Warning: Old ldap backup data in ${dbdir}/ldap-rpm-backup"
			echo "These files will be removed"
			rm -f ${dbdir}/ldap-rpm-backup/*
		fi
	
		echo "Moving the database files fom ${dbdir} to ${dbdir}/ldap-rpm-backup"
		mkdir -p ${dbdir}/ldap-rpm-backup
		mv -f ${dbdir}/{*.bdb,*.gdbm,*.dbb,log.*,__db*} ${dbdir}/ldap-rpm-backup 2>/dev/null
		echo "Importing $dbsuffix from ${dbdir}/${ldiffile}"
		if slapadd%{ol_major} -q -cv -b "$dbsuffix" -l ${dbdir}/${ldiffile} > \
		${dbdir}/rpm-ldif-import.log 2>&1
		then
			mv -f ${dbdir}/${ldiffile} ${dbdir}/${ldiffile}-imported
			echo "Import complete, see log ${dbdir}/rpm-ldif-import.log"
			echo "If any entries were not migrated, see ${dbdir}/${ldiffile}-imported"
		else
			mv -f ${dbdir}/${ldiffile} ${dbdir}/${ldiffile}-import-failed
			echo "Import failed on ${dbdir}/${ldifffile}, see ${dbdir}/rpm-ldif-import.log"
			echo "An ldif dump of $dbsuffix has been saved as ${dbdir}/${ldiffile}-import-failed"
			echo -e "\nYou can import it manually by running (as root):"
			echo "# service ldap%{ol_major} stop"
			echo "# slapadd%{ol_major} -c -l ${dbdir}/${ldiffile}-import-failed"
			echo "# chown $LDAPUSER:$LDAPGROUP ${dbdir}/*"
			echo "# service ldap%{ol_major} start"
		fi
	fi

	chown ${LDAPUSER}:${LDAPGROUP} -R ${dbdir}
	# openldap-2.0.x->2.1.x on ldbm/dbb backend seems to need reindex regardless:
	#slapindex -n $dbnum
	#dbnum=$[dbnum+1]
done
fi
[ $SLAPD_STATUS -eq 1 ] && service ldap%{ol_major} start

# Setup log facility for OpenLDAP on new install
if [ -f %{_sysconfdir}/syslog.conf -a $1 -eq 1 ]
then
	# clean syslog
	perl -pi -e "s|^.*ldap%{ol_major}.*\n||g" %{_sysconfdir}/syslog.conf 

	# probe free local-users
	cntlog=""
	for log in 7 6 5 3 2 1 0 4
	do 
		grep -vE "local${log}[^;]*\.none" %{_sysconfdir}/syslog.conf|grep -q local${log} || cntlog="${log}"
	done

	if [ "${cntlog}" != "" ];then
		echo "# added by %{name}-%{version} rpm $(date)" >> %{_sysconfdir}/syslog.conf
#   modified by Oden Eriksson
#		echo "local${cntlog}.*       /var/log/ldap/ldap.log" >> %{_sysconfdir}/syslog.conf
		echo -e "local${cntlog}.*\t\t\t\t\t\t\t-/var/log/ldap%{ol_major}/ldap.log" >> %{_sysconfdir}/syslog.conf

		# reset syslog daemon
		if [ -f /var/lock/subsys/syslog ]; then
        		service syslog restart  > /dev/null 2>/dev/null || : 
		fi
	else
		echo "I can't set syslog local-user!"
	fi
		
	# set syslog local-user in /etc/sysconfig/ldap
	perl -pi -e "s|^.*SLAPDSYSLOGLOCALUSER.*|SLAPDSYSLOGLOCALUSER=\"LOCAL${cntlog}\"|g" %{_sysconfdir}/sysconfig/ldap%{ol_major}

fi

# generate the ldap.pem cert here instead of the initscript
if [ ! -e %{_sysconfdir}/ssl/%{name}/ldap.pem ] ; then
  if [ -x %{_datadir}/%{name}/gencert.sh ] ; then
    echo "Generating self-signed certificate..."
    pushd %{_sysconfdir}/ssl/%{name}/ > /dev/null
    yes ""|%{_datadir}/%{name}/gencert.sh >/dev/null 2>&1
    chmod 640 ldap.pem
    chown root:ldap ldap.pem
    popd > /dev/null
  fi
  echo "To generate a self-signed certificate, you can use the utility"
  echo "%{_datadir}/%{name}/gencert.sh..."
fi

pushd %{_sysconfdir}/%{name}/ > /dev/null
for i in slapd.conf slapd.access.conf ; do
	if [ -f $i ]; then
		chmod 0640 $i
		chown root:ldap $i
	fi
done
popd > /dev/null


%_post_service ldap%{ol_major}

# nscd reset
if [ -f /var/lock/subsys/nscd ]; then
        service nscd restart  > /dev/null 2>/dev/null || : 
fi


%preun servers
%_preun_service ldap%{ol_major}


%postun servers
/sbin/ldconfig
if [ $1 = 0 ]; then 
	# remove ldap entry 
	perl -pi -e "s|^.*ldap.*\n||g" %{_sysconfdir}/syslog.conf 

	# reset syslog daemon
	if [ -f /var/lock/subsys/syslog ]; then
	        service syslog restart  > /dev/null 2>/dev/null || : 
	fi
fi
%_postun_userdel ldap


%post -n %{libname} -p /sbin/ldconfig
%postun -n %{libname} -p /sbin/ldconfig

%triggerpostun -- openldap-clients < 2.1.25-5mdk
# We may have openldap client configuration in /etc/ldap.conf
# which now needs to be in /etc/openldap/ldap.conf
if [ -f /etc/ldap.conf ] 
then
	mv -f /etc/%{name}/ldap.conf /etc/%{name}/ldap.conf.rpmfix
	cp -af /etc/ldap.conf /etc/%{name}/ldap.conf
fi

%files
%defattr(-,root,root)
%config(noreplace) %{_sysconfdir}/%{name}/ldapserver
%attr(644,root,root) %config(noreplace) %{_sysconfdir}/%{name}/ldap.conf
%{_mandir}/man5/ldap.conf%{ol_major}.5*
%{_mandir}/man5/ldif%{ol_major}.5*
%doc README.mdk


%files doc
%defattr(-,root,root)
%doc ANNOUNCEMENT CHANGES COPYRIGHT LICENSE README 
%if %build_migration
%doc README.migration TOOLS.migration
%endif
%doc doc/rfc doc/drafts
#%config(noreplace) %{_sysconfdir}/%{name}/ldapfilter.conf
#%config(noreplace) %{_sysconfdir}/%{name}/ldapsearchprefs.conf
#%config(noreplace) %{_sysconfdir}/%{name}/ldaptemplates.conf
#%{_datadir}/%{name}/ldapfriendly
#%{_mandir}/man5/ldapfilter.conf.5*
#%{_mandir}/man5/ldapfriendly.5*
#%{_mandir}/man5/ldapsearchprefs.conf.5*
#%{_mandir}/man5/ldaptemplates.conf.5*
%doc %{_docdir}/%{name}-guide

%if %build_migration
%files migration
%defattr(-,root,root)
%{_datadir}/%{name}/migration
%endif


%files servers
%defattr(-,root,root)
%dir %{_sysconfdir}/%{name}
%dir %{_sysconfdir}/%{name}/schema
#%dir %{_sysconfdir}/%{name}/slapd.d
#%attr(640,root,ldap) %config(noreplace) %{_sysconfdir}/ssl/openldap/ldap.pem
%attr(640,root,ldap) %config(noreplace) %{_sysconfdir}/%{name}/slapd.conf
%attr(640,root,ldap) %{_sysconfdir}/%{name}/DB_CONFIG.example
%attr(640,root,ldap) %config %{_sysconfdir}/%{name}/slapd.access.conf

%dir %{_sysconfdir}/ssl/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/schema/*.schema
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/schema
%{_datadir}/%{name}/schema/*.schema
%{_datadir}/%{name}/schema/*.ldif
%{_datadir}/%{name}/schema/README
#%dir %{_datadir}/%{name}/ucdata
#%{_datadir}/%{name}/ucdata/*.dat
%{_datadir}/%{name}/scripts
%{_sysconfdir}/cron.hourly/ldap-hot-db-backup%{ol_major}
%{_sysconfdir}/cron.daily/ldap-hot-db-backup%{ol_major}
%{_sysconfdir}/cron.weekly/ldap-hot-db-backup%{ol_major}
%{_sysconfdir}/cron.monthly/ldap-hot-db-backup%{ol_major}
%{_sysconfdir}/cron.yearly/ldap-hot-db-backup%{ol_major}

%config(noreplace) %{_sysconfdir}/sysconfig/ldap%{ol_major}
%config(noreplace) %{_initrddir}/ldap%{ol_major}
%attr(750,ldap,ldap) %dir %{_var}/lib/ldap%{ol_major}
%config(noreplace) %{_var}/lib/ldap%{ol_major}/DB_CONFIG
%{_var}/lib/ldap%{ol_major}/DB_CONFIG.example
%attr(755,ldap,ldap) %dir /var/run/ldap%{ol_major}
#%{_datadir}/openldap/*.help
%{_datadir}/%{name}/gencert.sh
%{_sbindir}/*


%dir %{_libdir}/%{name}
%if %build_modules && !%build_modpacks
%{_libdir}/%{name}/*.la
%{_libdir}/%{name}/*.so*
#%exclude %{_libdir}/%{name}/*.a
%endif

%{_mandir}/man5/slap*.5*
%{_mandir}/man8/*

%attr(750,ldap,ldap) %dir /var/log/ldap%{ol_major}
%config(noreplace) %{_sysconfdir}/logrotate.d/ldap%{ol_major}

%if %db4_internal
#internal version of db4
%{_libdir}/libslapd%{ol_suffix}_db*
%attr(755,root,root)%{_bindir}/slapd_db*
%exclude %{_prefix}/docs
%exclude %{_includedir}/db*.h
%endif

%doc contrib/slapd-modules/smbk5pwd/README.smbk5passwd
%doc contrib/slapd-modules/passwd/README{,.passwd}
%doc contrib/slapd-modules/acl/README{,.acl}

%files clients
%defattr(-,root,root)
%{_bindir}/ldap*
%{_mandir}/man1/*
#%{_mandir}/man5/ud.conf.5*

%files -n %libname
%defattr(-,root,root)
%{_libdir}/lib*.so.*


%files -n %libname-devel
%defattr(-,root,root)
%{_libdir}/libl*.so
%{_libdir}/libl*.la
%{_includedir}/l*.h
%{_includedir}/s*.h
%{_mandir}/man3/*

%files -n %libname-static-devel
%defattr(-,root,root)
%{_libdir}/lib*.a

%if %build_modpacks
%files back_dnssrv
%defattr(-,root,root)
%{_libdir}/%{name}/back_dnssrv.la
%{_libdir}/%{name}/back_dnssrv*.so.*
%{_libdir}/%{name}/back_dnssrv*.so

%files back_ldap
%defattr(-,root,root)
%{_libdir}/%{name}/back_ldap.la
%{_libdir}/%{name}/back_ldap*.so.*
%{_libdir}/%{name}/back_ldap*.so

%files back_passwd
%defattr(-,root,root)
%{_libdir}/%{name}/back_passwd.la
%{_libdir}/%{name}/back_passwd*.so.*
%{_libdir}/%{name}/back_passwd*.so
%endif #build_modpacks

%if %sql && %build_modpacks
%files back_sql
%defattr(-,root,root)
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/back_sql.la
%{_libdir}/%{name}/back_sql.a
%{_libdir}/%{name}/back_sql*.so.*
%{_libdir}/%{name}/back_sql*.so
%endif

%files tests
%defattr(-,root,root)
%{_datadir}/%{name}/tests

%files testprogs
%defattr(-,root,root)
%{_bindir}/slapd-*
#
# Todo:
# - add cron-job to remove transaction logs (bdb)


