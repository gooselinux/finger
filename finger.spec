Summary: The finger client
Name: finger
Version: 0.17
Release: 39%{?dist}
License: BSD
Group: Applications/Internet
Source: ftp://ftp.uk.linux.org/pub/linux/Networking/netkit/bsd-finger-%{version}.tar.gz
Source1: finger-xinetd
Patch1: bsd-finger-0.16-pts.patch
Patch2: bsd-finger-0.17-exact.patch
Patch3: bsd-finger-0.16-allocbroken.patch
Patch4: bsd-finger-0.17-rfc742.patch
Patch5: bsd-finger-0.17-time.patch
Patch6: bsd-finger-0.17-usagi-ipv6.patch
Patch7: bsd-finger-0.17-typo.patch
Patch8: bsd-finger-0.17-strip.patch
Patch9: bsd-finger-0.17-utmp.patch
Patch10: bsd-finger-wide-char-support5.patch
Patch11: bsd-finger-0.17-init-realname.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: glibc-devel

%description
Finger is a utility which allows users to see information about system
users (login name, home directory, name, how long they've been logged
in to the system, etc.).  The finger package includes a standard
finger client.

You should install finger if you'd like to retrieve finger information
from other systems.

%package server
Summary: The finger daemon
Group: System Environment/Daemons
Requires: xinetd

%description server
Finger is a utility which allows users to see information about system
users (login name, home directory, name, how long they've been logged
in to the system, etc.).  The finger-server package includes a standard
finger server. The server daemon (fingerd) runs from /etc/inetd.conf,
which must be modified to disable finger requests.

You should install finger-server if your system is used by multiple users
and you'd like finger information to be available.

%prep
%setup -q -n bsd-finger-%{version}
%patch1 -p1 -b .pts
%patch2 -p1 -b .exact
%patch3 -p1
%patch4 -p1 -b .rfc742
%patch5 -p1 -b .time
%patch6 -p1 -b .ipv6
%patch7 -p1 -b .typo
%patch8 -p1 -b .strip
%patch9 -p1 -b .utmp
%patch10 -p1 -b .widechar
%patch11 -p1 

%build
sh configure --enable-ipv6
perl -pi -e '
	s,^CC=.*$,CC=cc,;
	s,-O2,-fPIC \$(RPM_OPT_FLAGS),;
	s,^BINDIR=.*$,BINDIR=%{_bindir},;
	s,^MANDIR=.*$,MANDIR=%{_mandir},;
	s,^SBINDIR=.*$,SBINDIR=%{_sbindir},;
	s,^LDFLAGS=.*$,LDFLAGS=-pie,;
	' MCONFIG

make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_mandir}/man{1,8}
mkdir -p ${RPM_BUILD_ROOT}%{_sbindir}

mkdir -p ${RPM_BUILD_ROOT}/etc/xinetd.d
install -m 644 %SOURCE1 ${RPM_BUILD_ROOT}/etc/xinetd.d/finger

make INSTALLROOT=${RPM_BUILD_ROOT} install

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%attr(0755,root,root)	%{_bindir}/finger
%{_mandir}/man1/finger.1*

%files server
%defattr(-,root,root)
%config(noreplace) /etc/xinetd.d/finger
%attr(0755,root,root)	%{_sbindir}/in.fingerd
%{_mandir}/man8/in.fingerd.8*
%{_mandir}/man8/fingerd.8*

%changelog
* Mon Sep  7 2009 Radek Vokal <rvokal@redhat.com> - 0.17-39
- init realname fix (#520203)

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-38
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.17-37
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Feb 19 2008 Fedora Release Engineering <rel-eng@fedoraproject.org> - 0.17-36
- Autorebuild for GCC 4.3

* Thu Aug 23 2007 Radek Vokál <rvokal@redhat.com> - 0.17-35
- rebuilt

* Sun Feb  4 2007 Radek Vokál <rvokal@redhat.com> - 0.17-34
- finger server permissions (#225754)

* Sun Feb  4 2007 Radek Vokál <rvokal@redhat.com> - 0.17-33
- spec files cleanups according to MergeReview (#225754)
- dist tag added

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.17-32.2.1.1
- rebuild

* Wed Jul 12 2006 Jesse Keating <jkeating@redhat.com> - 0.17-32.2.1
- rebuild

* Fri Feb 10 2006 Jesse Keating <jkeating@redhat.com> - 0.17-32.2
- bump again for double-long bug on ppc(64)

* Tue Feb 07 2006 Jesse Keating <jkeating@redhat.com> - 0.17-32.1
- rebuilt for new gcc4.1 snapshot and glibc changes

* Thu Dec 15 2005 Radek Vokal <rvokal@redhat.com> 0.17-32
- another UTF-8 fix

* Tue Dec 13 2005 Radek Vokal <rvokal@redhat.com> 0.17-31
- real UTF-8 patch by <bnocera@redhat.com>

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Mon Nov 28 2005 Radek Vokal <rvokal@redhat.com> 0.17-30
- make finger UTF-8 happy (#174352)

* Wed Jul 13 2005 Radek Vokal <rvokal@redhat.com> 0.17-29
- make finger world readable (#162643)

* Fri Mar 04 2005 Radek Vokal <rvokal@redhat.com> 0.17-28
- gcc4 rebuilt

* Wed Feb 09 2005 Radek Vokal <rvokal@redhat.com> 0.17-27
- rebuilt to get fortified

* Mon Sep 06 2004 Radek Vokal <rvokal@redhat.com> 0.17-26
- rebuilt

* Tue Jun 15 2004 Alan Cox <alan@redhat.com>
- Made finger agree with our other apps about how utmp is managed
- Removed dead users from the lists as a result
- Fixed random idle time bug

* Tue Jun 15 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Wed Feb 25 2004 Phil Knirsch <pknirsch@redhat.com> 0.17-21
- rebuilt
- Made fingerd PIE.

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Mon Sep 01 2003 Phil Knirsch <pknirsch@redhat.com> 0.17-18.1
- rebuilt

* Mon Sep 01 2003 Phil Knirsch <pknirsch@redhat.com> 0.17-18
- Fixed manpage bug (#75705).

* Wed Jun 04 2003 Elliot Lee <sopwith@redhat.com> 0.17-17
- rebuilt

* Wed Jan 22 2003 Tim Powers <timp@redhat.com> 0.17-16
- rebuilt

* Wed Dec 11 2002 Tim Powers <timp@redhat.com> 0.17-15
- rebuild on all arches

* Fri Jun 21 2002 Tim Powers <timp@redhat.com> 0.17-14
- automated rebuild

* Wed Jun 19 2002 Phil Knirsch <pknirsch@redhat.com> 0.17-13
- Don't forcibly strip binaries

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jan 24 2002 Phil Knirsch <pknirsch@redhat.com>
- Fixed various typos in manpage/app (#51891, #54916, #57588)

* Wed Jan 09 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Apr 18 2001 Crutcher Dunnavant <crutcher@redhat.com>
- Approved
- * Sun Mar 11 2001 Pekka Savola <pekkas@netcore.fi>
- - Add IPv6 support from USAGI, update to 0.17 final (no changes)

* Tue Feb 27 2001 Preston Brown <pbrown@redhat.com>
- noreplace xinetd.d config file

* Mon Feb 12 2001 Crutcher Dunnavant <crutcher@redhat.com>
- time patch to handle time.h moving, credit to howarth@fuse.net
- closes bug #26766

* Fri Dec  1 2000 Trond Eivind Glomsred <teg@redhat.com>
- make sure finger is turned off by default

* Sun Aug 27 2000 Nalin Dahyabhai <nalin@redhat.com>
- add patch to always call getpwnam() instead of just when -m is specified

* Sat Jul 22 2000 Jeff Johnson <jbj@redhat.com>
- fix RFC742 problem (again) (#6728).

* Tue Jul 18 2000 Bill Nottingham <notting@redhat.com>
- add description & default to xinetd file

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Sun Jun 18 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.
- update to 0.17.

* Wed May 31 2000 Cristian Gafton <gafton@redhat.com>
- fix the broken malloc code in finger client

* Mon May 22 2000 Trond Eivind Glomsred <teg@redhat.com>
- converted to use /etc/xinetd.d

* Tue May 16 2000 Chris Evans <chris@ferret.lmh.ox.ac.uk>
- make some files mode -rwx--x--x as a security hardening measure 

* Fri Feb 11 2000 Bill Nottingham <notting@redhat.com>
- fix description

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- handle compressed manpages

* Wed Feb 02 2000 Cristian Gafton <gafton@redhat.com>
- fix description
- man pages are compressed

* Tue Jan  4 2000 Bill Nottingham <notting@redhat.com>
- split client and server

* Tue Dec 21 1999 Jeff Johnson <jbj@redhat.com>
- update to 0.16.

* Wed Jul 28 1999 Jeff Johnson <jbj@redhat.com>
- exact match w/o -m and add missing pts patch (#2118).
- recompile with correct PATH_MAILDIR (#4218).

* Thu Apr  8 1999 Jeff Johnson <jbj@redhat.com>
- fix process table filled DOS attack (#1271)
- fix pts display problems (#1987 partially)

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 22)

* Mon Mar 15 1999 Jeff Johnson <jbj@redhat.com>
- compile for 6.0.

* Wed Aug 12 1998 Jeff Johnson <jbj@redhat.com>
- fix error message typo.

* Tue Aug 11 1998 Jeff Johnson <jbj@redhat.com>
- build root

* Mon Apr 27 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Mon Sep 22 1997 Erik Troan <ewt@redhat.com>
- added check for getpwnam() failure
