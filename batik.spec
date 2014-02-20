%{?_javapackages_macros:%_javapackages_macros}
Name:           batik
Version:        1.8
Release:        0.10.svn1230816.1%{?dist}
Summary:        Scalable Vector Graphics for Java
License:        ASL 2.0 and W3C
URL:            http://xml.apache.org/batik/
#Source0:        http://apache.crihan.fr/dist/xmlgraphics/batik/batik-src-%%{version}.zip
Source0:        %{name}-repack-%{version}.zip
Source1:        %{name}.squiggle.script
Source2:        %{name}.svgpp.script
Source3:        %{name}.ttf2svg.script
Source4:        %{name}.rasterizer.script
Source5:        %{name}.slideshow.script
Source6:        %{name}-squiggle.desktop
Source7:        %{name}-repack.sh

%global inner_version 1.8pre

# These manifests with OSGi metadata are taken from the Eclipse Orbit
# project:  http://download.eclipse.org/tools/orbit/downloads/drops/R20110523182458/
#
# for f in `ls *.jar`; do unzip -d `basename $f .jar | sed s/_.*//` $f; done
# for f in `find -name MANIFEST.MF`; do mv $f $(echo $f | sed "s|./org.apache.||" | sed "s|/META-INF/|-|" | sed "s/\./-/g" | sed "s|MANIFEST-MF|MANIFEST.MF|"); done
# Then manually remove all lines containing MD5sums/crypto hashes.
# tar czf batik-1.6-orbit-manifests.tar.gz *.MF
#
# FIXME:  move to 1.7 manifests
Source8:        %{name}-1.6-orbit-manifests.tar.gz


Patch0:         %{name}-manifests.patch
Patch1:         %{name}-policy.patch
# remove dependency on bundled rhino from pom
Patch2:		%{name}-script-remove-js.patch
# SMIL in Fedora has been merged into xml-commons-apis-ext like it has
# been upstream.  It's easier to take the OSGi manifests from Orbit
# directly and patch this one.
#
# FIXME:  move to 1.7 manifest from Eclipse Orbit project
Patch3:         %{name}-1.6-nosmilInDOMSVGManifest.patch

BuildArch:      noarch

BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  jpackage-utils >= 1.5
BuildRequires:  ant
BuildRequires:  subversion
BuildRequires:  zip

BuildRequires:  rhino >= 1.5
BuildRequires:  jpackage-utils >= 1.5
BuildRequires:  xerces-j2
BuildRequires:  xalan-j2
BuildRequires:  xml-commons-apis >= 1.3.04

BuildRequires:  java-javadoc >= 1:1.6.0
BuildRequires:  rhino-javadoc

Requires:       java >= 1:1.6.0
Requires:       jpackage-utils
#full support for tiff
Requires:	jai-imageio-core
Requires:       rhino >= 1.5
Requires:       xalan-j2
Requires:       xml-commons-apis >= 1.3.04

%description
Batik is a Java(tm) technology based toolkit for applications that want
to use images in the Scalable Vector Graphics (SVG) format for various
purposes, such as viewing, generation or manipulation.

%package        squiggle
Summary:        Batik SVG browser

Requires:       %{name} = %{version}-%{release}
Requires:       xerces-j2 >= 2.3

%description    squiggle
The Squiggle SVG Browser lets you view SVG file, zoom, pan and rotate
in the content and select text items in the image and much more.

%package        svgpp
Summary:        Batik SVG pretty printer

Requires:       %{name} = %{version}-%{release}
Requires:       xerces-j2 >= 2.3

%description    svgpp
The SVG Pretty Printer lets developers "pretty-up" their SVG files and
get their tabulations and other cosmetic parameters in order. It can
also be used to modify the DOCTYPE declaration on SVG files.

%package        ttf2svg
Summary:        Batik SVG font converter

Requires:       %{name} = %{version}-%{release}

%description    ttf2svg
The SVG Font Converter lets developers convert character ranges from
the True Type Font format to the SVG Font format to embed in SVG
documents. This allows SVG document to be fully self-contained be
rendered exactly the same on all systems.

%package        rasterizer
Summary:        Batik SVG rasterizer

Requires:       %{name} = %{version}-%{release}
Requires:       xerces-j2 >= 2.3

%description    rasterizer
The SVG Rasterizer is a utility that can convert SVG files to a raster
format. The tool can convert individual files or sets of files, making
it easy to convert entire directories of SVG files. The supported
formats are JPEG, PNG, and TIFF, however the design allows new formats
to be added easily.

%package        slideshow
Summary:        Batik SVG slideshow

Requires:       %{name} = %{version}-%{release}
Requires:       xerces-j2 >= 2.3

%description    slideshow
Batik SVG slideshow.

%package        javadoc
Summary:        Javadoc for %{name}

%description    javadoc
Javadoc for %{name}.

%package        demo
Summary:        Demo for %{name}
Requires:       %{name} = %{version}-%{release}

%description    demo
Demonstrations and samples for %{name}.


%prep
%setup -q -n %{name}-%{version}

find -name '*.class' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;

%patch0 -p1
%patch1 -p1
rm -f `find -name readOnly.png`
rm -f `find -name properties`
mkdir orbit
pushd orbit
tar xzf %{SOURCE8}
%patch3
popd

# create poms from templates
for module in anim awt-util bridge codec css dom ext extension gui-util \
              gvt parser script svg-dom svggen swing transcoder util xml \
              rasterizer slideshow squiggle svgpp ttf2svg; do
      sed "s:@version@:%{version}:g" sources/%{name}-$module.pom.template \
      	  > %{name}-$module.pom
done
%patch2

%build
export CLASSPATH=$(build-classpath xml-commons-apis xml-commons-apis-ext js rhino xalan-j2 xalan-j2-serializer xerces-j2)
ant all-jar jars\
        -Ddebug=on \
        -Dsun-codecs.present=false \
        -Dsun-codecs.disabled=true \
        svg-pp-jar \
        svg-slideshow-jar \
        squiggle-jar \
        rasterizer-jar \
        ttf2svg-jar

for j in $(find batik-%{version} -name *.jar); do
 export CLASSPATH=$CLASSPATH:${j}
done
ant javadoc


%install
# inject OSGi manifests
mkdir -p META-INF
cp -p orbit/batik-bridge-MANIFEST.MF META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}-%{inner_version}/lib/batik-bridge.jar META-INF/MANIFEST.MF
cp -p orbit/batik-css-MANIFEST.MF META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}-%{inner_version}/lib/batik-css.jar META-INF/MANIFEST.MF
cp -p orbit/batik-dom-MANIFEST.MF META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}-%{inner_version}/lib/batik-dom.jar META-INF/MANIFEST.MF
cp -p orbit/batik-dom-svg-MANIFEST.MF META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}-%{inner_version}/lib/batik-svg-dom.jar META-INF/MANIFEST.MF
cp -p orbit/batik-ext-awt-MANIFEST.MF META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}-%{inner_version}/lib/batik-awt-util.jar META-INF/MANIFEST.MF
cp -p orbit/batik-extension-MANIFEST.MF META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}-%{inner_version}/lib/batik-extension.jar META-INF/MANIFEST.MF
cp -p orbit/batik-parser-MANIFEST.MF META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}-%{inner_version}/lib/batik-parser.jar META-INF/MANIFEST.MF
cp -p orbit/batik-svggen-MANIFEST.MF META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}-%{inner_version}/lib/batik-svggen.jar META-INF/MANIFEST.MF
cp -p orbit/batik-swing-MANIFEST.MF META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}-%{inner_version}/lib/batik-swing.jar META-INF/MANIFEST.MF
cp -p orbit/batik-transcoder-MANIFEST.MF META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}-%{inner_version}/lib/batik-transcoder.jar META-INF/MANIFEST.MF
cp -p orbit/batik-util-gui-MANIFEST.MF META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}-%{inner_version}/lib/batik-gui-util.jar META-INF/MANIFEST.MF
cp -p orbit/batik-util-MANIFEST.MF META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}-%{inner_version}/lib/batik-util.jar META-INF/MANIFEST.MF
cp -p orbit/batik-xml-MANIFEST.MF META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}-%{inner_version}/lib/batik-xml.jar META-INF/MANIFEST.MF


# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
mkdir -p $RPM_BUILD_ROOT%{_javadir}/%{name}
pushd %{name}-%{inner_version}/lib
for jarname in $(find batik-*.jar); do
    cp -p ${jarname} $RPM_BUILD_ROOT%{_javadir}/%{name}/
done

rm -fr $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-all.jar
cp -p %{name}-all.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-all.jar

popd

cp -p %{name}-%{inner_version}/batik-rasterizer.jar \
        %{name}-%{inner_version}/%{name}-slideshow.jar \
        %{name}-%{inner_version}/%{name}-squiggle.jar \
        %{name}-%{inner_version}/%{name}-svgpp.jar \
        %{name}-%{inner_version}/%{name}-ttf2svg.jar \
        $RPM_BUILD_ROOT%{_javadir}

# poms and depmaps for subpackages are different (no batik subdir)
install -d -m 755 $RPM_BUILD_ROOT/%{_mavenpomdir}
for module in rasterizer slideshow squiggle svgpp ttf2svg; do
      install -pm 644 %{name}-$module.pom $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-%{name}-$module.pom
      %add_maven_depmap JPP-%{name}-$module.pom %{name}-$module.jar -a "%{name}:%{name}-$module" -f $module
done

# main pom files and maven depmaps
for module in anim awt-util bridge codec css dom ext extension gui-util \
              gvt parser script svg-dom svggen swing transcoder util xml; do

      install -pm 644 %{name}-$module.pom $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-%{name}-$module.pom
      %add_maven_depmap JPP.%{name}-%{name}-$module.pom %{name}/%{name}-$module.jar -a "%{name}:%{name}-$module"
done




# scripts
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/squiggle
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/svgpp
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/ttf2svg
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_bindir}/rasterizer
cp -p %{SOURCE5} $RPM_BUILD_ROOT%{_bindir}/slideshow

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr %{name}-%{inner_version}/docs/* \
  $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr contrib resources samples test-resources test-sources \
  $RPM_BUILD_ROOT%{_datadir}/%{name}

#Fix perms
chmod +x $RPM_BUILD_ROOT%{_datadir}/%{name}/contrib/rasterizertask/build.sh
chmod +x $RPM_BUILD_ROOT%{_datadir}/%{name}/contrib/charts/convert.sh


%files -f .mfiles
%doc LICENSE NOTICE
%doc KEYS MAINTAIN README
%{_javadir}/%{name}-all.jar
%dir %{_javadir}/batik

%files squiggle -f .mfiles-squiggle
%attr(0755,root,root) %{_bindir}/squiggle

%files svgpp -f .mfiles-svgpp
%attr(0755,root,root) %{_bindir}/svgpp

%files ttf2svg -f .mfiles-ttf2svg
%attr(0755,root,root) %{_bindir}/ttf2svg

%files rasterizer -f .mfiles-rasterizer
%attr(0755,root,root) %{_bindir}/rasterizer

%files slideshow -f .mfiles-slideshow
%attr(0755,root,root) %{_bindir}/slideshow

%files javadoc
%doc LICENSE NOTICE
%{_javadocdir}/%{name}

%files demo
%{_datadir}/%{name}


%changelog
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
