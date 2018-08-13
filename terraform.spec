%global file() %%{name}_%%{version}_%%*
%global mirror_url() https://releases.hashicorp.com/%%{name}/%%{version}/%%*
%define undefined()    %{expand:%%{?%{1}:0}%%{!?%{1}:1}}

Name:     terraform
%if %{undefined bin_version}
Version:  0.11.7
%else
Version: %{bin_version}
%endif
Release:  1
Summary:  Terraform is a tool for building, changing, and versioning infrastructure safely and efficiently. Terraform can manage existing and popular service providers as well as custom in-house solutions.
License:  Mozilla Public License, version 2.0
URL:      https://www.terraform.io
# Download this file from the terraform website
# Ensure that you verify it with the hashicorp private key before allowing this to be built
Source0: %{mirror_url %{file SHA256SUMS}}
Source1: %{mirror_url %{file SHA256SUMS.sig}}
Source2: gpgkey-hashicorp.gpg

BuildRequires: coreutils gpg unzip
ExclusiveArch: %{ix86} x86_64 ${arm} aarch64

%prep
# Converting key from ASCII armored format
keyring=`mktemp --tmpdir keyring.XXXXXXXX.gpg`
gpg --keyring "$keyring" --import %{SOURCE2}

# Check signature
gpg --keyring "$keyring" --verify %{SOURCE1} %{SOURCE0}

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
Terraform is a tool for building, changing, and versioning infrastructure safely and efficiently. Terraform can manage existing and popular service providers as well as custom in-house solutions.

Configuration files describe to Terraform the components needed to run a single application or your entire datacenter. Terraform generates an execution plan describing what it will do to reach the desired state, and then executes it to build the described infrastructure. As the configuration changes, Terraform is able to determine what changed and create incremental execution plans which can be applied.
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