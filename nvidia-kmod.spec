%global	kmod_name nvidia

%global	debug_package %{nil}

# Generate kernel symbols requirements:
%global _use_internal_dependency_generator 0

# If kversion isn't defined on the rpmbuild line, define it here. For Fedora,
# kversion needs always to be defined as there is no kABI support.

%if 0%{?rhel} == 7
%{!?kversion: %global kversion 3.10.0-1160.21.1.el7}
%endif

%if 0%{?rhel} == 8
%{!?kversion: %global kversion 4.18.0-240.22.1.el8_3}
%endif

Name:           %{kmod_name}-kmod
Version:        460.73.01
Release:        1%{?dist}
Summary:        NVIDIA display driver kernel module
Epoch:          3
License:        NVIDIA License
URL:            http://www.nvidia.com/
ExclusiveArch:  x86_64

Source0:        %{kmod_name}-kmod-%{version}-x86_64.tar.xz

BuildRequires:  elfutils-libelf-devel
BuildRequires:  gcc
BuildRequires:  kernel-devel %{?kversion:== %{kversion}}
BuildRequires:  kernel-abi-whitelists %{?kversion:== %{kversion}}
BuildRequires:  kmod
BuildRequires:  redhat-rpm-config

%description
This package provides the proprietary NVIDIA OpenGL kernel driver module.
It is built to depend upon the specific ABI provided by a range of releases of
the same variant of the Linux kernel and not on any one specific build.

%package -n kmod-%{kmod_name}
Summary:    %{kmod_name} kernel module(s)

Provides:   kabi-modules = %{kversion}.%{_target_cpu}
Provides:   %{kmod_name}-kmod = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:   module-init-tools

%description -n kmod-%{kmod_name}
This package provides the %{kmod_name} kernel module(s) built for the Linux kernel
using the %{_target_cpu} family of processors.

%post -n kmod-%{kmod_name}
if [ -e "/boot/System.map-%{kversion}.%{_target_cpu}" ]; then
    /usr/sbin/depmod -aeF "/boot/System.map-%{kversion}.%{_target_cpu}" "%{kversion}.%{_target_cpu}" > /dev/null || :
fi
modules=( $(find /lib/modules/%{kversion}.%{_target_cpu}/extra/%{kmod_name} | grep '\.ko$') )
if [ -x "/usr/sbin/weak-modules" ]; then
    printf '%s\n' "${modules[@]}" | /usr/sbin/weak-modules --add-modules
fi

%preun -n kmod-%{kmod_name}
rpm -ql kmod-%{kmod_name}-%{version}-%{release}.%{_target_cpu} | grep '\.ko$' > /var/run/rpm-kmod-%{kmod_name}-modules

%postun -n kmod-%{kmod_name}
if [ -e "/boot/System.map-%{kversion}.%{_target_cpu}" ]; then
    /usr/sbin/depmod -aeF "/boot/System.map-%{kversion}.%{_target_cpu}" "%{kversion}.%{_target_cpu}" > /dev/null || :
fi
modules=( $(cat /var/run/rpm-kmod-%{kmod_name}-modules) )
rm /var/run/rpm-kmod-%{kmod_name}-modules
if [ -x "/usr/sbin/weak-modules" ]; then
    printf '%s\n' "${modules[@]}" | /usr/sbin/weak-modules --remove-modules
fi

%prep
%autosetup -p1 -n %{kmod_name}-kmod-%{version}-x86_64

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

make -C %{_usrsrc}/kernels/%{kversion}.%{_target_cpu} modules_install M=$PWD

install -d %{buildroot}%{_sysconfdir}/depmod.d/
install kmod-%{kmod_name}.conf %{buildroot}%{_sysconfdir}/depmod.d/
# Remove the unrequired files.
rm -f %{buildroot}/lib/modules/%{kversion}.%{_target_cpu}/modules.*

%files -n kmod-%{kmod_name}
/lib/modules/%{kversion}.%{_target_cpu}/extra/*
%config /etc/depmod.d/kmod-%{kmod_name}.conf

%changelog
* Sun Apr 18 2021 Simone Caronni <negativo17@gmail.com> - 3:460.73.01-1
- Update to 460.73.01.

* Fri Mar 19 2021 Simone Caronni <negativo17@gmail.com> - 3:460.67-1
- Update to 460.67.

* Mon Mar 01 2021 Simone Caronni <negativo17@gmail.com> - 3:460.56-1
- Update to 460.56.

* Wed Jan 27 2021 Simone Caronni <negativo17@gmail.com> - 3:460.39-1
- Update to 460.39.

* Wed Jan 13 2021 Simone Caronni <negativo17@gmail.com> - 3:460.32.03-2
- Merge kmodtool script into SPEC file and remove obsolete stuff.

* Thu Jan  7 2021 Simone Caronni <negativo17@gmail.com> - 3:460.32.03-1
- Update to 460.32.03.

* Sun Dec 20 2020 Simone Caronni <negativo17@gmail.com> - 3:460.27.04-1
- Update to 460.27.04.
- Trim changelog.

* Mon Dec 07 2020 Simone Caronni <negativo17@gmail.com> - 3:450.80.02-2
- Drop support for CentOS/RHEL 6.

* Tue Oct 06 2020 Simone Caronni <negativo17@gmail.com> - 3:450.80.02-1
- Update to 450.80.02.

* Thu Aug 20 2020 Simone Caronni <negativo17@gmail.com> - 3:450.66-1
- Update to 450.66.

* Fri Jul 10 2020 Simone Caronni <negativo17@gmail.com> - 3:450.57-1
- Update to 450.57.

* Thu Jun 25 2020 Simone Caronni <negativo17@gmail.com> - 3:440.100-1
- Update to 440.100.

* Thu Apr 09 2020 Simone Caronni <negativo17@gmail.com> - 3:440.82-1
- Update to 440.82.

* Fri Feb 28 2020 Simone Caronni <negativo17@gmail.com> - 3:440.64-1
- Update to 440.64.

* Tue Feb 04 2020 Simone Caronni <negativo17@gmail.com> - 3:440.59-1
- Update to 440.59.

* Sun Feb 02 2020 Simone Caronni <negativo17@gmail.com> - 3:440.44-2
- Rebuild for CentOS/RHEL 8.1 kernels.

* Sat Dec 14 2019 Simone Caronni <negativo17@gmail.com> - 3:440.44-1
- Update to 440.44.

* Sat Nov 30 2019 Simone Caronni <negativo17@gmail.com> - 3:440.36-1
- Update to 440.36.

* Mon Nov 11 2019 Simone Caronni <negativo17@gmail.com> - 3:440.31-1
- Update to 440.31.

* Tue Oct 01 2019 Simone Caronni <negativo17@gmail.com> - 3:435.21-1
- Update to 435.21.

* Fri Sep 20 2019 Simone Caronni <negativo17@gmail.com> - 3:430.50-2
- Build for 7.7 kernels.

* Sat Sep 14 2019 Simone Caronni <negativo17@gmail.com> - 3:430.50-1
- Update to 430.50.

* Wed Jul 31 2019 Simone Caronni <negativo17@gmail.com> - 3:430.40-1
- Update to 430.40.

* Fri Jul 12 2019 Simone Caronni <negativo17@gmail.com> - 3:430.34-1
- Update to 430.34.

* Wed Jun 12 2019 Simone Caronni <negativo17@gmail.com> - 3:430.26-1
- Update to 430.26.

* Fri Jun 07 2019 Simone Caronni <negativo17@gmail.com> - 3:430.14-1
- Update to 430.14.

* Thu May 09 2019 Simone Caronni <negativo17@gmail.com> - 3:418.74-1
- Update to 418.74.

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
