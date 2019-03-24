# Define the kmod package name here.
%global	kmod_name nvidia

# If kversion isn't defined on the rpmbuild line, define it here. For Fedora,
# kversion needs always to be defined as there is no kABI support.

# RHEL 6.10
%if 0%{?rhel} == 6
%{!?kversion: %global kversion 2.6.32-754.el6}
%endif

# RHEL 7.6
%if 0%{?rhel} == 7
%{!?kversion: %global kversion 3.10.0-957.el7}
%endif

Name:           %{kmod_name}-kmod
Version:        418.56
Release:        1%{?dist}
Summary:        NVIDIA display driver kernel module
Epoch:          3
License:        NVIDIA License
URL:            http://www.nvidia.com/
ExclusiveArch:  x86_64

Source0:        %{kmod_name}-kmod-%{version}-x86_64.tar.xz
Source10:       kmodtool-%{kmod_name}-el6.sh

BuildRequires:  gcc
BuildRequires:  redhat-rpm-config
BuildRequires:  kernel-devel %{?kversion:== %{kversion}}
BuildRequires:  kernel-abi-whitelists %{?kversion:== %{kversion}}

%if 0%{?rhel} == 6
BuildRequires:  module-init-tools
%else
BuildRequires:  kmod
%endif

# Magic hidden here.
%global kmodtool sh %{SOURCE10}
%{expand:%(%{kmodtool} rpmtemplate %{kmod_name} %{kversion}.%{_target_cpu} "" 2>/dev/null)}

# Disable building of the debug package(s).
%global	debug_package %{nil}

%description
This package provides the proprietary NVIDIA OpenGL kernel driver module.
It is built to depend upon the specific ABI provided by a range of releases of
the same variant of the Linux kernel and not on any one specific build.

%prep
%autosetup -n %{kmod_name}-kmod-%{version}-x86_64

mv kernel/* .

echo "override %{kmod_name} * weak-updates/%{kmod_name}" > kmod-%{kmod_name}.conf

%build
export SYSSRC=%{_usrsrc}/kernels/%{kversion}.%{_target_cpu}
export IGNORE_XEN_PRESENCE=1
export IGNORE_PREEMPT_RT_PRESENCE=1
export IGNORE_CC_MISMATCH=1

make %{?_smp_mflags} module

%install
export INSTALL_MOD_PATH=%{buildroot}
export INSTALL_MOD_DIR=extra/%{kmod_name}
ksrc=%{_usrsrc}/kernels/%{kversion}.%{_target_cpu}
make -C "${ksrc}" modules_install M=$PWD

install -d %{buildroot}%{_sysconfdir}/depmod.d/
install kmod-%{kmod_name}.conf %{buildroot}%{_sysconfdir}/depmod.d/
# Remove the unrequired files.
rm -f %{buildroot}/lib/modules/%{kversion}.%{_target_cpu}/modules.*

%changelog
* Sun Mar 24 2019 Simone Caronni <negativo17@gmail.com> - 3:418.56-1
- Update to 418.56.
- Change logic for kernel versions.

* Fri Feb 22 2019 Simone Caronni <negativo17@gmail.com> - 3:418.43-1
- Update to 418.43.
- Trim changelog.

* Sun Feb 03 2019 Simone Caronni <negativo17@gmail.com> - 3:410.93-2
- Do not require nvidia-driver, require nvidia-kmod-common.

* Fri Jan 04 2019 Simone Caronni <negativo17@gmail.com> - 3:410.93-1
- Update to 410.93.

* Mon Nov 19 2018 Simone Caronni <negativo17@gmail.com> - 3:410.78-1
- Update to 410.78.

* Sun Nov 18 2018 Simone Caronni <negativo17@gmail.com> - 3:410.73-2
- Update for 7.6 kernel.

* Fri Oct 26 2018 Simone Caronni <negativo17@gmail.com> - 3:410.73-1
- Update to 410.73.

* Wed Oct 17 2018 Simone Caronni <negativo17@gmail.com> - 3:410.66-1
- Update to 410.66.

* Thu Sep 06 2018 Simone Caronni <negativo17@gmail.com> - 3:390.87-1
- Update to 390.87.

* Tue Jul 17 2018 Simone Caronni <negativo17@gmail.com> - 3:390.77-1
- Update to 390.77.

* Mon Jun 11 2018 Simone Caronni <negativo17@gmail.com> - 3:390.67-1
- Update to 390.67.

* Tue May 22 2018 Simone Caronni <negativo17@gmail.com> - 3:390.59-1
- Update to 390.59.

* Wed May 02 2018 Simone Caronni <negativo17@gmail.com> - 3:390.48-2
- Update for 7.5 kernel.

* Tue Apr 03 2018 Simone Caronni <negativo17@gmail.com> - 3:390.48-1
- Update to 390.48.

* Wed Mar 21 2018 Simone Caronni <negativo17@gmail.com> - 3:390.42-2
- Re-add kernel 4.15 patch.

* Thu Mar 15 2018 Simone Caronni <negativo17@gmail.com> - 3:390.42-1
- Update to 390.42.

* Tue Feb 27 2018 Simone Caronni <negativo17@gmail.com> - 3:390.25-3
- Update Epoch so packages do not overlap with RPMFusion.

* Wed Feb 21 2018 Simone Caronni <negativo17@gmail.com> - 2:390.25-2
- Add kernel 4.15 patch.

* Tue Jan 30 2018 Simone Caronni <negativo17@gmail.com> - 2:390.25-1
- Update to 390.25.

* Thu Jan 11 2018 Simone Caronni <negativo17@gmail.com> - 2:384.111-1
- Update to 384.111.
