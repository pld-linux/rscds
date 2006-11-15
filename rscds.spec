Summary:	Really Simple CalDAV Store
Summary(pl):	Really Simple CalDAV Store - proste sk³adowisko CalDAV
Name:		rscds
Version:	0.2.2
Release:	1
License:	GPL
Group:		Applications/WWW
Source0:	http://dl.sourceforge.net/rscds/rscds_%{version}.tar.gz
# Source0-md5:	3a5efdd04db69d90d78cb7fde70b2a45
Source1:	%{name}-apache.conf
Source2:	%{name}-lighttpd.conf
URL:		http://rscds.sourceforge.net/
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	webapps
Requires:	php-awl
# see SOURCES/webapps.README for description and complete listing
#Requires:	webserver(access)
#Requires:	webserver(alias)
#Requires:	webserver(auth)
#Requires:	webserver(cgi)
#Requires:	webserver(indexfile)
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{name}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

%description
Really Simple CalDAV Store.

%description -l pl
Really Simple CalDAV Store - proste sk³adowisko CalDAV.

%prep
%setup -q -n %{name}
install %{SOURCE1} apache.conf
install %{SOURCE2} lighttpd.conf

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir},%{_appdir}}

#install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
install apache.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
install lighttpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/lighttpd.conf
cp -a config dba htdocs  inc $RPM_BUILD_ROOT%{_appdir}
mv $RPM_BUILD_ROOT%{_appdir}/config/config.php $RPM_BUILD_ROOT%{_sysconfdir}/config.php
ln -sf %{_sysconfdir}/config.php $RPM_BUILD_ROOT%{_appdir}/config/config.php

%clean
rm -rf $RPM_BUILD_ROOT

%triggerin -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%triggerin -- lighttpd
%webapp_register lighttpd %{_webapp}

%triggerun -- lighttpd
%webapp_unregister lighttpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc docs README INSTALL *.txt
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/lighttpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*.php
%{_appdir}
