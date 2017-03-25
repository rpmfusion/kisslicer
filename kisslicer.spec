Name:           kisslicer
%global cname   KISSlicer
%global maj     1
%global min     1
%global rev     0
Version:        %{maj}.%{min}.%{rev}
Release:        2%{?dist}
Summary:        Keep It Simple Slicer
URL:            http://www.kisslicer.com/

# License information: http://www.kisslicer.com/download.html "MAY be shared freely"
License:        Redistributable, no modification permitted

# Download for both 64 and 32 bit
Source0:        %{url}/files/%{maj}%{min}%{rev}/%{cname}_Linux64_%{maj}_%{min}_%{rev}.zip
Source1:        %{url}/files/%{maj}%{min}%{rev}/%{cname}_Linux32_%{maj}_%{min}_%{rev}.zip
# Get the Windows binary for icon extraction
Source2:        %{url}/files/%{maj}%{min}%{rev}/%{cname}_Win32_%{maj}_%{min}_%{rev}.zip

BuildRequires:  desktop-file-utils
BuildRequires:  /usr/bin/wrestool
BuildRequires:  /usr/bin/convert

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
%setup -qTc -b0
%endif

# Unpack 32bit binary
%ifarch %{ix86}
%setup -qTc -b1
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
MimeType=application/sla;application/x-3ds;model/mesh;image/x-3ds;model/x3d+xml;model/x3d+binary;
Categories=Graphics;3DGraphics;
StartupNotify=true
EOF

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/%{name}.desktop

%post
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
/usr/bin/update-desktop-database &>/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi
/usr/bin/update-desktop-database &>/dev/null || :

%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-desktop-database &>/dev/null || :

%files
%{_bindir}/%{name}
%{_bindir}/%{cname}
%{_libexecdir}/%{cname}
%{_datadir}/applications/*
%{_datadir}/icons/hicolor/*/apps/*


%changelog
* Sat Mar 25 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 1.1.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Feb 22 2016 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-1
- Initial package
