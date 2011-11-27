Name:           batik
Version:        1.7
Release:        14
Summary:        Scalable Vector Graphics for Java
License:        ASL 2.0
URL:            http://xml.apache.org/batik/
Group:          Development/Java
#Source0:        http://apache.crihan.fr/dist/xmlgraphics/batik/batik-src-%%{version}.zip
Source0:        %{name}-repack-%{version}.zip
Source1:        %{name}.squiggle.script
Source2:        %{name}.svgpp.script
Source3:        %{name}.ttf2svg.script
Source4:        %{name}.rasterizer.script
Source5:        %{name}.slideshow.script
Source6:        %{name}-squiggle.desktop
Source7:        %{name}-repack.sh
Source8:        %{name}-orbit-manifests.tar.gz


Patch0:         %{name}-manifests.patch
Patch1:         %{name}-policy.patch
# remove dependency on bundled rhino from pom
Patch2:		%{name}-script-remove-js.patch
Requires:       rhino >= 1.5

BuildArch:      noarch

BuildRequires:  java-devel >= 0:1.6.0
BuildRequires:  jpackage-utils >= 1.5
BuildRequires:  ant
BuildRequires:  ant-nodeps
BuildRequires:  subversion

BuildRequires:  jython
BuildRequires:  rhino >= 1.5
BuildRequires:  jpackage-utils >= 1.5
BuildRequires:  xerces-j2
BuildRequires:  xalan-j2
BuildRequires:  xml-commons-apis >= 1.3.04

BuildRequires:  java-javadoc >= 0:1.6.0
BuildRequires:  rhino-javadoc

BuildRequires:  zip

Requires:       java >= 0:1.6.0
Requires:       rhino >= 1.5
Requires:       xalan-j2
Requires:       xml-commons-apis >= 1.3.04
Requires:       jpackage-utils
Requires(post):    jpackage-utils
Requires(postun):  jpackage-utils



%description
Batik is a Java(tm) technology based toolkit for applications that want
to use images in the Scalable Vector Graphics (SVG) format for various
purposes, such as viewing, generation or manipulation.

%package        squiggle
Summary:        Batik SVG browser
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}
Requires:       jpackage-utils >= 1.5, xerces-j2 >= 2.3

%description    squiggle
The Squiggle SVG Browser lets you view SVG file, zoom, pan and rotate
in the content and select text items in the image and much more.

%package        svgpp
Summary:        Batik SVG pretty printer
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}
Requires:       jpackage-utils >= 1.5, xerces-j2 >= 2.3

%description    svgpp
The SVG Pretty Printer lets developers "pretty-up" their SVG files and
get their tabulations and other cosmetic parameters in order. It can
also be used to modify the DOCTYPE declaration on SVG files.

%package        ttf2svg
Summary:        Batik SVG font converter
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}
Requires:       jpackage-utils >= 1.5

%description    ttf2svg
The SVG Font Converter lets developers convert character ranges from
the True Type Font format to the SVG Font format to embed in SVG
documents. This allows SVG document to be fully self-contained be
rendered exactly the same on all systems.

%package        rasterizer
Summary:        Batik SVG rasterizer
Group:          Development/Java
Requires:       %{name} = %{version}-%{release}
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
Requires:       %{name} = %{version}-%{release}
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
zip -u %{name}-%{version}/lib/batik-bridge.jar META-INF/MANIFEST.MF
cp -p orbit/batik-css-MANIFEST.MF META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}-%{version}/lib/batik-css.jar META-INF/MANIFEST.MF
cp -p orbit/batik-dom-MANIFEST.MF META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}-%{version}/lib/batik-dom.jar META-INF/MANIFEST.MF
cp -p orbit/batik-dom-svg-MANIFEST.MF META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}-%{version}/lib/batik-svg-dom.jar META-INF/MANIFEST.MF
cp -p orbit/batik-ext-awt-MANIFEST.MF META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}-%{version}/lib/batik-awt-util.jar META-INF/MANIFEST.MF
cp -p orbit/batik-extension-MANIFEST.MF META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}-%{version}/lib/batik-extension.jar META-INF/MANIFEST.MF
cp -p orbit/batik-parser-MANIFEST.MF META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}-%{version}/lib/batik-parser.jar META-INF/MANIFEST.MF
cp -p orbit/batik-svggen-MANIFEST.MF META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}-%{version}/lib/batik-svggen.jar META-INF/MANIFEST.MF
cp -p orbit/batik-swing-MANIFEST.MF META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}-%{version}/lib/batik-swing.jar META-INF/MANIFEST.MF
cp -p orbit/batik-transcoder-MANIFEST.MF META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}-%{version}/lib/batik-transcoder.jar META-INF/MANIFEST.MF
cp -p orbit/batik-util-gui-MANIFEST.MF META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}-%{version}/lib/batik-gui-util.jar META-INF/MANIFEST.MF
cp -p orbit/batik-util-MANIFEST.MF META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}-%{version}/lib/batik-util.jar META-INF/MANIFEST.MF
cp -p orbit/batik-xml-MANIFEST.MF META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u %{name}-%{version}/lib/batik-xml.jar META-INF/MANIFEST.MF


# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}
mkdir -p $RPM_BUILD_ROOT%{_javadir}/%{name}
pushd %{name}-%{version}/lib
for jarname in $(find batik-*.jar); do
    cp -p ${jarname} $RPM_BUILD_ROOT%{_javadir}/%{name}/
done

rm -fr $RPM_BUILD_ROOT%{_javadir}/%{name}/%{name}-all.jar
cp -p %{name}-all.jar $RPM_BUILD_ROOT%{_javadir}/%{name}-all.jar

popd

cp -p %{name}-%{version}/batik-rasterizer.jar \
        %{name}-%{version}/%{name}-slideshow.jar \
        %{name}-%{version}/%{name}-squiggle.jar \
        %{name}-%{version}/%{name}-svgpp.jar \
        %{name}-%{version}/%{name}-ttf2svg.jar \
        $RPM_BUILD_ROOT%{_javadir}

# poms and depmaps for subpackages are different (no batik subdir)
install -d -m 755 $RPM_BUILD_ROOT/%{_mavenpomdir}
for module in rasterizer slideshow squiggle svgpp ttf2svg; do
      install -pm 644 %{name}-$module.pom $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-%{name}-$module.pom
      %add_to_maven_depmap org.apache.xmlgraphics %{name}-$module %{version} JPP %{name}-$module
      # compatibility depmap
      %add_to_maven_depmap batik %{name}-$module %{version} JPP %{name}-$module
      mv $RPM_BUILD_ROOT%{_mavendepmapfragdir}/%{name} $RPM_BUILD_ROOT%{_mavendepmapfragdir}/%{name}-$module
done

# main pom files and maven depmaps
for module in anim awt-util bridge codec css dom ext extension gui-util \
              gvt parser script svg-dom svggen swing transcoder util xml; do

      install -pm 644 %{name}-$module.pom $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP.%{name}-%{name}-$module.pom
      %add_to_maven_depmap org.apache.xmlgraphics %{name}-$module %{version} JPP/%{name} %{name}-$module
      # compatibility depmap
      %add_to_maven_depmap batik %{name}-$module %{version} JPP/%{name} %{name}-$module
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
cp -pr %{name}-%{version}/docs/* \
  $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr contrib resources samples test-resources test-sources \
  $RPM_BUILD_ROOT%{_datadir}/%{name}

#Fix perms
chmod +x $RPM_BUILD_ROOT%{_datadir}/%{name}/contrib/rasterizertask/build.sh
chmod +x $RPM_BUILD_ROOT%{_datadir}/%{name}/contrib/charts/convert.sh

%post
%update_maven_depmap

%postun
%update_maven_depmap

%post squiggle
%update_maven_depmap

%postun squiggle
%update_maven_depmap

%post svgpp
%update_maven_depmap

%postun svgpp
%update_maven_depmap

%post ttf2svg
%update_maven_depmap

%postun ttf2svg
%update_maven_depmap

%post rasterizer
%update_maven_depmap

%postun rasterizer
%update_maven_depmap

%post slideshow
%update_maven_depmap

%postun slideshow
%update_maven_depmap

%pre javadoc
# workaround for rpm bug, can be removed in F-17
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :


%files
%doc KEYS LICENSE MAINTAIN NOTICE README
%{_mavenpomdir}/JPP.%{name}-*pom
%{_mavendepmapfragdir}/%{name}
%{_javadir}/%{name}-all.jar
%{_javadir}/batik

%files squiggle
%{_javadir}/%{name}-squiggle.jar
%{_mavendepmapfragdir}/%{name}-squiggle
%{_mavenpomdir}/JPP-%{name}-squiggle.pom
%attr(0755,root,root) %{_bindir}/squiggle

%files svgpp
%{_javadir}/%{name}-svgpp.jar
%{_mavendepmapfragdir}/%{name}-svgpp
%{_mavenpomdir}/JPP-%{name}-svgpp.pom
%attr(0755,root,root) %{_bindir}/svgpp

%files ttf2svg
%{_javadir}/%{name}-ttf2svg.jar
%{_mavendepmapfragdir}/%{name}-ttf2svg
%{_mavenpomdir}/JPP-%{name}-ttf2svg.pom
%attr(0755,root,root) %{_bindir}/ttf2svg

%files rasterizer
%{_javadir}/%{name}-rasterizer.jar
%{_mavendepmapfragdir}/%{name}-rasterizer
%{_mavenpomdir}/JPP-%{name}-rasterizer.pom
%attr(0755,root,root) %{_bindir}/rasterizer

%files slideshow
%{_javadir}/%{name}-slideshow.jar
%{_mavendepmapfragdir}/%{name}-slideshow
%{_mavenpomdir}/JPP-%{name}-slideshow.pom
%attr(0755,root,root) %{_bindir}/slideshow

%files javadoc
%{_javadocdir}/%{name}

%files demo
%{_datadir}/%{name}


