%global pypi_name         knx-stack

Name:           python-%{pypi_name}
Version:        0.9.2
Release:        1%{?dist}
Summary:        A Python 3 KNX stack, not complete but easily extensible

License:        MIT

Url:            https://github.com/majamassarini/knx-stack
Source0:        https://github.com/majamassarini/knx-stack/archive/%{version}/%{pypi_name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  python3-devel

%global _description %{expand:
A Python 3 KNX stack, not complete but easily extensible.
Able to encode/decode messages both for USB HID and KNXnet IP.
}

%description %_description

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%py_provides    python3-%{pypi_name}

%description -n python3-%{pypi_name} %_description

%prep
%autosetup -n %{pypi_name}-%{version} -p1

%generate_buildrequires
%pyproject_buildrequires -r

%build
%pyproject_wheel

%install
%pyproject_install

%check
%{python3} -m unittest

%files -n python3-%{pypi_name}
%license COPYING
%doc README.md
%{python3_sitelib}/knx_stack-%{version}.dist-info/
%{python3_sitelib}/knx_stack

%changelog
%autochangelog