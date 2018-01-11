# Define the kmod package name here.
%global	kmod_name nvidia

# If kversion isn't defined on the rpmbuild line, define it here. For Fedora,
# kversion needs always to be defined as there is no kABI support.

# RHEL 6.9
%if 0%{?rhel} == 6
%{!?kversion: %global kversion 2.6.32-696.el6.%{_target_cpu}}
%endif

# RHEL 7.4
%if 0%{?rhel} == 7
%{!?kversion: %global kversion 3.10.0-693.el7.%{_target_cpu}}
%endif

Name:           %{kmod_name}-kmod
Version:        384.111
Release:        1%{?dist}
Summary:        NVIDIA display driver kernel module
Epoch:          2
License:        NVIDIA License
URL:            http://www.nvidia.com/
ExclusiveArch:  %{ix86} x86_64

Source0:        %{kmod_name}-kmod-%{version}-i386.tar.xz
Source1:        %{kmod_name}-kmod-%{version}-x86_64.tar.xz
Source10:       kmodtool-%{kmod_name}-el6.sh

BuildRequires:  redhat-rpm-config
BuildRequires:  kernel-abi-whitelists

%if 0%{?rhel} == 6
BuildRequires:  module-init-tools
%else
BuildRequires:  kmod
%endif

# Magic hidden here.
%global kmodtool sh %{SOURCE10}
%{expand:%(%{kmodtool} rpmtemplate %{kmod_name} %{kversion} "" 2>/dev/null)}

# Disable building of the debug package(s).
%global	debug_package %{nil}

%description
This package provides the proprietary NVIDIA OpenGL kernel driver module.
It is built to depend upon the specific ABI provided by a range of releases of
the same variant of the Linux kernel and not on any one specific build.

%prep
%ifarch %{ix86}
%setup -q -n %{kmod_name}-kmod-%{version}-i386
%endif

%ifarch x86_64
%setup -q -T -b 1 -n %{kmod_name}-kmod-%{version}-x86_64
%endif

mv kernel/* .

echo "override %{kmod_name} * weak-updates/%{kmod_name}" > kmod-%{kmod_name}.conf

%build
export SYSSRC=%{_usrsrc}/kernels/%{kversion}
export IGNORE_XEN_PRESENCE=1
export IGNORE_PREEMPT_RT_PRESENCE=1
export IGNORE_CC_MISMATCH=1

make %{?_smp_mflags} module

%install
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=extra/%{kmod_name}
ksrc=%{_usrsrc}/kernels/%{kversion}
make -C "${ksrc}" modules_install M=$PWD

install -d %{buildroot}%{_sysconfdir}/depmod.d/
install kmod-%{kmod_name}.conf %{buildroot}%{_sysconfdir}/depmod.d/
# Remove the unrequired files.
rm -f %{buildroot}/lib/modules/%{kversion}/modules.*

%changelog
* Thu Jan 11 2018 Simone Caronni <negativo17@gmail.com> - 2:384.111-1
- Update to 384.111.

* Tue Nov 14 2017 Simone Caronni <negativo17@gmail.com> - 2:384.98-1
- Update to 384.98.

* Mon Oct 09 2017 Simone Caronni <negativo17@gmail.com> - 2:384.90-2
- Ignore mismatching GCC version when compiling, useful when the distribution is
  not yet released and compilers are being updated.

* Fri Sep 22 2017 Simone Caronni <negativo17@gmail.com> - 2:384.90-1
- Update to 384.90.

* Wed Aug 30 2017 Simone Caronni <negativo17@gmail.com> - 2:384.69-1
- Update to 384.69.

* Fri Aug 25 2017 Simone Caronni <negativo17@gmail.com> - 2:384.59-2
- Requires RHEL/CentOS 7.4 kernel.

* Wed Jul 26 2017 Simone Caronni <negativo17@gmail.com> - 2:384.59-1
- Update to 384.59.
- Instantiated module support is long gone.

* Thu May 11 2017 Simone Caronni <negativo17@gmail.com> - 2:375.66-2
- Add kernel 4.11 patch.

* Wed May 10 2017 Simone Caronni <negativo17@gmail.com> - 2:375.66-1
- Update to 375.66.

* Fri Apr 07 2017 Simone Caronni <negativo17@gmail.com> - 2:375.39-4
- Update RHEL 6.9 kernel version.

* Wed Mar 15 2017 Simone Caronni <negativo17@gmail.com> - 2:375.39-3
- Update kernel requirement for RHEL 7.

* Wed Mar 01 2017 Simone Caronni <negativo17@gmail.com> - 2:375.39-2
- Add kernel 4.10 patch.

* Wed Feb 15 2017 Simone Caronni <negativo17@gmail.com> - 2:375.39-1
- Update to 375.39.

* Thu Dec 15 2016 Simone Caronni <negativo17@gmail.com> - 2:375.26-1
- Update to 375.26

* Mon Dec 12 2016 Simone Caronni <negativo17@gmail.com> - 2:375.20-2
- Rebuild for RHEL 7.3 kernel.

* Sat Nov 19 2016 Simone Caronni <negativo17@gmail.com> - 2:375.20-1
- Update to 375.20.

* Fri Nov 04 2016 Simone Caronni <negativo17@gmail.com> - 2:367.57-2
- Require module-init-tools (provided by kmod) instead of /sbin/depmod.

* Mon Oct 10 2016 Simone Caronni <negativo17@gmail.com> - 2:367.57-1
- Update to 367.57.

* Thu Aug 25 2016 Simone Caronni <negativo17@gmail.com> - 2:367.44-1
- Update to 367.44.

* Fri Jul 22 2016 Simone Caronni <negativo17@gmail.com> - 2:367.35-1
- Update to 367.35.

* Mon Jun 13 2016 Simone Caronni <negativo17@gmail.com> - 2:367.27-1
- Update to 367.27.

* Fri May 27 2016 Simone Caronni <negativo17@gmail.com> - 2:361.45.11-1
- Update to 361.45.11.

* Wed Mar 30 2016 Simone Caronni <negativo17@gmail.com> - 2:361.42-1
- Update to 361.42, use new kernel module build mechanism.
- Remove ARM (Carma, Kayla) support.

* Tue Jan 26 2016 Simone Caronni <negativo17@gmail.com> - 2:352.79-1
- Update to 352.79.

* Tue Jan 12 2016 Simone Caronni <negativo17@gmail.com> - 2:352.63-2
- Update kernel build requirements.

* Wed Nov 18 2015 Simone Caronni <negativo17@gmail.com> - 2:352.63-1
- Update to 352.63.

* Tue Oct 20 2015 Simone Caronni <negativo17@gmail.com> - 2:352.55-1
- Update to 352.55.

* Fri Aug 28 2015 Simone Caronni <negativo17@gmail.com> - 2:352.41-1
- Update to 352.41.

* Wed Jul 29 2015 Simone Caronni <negativo17@gmail.com> - 2:352.30-1
- Update to 352.30.

* Wed Jun 17 2015 Simone Caronni <negativo17@gmail.com> - 2:352.21-1
- Update to 352.21.

* Tue May 19 2015 Simone Caronni <negativo17@gmail.com> - 2:352.09-1
- Update to 352.09.

* Wed May 13 2015 Simone Caronni <negativo17@gmail.com> - 2:346.72-1
- Update to 346.72.

* Tue Apr 07 2015 Simone Caronni <negativo17@gmail.com> - 2:346.59-1
- Update to 346.59.
- Removed unused patch.

* Thu Mar 12 2015 Simone Caronni <negativo17@gmail.com> - 2:346.47-2
- Add patch for kernel 4.0.

* Wed Feb 25 2015 Simone Caronni <negativo17@gmail.com> - 2:346.47-1
- Update to 346.47.
- Removed upstreamed patch.

* Thu Jan 29 2015 Simone Caronni <negativo17@gmail.com> - 2:346.35-2
- Add kernel patch for 3.18.

* Sat Jan 17 2015 Simone Caronni <negativo17@gmail.com> - 2:346.35-1
- Update to 346.35.

* Tue Dec 09 2014 Simone Caronni <negativo17@gmail.com> - 2:346.22-1
- Update to 346.22.

* Fri Nov 14 2014 Simone Caronni <negativo17@gmail.com> - 2:346.16-1
- Update to 346.16.
- UVM kernel module is gone on i*86.
- Update minimum kernel requirement on CentOS/RHEL 6 to be 6.6.

* Wed Oct 01 2014 Simone Caronni <negativo17@gmail.com> - 2:343.22-2
- Attempt building even if Xen or RT are enabled.

* Mon Sep 22 2014 Simone Caronni <negativo17@gmail.com> - 2:343.22-1
- Update to 343.22.

* Thu Aug 07 2014 Simone Caronni <negativo17@gmail.com> - 2:343.13-1
- Update to 343.13.

* Tue Jul 08 2014 Simone Caronni <negativo17@gmail.com> - 2:340.24-1
- Update to 340.24.
- Require modinfo for building.
- Use global instead of define.
- Use default different kernel version for different RHEL releases.

* Mon Jun 09 2014 Simone Caronni <negativo17@gmail.com> - 2:340.17-1
- Update to 340.17.

* Mon Jun 02 2014 Simone Caronni <negativo17@gmail.com> - 2:337.25-1
- Update to 337.25.

* Tue May 06 2014 Simone Caronni <negativo17@gmail.com> - 2:337.19-1
- Update to 337.19.

* Tue Apr 08 2014 Simone Caronni <negativo17@gmail.com> - 2:337.12-1
- Update to 337.12.

* Tue Mar 04 2014 Simone Caronni <negativo17@gmail.com> - 2:334.21-1
- Update to 334.21, update patch.

* Tue Feb 18 2014 Simone Caronni <negativo17@gmail.com> - 2:334.16-2
- Add kernel 3.14 patch.

* Sat Feb 08 2014 Simone Caronni <negativo17@gmail.com> - 2:334.16-1
- Update to 334.16.

* Tue Jan 14 2014 Simone Caronni <negativo17@gmail.com> - 2:331.38-1
- Update to 331.38.

* Fri Dec 13 2013 Simone Caronni <negativo17@gmail.com> - 2:331.20-2
- Update required kernel version to 6.5 release.

* Thu Nov 07 2013 Simone Caronni <negativo17@gmail.com> - 2:331.20-1
- Update to 331.20.
- Removed upstreamed patch.
- Support for multiple kernels is currently disabled, as kABI symbols are not
  correctly extracted from the multiple kernel modules.

* Fri Nov 01 2013 Simone Caronni <negativo17@gmail.com> - 2:319.60-2
- Use official patch from Nvidia for 3.11+ kernels.

* Wed Oct 02 2013 Simone Caronni <negativo17@gmail.com> - 0:319.60-1
- Update to 319.60.

* Wed Aug 21 2013 Simone Caronni <negativo17@gmail.com> - 2:319.49-1
- Updated to 319.49.

* Tue Jul 02 2013 Simone Caronni <negativo17@gmail.com> - 2:319.32-2
- Add armv7hl support.
- Fix nvidia driver dependency.

* Sat Jun 29 2013 Simone Caronni <negativo17@gmail.com> - 1:319.32-1
- Updated to 319.32.

* Fri May 31 2013 Simone Caronni <negativo17@gmail.com> - 1:319.23-1
- Updated to 319.23.

* Tue May 07 2013 Simone Caronni <negativo17@gmail.com> - 1:319.17-1
- Update to 319.17; based on elrepo package.
- Bump epoch.
- Switch source to generated source.

* Sat Mar 09 2013 Philip J Perry <phil@elrepo.org> - 310.40-1.el6.elrepo
- Updated to version 310.40
