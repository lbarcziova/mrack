Name:           mrack
Version:        1.15.0
Release:        1%{?dist}
Summary:        Multicloud use-case based multihost async provisioner

License:        Apache-2.0
URL:            https://github.com/neoave/mrack
Source0:        %{URL}/releases/download/v%{version}/%{name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python3-devel
BuildRequires:  python3-click
BuildRequires:  python3-pyyaml
BuildRequires:  python3-setuptools

# coma separated list of provider plugins
%global provider_plugins aws,beaker,openstack,podman,virt

Requires:       %{name}-cli = %{version}-%{release}
Requires:       python3-%{name}lib = %{version}-%{release}
Requires:       python3-%{name}-aws = %{version}-%{release}
Requires:       python3-%{name}-beaker = %{version}-%{release}
Requires:       python3-%{name}-openstack = %{version}-%{release}
Requires:       python3-%{name}-podman = %{version}-%{release}
Requires:       python3-%{name}-virt = %{version}-%{release}

# We filter out the asyncopenstackclient dependency of this package
# so it is not forcing installation of missing dependencies in Fedora
# Once python3-AsyncOpenStackClient is in fedora we can drop this line
%global __requires_exclude asyncopenstackclient
%{?python_disable_dependency_generator}

%description
mrack is a provisioning tool and a library for CI and local multi-host
testing supporting multiple provisioning providers (e.g. AWS, Beaker,
Openstack). But in comparison to other multi-cloud libraries,
the aim is to be able to describe host from application perspective.

%package        cli
Summary:        Command line interface for mrack
Requires:       python3-%{name}lib = %{version}-%{release}
Requires:       python3-click

%package -n     python3-%{name}lib
Summary:        Core mrack libraries
Requires:       python3-pyyaml
Recommends:     python3-gssapi
Requires:       sshpass

%{?python_provide:%python_provide python3-%{name}lib}

%package -n     python3-%{name}-aws
Summary:        AWS provider plugin for mrack
Requires:       python3-%{name}lib = %{version}-%{release}
Requires:       python3-boto3
Requires:       python3-botocore

%{?python_provide:%python_provide python3-%{name}-aws}


%package -n     python3-%{name}-beaker
Summary:        Beaker provider plugin for mrack
Requires:       python3-%{name}lib = %{version}-%{release}
%if 0%{?rhel} == 8
# c8s has missing beaker-client package
Recommends:     beaker-client
%else
Requires:       beaker-client
%endif

%{?python_provide:%python_provide python3-%{name}-beaker}


%package -n     python3-%{name}-openstack
Summary:        Openstack provider plugin for mrack
Requires:       python3-%{name}lib = %{version}-%{release}
Recommends:     python3-AsyncOpenStackClient

%{?python_provide:%python_provide python3-%{name}-openstack}


%package -n     python3-%{name}-podman
Summary:        Podman provider plugin for mrack
Requires:       python3-%{name}lib = %{version}-%{release}
Requires:       podman

%{?python_provide:%python_provide python3-%{name}-podman}

%package -n     python3-%{name}-virt
Summary:        Virtualization provider plugin for mrack using testcloud
Requires:       python3-%{name}lib = %{version}-%{release}
Requires:       testcloud

%{?python_provide:%python_provide python3-%{name}-virt}

%description        cli
%{name}-cli contains mrack command which functionality
can be extended by installing mrack plugins

%description -n     python3-%{name}lib
python3-%{name}lib contains core mrack functionalities
and static provider which can be used as a library

%description -n     python3-%{name}-aws
%{name}-aws is an additional plugin with AWS provisioning
library extending mrack package

%description -n     python3-%{name}-beaker
%{name}-beaker is an additional plugin with Beaker provisioning
library extending mrack package

%description -n     python3-%{name}-openstack
%{name}-openstack is an additional plugin with OpenStack provisioning
library extending mrack package

%description -n     python3-%{name}-podman
%{name}-podman is an additional plugin with Podman provisioning
library extending mrack package

%description -n     python3-%{name}-virt
%{name}-virt is an additional plugin with Virualization provisioning
library extending mrack package using testcloud

%prep
%autosetup -p1 -n %{name}-%{version}
# Remove bundled egg-info
rm -r src/%{name}.egg-info

%build
%py3_build

%install
%py3_install

%files
%license LICENSE
%doc README.md
%doc CHANGELOG.md

%files cli
# the mrack man page RFE: https://github.com/neoave/mrack/issues/197
%license LICENSE
%doc README.md
%doc CHANGELOG.md
%{_bindir}/%{name}
%{python3_sitelib}/%{name}/{,__pycache__/}run.*

%files -n python3-%{name}lib
%license LICENSE
%doc README.md
%doc CHANGELOG.md
%{python3_sitelib}/%{name}
%{python3_sitelib}/%{name}-%{version}-py%{python3_version}.egg-info
%exclude %{python3_sitelib}/%{name}/{,__pycache__/}run.*
%exclude %{python3_sitelib}/%{name}/providers/utils/{,__pycache__/}osapi.*
%exclude %{python3_sitelib}/%{name}/providers/utils/{,__pycache__/}testcloud.*
%exclude %{python3_sitelib}/%{name}/providers/utils/{,__pycache__/}podman.*
%exclude %{python3_sitelib}/%{name}/providers/{,__pycache__/}{%{provider_plugins}}.*
%exclude %{python3_sitelib}/%{name}/transformers/{,__pycache__/}{%{provider_plugins}}.*

%files -n python3-%{name}-aws
%{python3_sitelib}/%{name}/transformers/{,__pycache__/}aws.*
%{python3_sitelib}/%{name}/providers/{,__pycache__/}aws.*

%files -n python3-%{name}-beaker
%{python3_sitelib}/%{name}/transformers/{,__pycache__/}beaker.*
%{python3_sitelib}/%{name}/providers/{,__pycache__/}beaker.*

%files -n python3-%{name}-openstack
%{python3_sitelib}/%{name}/transformers/{,__pycache__/}openstack.*
%{python3_sitelib}/%{name}/providers/{,__pycache__/}openstack.*
%{python3_sitelib}/%{name}/providers/utils/{,__pycache__/}osapi.*

%files -n python3-%{name}-podman
%{python3_sitelib}/%{name}/transformers/{,__pycache__/}podman.*
%{python3_sitelib}/%{name}/providers/{,__pycache__/}podman.*
%{python3_sitelib}/%{name}/providers/utils/{,__pycache__/}podman.*

%files -n python3-%{name}-virt
%{python3_sitelib}/%{name}/transformers/{,__pycache__/}virt.*
%{python3_sitelib}/%{name}/providers/{,__pycache__/}virt.*
%{python3_sitelib}/%{name}/providers/utils/{,__pycache__/}testcloud.*

%changelog
* Tue Apr 18 2023 Tibor Dudlák <tdudlak@redhat.com> - 1.15.0-1
- f9f0e33 test: Add missing strategy_retry test (Tibor Dudlák)
- 121c5db refactor(provider): take max_utilization out to method to ease mocking (Tibor Dudlák)
- dc74ced test: Add missing tests for fixed code from https://github.com/neoave/mrack/pull/245 (Tibor Dudlák)
- 86393ab feat(outputs): preset username and password for windows host in pytest-mh (Tibor Dudlák)
- 4c26b5f feat(outputs): merge nested dictionary instead of overriding it (Tibor Dudlák)
- 4dde2e5 feat(utils): add merge_dict (Tibor Dudlák)
- 5440be1 refactor: fixes _openstack_gather_responses test warnings and exec time (David Pascual)
- e29031b fix: Handle 403 AuthError (out of quota) in openstack provisioning (David Pascual)
- a4e5075 feat: configurable ssh options (Petr Vobornik)
- e9d716e chore: fix docs dependencies in tox run (Petr Vobornik)
- 6f1943b chore: add Markdown support to docs and add design section (Petr Vobornik)
- 88458e1 docs: SSH options design (Petr Vobornik)

* Thu Mar 16 2023 Tibor Dudlák <tdudlak@redhat.com> - 1.14.1-1
- a9c4e62 fix: mrack not re-provisioning hosts which were destroyed (Tibor Dudlák)
- 17b45e4 fix: Replace coroutines with tasks to avoid RuntimeError (David Pascual)

* Wed Mar 08 2023 Tibor Dudlák <tdudlak@redhat.com> - 1.14.0-1
- e319b73 refactor(AWS): change variable name typo in get_ip_addresses (Tibor Dudlák)
- d95e65f fix(OpenStack): Add missing await for self._load_limits() method call (Tibor Dudlák)
- d0c2d8f refactor: Update supported providers (Tibor Dudlák)
- 13ad3df fix(outputs): remove config section from pytest-multihost (Tibor Dudlák)
- d3da251 feat(outputs): allow to overwrite ansible layout (Tibor Dudlák)
- d3ac20d feat(outputs): allow to choose which outputs should be generated (Tibor Dudlák)
- 66f2877 feat(outputs): add support for pytest-mh (Tibor Dudlák)
- db633b7 feat(utils): relax condition in get_fqdn (Tibor Dudlák)
- 0735e36 fix(outputs): add host to correct group in layout (Tibor Dudlák)
- b1f5318 feat(utils): add get_os_type (Tibor Dudlák)
- 0ab88e6 refactor(black): reformat code (Tibor Dudlák)

* Wed Mar 01 2023 Tibor Dudlák <tdudlak@redhat.com> - 1.13.3-1
- 0f62237 fix(OpenStack): await loading limits to not break provisioning (Tibor Dudlák)

* Wed Mar 01 2023 Tibor Dudlák <tdudlak@redhat.com> - 1.13.2-1
- 06f18d1 fix: Use get method when host error object is a dictionary (Tibor Dudlák)
- fd33d68 fix(Beaker): rerurn common dictionary when validation fails (Tibor Dudlák)
- b6c5ef4 fix(OpenStack): Add exception parameter when validation fails (Tibor Dudlák)
- fa2c779 fix(OpenStack): load limits properly by one method (Tibor Dudlák)
- 61e515f chore: change back mrack dist release to 1 (Tibor Dudlák)

* Tue Feb 21 2023 Tibor Dudlák <tdudlak@redhat.com> - 1.13.1-1
- 1421b37 fix(MrackConfig): Fix MrackConfig class properties (Tibor Dudlák)

* Fri Feb 17 2023 Tibor Dudlák <tdudlak@redhat.com> - 1.13.0-1
- 72cc2f3 test: add extra dnf options when dealing with rhel/epel 8 (Tibor Dudlák)
- 32a754b chore: set packit to sync changelog as well (Tibor Dudlák)
- b0512b4 chore: sync fedora spec to upstream to maintain changelog history for fedora (Tibor Dudlák)
- be7b50a chore: Generate proper changelog from commit history when releasing (Tibor Dudlák)
- 98f4035 chore: Bump python-semantic-release to latest (Tibor Dudlák)
- a0e76dd test(OpenStack): Fixup the network spread tests (Tibor Dudlák)
- 88b9332 test(OpenStack): rewrite network alloaction tests (Tibor Dudlák)
- 777862f feat(OpenStack): Provide a way to disable network spreading (Tibor Dudlák)
- ff7331d fix(OpenStack): fix condition for network to get in interval (Tibor Dudlák)
- 943316d fix: fqdn in name is ignored and mrack guesses the name instead #237 (Tibor Dudlák)
- 46141dc feat(AWS): Add utilization check method (Tibor Dudlák)
- bb80060 feat(OpenStack): Add utilization check method (Tibor Dudlák)
- 55f9c2c feat: Do not use same sleep for every mrack run (Tibor Dudlák)
- 6ce3927 test(AnsibleInventory): global level output values override (Tibor Dudlák)
- a7a896a feat(AnsibleInventory): Allow additional global level values (Tibor Dudlák)
- 91c562c feat(AnsibleInventory): Allow additional domain level ansible inventory values (Tibor Dudlák)
- 109b03c test(OpenStack): Update calls in openststack tests (Tibor Dudlák)
- 4467cc2 refactor(OpenStack): make private openstack methods truly private (Tibor Dudlák)
- 72b9b9c chore: use custom release_suffix for PR testing via packit (Petr Vobornik)
- f3f734a chore: disable pylint pre-commit hook (Petr Vobornik)
- 4aa9b0a chore(Packit): Add synchronization of tmt plans and tests (Tibor Dudlák)
- 02c3e01 chore(Packit): Configure users on whose actions packit is allowed to be run (Tibor Dudlák)
- cf14ed9 chore(Packit): Add missing ci.fmf to synced files (Tibor Dudlák)

* Tue Dec 13 2022 Tibor Dudlák <tdudlak@redhat.com> - 1.12.3-4
- chore: Add add tmt tests and plans and add them to sync (Tibor Dudlák)

* Tue Dec 13 2022 Tibor Dudlák <tdudlak@redhat.com> - 1.12.3-3
- chore: Add fmf/version and allowed users to run packit (Tibor Dudlák)

* Tue Dec 13 2022 Tibor Dudlák <tdudlak@redhat.com> - 1.12.3-2
- chore: Add ci.fmf to the repo (Tibor Dudlák)

* Tue Dec 13 2022 Packit <hello@packit.dev> - 1.12.3-1
- chore: Release version 1.12.3 (github-actions)
- chore(Packit): Enable copr build for commit to main only. (Tibor Dudlák)
- chore(Packit): Enable TF tests job to run on pull request. (Tibor Dudlák)
- chore(Packit): Add fedora gating.yaml to synced files. (Tibor Dudlák)
- chore(TestingFarm): Add gating for fedora workflow (Tibor Dudlák)
- fix: Add cache decorator for older python versions. (Tibor Dudlák)
- fix(mrack.spec): Missing dependency in c8s for beaker-client (Tibor Dudlák)
- chore(Packit): enable epel-8 and epel-9 updates and tests (Tibor Dudlák)
- fix(AWS): refactor sources to be py3.6 compatible (Tibor Dudlák)

* Fri Dec 02 2022 Packit <hello@packit.dev> - 1.12.2-1
- chore: Release version 1.12.2 (github-actions)
- chore: Use python 3.10 in GH actions (Tibor Dudlák)
- refactor: pylint fixes related to Python 3.10 (Tibor Dudlák)
- test: Fix test_utils.py to be included in pytest run (Tibor Dudlák)
- chore(pytest): add missing python_path when using pytest >=7.0.0 (Tibor Dudlák)
- test: Add test for value_to_bool util function (Tibor Dudlák)
- fix: Owner requirement boolean parsing from string (Tibor Dudlák)
- chore(Packit): Add upstream_tag_template to .packit.yaml (Tibor Dudlák)

* Thu Nov 24 2022 Tibor Dudlák <tdudlak@redhat.com> - 1.12.1-1
- Released upstream version 1.12.1

* Mon Nov 14 2022 Tibor Dudlák <tdudlak@redhat.com> - 1.12.0-1
- Released upstream version 1.12.0

* Thu Nov 03 2022 Tibor Dudlák <tdudlak@redhat.com> - 1.11.0-1
- Released upstream version 1.11.0

* Wed Oct 26 2022 Tibor Dudlák <tdudlak@redhat.com> - 1.10.0-1
- Released upstream version 1.10.0

* Thu Oct 20 2022 Tibor Dudlák <tdudlak@redhat.com> - 1.9.1-1
- Released upstream version 1.9.1

* Wed Oct 12 2022 Tibor Dudlák <tdudlak@redhat.com> - 1.9.0-1
- Released upstream version 1.9.0

* Mon Oct 10 2022 Tibor Dudlák <tdudlak@redhat.com> - 1.8.1-1
- Released upstream version 1.8.1

* Mon Oct 10 2022 Tibor Dudlák <tdudlak@redhat.com> - 1.8.0-1
- Released upstream version 1.8.0

* Tue Sep 20 2022 Tibor Dudlák <tdudlak@redhat.com> - 1.7.0-1
- Released upstream version 1.7.0

* Wed Jul 27 2022 Tibor Dudlák <tdudlak@redhat.com> - 1.6.0-1
- Released upstream version 1.6.0

* Fri Jul 08 2022 Tibor Dudlák <tdudlak@redhat.com> - 1.5.0-1
- Released upstream version 1.5.0

* Fri Jun 17 2022 David Pascual Hernandez <davherna@redhat.com> - 1.4.1-1
- Released upstream version 1.4.1

* Thu May 05 2022 Tibor Dudlák <tdudlak@redhat.com> - 1.4.0-1
- Released upstream version 1.4.0

* Tue Apr 05 2022 Tibor Dudlák <tdudlak@redhat.com> - 1.3.1-1
- Released upstream version 1.3.1

* Fri Apr 01 2022 David Pascual Hernandez <davherna@redhat.com> - 1.3.0-1
- Released upstream version 1.3.0

* Wed Dec 15 2021 Tibor Dudlák <tdudlak@redhat.com> - 1.2.0-1
- Released upstream version 1.2.0

* Thu Nov 25 2021 Tibor Dudlák <tdudlak@redhat.com> - 1.1.1-1
- Released upstream version 1.1.1

* Tue Nov 23 2021 Tibor Dudlák <tdudlak@redhat.com> - 1.1.0-1
- Released upstream version 1.1.0

* Fri Sep 03 2021 Tibor Dudlák <tdudlak@redhat.com> - 1.0.0-1
- Released upstream version 1.0.0

* Thu Jul 01 2021 Tibor Dudlák <tdudlak@redhat.com> - 0.14.0-1
- Released upstream version 0.14.0

* Tue Jun 08 2021 Francisco Triviño <ftrivino@redhat.com> - 0.13.0-1
- Released upstream version 0.13.0

* Thu May 13 2021 Tibor Dudlák <tdudlak@redhat.com> - 0.12.0-1
- Released upstream version 0.12.0

* Fri May 07 2021 Tibor Dudlák <tdudlak@redhat.com> - 0.11.0-1
- Released upstream version 0.11.0

* Fri Apr 30 2021 Bhavik Bhavsar <bbhavsar@redhat.com> - 0.10.0-1
- Released upstream version 0.10.0

* Mon Apr 19 2021 Armando Neto <abiagion@redhat.com> - 0.9.0-1
- Released upstream version 0.9.0

* Thu Apr 15 2021 Armando Neto <abiagion@redhat.com> - 0.8.0-1
- Released upstream version 0.8.0

* Tue Mar 23 2021 Armando Neto <abiagion@redhat.com> - 0.7.1-1
- Released upstream version 0.7.1

* Mon Mar 22 2021 Tibor Dudlák <tdudlak@redhat.com> - 0.7.0-1
- Released upstream version 0.7.0

* Thu Feb 04 2021 Armando Neto <abiagion@redhat.com> - 0.6.0-1
- Initial package.
