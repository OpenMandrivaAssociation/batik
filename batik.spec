%define gcj_support 0

Summary:	Scalable Vector Graphics for Java
Name:		batik
Version:	1.7
Release:	%mkrel 0.1.5
Epoch:		0
Group:		Development/Java
License:	Apache License
URL:		http://xml.apache.org/batik/
Source0:	%{name}-src-%{version}.zip
Source1:	%{name}.squiggle.script
Source2:	%{name}.svgpp.script
Source3:	%{name}.ttf2svg.script
Source4:	%{name}.rasterizer.script
Source5:	%{name}.slideshow.script
Source6:	%{name}-squiggle.desktop
Patch1:		%{name}-manifests.patch
Patch2:		%{name}-policy.patch
Requires:	rhino >= 0:1.5
Requires:	xml-commons-jaxp-1.3-apis >= 0:1.3.04
BuildRequires:	ant
BuildRequires:	rhino >= 0:1.5
BuildRequires:	java-rpmbuild >= 0:1.5
BuildRequires:	xerces-j2
BuildRequires:	jython
BuildRequires:	java-javadoc
BuildRequires:	rhino-javadoc
BuildRequires:	xml-commons-jaxp-1.3-apis >= 0:1.3.04
%if %{gcj_support}
BuildRequires:	java-gcj-compat-devel
%else
BuildArch:	noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Batik is a Java(tm) technology based toolkit for applications that want
to use images in the Scalable Vector Graphics (SVG) format for various
purposes, such as viewing, generation or manipulation.

%package        squiggle
Summary:        Batik SVG browser
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       jpackage-utils >= 0:1.5, xerces-j2 >= 0:2.3

%description    squiggle
The Squiggle SVG Browser lets you view SVG file, zoom, pan and rotate
in the content and select text items in the image and much more.

%package        svgpp
Summary:        Batik SVG pretty printer
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       jpackage-utils >= 0:1.5, xerces-j2 >= 0:2.3

%description    svgpp
The SVG Pretty Printer lets developers "pretty-up" their SVG files and
get their tabulations and other cosmetic parameters in order. It can
also be used to modify the DOCTYPE declaration on SVG files.

%package        ttf2svg
Summary:        Batik SVG font converter
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       jpackage-utils >= 0:1.5

%description    ttf2svg
The SVG Font Converter lets developers convert character ranges from
the True Type Font format to the SVG Font format to embed in SVG
documents. This allows SVG document to be fully self-contained be
rendered exactly the same on all systems.

%package        rasterizer
Summary:        Batik SVG rasterizer
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       jpackage-utils >= 0:1.5, xerces-j2 >= 0:2.3

%description    rasterizer
The SVG Rasterizer is a utility that can convert SVG files to a raster
format. The tool can convert individual files or sets of files, making
it easy to convert entire directories of SVG files. The supported
formats are JPEG, PNG, and TIFF, however the design allows new formats
to be added easily.

%package        slideshow
Summary:        Batik SVG slideshow
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       jpackage-utils >= 0:1.5, xerces-j2 >= 0:2.3

%description    slideshow
Batik SVG slideshow.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Java

%description    javadoc
Javadoc for %{name}.

%package        demo
Summary:        Demo for %{name}
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    demo
Demonstrations and samples for %{name}.

%prep
%setup -q
%patch1 -p1
%patch2 -p1
rm -f `find -name readOnly.png`
rm -f `find -name properties`


%build
export CLASSPATH
export OPT_JAR_LIST=:
%{ant} all-jar \
        javadoc \
        svg-pp-jar \
        svg-slideshow-jar \
        squiggle-jar \
        rasterizer-jar \
        ttf2svg-jar

%install
rm -rf %{buildroot}

# jars
mkdir -p %{buildroot}%{_javadir}
cp -p %{name}-%{version}/lib/%{name}-all.jar \
       %{buildroot}%{_javadir}/%{name}-all-%{version}.jar
cp -p %{name}-%{version}/batik-rasterizer.jar \
        %{name}-%{version}/batik-slideshow.jar \
        %{name}-%{version}/batik-squiggle.jar \
        %{name}-%{version}/batik-svgpp.jar \
        %{name}-%{version}/batik-ttf2svg.jar \
        %{buildroot}%{_javadir}
pushd %{buildroot}%{_javadir}
  for jar in *-%{version}*; 
    do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; 
  done
popd

# scripts
mkdir -p %{buildroot}%{_bindir}
cp -p %{SOURCE1} %{buildroot}%{_bindir}/squiggle
cp -p %{SOURCE2} %{buildroot}%{_bindir}/svgpp
cp -p %{SOURCE3} %{buildroot}%{_bindir}/ttf2svg
cp -p %{SOURCE4} %{buildroot}%{_bindir}/rasterizer
cp -p %{SOURCE5} %{buildroot}%{_bindir}/slideshow

# javadoc
mkdir -p %{buildroot}%{_javadocdir}/%{name}-%{version}
cp -pr %{name}-%{version}/docs/javadoc/* \
  %{buildroot}%{_javadocdir}/%{name}-%{version} || :
rm -rf %{name}-%{version}/docs/javadoc
ln -s %{name}-%{version} %{buildroot}%{_javadocdir}/%{name}

# demo
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -pr contrib resources samples test-resources test-sources \
  %{buildroot}%{_datadir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf %{buildroot}

%if %{gcj_support}
%post
%{update_gcjdb}

%postun
%{clean_gcjdb}
%endif

%files
%defattr(-,root,root,-)
%doc KEYS LICENSE MAINTAIN NOTICE README
%{_javadir}/%{name}-all-%{version}.jar
%{_javadir}/%{name}-all.jar
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%{_libdir}/gcj/%{name}/*
%endif
%files squiggle
%defattr(-,root,root,-)
%{_javadir}/%{name}-squiggle.jar
%attr(0755,root,root) %{_bindir}/squiggle

%files svgpp
%defattr(-,root,root,-)
%{_javadir}/%{name}-svgpp.jar
%attr(0755,root,root) %{_bindir}/svgpp

%files ttf2svg
%defattr(-,root,root,-)
%{_javadir}/%{name}-ttf2svg.jar
%attr(0755,root,root) %{_bindir}/ttf2svg

%files rasterizer
%defattr(-,root,root,-)
%{_javadir}/%{name}-rasterizer.jar
%attr(0755,root,root) %{_bindir}/rasterizer

%files slideshow
%defattr(-,root,root,-)
%{_javadir}/%{name}-slideshow.jar
%attr(0755,root,root) %{_bindir}/slideshow

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files demo
%defattr(-,root,root,-)
%{_datadir}/%{name}
%attr(0755,root,root) %{_datadir}/%{name}/contrib/rasterizertask/build.sh 
%attr(0755,root,root) %{_datadir}/%{name}/contrib/charts/convert.sh
