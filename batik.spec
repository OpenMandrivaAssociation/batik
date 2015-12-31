%{?_javapackages_macros:%_javapackages_macros}
Name:           batik
Version:        1.8
Release:        0.13.svn1230816%{?dist}
Summary:        Scalable Vector Graphics for Java
License:        ASL 2.0 and W3C
URL:            http://xml.apache.org/batik/
Group:		Development/Java
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
Source8:        %{name}-1.7-orbit-manifests.tar.gz


Patch0:         %{name}-manifests.patch
Patch1:         %{name}-policy.patch
# remove dependency on bundled rhino from pom
Patch2:         %{name}-script-remove-js.patch

# make sure we fail build if javadocs fail (run OOM)
# also make maxmem a bit higher. we seem to need more...
# https://issues.apache.org/jira/browse/BATIK-1065
Patch3:         %{name}-javadoc-task-failonerror-and-oom.patch

BuildArch:      noarch

BuildRequires:  java-devel >= 1:1.6.0
BuildRequires:  javapackages-tools >= 1.5
BuildRequires:  ant
BuildRequires:  subversion
BuildRequires:  zip

BuildRequires:  rhino >= 1.5
BuildRequires:  jpackage-utils >= 1.5
BuildRequires:  xerces-j2
BuildRequires:  xalan-j2
BuildRequires:  xml-commons-apis >= 1.3.04

BuildRequires:  java-javadoc >= 1:1.6.0

Requires:       java >= 1:1.6.0
Requires:       javapackages-tools
#full support for tiff
Requires:       jai-imageio-core
Requires:       rhino >= 1.5
Requires:       xalan-j2
Requires:       xml-commons-apis >= 1.3.04


%description
Batik is a Java(tm) technology based toolkit for applications that want
to use images in the Scalable Vector Graphics (SVG) format for various
purposes, such as viewing, generation or manipulation.

%package        squiggle
Summary:        Batik SVG browser
Group:		Development/Java
Requires:       %{name} = %{version}-%{release}
Requires:       xerces-j2 >= 2.3

%description    squiggle
The Squiggle SVG Browser lets you view SVG file, zoom, pan and rotate
in the content and select text items in the image and much more.

%package        svgpp
Summary:        Batik SVG pretty printer
Group:		Development/Java
Requires:       %{name} = %{version}-%{release}
Requires:       xerces-j2 >= 2.3

%description    svgpp
The SVG Pretty Printer lets developers "pretty-up" their SVG files and
get their tabulations and other cosmetic parameters in order. It can
also be used to modify the DOCTYPE declaration on SVG files.

%package        ttf2svg
Summary:        Batik SVG font converter
Group:		Development/Java
Requires:       %{name} = %{version}-%{release}

%description    ttf2svg
The SVG Font Converter lets developers convert character ranges from
the True Type Font format to the SVG Font format to embed in SVG
documents. This allows SVG document to be fully self-contained be
rendered exactly the same on all systems.

%package        rasterizer
Summary:        Batik SVG rasterizer
Group:		Development/Java
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
Group:		Development/Java
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
popd

# create poms from templates
for module in anim awt-util bridge codec css dom ext extension gui-util \
              gvt parser script svg-dom svggen swing transcoder util xml \
              rasterizer slideshow squiggle svgpp ttf2svg; do
      sed "s:@version@:%{version}:g" sources/%{name}-$module.pom.template \
         > %{name}-$module.pom
done
%patch2

%patch3

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
