Summary: An utility for manipulating storage encryption keys and passphrases
Name: volume_key
Version: 0.3.9
Release: 1
License: GPLv2
Group: Applications/System
URL: https://pagure.io/volume_key/
Requires: volume_key-libs = %{version}-%{release}

Source0: %{name}-%{version}.tar.gz
# Upstream commit 04991fe8c4f77c4e5c7874c2db8ca32fb4655f6e
Patch1: volume_key-0.3.9-fips-crash.patch
# Upstream commit 8f8698aba19b501f01285e9eec5c18231fc6bcea
Patch2: volume_key-0.3.9-config.h.patch
# Upstream commit ecef526a51c5a276681472fd6df239570c9ce518
Patch3: volume_key-0.3.9-crypt_get_error.patch
Patch4: 0001-Drop-Python.patch
BuildRequires: pkgconfig(libcryptsetup) >= 1.4.0
BuildRequires: pkgconfig(glib-2.0)
BuildRequires: pkgconfig(nss)
BuildRequires: gettext-devel
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
BuildRequires: gnupg2
BuildRequires: gpgme-devel
BuildRequires: libblkid-devel
BuildRequires: swig

%description
This package provides a command-line tool for manipulating storage volume
encryption keys and storing them separately from volumes.

The main goal of the software is to allow restoring access to an encrypted
hard drive if the primary user forgets the passphrase.  The encryption key
back up can also be useful for extracting data after a hardware or software
failure that corrupts the header of the encrypted volume, or to access the
company data after an employee leaves abruptly.

%package devel
Summary: A library for manipulating storage encryption keys and passphrases
Group: Development/Libraries
Requires: volume_key-libs = %{version}-%{release}

%description devel
This package provides libvolume_key, a library for manipulating storage volume
encryption keys and storing them separately from volumes.

The main goal of the software is to allow restoring access to an encrypted
hard drive if the primary user forgets the passphrase.  The encryption key
back up can also be useful for extracting data after a hardware or software
failure that corrupts the header of the encrypted volume, or to access the
company data after an employee leaves abruptly.

%package libs
Summary: A library for manipulating storage encryption keys and passphrases
Group: System Environment/Libraries
Requires: gnupg2

%description libs
This package provides libvolume_key, a library for manipulating storage volume
encryption keys and storing them separately from volumes.

The main goal of the software is to allow restoring access to an encrypted
hard drive if the primary user forgets the passphrase.  The encryption key
back up can also be useful for extracting data after a hardware or software
failure that corrupts the header of the encrypted volume, or to access the
company data after an employee leaves abruptly.

%prep
%setup -q -n %{name}-%{version}/%{name}

%patch1 -p1 -b .fips-crash
%patch2 -p1 -b .config.h
%patch3 -p1 -b .crypt_get_error
%patch4 -p1 -b .drop_python

%build
autoreconf -vfi
%configure
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL='install -p'

%find_lang volume_key

%clean
rm -rf $RPM_BUILD_ROOT

%post libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc README contrib
%{_bindir}/volume_key
%{_mandir}/man8/volume_key.8*

%files devel
%defattr(-,root,root,-)
%doc COPYING ChangeLog NEWS
%{_includedir}/volume_key
%exclude %{_libdir}/libvolume_key.la
%{_libdir}/libvolume_key.so

%files libs -f volume_key.lang
%defattr(-,root,root,-)
%doc AUTHORS
%{_libdir}/libvolume_key.so.*

