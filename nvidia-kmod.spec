# buildforkernels macro hint: when you build a new version or a new release
# that contains bugfixes or other improvements then you must disable the
# "buildforkernels newest" macro for just that build; immediately after
# queuing that build enable the macro again for subsequent builds; that way
# a new akmod package will only get build when a new one is actually needed
%define buildforkernels akmod

%global debug_package %{nil}

%global mok_algo sha512
%global mok_key /usr/src/akmods/mok.key
%global mok_der /usr/src/akmods/mok.der

%define __spec_install_post \
  %{__arch_install_post}\
  %{__os_install_post}\
  %{__mod_install_post}

%define __mod_install_post \
  if [ $kernel_version ]; then \
    find %{buildroot} -type f -name '*.ko' | xargs %{__strip} --strip-debug; \
    if [ -f /usr/src/akmods/mok.key ] && [ -f /usr/src/akmods/mok.der ]; then \
      find %{buildroot} -type f -name '*.ko' | xargs echo; \
      find %{buildroot} -type f -name '*.ko' | xargs -L1 /usr/lib/modules/${kernel_version%%___*}/build/scripts/sign-file %{mok_algo} %{mok_key} %{mok_der}; \
    fi \
    find %{buildroot} -type f -name '*.ko' | xargs xz; \
  fi

Name:           nvidia-kmod
Version:        545.29.02
Release:        2%{?dist}
Summary:        NVIDIA display driver kernel module
Epoch:          3
License:        NVIDIA License
URL:            http://www.nvidia.com/object/unix.html
ExclusiveArch:  x86_64

Source0:        %{name}-%{version}-x86_64.tar.xz

# get the needed BuildRequires (in parts depending on what we build for)
BuildRequires:  kmodtool

# kmodtool does its magic here
%{expand:%(kmodtool --target %{_target_cpu} --repo negativo17.org --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null) }

%description
The NVidia %{version} display driver kernel module for kernel %{kversion}.

%prep
# error out if there was something wrong with kmodtool
%{?kmodtool_check}
# print kmodtool output for debugging purposes:
kmodtool  --target %{_target_cpu}  --repo negativo17.org --kmodname %{name} %{?buildforkernels:--%{buildforkernels}} %{?kernels:--for-kernels "%{?kernels}"} 2>/dev/null

%autosetup -p0 -n %{name}-%{version}-x86_64

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
* Sun Nov 12 2023 Simone Caronni <negativo17@gmail.com> - 3:545.29.02-2
- Trim changelog.

* Tue Oct 31 2023 Simone Caronni <negativo17@gmail.com> - 3:545.29.02-1
- Update to 545.29.02.

* Wed Oct 18 2023 Simone Caronni <negativo17@gmail.com> - 3:545.23.06-1
- Update to 545.23.06.

* Fri Sep 22 2023 Simone Caronni <negativo17@gmail.com> - 3:535.113.01-1
- Update to 535.113.01.

* Thu Aug 24 2023 Simone Caronni <negativo17@gmail.com> - 3:535.104.05-1
- Update to 535.104.05.

* Wed Aug 09 2023 Simone Caronni <negativo17@gmail.com> - 3:535.98-1
- Update to 535.98.

* Wed Jul 19 2023 Simone Caronni <negativo17@gmail.com> - 3:535.86.05-1
- Update to 535.86.05.

* Thu Jun 15 2023 Simone Caronni <negativo17@gmail.com> - 3:535.54.03-1
- Update to 535.54.03.

* Tue Jun 13 2023 Simone Caronni <negativo17@gmail.com> - 3:535.43.02-1
- Update to 535.43.02.

* Fri Mar 24 2023 Simone Caronni <negativo17@gmail.com> - 3:530.41.03-1
- Update to 530.41.03.

* Wed Mar 08 2023 Simone Caronni <negativo17@gmail.com> - 3:530.30.02-1
- Update to 530.30.02.

* Fri Feb 10 2023 Simone Caronni <negativo17@gmail.com> - 3:525.89.02-1
- Update to 525.89.02.

* Fri Jan 20 2023 Simone Caronni <negativo17@gmail.com> - 3:525.85.05-1
- Update to 525.85.05.

* Mon Jan 09 2023 Simone Caronni <negativo17@gmail.com> - 3:525.78.01-1
- Update to 525.78.01.

* Tue Nov 29 2022 Simone Caronni <negativo17@gmail.com> - 3:525.60.11-1
- Update to 525.60.11.

* Thu Oct 13 2022 Simone Caronni <negativo17@gmail.com> - 3:520.56.06-1
- Update to 520.56.06.

* Wed Sep 21 2022 Simone Caronni <negativo17@gmail.com> - 3:515.76-1
- Update to 515.76.

* Mon Aug 08 2022 Simone Caronni <negativo17@gmail.com> - 3:515.65.01-1
- Update to 515.65.01.

* Wed Jun 29 2022 Simone Caronni <negativo17@gmail.com> - 3:515.57-1
- Update to 515.57.

* Wed Jun 01 2022 Simone Caronni <negativo17@gmail.com> - 3:515.48.07-1
- Update to 515.48.07.

* Thu May 12 2022 Simone Caronni <negativo17@gmail.com> - 3:515.43.04-1
- Update to 515.43.04.

* Mon May 02 2022 Simone Caronni <negativo17@gmail.com> - 3:510.68.02-1
- Update to 510.68.02.

* Mon Mar 28 2022 Simone Caronni <negativo17@gmail.com> - 3:510.60.02-1
- Update to 510.60.02.

* Mon Feb 14 2022 Simone Caronni <negativo17@gmail.com> - 3:510.54-1
- Update to 510.54.

* Wed Feb 02 2022 Simone Caronni <negativo17@gmail.com> - 3:510.47.03-1
- Update to 510.47.03.
