%{?_javapackages_macros:%_javapackages_macros}
%global classpath batik:rhino:xml-commons-apis:xml-commons-apis-ext:xmlgraphics-commons:jai_imageio

Name:           batik
Version:        1.9
Release:        3.2
Summary:        Scalable Vector Graphics for Java
License:        ASL 2.0 and W3C
Group:          Development/Java
URL:            https://xmlgraphics.apache.org/batik/
Source0:        http://archive.apache.org/dist/xmlgraphics/batik/source/batik-src-%{version}.zip
Source1:        %{name}-security.policy

Patch1:         0001-Fix-imageio-codec-lookup.patch

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(junit:junit)
BuildRequires:  mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:  mvn(org.apache.xmlgraphics:xmlgraphics-commons)
BuildRequires:  mvn(org.mozilla:rhino)
BuildRequires:  mvn(org.python:jython)
BuildRequires:  mvn(xalan:xalan)
BuildRequires:  mvn(xml-apis:xml-apis)
BuildRequires:  mvn(xml-apis:xml-apis-ext)

# full support for tiff
Requires:       jai-imageio-core

%description
Batik is a Java(tm) technology based toolkit for applications that want
to use images in the Scalable Vector Graphics (SVG) format for various
purposes, such as viewing, generation or manipulation.

%package css
Summary:        Batik CSS engine
Obsoletes:      %{name} < 1.8-0.17.svn1230816

%description css
CSS component of the Apache Batik SVG manipulation and rendering library.

%package        squiggle
Summary:        Batik SVG browser

%description    squiggle
The Squiggle SVG Browser lets you view SVG file, zoom, pan and rotate
in the content and select text items in the image and much more.

%package        svgpp
Summary:        Batik SVG pretty printer

%description    svgpp
The SVG Pretty Printer lets developers "pretty-up" their SVG files and
get their tabulations and other cosmetic parameters in order. It can
also be used to modify the DOCTYPE declaration on SVG files.

%package        ttf2svg
Summary:        Batik SVG font converter

%description    ttf2svg
The SVG Font Converter lets developers convert character ranges from
the True Type Font format to the SVG Font format to embed in SVG
documents. This allows SVG document to be fully self-contained be
rendered exactly the same on all systems.

%package        rasterizer
Summary:        Batik SVG rasterizer

%description    rasterizer
The SVG Rasterizer is a utility that can convert SVG files to a raster
format. The tool can convert individual files or sets of files, making
it easy to convert entire directories of SVG files. The supported
formats are JPEG, PNG, and TIFF, however the design allows new formats
to be added easily.

%package        slideshow
Summary:        Batik SVG slideshow

%description    slideshow
Batik SVG slideshow.

%package        javadoc
Summary:        Javadoc for %{name}

%description    javadoc
Javadoc for %{name}.

%package        demo
Summary:        Samples for %{name}
Requires:       %{name} = %{version}-%{release}

%description    demo
Demonstrations and samples for %{name}.


%prep
%setup -q -n %{name}-%{version}

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

%patch1 -p1

cp -p %{SOURCE1} batik-svgrasterizer/src/main/resources/org/apache/batik/apps/rasterizer/resources/rasterizer.policy
cp -p %{SOURCE1} batik-svgbrowser/src/main/resources/org/apache/batik/apps/svgbrowser/resources/svgbrowser.policy

# We don't want a dependency
%pom_xpath_inject 'pom:dependency[pom:artifactId="jython"]' '<optional>true</optional>' batik-script

# It's an uberjar, it shouldn't have requires
%pom_xpath_inject pom:dependency '<optional>true</optional>' batik-all

# eclipse expects xmlgraphics to be optional
%pom_xpath_inject 'pom:dependency[pom:artifactId="xmlgraphics-commons"]' '<optional>true</optional>' batik-css

# eclipse expects it there
cp -pr batik-i18n/src/main/java/org/apache/batik/i18n batik-util/src/main/java/org/apache/batik/
%pom_remove_dep :batik-i18n batik-util

for pom in `find -mindepth 2 -name pom.xml -not -path ./batik-all/pom.xml`; do
    %pom_add_plugin org.apache.felix:maven-bundle-plugin $pom "
        <extensions>true</extensions>
        <configuration>
            <instructions>
                <Bundle-SymbolicName>org.apache.batik.$(sed 's:./batik-::;s:/pom.xml::' <<< $pom)</Bundle-SymbolicName>
                <!-- To prevent breaking eclipse -->
                <Bundle-Version>1.7.0</Bundle-Version>
            </instructions>
        </configuration>
    "
    %pom_xpath_inject pom:project '<packaging>bundle</packaging>' $pom
done

# for eclipse
%pom_xpath_set pom:Bundle-SymbolicName org.apache.batik.util.gui batik-gui-util

%mvn_package :batik-squiggle squiggle
%mvn_package :batik-squiggle-ext squiggle
%mvn_package :batik-svgpp svgpp
%mvn_package :batik-ttf2svg ttf2svg
%mvn_package :batik-rasterizer rasterizer
%mvn_package :batik-rasterizer-ext rasterizer
%mvn_package :batik-slideshow slideshow
%mvn_package :batik-css css

%mvn_file :batik-all batik-all

%build
%mvn_build

%install
%mvn_install

%jpackage_script org.apache.batik.apps.svgbrowser.Main '' '' %{classpath} squiggle true
%jpackage_script org.apache.batik.apps.svgpp.Main '' '' %{classpath} svgpp true
%jpackage_script org.apache.batik.apps.ttf2svg.Main '' '' %{classpath} ttf2svg true
%jpackage_script org.apache.batik.apps.rasterizer.Main '' '' %{classpath} rasterizer true
%jpackage_script org.apache.batik.apps.slideshow.Main '' '' %{classpath} slideshow true

# Demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}/
cp -pr samples $RPM_BUILD_ROOT%{_datadir}/%{name}/


%files -f .mfiles
%doc LICENSE NOTICE
%doc CHANGES MAINTAIN README

%files css -f .mfiles-css

%files squiggle -f .mfiles-squiggle
%{_bindir}/squiggle

%files svgpp -f .mfiles-svgpp
%{_bindir}/svgpp

%files ttf2svg -f .mfiles-ttf2svg
%{_bindir}/ttf2svg

%files rasterizer -f .mfiles-rasterizer
%{_bindir}/rasterizer

%files slideshow -f .mfiles-slideshow
%{_bindir}/slideshow

%files javadoc -f .mfiles-javadoc
%doc LICENSE NOTICE

%files demo
%{_datadir}/%{name}


%changelog
* Thu May 04 2017 Michael Simacek <msimacek@redhat.com> - 1.9-3
- Suppress requires from batik-all uberjar

* Wed Apr 26 2017 Michael Simacek <msimacek@redhat.com> - 1.9-2
- Fix OSGi metadata generation and eclipse compatibility

* Thu Apr 20 2017 Michael Simacek <msimacek@redhat.com> - 1.9-1
- Update to upstream version 1.9
- Fixes CVE-2017-5662

* Wed Apr 19 2017 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8-8
- Add missing requires on xmlgraphics-commons
- Resolves: rhbz#1443567

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.8-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Tue Dec 01 2015 Michael Simacek <msimacek@redhat.com> - 1.8-5
- Add jai to classpath of remaining scripts

* Fri Nov 27 2015 Michael Simacek <msimacek@redhat.com> - 1.8-4
- Fix imageio codec lookup
- Add jai-imageio-core on rasterizer's classpath

* Fri Nov 27 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8-3
- Use custom security policy files
- Fix rasterizer and squiggle classpath
- Resolves: rhbz#1277998

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu May 21 2015 Alexander Kurtakov <akurtako@redhat.com> 1.8-1
- Update to 1.8 final.

* Wed May 13 2015 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8-0.18.svn1230816
- Disable javadoc doclint

* Mon Jan 12 2015 Alexander Kurtakov <akurtako@redhat.com> 1.8-0.17.svn1230816
- Add obsoletes in batik-css to ease updates.

* Mon Dec 8 2014 Alexander Kurtakov <akurtako@redhat.com> 1.8-0.16.svn1230816
- Split css in subpackage.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-0.15.svn1230816
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Wed Mar 05 2014 Roland Grunberg <rgrunber@redhat.com> - 1.8-0.14.svn1230816
- Remove provenance=W3C attribute from Import-Package. (rhbz #1073110)

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.8-0.13.svn1230816
- Use Requires: java-headless rebuild (#1067528)

* Sun Feb 23 2014 Alexander Kurtakov <akurtako@redhat.com> 1.8-0.12.svn1230816
- Move to Batik 1.7 manifests.
- Remove old stuff.

* Thu Jan 16 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.8-0.11.svn1230816
- Fix classpath for slideshow script
- Change javadoc task maxmem to 512MB to avoid OOM

* Thu Aug 08 2013 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.8-0.10.svn1230816
- Update to latest packaging guidelines

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-0.9.svn1230816
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8-0.8.svn1230816
- Remove BR: ant-nodeps

* Fri Jun 28 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8-0.8.svn1230816
- Rebuild to regenerate API documentation
- Resolves: CVE-2013-1571

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-0.7.svn1230816
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Nov 20 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8-0.6.svn1230816
- Remove unneeded BR: jython

* Fri Oct  5 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8-0.5.svn1230816
- Fix rasterizer classpath
- Resolves: rhbz#577486

* Fri Aug 24 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8-0.4.svn1230816
- Fix license tag
- Install LICENSE and NOTICE with javadoc package
- Remove RPM bug workaround
- Update to current packaging guidelines

* Thu Jul 19 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.8-0.3.svn1230816
- Add BR: zip

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8-0.2.svn1230816
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Mon Feb 20 2012 Jiri Vanek <jvanek@redhat.com> 1.7-14
- Solving jdk7's  removed internal (since 1.4.2 deprecated) com.sun.image.codec package
- Gripped new sources from 1.8pre trunk which have support adapters for removed classes,
- Removed all old an unused tiff classes from it -  org.apache.batik.ext.awt.image.code.tiff
- Added requires JAI which provides tiff support
- Added inner_version variable, which helps to keep 1.8 outside and 1.8pre inside

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Fri Jul 8 2011 Andrew Overholt <overholt@redhat.com> 1.7-12
- New OSGi manifests from Eclipse Orbit.

* Tue May  3 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.7-11
- Add maven metadata and pom files
- Versionless jars & javadocs

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Oct 25 2010 Alexander Kurtakov <akurtako@redhat.com> 1.7-9
- Fix utilities startup scripts.

* Fri Oct 1 2010 Alexander Kurtakov <akurtako@redhat.com> 1.7-8
- Fix build.

* Fri Oct 1 2010 Alexander Kurtakov <akurtako@redhat.com> 1.7-7
- BR/R java 1.6.0 not java-openjdk.
- Cleanup build section.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Jul 15 2009 Lillian Angel <langel@redhat.com> - 1.7-5
- Fixed javadocs issue.
- Resolves: rhbz#511767

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.7-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Fri Feb 6 2009 Alexander Kurtakov <akurtako@redhat.com> 1.7-3
- Install separate jars and put OSGi manifests in them.

* Tue Jan 06 2009 Lillian Angel  <langel@redhat.com> - 1.7-2
- Fixed java dependencies to check for java-1.6.0-openjdk instead.

* Mon Jan 05 2009 Lillian Angel  <langel@redhat.com> - 1.7-1
- Updated batik-repack.sh to remove font files from test resources.
- Resolves: rhbz#477369

* Mon Jan 05 2009 Nicolas Chauvet <kwizart@gmail.com> - 1.7-1
- Fix release field
- Repack the source (without included jar files)
- Fix dual listed files in the demo subpackage
- Fix BR subversion used in determine-svn-revision-svn-info
- Fix BR that was previously bundled within the source archive
- Resolves: rhbz#472736

* Fri Nov 28 2008 Lillian Angel <langel at redhat.com> - 1.7-0.7
- Fixed BASE_JARS in batik.rasterizer.script.
- Resolves: rhbz#455397

* Mon Apr 28 2008 Lillian Angel <langel at redhat.com> - 1.7-0.5.beta1
- Fixed BASE_JARS in batik-squiggle.script.
- Resolves: rhbz#444358

* Mon Mar 31 2008 Lillian Angel <langel at redhat.com> - 1.7-0.2.beta1
- Updated sources.
- Updated release.
- Added CLASSPATH to build.
- Removed codecs patch.

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

* Fri Nov 9 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 1.1-0.rc3.1jpp
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
