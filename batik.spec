# Copyright (c) 2000-2007, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}
%define bootstrap %{?_with_bootstrap:1}%{!?_with_bootstrap:%{?_without_bootstrap:0}%{!?_without_bootstrap:%{?_bootstrap:%{_bootstrap}}%{!?_bootstrap:0}}}

%define section free

Name:           batik
Version:        1.6
Release:        %mkrel 3
Epoch:          0
Summary:        Scalable Vector Graphics for Java
License:        Apache Software License
URL:            http://xml.apache.org/batik/
Group:          Multimedia/Graphics
Vendor:         JPackage Project
Distribution:   JPackage
Source0:        http://archive.apache.org/dist/xml/batik/%{name}-src-%{version}.zip
Source1:        %{name}.squiggle.script
Source2:        %{name}.svgpp.script
Source3:        %{name}.ttf2svg.script
Source4:        %{name}.rasterizer.script
Source5:        %{name}.slideshow.script
Source6:        %{name}-squiggle.desktop
Patch0:         %{name}-javadoc-crosslink.patch
Patch1:         %{name}-stylebook-headless.patch
Requires:       java >= 0:1.4
Obsoletes:      batik-monolithic < 0:1.5-5jpp
BuildRequires:  ant
BuildRequires:  jpackage-utils >= 0:1.6
BuildRequires:  xerces-j2
%if ! %{bootstrap}
BuildRequires:  jython
BuildRequires:  rhino >= 0:1.5
BuildRequires:  rhino-javadoc
Requires:       rhino >= 0:1.5
%endif
BuildRequires:  java-javadoc
BuildRequires:  %{__perl}
BuildRequires:  java-devel >= 0:1.4
%if ! %{gcj_support}
BuildArch:      noarch
%endif
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-buildroot
%if %{gcj_support}
BuildRequires:    gnu-crypto
BuildRequires:    java-gcj-compat-devel
Requires(post):   java-gcj-compat
Requires(postun): java-gcj-compat
%endif


%description
Batik is a Java(tm) technology based toolkit for applications that want
to use images in the Scalable Vector Graphics (SVG) format for various
purposes, such as viewing, generation or manipulation.
The project's ambition is to give developers a set of core modules
which can be used together or individually to support specific SVG
solutions. Example modules are, SVG parsers, SVG generators and SVG DOM
implementations. Another ambition for the Batik project is to make it
highly extensible (for example, Batik allows the developer to handle
custom SVG tags). Even though the goal of the project is to provide a
set of core modules, one of the deliverables is a full fledged SVG
browser implementation which validates the various modules and their
interoperability.

%if ! %{bootstrap}
%package        squiggle
Summary:        Batik SVG browser
Group:          Multimedia/Graphics
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       jpackage-utils >= 0:1.6, xerces-j2
Obsoletes:      %{name}-svgbrowser
%if %{gcj_support}
Requires(post):   java-gcj-compat
Requires(postun): java-gcj-compat
%endif

%description    squiggle
The Squiggle SVG Browser lets you view SVG file, zoom, pan and rotate
in the content and select text items in the image and much more.
%endif

%package        svgpp
Summary:        Batik SVG pretty printer
Group:          Multimedia/Graphics
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       jpackage-utils >= 0:1.6, xerces-j2
%if %{gcj_support}
Requires(post):   java-gcj-compat
Requires(postun): java-gcj-compat
%endif

%description    svgpp
The SVG Pretty Printer lets developers "pretty-up" their SVG files and
get their tabulations and other cosmetic parameters in order. It can
also be used to modify the DOCTYPE declaration on SVG files.

%package        ttf2svg
Summary:        Batik SVG font converter
Group:          Multimedia/Graphics
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       jpackage-utils >= 0:1.6
%if %{gcj_support}
Requires(post):   java-gcj-compat
Requires(postun): java-gcj-compat
%endif

%description    ttf2svg
The SVG Font Converter lets developers convert character ranges from
the True Type Font format to the SVG Font format to embed in SVG
documents. This allows SVG document to be fully self-contained be
rendered exactly the same on all systems.

%package        rasterizer
Summary:        Batik SVG rasterizer
Group:          Multimedia/Graphics
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       jpackage-utils >= 0:1.6, xerces-j2
%if %{gcj_support}
Requires(post):   java-gcj-compat
Requires(postun): java-gcj-compat
%endif

%description    rasterizer
The SVG Rasterizer is a utility that can convert SVG files to a raster
format. The tool can convert individual files or sets of files, making
it easy to convert entire directories of SVG files. The supported
formats are JPEG, PNG, and TIFF, however the design allows new formats
to be added easily.

%package        slideshow
Summary:        Batik SVG slideshow
Group:          Multimedia/Graphics
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       jpackage-utils >= 0:1.6, xerces-j2
%if %{gcj_support}
Requires(post):   java-gcj-compat
Requires(postun): java-gcj-compat
%endif

%description    slideshow
Batik SVG slideshow.

%package        manual
Summary:        Manual for %{name}
Group:          Multimedia/Graphics
BuildRequires:  xalan-j2
#BuildRequires: stylebook1.0b3, xerces-j1

%description    manual
Documentation for %{name}.

%package        javadoc
Summary:        Javadoc for %{name}
Group:          Development/Documentation
Requires(post):   /bin/rm,/bin/ln
Requires(postun): /bin/rm

%description    javadoc
Javadoc for %{name}.

%package        demo
Summary:        Demo for %{name}
Group:          Development/Documentation
Requires:       %{name} = %{epoch}:%{version}-%{release}

%description    demo
Demonstrations and samples for %{name}.


%prep
%setup -q -n xml-%{name}
%patch0 -p0
%patch1 -p0

# Clean up manifest files.
%{__perl} -pi -e 's/^.*\.jar\b.*$//s' sources/*.mf

# Remove all binary libs, except the ones used to build the manual.
find . -name "*.jar" -a ! -name "stylebook*" -a ! -name "crimson*" \
  -exec rm -f {} \;

# Fix up linefeeds and jar names in policy files.
%{__perl} -pi -e \
  's|(\r(\n)?)+|\n|g ;
   s|\blib/||g ;
   s|\bbatik-||g ;
   s|\bxerces.*?\.jar|../xerces-j2.jar|g ;
   s|\bjs.*?\.jar|../rhino.jar|g' \
  `find . -type f -name "*.policy"`

%if %{bootstrap}
# omit squiggle on bootstrap
rm -rf sources/org/apache/batik/apps/svgbrowser
%endif

%build
# stylebook1.0b3 xerces-j1
%if %{bootstrap}
export CLASSPATH=$(build-classpath xerces-j2 xalan-j2)
ant \
  -Dbuild.sysclasspath=first \
  -Djdk.javadoc=%{_javadocdir}/java \
  jars html
%else
export CLASSPATH=$(build-classpath rhino xerces-j2 xalan-j2 jython)
ant \
  -Dbuild.sysclasspath=first \
  -Djdk.javadoc=%{_javadocdir}/java \
  -Drhino.javadoc=%{_javadocdir}/rhino \
  jars html
%endif


%install
rm -rf $RPM_BUILD_ROOT

# jars
mkdir -p $RPM_BUILD_ROOT%{_javadir}/%{name}
%if ! %{bootstrap}
cp -p %{name}-%{version}/%{name}-squiggle.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/squiggle-%{version}.jar
%endif
cp -p %{name}-%{version}/%{name}-svgpp.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/svgpp-%{version}.jar
cp -p %{name}-%{version}/%{name}-ttf2svg.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/ttf2svg-%{version}.jar
cp -p %{name}-%{version}/%{name}-rasterizer.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/rasterizer-%{version}.jar
cp -p %{name}-%{version}/%{name}-slideshow.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/slideshow-%{version}.jar
cp -p %{name}-%{version}/lib/%{name}-awt-util.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/awt-util-%{version}.jar
cp -p %{name}-%{version}/lib/%{name}-bridge.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/bridge-%{version}.jar
cp -p %{name}-%{version}/lib/%{name}-css.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/css-%{version}.jar
cp -p %{name}-%{version}/lib/%{name}-dom.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/dom-%{version}.jar
cp -p %{name}-%{version}/lib/%{name}-extension.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/extension-%{version}.jar
cp -p %{name}-%{version}/lib/%{name}-ext.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/ext-%{version}.jar
cp -p %{name}-%{version}/lib/%{name}-gui-util.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/gui-util-%{version}.jar
cp -p %{name}-%{version}/lib/%{name}-gvt.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/gvt-%{version}.jar
cp -p %{name}-%{version}/lib/%{name}-parser.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/parser-%{version}.jar
cp -p %{name}-%{version}/lib/%{name}-script.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/script-%{version}.jar
cp -p %{name}-%{version}/lib/%{name}-svg-dom.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/svg-dom-%{version}.jar
cp -p %{name}-%{version}/lib/%{name}-svggen.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/svggen-%{version}.jar
cp -p %{name}-%{version}/lib/%{name}-swing.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/swing-%{version}.jar
cp -p %{name}-%{version}/lib/%{name}-transcoder.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/transcoder-%{version}.jar
cp -p %{name}-%{version}/lib/%{name}-util.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/util-%{version}.jar
cp -p %{name}-%{version}/lib/%{name}-xml.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/xml-%{version}.jar
cp -p %{name}-%{version}/extensions/%{name}-rasterizer-ext.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/rasterizer-ext-%{version}.jar
%if ! %{bootstrap}
cp -p %{name}-%{version}/extensions/%{name}-squiggle-ext.jar \
  $RPM_BUILD_ROOT%{_javadir}/%{name}/squiggle-ext-%{version}.jar
%endif
(cd $RPM_BUILD_ROOT%{_javadir}/%{name} && for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed "s|-%{version}||g"`; done)

# scripts
mkdir -p $RPM_BUILD_ROOT%{_bindir}
%if ! %{bootstrap}
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_bindir}/squiggle
%endif
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/svgpp
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_bindir}/ttf2svg
cp -p %{SOURCE4} $RPM_BUILD_ROOT%{_bindir}/rasterizer
cp -p %{SOURCE5} $RPM_BUILD_ROOT%{_bindir}/slideshow

# javadoc
mkdir -p $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr %{name}-%{version}/docs/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
rm -rf %{name}-%{version}/docs/javadoc
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

# demo
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -pr contrib resources samples test-resources test-sources \
  $RPM_BUILD_ROOT%{_datadir}/%{name}

%if ! %{bootstrap}
# freedesktop.org menu entry
install -D -p -m 755 %{SOURCE6} \
  $RPM_BUILD_ROOT%{_datadir}/applications/jpackage-squiggle.desktop
install -D -p -m 644 \
  resources/org/apache/batik/apps/svgbrowser/resources/squiggleIcon.png \
  $RPM_BUILD_ROOT%{_datadir}/pixmaps/squiggle.png
%endif

%if %{gcj_support}
export CLASSPATH=$(build-classpath gnu-crypto)
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
    rm -f %{_javadocdir}/%{name}
fi

%if %{gcj_support}
%post
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if ! %{bootstrap}
%if %{gcj_support}
%post squiggle
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun squiggle
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif
%endif

%if %{gcj_support}
%post svgpp
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun svgpp
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%post ttf2svg
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun ttf2svg
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%post rasterizer
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun rasterizer
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%post slideshow
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%if %{gcj_support}
%postun slideshow
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE MAINTAIN NOTICE README
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/awt-util-%{version}.jar
%{_javadir}/%{name}/awt-util.jar
%{_javadir}/%{name}/bridge-%{version}.jar
%{_javadir}/%{name}/bridge.jar
%{_javadir}/%{name}/css-%{version}.jar
%{_javadir}/%{name}/css.jar
%{_javadir}/%{name}/dom-%{version}.jar
%{_javadir}/%{name}/dom.jar
%{_javadir}/%{name}/extension-%{version}.jar
%{_javadir}/%{name}/extension.jar
%{_javadir}/%{name}/ext-%{version}.jar
%{_javadir}/%{name}/ext.jar
%{_javadir}/%{name}/gui-util-%{version}.jar
%{_javadir}/%{name}/gui-util.jar
%{_javadir}/%{name}/gvt-%{version}.jar
%{_javadir}/%{name}/gvt.jar
%{_javadir}/%{name}/parser-%{version}.jar
%{_javadir}/%{name}/parser.jar
%{_javadir}/%{name}/script-%{version}.jar
%{_javadir}/%{name}/script.jar
%{_javadir}/%{name}/svg-dom-%{version}.jar
%{_javadir}/%{name}/svg-dom.jar
%{_javadir}/%{name}/svggen-%{version}.jar
%{_javadir}/%{name}/svggen.jar
%{_javadir}/%{name}/swing-%{version}.jar
%{_javadir}/%{name}/swing.jar
%{_javadir}/%{name}/transcoder-%{version}.jar
%{_javadir}/%{name}/transcoder.jar
%{_javadir}/%{name}/util-%{version}.jar
%{_javadir}/%{name}/util.jar
%{_javadir}/%{name}/xml-%{version}.jar
%{_javadir}/%{name}/xml.jar
%if %{gcj_support}
%dir %attr(-,root,root) %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/awt-util-%{version}.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/bridge-%{version}.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/css-%{version}.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/dom-%{version}.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/extension-%{version}.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/ext-%{version}.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/gui-util-%{version}.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/gvt-%{version}.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/parser-%{version}.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/script-%{version}.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/svg-dom-%{version}.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/svggen-%{version}.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/swing-%{version}.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/transcoder-%{version}.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/util-%{version}.jar.*
%attr(-,root,root) %{_libdir}/gcj/%{name}/xml-%{version}.jar.*
%endif


%if ! %{bootstrap}
%files squiggle
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/squiggle
%{_javadir}/%{name}/squiggle*.jar
%{_datadir}/applications/*squiggle.desktop
%{_datadir}/pixmaps/squiggle.png
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/squiggle-%{version}.jar.*
%endif
%endif

%files svgpp
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/svgpp
%{_javadir}/%{name}/svgpp*.jar
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/svgpp-%{version}.jar.*
%endif

%files ttf2svg
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/ttf2svg
%{_javadir}/%{name}/ttf2svg*.jar
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/ttf2svg-%{version}.jar.*
%endif

%files rasterizer
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/rasterizer
%{_javadir}/%{name}/rasterizer*.jar
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/rasterizer-%{version}.jar.*
%endif

%files slideshow
%defattr(0644,root,root,0755)
%attr(0755,root,root) %{_bindir}/slideshow
%{_javadir}/%{name}/slideshow*.jar
%if %{gcj_support}
%attr(-,root,root) %{_libdir}/gcj/%{name}/slideshow-%{version}.jar.*
%endif

%files manual
%defattr(0644,root,root,0755)
%doc %{name}-%{version}/docs/*

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%ghost %doc %{_javadocdir}/%{name}

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}
