Name:           kisslicer
%global cname   KISSlicer
Version:        1.6.3
Release:        10%{?dist}
Summary:        Keep It Simple Slicer
URL:            http://www.kisslicer.com/

# License information: http://www.kisslicer.com/download.html "MAY be shared freely"
License:        Redistributable, no modification permitted

# Download for both 64 and 32 bit
Source0:        %{url}uploads/1/5/3/8/15381852/%{name}_linux64_%{version}_release.zip
Source1:        %{url}uploads/1/5/3/8/15381852/%{name}_linux32_%{version}_release.zip
# Get the Windows binary for icon extraction
Source2:        %{url}uploads/1/5/3/8/15381852/%{name}_win32_%{version}_release_unpacked.zip

BuildRequires:  desktop-file-utils
BuildRequires:  /usr/bin/wrestool
BuildRequires:  /usr/bin/convert
BuildRequires:  /usr/bin/file

ExclusiveArch:  %{ix86} x86_64
%global debug_package %{nil}

# Provide a capitalized version as well
Provides:       %{cname}%{?_isa} = %{version}-%{release}

%description
KISSlicer is a fast, easy-to-use, cross-platform program that takes 3D files
(STL) and generates path information (G-code) for a 3D Printer.  This FREE
version has all the features needed for the hobbyist who uses a single-head
machine.

%prep

# Unpack 64bit binary
%ifarch x86_64
%setup -qTc -a0
%endif

# Unpack 32bit binary
%ifarch %{ix86}
%setup -qTc -a1
%endif

# Unpack Windows binary
%setup -qTD -a2


%build
# Extract the icon from the Windows binary
wrestool -x -t 14 %{cname}.exe > %{name}.ico
rm %{cname}.exe
# And convert it to PNGs
for res in 256 128 96 64 48; do
  mkdir -p hicolor/${res}x${res}/apps
done
cd hicolor
convert ../%{name}.ico %{name}.png
mv %{name}-0.png 256x256/apps/%{name}.png
mv %{name}-1.png 128x128/apps/%{name}.png
mv %{name}-2.png 96x96/apps/%{name}.png
mv %{name}-3.png 64x64/apps/%{name}.png
mv %{name}-4.png 48x48/apps/%{name}.png
rm %{name}-*.png
cd -
rm %{name}.ico


%install
# Install the binary into libexec, because it expects user-writable config files right next to it
mkdir -p %{buildroot}%{_libexecdir}
install -pm 0755 %{cname} %{buildroot}%{_libexecdir}/%{cname}

# Shell wrapper that links the binary to home
mkdir -p %{buildroot}%{_bindir}

cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/bin/bash
mkdir -p ~/.%{cname} 2>/dev/null
[ ! -f ~/.%{cname}/%{cname} ] &&
  ln -sf %{_libexecdir}/%{cname} ~/.%{cname}/%{cname}

exec ~/.%{cname}/%{cname} "\$@"
EOF

# Also provides capitalized executable
ln -sf %{name} %{buildroot}%{_bindir}/%{cname}

# Make sure it's executable
chmod 0755 %{buildroot}%{_bindir}/*

# Icons
mkdir -p %{buildroot}%{_datadir}/icons
cp -r hicolor %{buildroot}%{_datadir}/icons

# desktopfile
mkdir -p %{buildroot}%{_datadir}/applications

cat > %{buildroot}%{_datadir}/applications/%{name}.desktop << EOF
[Desktop Entry]
Type=Application
Version=1.0
Name=%{cname}
Comment=%{summary}
Icon=%{name}
TryExec=%{_bindir}/%{name}
Exec=%{_bindir}/%{name} %U
Terminal=false
MimeType=model/x.stl-binary;model/x.stl-ascii;application/sla;application/x-3ds;model/mesh;image/x-3ds;model/x3d+xml;model/x3d+binary;
Categories=Graphics;3DGraphics;
StartupNotify=true
EOF

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop
for RES in $(ls hicolor); do
  file hicolor/$RES/apps/kisslicer.png | grep "$(echo $RES | sed 's/x/ x /')"
done


%files
%{_bindir}/%{name}
%{_bindir}/%{cname}
%{_libexecdir}/%{cname}
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/apps/*


%changelog
* Wed Jan 29 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.6.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.6.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.6.3-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Thu Aug 03 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.6.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.6.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Thu Feb 10 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 1.6.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.6.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.6.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 19 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Thu Jun 11 2020 Sérgio Basto <sergio@serjux.com> - 1.6.3-1
- Update to 1.6.3

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.5-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Aug 10 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.5-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.5-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 1.5-6
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 1.5-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 1.5-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Sep 18 2017 Sérgio Basto <sergio@serjux.com> - 1.5-3
- Fixup rpm setup macro use -a instead -b

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Apr 02 2017 Miro Hrončok <mhroncok@redhat.com> - 1.5-1
- New 1.5 version
- Add new MIME types model/x.stl-binary and model/x.stl-ascii

* Sat Mar 25 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Feb 22 2016 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-1
- Initial package
