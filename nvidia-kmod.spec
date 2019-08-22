# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%define buildforkernels akmod

%global debug_package %{nil}

%global zipmodules 1

%define __spec_install_post \
  %{__arch_install_post}\
  %{__os_install_post}\
  %{__mod_compress_install_post}

%define __mod_compress_install_post \
  if [ "%{zipmodules}" -eq "1" ] && [ $kernel_version ]; then \
    find %{buildroot}/usr/lib/modules/ -type f -name '*.ko' | xargs xz; \
  fi

Name:           nvidia-kmod
Version:        435.17
Release:        1%{?dist}
Summary:        NVIDIA display driver kernel module
Epoch:          3
License:        NVIDIA License
URL:            http://www.nvidia.com/object/unix.html
ExclusiveArch:  x86_64

Source0:        %{name}-%{version}-x86_64.tar.xz
Source11:       nvidia-kmodtool-excludekernel-filterfile

# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:  kmodtool

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} --obsolete-name nvidia-newest --obsolete-version "%{version}" %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
The NVidia %{version} display driver kernel module for kernel %{kversion}.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo rpmfusion --kmodname %{name} --filterfile %{SOURCE11} --obsolete-name nvidia-newest --obsolete-version "%{version}" %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%setup -q -n %{name}-%{version}-x86_64

for kernel_version in %{?kernel_versions}; do
    mkdir _kmod_build_${kernel_version%%___*}
    cp -fr kernel/* _kmod_build_${kernel_version%%___*}
done

%build
for kernel_version in %{?kernel_versions}; do
    pushd _kmod_build_${kernel_version%%___*}/
        make %{?_smp_mflags} \
            IGNORE_XEN_PRESENCE=1 \
            IGNORE_PREEMPT_RT_PRESENCE=1 \
            IGNORE_CC_MISMATCH=1 \
            SYSSRC="${kernel_version##*___}" \
            module
    popd
done

%install
for kernel_version in %{?kernel_versions}; do
    mkdir -p %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
    install -p -m 0755 _kmod_build_${kernel_version%%___*}/*.ko \
        %{buildroot}/%{kmodinstdir_prefix}/${kernel_version%%___*}/%{kmodinstdir_postfix}/
done
%{?akmod_install}

%changelog
* Thu Aug 22 2019 Simone Caronni <negativo17@gmail.com> - 3:435.17-1
- Update to 435.17.

* Wed Jul 31 2019 Simone Caronni <negativo17@gmail.com> - 3:430.40-1
- Update to 430.40.

* Fri Jul 12 2019 Simone Caronni <negativo17@gmail.com> - 3:430.34-1
- Update to 430.34.

* Wed Jun 12 2019 Simone Caronni <negativo17@gmail.com> - 3:430.26-1
- Update to 430.26.

* Sat May 18 2019 Simone Caronni <negativo17@gmail.com> - 3:430.14-1
- Update to 430.14.

* Thu May 09 2019 Simone Caronni <negativo17@gmail.com> - 3:418.74-1
- Update to 418.74.

* Sun Mar 24 2019 Simone Caronni <negativo17@gmail.com> - 3:418.56-1
- Update to 418.56.

* Fri Feb 22 2019 Simone Caronni <negativo17@gmail.com> - 3:418.43-1
- Update to 418.43.
- Trim changelog.

* Thu Jan 17 2019 Simone Caronni <negativo17@gmail.com> - 3:415.27-1
- Update to 415.27.

* Thu Dec 20 2018 Simone Caronni <negativo17@gmail.com> - 3:415.25-1
- Update to 415.25.

* Fri Dec 14 2018 Simone Caronni <negativo17@gmail.com> - 3:415.23-1
- Update to 415.23.

* Sun Dec 09 2018 Simone Caronni <negativo17@gmail.com> - 3:415.22-1
- Update to 415.22.

* Thu Nov 22 2018 Simone Caronni <negativo17@gmail.com> - 3:415.18-1
- Update to 415.18.

* Mon Nov 19 2018 Simone Caronni <negativo17@gmail.com> - 3:410.78-1
- Update to 410.78.

* Fri Oct 26 2018 Simone Caronni <negativo17@gmail.com> - 3:410.73-1
- Update to 410.73.

* Wed Oct 17 2018 Simone Caronni <negativo17@gmail.com> - 3:410.66-1
- Update to 410.66.

* Sat Sep 22 2018 Simone Caronni <negativo17@gmail.com> - 3:410.57-1
- Update to 410.57.

* Wed Aug 22 2018 Simone Caronni <negativo17@gmail.com> - 3:396.54-1
- Update to 396.54.

* Sun Aug 19 2018 Simone Caronni <negativo17@gmail.com> - 3:396.51-1
- Update to 396.51.

* Fri Jul 20 2018 Simone Caronni <negativo17@gmail.com> - 3:396.45-1
- Update to 396.45.

* Fri Jun 01 2018 Simone Caronni <negativo17@gmail.com> - 3:396.24-1
- Update to 396.24, x86_64 only.

* Tue May 22 2018 Simone Caronni <negativo17@gmail.com> - 3:390.59-1
- Update to 390.59.

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

* Fri Jan 19 2018 Simone Caronni <negativo17@gmail.com> - 2:390.12-1
- Update to 390.12.
