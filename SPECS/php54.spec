%global scl_name_base    php
%global scl_name_version 54
%global scl              %{scl_name_base}%{scl_name_version}
%scl_package %scl

# do not produce empty debuginfo package
%global debug_package %{nil}

Summary:       Package that installs PHP 5.4
Name:          %scl_name
Version:       1.1
Release:       6%{?dist}
Group:         Development/Languages
License:       GPLv2+

Source0:       macros-build
Source1:       README
Source2:       LICENSE

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: scl-utils-build
BuildRequires: help2man
# Temporary work-around
BuildRequires: iso-codes

Requires:      %{?scl_prefix}php-common
Requires:      %{?scl_prefix}php-cli
Requires:      %{?scl_prefix}php-pear

%description
This is the main package for %scl Software Collection,
that install PHP 5.4 language.


%package runtime
Summary:   Package that handles %scl Software Collection.
Group:     Development/Languages
Requires:  scl-utils

%description runtime
Package shipping essential scripts to work with %scl Software Collection.


%package build
Summary:   Package shipping basic build configuration
Group:     Development/Languages
Requires:  scl-utils-build

%description build
Package shipping essential configuration macros
to build %scl Software Collection.


%package scldevel
Summary:   Package shipping development files for %scl
Group:     Development/Languages

%description scldevel
Package shipping development files, especially usefull for development of
packages depending on %scl Software Collection.


%prep
%setup -c -T

cat <<EOF | tee enable
export PATH=%{_bindir}:%{_sbindir}\${PATH:+:\${PATH}}
export MANPATH=%{_mandir}:\${MANPATH}
EOF

# generate rpm macros file for depended collections
cat << EOF | tee scldev
%%scl_%{scl_name_base}         %{scl}
%%scl_prefix_%{scl_name_base}  %{scl_prefix}
EOF

# This section generates README file from a template and creates man page
# from that file, expanding RPM macros in the template file.
cat >README <<'EOF'
%{expand:%(cat %{SOURCE1})}
EOF

# copy the license file so %%files section sees it
cp %{SOURCE2} .


%build
# generate a helper script that will be used by help2man
cat >h2m_helper <<'EOF'
#!/bin/bash
[ "$1" == "--version" ] && echo "%{scl_name} %{version} Software Collection" || cat README
EOF
chmod a+x h2m_helper

# generate the man page
help2man -N --section 7 ./h2m_helper -o %{scl_name}.7


%install
install -D -m 644 enable %{buildroot}%{_scl_scripts}/enable
install -D -m 644 scldev %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel
install -D -m 644 %{scl_name}.7 %{buildroot}%{_mandir}/man7/%{scl_name}.7

%scl_install

# Add the scl_package_override macro
sed -e 's/@SCL@/%{scl}/g' %{SOURCE0} \
  | tee -a %{buildroot}%{_root_sysconfdir}/rpm/macros.%{scl}-config


%files


%files runtime
%defattr(-,root,root)
%doc README LICENSE
%scl_files
%{_mandir}/man7/%{scl_name}.*


%files build
%defattr(-,root,root)
%{_root_sysconfdir}/rpm/macros.%{scl}-config


%files scldevel
%defattr(-,root,root)
%{_root_sysconfdir}/rpm/macros.%{scl_name_base}-scldevel


%changelog
* Mon Mar 31 2014 Honza Horak <hhorak@redhat.com> - 1.1-6
- Fix path typo in README
  Related: #1061454

* Mon Mar 24 2014 Remi Collet <rcollet@redhat.com> 1.1-5
- own man directories, #1074012

* Wed Feb 12 2014 Remi Collet <rcollet@redhat.com> 1.1-4
- avoid empty debuginfo subpackage
- add LICENSE, README and php54.7 man page #1061454
- add scldevel subpackage #1063356

* Mon Jan 20 2014 Remi Collet <rcollet@redhat.com> 1.1-3
- rebuild with latest scl-utils #1054728

* Tue Sep 24 2013 Remi Collet <rcollet@redhat.com> 1.1-1
- add scl_package_override to macros.php54-config

* Fri May 24 2013 Remi Collet <rcollet@redhat.com> 1-7
- Really fix MANPATH variable definition (#966390)

* Thu May 23 2013 Remi Collet <rcollet@redhat.com> 1-6
- Fix MANPATH variable definition (#966390)

* Fri May  3 2013 Remi Collet <rcollet@redhat.com> 1-5
- Fix PATH variable definition (#957204)
- meta package requires php-cli and php-pear

* Mon Apr 29 2013 Remi Collet <rcollet@redhat.com> 1-4
- Fix LIBRARY_PATH variabls definition (#957204)

* Wed Apr 10 2013 Remi Collet <rcollet@redhat.com> 1-3
- drop unneeded LD_LIBRARY_PATH

* Tue Oct 23 2012 Remi Collet <rcollet@redhat.com> 1-2
- EL-5 compatibility (buildroot, ...)

* Fri Sep 28 2012 Remi Collet <rcollet@redhat.com> 1-1
- initial packaging
