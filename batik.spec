%define gcj_support 1

Name:           batik
Version:        1.7
Release:        %mkrel 0.1.1
Epoch:          0
Summary:        Scalable Vector Graphics for Java
License:        Apache License
URL:            http://xml.apache.org/batik/
Group:          Development/Java
Source0:        %{name}-src-%{version}.zip
Source1:        %{name}.squiggle.script
Source2:        %{name}.svgpp.script
Source3:        %{name}.ttf2svg.script
Source4:        %{name}.rasterizer.script
Source5:        %{name}.slideshow.script
Source6:        %{name}-squiggle.desktop
Patch0:         %{name}-sun-codecs.patch
Patch1:         %{name}-manifests.patch
Patch2:         %{name}-policy.patch
Requires:       rhino >= 1.5
Requires:       xml-commons-apis >= 1.3.04

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:  ant
BuildRequires:  rhino >= 1.5
BuildRequires:  java-rpmbuild >= 1.5
BuildRequires:  xerces-j2
BuildRequires:  jython
BuildRequires:  java-javadoc
BuildRequires:  rhino-javadoc
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
BuildArch:      noarch
%endif

%description
Batik is a Java(tm) technology based toolkit for applications that want
to use images in the Scalable Vector Graphics (SVG) format for various
purposes, such as viewing, generation or manipulation.

%package        squiggle
Summary:        Batik SVG browser
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       jpackage-utils >= 1.5, xerces-j2 >= 2.3

%description    squiggle
The Squiggle SVG Browser lets you view SVG file, zoom, pan and rotate
in the content and select text items in the image and much more.

%package        svgpp
Summary:        Batik SVG pretty printer
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       jpackage-utils >= 1.5, xerces-j2 >= 2.3

%description    svgpp
The SVG Pretty Printer lets developers "pretty-up" their SVG files and
get their tabulations and other cosmetic parameters in order. It can
also be used to modify the DOCTYPE declaration on SVG files.

%package        ttf2svg
Summary:        Batik SVG font converter
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       jpackage-utils >= 1.5

%description    ttf2svg
The SVG Font Converter lets developers convert character ranges from
the True Type Font format to the SVG Font format to embed in SVG
documents. This allows SVG document to be fully self-contained be
rendered exactly the same on all systems.

%package        rasterizer
Summary:        Batik SVG rasterizer
Group:          Development/Java
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       jpackage-utils >= 1.5, xerces-j2 >= 2.3

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
Requires:       jpackage-utils >= 1.5, xerces-j2 >= 2.3

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
%setup -q -n %{name}-%{version}
%patch0 -p0
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
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
cp -p %{name}-%{version}/lib/%{name}-all.jar \
       $RPM_BUILD_ROOT%{_javadir}/%{name}-all-%{version}.jar
cp -p %{name}-%{version}/batik-rasterizer.jar \
        %{name}-%{version}/batik-slideshow.jar \
        %{name}-%{version}/batik-squiggle.jar \
        %{name}-%{version}/batik-svgpp.jar \
        %{name}-%{version}/batik-ttf2svg.jar \
        $RPM_BUILD_ROOT%{_javadir}
pushd $RPM_BUILD_ROOT%{_javadir}
  for jar in *-%{version}*; 
    do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; 
  done
popd

# scripts
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/squiggle
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/svgpp
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/ttf2svg
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_bindir}/rasterizer
cp -p %{SOURCE5} $RPM_BUILD_ROOT%{_bindir}/slideshow

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr %{name}-%{version}/docs/javadoc/* \
  $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version} || :
rm -rf %{name}-%{version}/docs/javadoc
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr contrib resources samples test-resources test-sources \
  $RPM_BUILD_ROOT%{_datadir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

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


%changelog
* Fri Nov 23 2007 Lillian Angel <langel at redhat.com> - 1.7-0.1.beta1
- Fixed rpmlint errors.

* Tue Sep 18 2007 Joshua Sumali <jsumali at redhat.com> - 0:1.7-1
- Update to batik 1.7 beta1

* Thu Feb 22 2007 Ralph Apel <r.apel at r-apel.de> - 0:1.6-3jpp
- Add gcj_support option
- Add option to avoid rhino, jython on bootstrap, omit -squiggle subpackage

* Wed Apr 26 2006 Fernando Nasser <fnasser@redhat.com> - 0:1.6-2jpp
- First JPP 1.7 build

* Tue Aug  2 2005 Ville Skyttä <scop at jpackage.org> - 0:1.6-1jpp
- 1.6.
- Fix build of manual (java.awt.headless for stylebook).

* Fri Jan 28 2005 Jason Corley - 0:1.5.1-1jpp
- Update to 1.5.1

* Mon Nov 22 2004 Ville Skyttä <scop at jpackage.org> - 0:1.5-5jpp
- Drop -monolithic and obsolete it in main package.  It shouldn't be needed
  in the first place, and the *.policy files that end up in it will contain
  wrong paths which causes all sorts of borkage.
- BuildRequire jython to get support for it built.
- Remove xml-commons-apis and xalan-j2 from scripts and install time
  dependencies, require Java >= 1.4 instead (xalan-j2 is still needed at
  build time).
- New style versionless javadoc dir symlinking.
- Crosslink with full J2SE javadocs.
- Associate SVG MIME type with Squiggle in freedesktop.org menu entry.

* Fri Aug 20 2004 Ralph Apel <r.apel at r-apel.de> - 0:1.5-4jpp
- Build with ant-1.6.2

* Mon Nov 03 2003 Paul Nasrat <pauln at truemesh.com> - 0:1.5-3jpp
- Fix non-versioned javadoc symlinks

* Fri Aug 15 2003 Ville Skyttä <scop at jpackage.org> - 0:1.5-2jpp
- Fix jar names in policy files, kudos to Scott Douglas-Watson.
- Add freedesktop.org menu entry for Squiggle.
- Improve subpackage descriptions.
- Save .spec in UTF-8, get rid of # ------- separators.

* Sat Jul 19 2003 Ville Skyttä <scop at jpackage.org> - 0:1.5-1jpp
- Update to 1.5.
- Crosslink with xml-commons-apis and rhino javadocs.

* Thu Apr 17 2003 Ville Skyttä <scop at jpackage.org> - 0:1.5-0.beta5.2jpp
- Rebuild to satisfy dependencies due to renamed rhino (r4 -> R4).

* Sun Mar 30 2003 Ville Skyttä <scop at jpackage.org> - 1.5-0.beta5.1jpp
- Update to 1.5 beta5.
- Rebuild for JPackage 1.5.
- Use bundled crimson and stylebook for building the manual.

* Tue May 07 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.1.1-4jpp
- vendor, distribution, group tags
- scripts use system prefs
- scripts source user prefs before configuration

* Thu Mar 28 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.1.1-3jpp
- libs package is now monolithic package

* Sun Jan 27 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.1.1-2jpp
- adaptation to new stylebook1.0b3 package

* Mon Jan 21 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.1.1-1jpp
- 1.1.1
- additional sources in individual archives
- no dependencies for manual and javadoc packages
- stricter dependency for demo package
- versioned dir for javadoc
- explicitely set xalan-j2.jar and xml-commons-api.jar in classpath
- splitted applications in distinct packages

* Wed Dec 5 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.1-0.rc4.3jpp
- javadoc into javadoc package
- new launch scripts using functions library
- Requires jpackage-utils
- added name-slideshow.jar
- main jar renamed name.jar

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 1.1-0.rc4.2jpp
- fixed previous changelog
- changed extension --> jpp

* Tue Nov 20 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 1.1-0.rc4.1jpp
- rc4

* Sat Nov 17 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 1.1-0.rc3.2jpp
- added batik-libs creation

* Thu Nov 9 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 1.1-0.rc3.1jpp
- changed version to 0.rc3.1

* Mon Nov 5 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 1.1rc3-1jpp
- 1.1rc3

* Sat Oct 6 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-4jpp
- first unified release
- removed xalan-j2 from classpath as it is autoloaded by stylebook-1.0b3
- used original tarball
- s/jPackage/JPackage

* Mon Sep 17 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-3mdk
- provided *working* startup scripts

* Sat Sep 15 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-2mdk
- requires specificaly crimson
- only manual buildrequires stylebook-1.0b3 and xerces-j1
- dropped xalan-j2 buildrequires as stylebook-1.0b3 needs it already
- changed samples package name to demo
- moved demo files to _datadir/name
- provided startup scripts

* Thu Aug 30 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 1.0-1mdk
- first Mandrake release
