%global file() %%{name}_%%{version}_%%*
%global mirror_url() https://releases.hashicorp.com/%%{name}/%%{version}/%%*
%define undefined()    %{expand:%%{?%{1}:0}%%{!?%{1}:1}}

Name:     packer
%if %{undefined bin_version}
Version:  1.2.5
%else
Version: %{bin_version}
%endif
Release:  1
Summary:  Packer is an open source tool for creating identical machine images for multiple platforms from a single source configuration.
License:  Mozilla Public License, version 2.0
URL:      https://www.packer.io/
# Download this file from the packer website
# Ensure that you verify it with the hashicorp private key before allowing this to be built
Source0: %{mirror_url %{file SHA256SUMS}}
Source1: %{mirror_url %{file SHA256SUMS.sig}}
Source2: gpgkey-hashicorp.gpg

BuildRequires: coreutils unzip
ExclusiveArch: %{ix86} x86_64 ${arm} aarch64

%prep
# Converting key from ASCII armored format
keyring=`mktemp --tmpdir keyring.XXXXXXXX.gpg`
gpg --keyring "$keyring" --import %{SOURCE2}
# Check signature
gpg --keyring "$keyring" %{SOURCE1} %{SOURCE0}

# Cleanup
rm -f "$keyring"

%setup -c -T
%global spec_build_dir %%{_builddir}/%%{name}-%%{version}
cp -T %{_sourcedir}/%{file SHA256SUMS} %{spec_build_dir}/sha256sum.txt

# Disable debugging for non-compiled package
%global debug_package %{nil}

%build
%ifarch %{arm}
%define bin_arch arm
%endif
%ifarch aarch64
%define bin_arch arm64
%endif
%ifarch %{ix86}
%define bin_arch 386
%endif
%ifarch x86_64
%define bin_arch amd64
%endif

%define bin_zip %{file linux_%{bin_arch}.zip}
cd %{spec_build_dir}
curl -o ./%{bin_zip} -L %{mirror_url %{bin_zip}}
sha256sum sha256sum.txt
mkdir -p ./bin
unzip ./%{bin_zip} -d ./bin/

%description
Packer is an open source tool for creating identical machine images for multiple platforms from a single source configuration. Packer is lightweight, runs on every major operating system, and is highly performant, creating machine images for multiple platforms in parallel. Packer does not replace configuration management like Chef or Puppet. In fact, when building images, Packer is able to use tools like Chef or Puppet to install software onto the image.

A machine image is a single static unit that contains a pre-configured operating system and installed software which is used to quickly create new running machines. Machine image formats change for each platform. Some examples include AMIs for EC2, VMDK/VMX files for VMware, OVF exports for VirtualBox, etc.

%install
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
install %{spec_build_dir}/bin/* $RPM_BUILD_ROOT/%{_bindir}/

%clean
rm -rf 

%files
%{_bindir}/*

%changelog
* Fri Oct 13 2017 Daniel Fallon <dfallon@dvtrading.co - 1.2.5
- Initial version of the package