#
# TODO:
# - gconf peer? (BR: GConf2-devel >= 2.6.0) (but libgcj needs split anyway)
# - gstreamer peer? (BR: gstreamer-devel, gstreamer-plugins-base-devel >= 0.10.10)
# - restore qt peer?
# - package?
#   /usr/bin/gjdoc [BR: antlr.jar] (but see gjdoc package, there are some additional jars?)
#   /usr/share/man/man1/gjdoc.1.gz
#
# Conditional build:
%bcond_with	base		# create base packages
# - languages:
%bcond_without	cxx		# build without C++ support
%bcond_without	java		# build without Java support
# - features:
%bcond_without	gomp		# build without OpenMP support
%bcond_without	multilib	# build without multilib support (which needs glibc[32&64]-devel)
%bcond_without	multilibx32	# build with x32 multilib support on x86_64 (needs x32 glibc-devel)
%bcond_without	profiling	# build without profiling
%bcond_without	python		# build without libstdc++ printers for gdb and aot-compile for java
# - libgcj options:
%bcond_without	alsa		# don't build libgcj ALSA MIDI interface
%bcond_without	dssi		# don't build libgcj DSSI MIDI interface
%bcond_without	gtk		# don't build libgcj GTK peer
%bcond_without	apidocs		# do not build and package API docs
%bcond_with	mozilla		# build libgcjwebplugin (needs fix for new xulrunner)
%bcond_with	qt		# build libgcj Qt peer (currently doesn't build with libtool-2.x)
%bcond_without	x		# don't build libgcj Xlib-dependent AWTs (incl. GTK/Qt)
# - other:
%bcond_without	bootstrap	# omit 3-stage bootstrap
%bcond_with	tests		# torture gcc
%bcond_with	symvers		# enable versioned symbols in libstdc++ (WARNING: changes soname from .so.6 to so.7)

%if %{with symvers}
%define		cxx_sover	7
%else
%define		cxx_sover	6
%endif

# java requires C++
%if %{without cxx}
%undefine	with_java
%endif

%if %{without bootstrap}
%undefine	with_profiling
%endif

%if %{without x}
%undefine	with_gtk
%undefine	with_qt
%endif

%ifnarch %{x8664} x32 aarch64 ppc64 s390x sparc64
%undefine	with_multilib
%endif
%ifnarch %{x8664}
%undefine	with_multilibx32
%endif

# setup internal semi-bconds based on bconds and architecture
%if %{with multilib}
%ifarch x32
%define		with_multilib2	1
%endif
%if %{with multilibx32}
%define		with_multilib2	1
%endif
%endif
%ifarch %{ix86} %{x8664} x32 alpha %{arm} ppc ppc64 sh sparc sparcv9 sparc64
# library for atomic operations not supported by hardware
%define		with_atomic	1
%endif
%ifarch %{ix86} %{x8664} x32
%define		with_cilkrts	1
%endif
%ifarch %{ix86} %{x8664} x32
%define		with_vtv	1
%endif

%define		major_ver	6
%define		minor_ver	5.0
%define		ecj_ver		4.9
# class data version seen with file(1) that this jvm is able to load
%define		_classdataversion 50.0
%define		gcj_soname_ver	17

Summary:	GNU Compiler Collection: the C compiler and shared files
Summary(es.UTF-8):	Colección de compiladores GNU: el compilador C y ficheros compartidos
Summary(pl.UTF-8):	Kolekcja kompilatorów GNU: kompilator C i pliki współdzielone
Summary(pt_BR.UTF-8):	Coleção dos compiladores GNU: o compilador C e arquivos compartilhados
Name:		gcc6-java
Version:	%{major_ver}.%{minor_ver}
Release:	1
Epoch:		6
License:	GPL v3+
Group:		Development/Languages
Source0:	https://ftp.gnu.org/pub/gnu/gcc/gcc-%{version}/gcc-%{version}.tar.xz
# Source0-md5:	edaeff1cc020b16a0c19a6d5e80dc2fd
Source1:	gcc-optimize-la.pl
Source4:	branch.sh
# use branch.sh to update gcc-branch.diff
Patch100:	gcc-branch.diff
# Patch100-md5:	5ad5a566cbaf57f985192534e5ef1c32
Patch0:		gcc-info.patch
Patch2:		gcc-nodebug.patch

Patch7:		gcc-libjava-multilib.patch
Patch8:		gcc-enable-java-awt-qt.patch
Patch10:	gcc-moresparcs.patch
URL:		http://gcc.gnu.org/
BuildRequires:	autoconf >= 2.64
%{?with_tests:BuildRequires:	autogen >= 5.5.4}
BuildRequires:	automake >= 1:1.11.1
BuildRequires:	binutils >= 3:2.23
BuildRequires:	bison
BuildRequires:	chrpath >= 0.13-2
%{?with_tests:BuildRequires:	dejagnu >= 1.4.4}
BuildRequires:	elfutils-devel >= 0.145-1
BuildRequires:	fileutils >= 4.0.41
BuildRequires:	flex >= 2.5.4
BuildRequires:	gdb
BuildRequires:	gettext-tools >= 0.14.5
BuildRequires:	glibc-devel >= 6:2.4-1
%if %{with multilib}
# Formerly known as gcc(multilib)
BuildRequires:	gcc(multilib-32)
%ifarch %{x8664}
%if %{with multilibx32}
BuildRequires:	gcc(multilib-x32)
BuildRequires:	glibc-devel(x32)
%endif
BuildRequires:	glibc-devel(ix86)
%endif
%ifarch x32
BuildRequires:	gcc(multilib-64)
BuildRequires:	glibc-devel(ix86)
BuildRequires:	glibc-devel(x86_64)
%endif
%ifarch aarch64
BuildRequires:	glibc-devel(arm)
%endif
%ifarch ppc64
BuildRequires:	glibc-devel(ppc)
%endif
%ifarch s390x
BuildRequires:	glibc-devel(s390)
%endif
%ifarch sparc64
BuildRequires:	glibc-devel(sparcv9)
%endif
%endif
BuildRequires:	gmp-c++-devel >= 4.3.2
BuildRequires:	gmp-devel >= 4.3.2
BuildRequires:	isl-devel >= 0.15
BuildRequires:	java-ecj >= %{ecj_ver}
BuildRequires:	libmpc-devel >= 0.8.1
BuildRequires:	mpfr-devel >= 2.4.2
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
%endif
BuildRequires:	rpmbuild(macros) >= 1.211
BuildRequires:	tar >= 1:1.22
BuildRequires:	texinfo >= 4.7
BuildRequires:	xz
BuildRequires:	zlib-devel
%if %{with java}
%{?with_alsa:BuildRequires:	alsa-lib-devel}
%if %{with dssi}
BuildRequires:	dssi-devel
BuildRequires:	jack-audio-connection-kit-devel
%endif
BuildRequires:	libtool >= 2:2
BuildRequires:	libxml2-devel >= 1:2.6.8
BuildRequires:	libxslt-devel >= 1.1.11
BuildRequires:	perl-base
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
BuildRequires:	zip
%if %{with gtk}
BuildRequires:	cairo-devel >= 1.1.8
BuildRequires:	freetype-devel >= 2
BuildRequires:	gdk-pixbuf2-devel >= 2.0
BuildRequires:	gtk+2-devel >= 2:2.8
BuildRequires:	libart_lgpl-devel >= 2.1
BuildRequires:	pango-devel
BuildRequires:	xorg-lib-libXrandr-devel
BuildRequires:	xorg-lib-libXrender-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xorg-lib-libXtst-devel
%endif
%if %{with qt}
BuildRequires:	QtCore-devel >= 4.1.0
BuildRequires:	QtGui-devel >= 4.1.0
BuildRequires:	qt4-build >= 4.1.0
%endif
%{?with_mozilla:BuildRequires:	xulrunner-devel >= 1.8.1.3-1.20070321.5}
%endif
BuildConflicts:	pdksh < 5.2.14-50
Requires:	binutils >= 3:2.23
Requires:	gmp >= 4.3.2
Requires:	isl >= 0.15
Requires:	libgcc >= %{epoch}:%{version}-%{release}
Requires:	libmpc >= 0.8.1
Requires:	mpfr >= 2.4.2
Provides:	cpp = %{epoch}:%{version}-%{release}
Obsoletes:	cpp
Obsoletes:	egcs-cpp
Obsoletes:	gcc-chill
Obsoletes:	gcc-cpp
Obsoletes:	gcc-ksi
Obsoletes:	gcc4
Obsoletes:	gont
Conflicts:	glibc-devel < 2.2.5-20
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_slibdir	/%{_lib}
%if %{with multilib}
# 32-bit environment on x86-64,aarch64,ppc64,s390x,sparc64
%define		_slibdir32	/lib
%define		_libdir32	/usr/lib
%define		_pkgconfigdir32	%{_libdir32}/pkgconfig
%if %{with multilib2}
# x32 environment on x86-64
%ifarch %{x8664}
%define		multilib2	x32
%define		m2_desc		ILP32
%define		_slibdirm2	/libx32
%define		_libdirm2	/usr/libx32
%define		_pkgconfigdirm2	%{_libdirm2}/pkgconfig
%endif
# 64-bit environment on x32
%ifarch x32
%define		multilib2	64
%define		m2_desc		LP64
%define		_slibdirm2	/lib64
%define		_libdirm2	/usr/lib64
%define		_pkgconfigdirm2	%{_libdir64}/pkgconfig
%endif
%endif
%endif
%define		gcclibdir	%{_libdir}/gcc/%{_target_platform}/%{version}
%define		gcjdbexecdir	gcj-%{version}-%{gcj_soname_ver}

%define		filterout	-fwrapv -fno-strict-aliasing -fsigned-char
%define		filterout_ld	-Wl,--as-needed

# functions with printf format attribute but with special parser and also
# receiving non constant format strings
%define		Werror_cflags	%{nil}

%define		skip_post_check_so	'.*(libcc1plugin|libxmlj|lib-gnu-awt-xlib|libmpxwrappers)\.so.*'
# private symbols
%define		_noautoreq		.*\(GLIBC_PRIVATE\)

%description
A compiler aimed at integrating all the optimizations and features
necessary for a high-performance and stable development environment.

This package contains the C compiler and some files shared by various
parts of the GNU Compiler Collection. In order to use another GCC
compiler you will need to install the appropriate subpackage.

%description -l es.UTF-8
Un compilador que intenta integrar todas las optimalizaciones y
características necesarias para un entorno de desarrollo eficaz y
estable.

Este paquete contiene el compilador de C y unos ficheros compartidos
por varias partes de la colección de compiladores GNU (GCC). Para usar
otro compilador de GCC será necesario que instale el subpaquete
adecuado.

%description -l pl.UTF-8
Kompilator, posiadający duże możliwości optymalizacyjne niezbędne do
wyprodukowania szybkiego i stabilnego kodu wynikowego.

Ten pakiet zawiera kompilator C i pliki współdzielone przez różne
części kolekcji kompilatorów GNU (GCC). Żeby używać innego kompilatora
z GCC, trzeba zainstalować odpowiedni podpakiet.

%description -l pt_BR.UTF-8
Este pacote adiciona infraestrutura básica e suporte a linguagem C ao
GNU Compiler Collection.

%package multilib-32
Summary:	GNU Compiler Collection: the C compiler 32-bit support
Summary(pl.UTF-8):	Kolekcja kompilatorów GNU: obsługa binariów 32-bitowych dla kompilatora C
License:	GPL v3+
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libgcc-multilib-32 >= %{epoch}:%{version}-%{release}
Obsoletes:	libgcc32
%ifarch %{x8664}
Requires:	glibc-devel(ix86)
%endif
%ifarch ppc64
Requires:	glibc-devel(ppc)
%endif
%ifarch s390x
Requires:	glibc-devel(s390)
%endif
%ifarch sparc64
Requires:	glibc-devel(sparcv9)
%endif
Provides:	gcc(multilib-32)
Obsoletes:	gcc-multilib

%description multilib-32
A compiler aimed at integrating all the optimizations and features
necessary for a high-performance and stable development environment.

This package contains the C compiler support for producing 32-bit
programs on 64-bit host.

%description multilib-32 -l pl.UTF-8
Kompilator, posiadający duże możliwości optymalizacyjne niezbędne do
wyprodukowania szybkiego i stabilnego kodu wynikowego.

Ten pakiet zawiera rozszerzenie kompilatora C o obsługę tworzenia
programów 32-bitowych na maszynie 64-bitowej.

%package multilib-%{multilib2}
Summary:	GNU Compiler Collection: the C compiler %{m2_desc} binaries support
Summary(pl.UTF-8):	Kolekcja kompilatorów GNU: obsługa binariów %{m2_desc} dla kompilatora C
License:	GPL v3+
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libgcc-multilib-%{multilib2} = %{epoch}:%{version}-%{release}
%{?with_multilib:Provides:	gcc(multilib-%{multilib2})}
%ifarch %{x8664}
Requires:	glibc-devel(x32)
%endif
%ifarch x32
Requires:	glibc-devel(x86_64)
%endif

%description multilib-%{multilib2}
A compiler aimed at integrating all the optimizations and features
necessary for a high-performance and stable development environment.

This package contains the C compiler support for producing %{m2_desc}
binaries.

%description multilib-%{multilib2} -l pl.UTF-8
Kompilator, posiadający duże możliwości optymalizacyjne niezbędne do
wyprodukowania szybkiego i stabilnego kodu wynikowego.

Ten pakiet zawiera rozszerzenie kompilatora C o obsługę tworzenia
binariów %{m2_desc}.

%package c++
Summary:	C++ language support for GCC
Summary(es.UTF-8):	Soporte de C++ para GCC
Summary(pl.UTF-8):	Obsługa języka C++ dla GCC
Summary(pt_BR.UTF-8):	Suporte C++ para o GCC
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}
Obsoletes:	egcc-c++
Obsoletes:	egcs-c++
Obsoletes:	gcc4-c++

%description c++
This package adds C++ support to the GNU Compiler Collection. It
includes support for most of the current C++ specification, including
templates and exception handling. It does not include a standard C++
library, which is available separately.

%description c++ -l de.UTF-8
Dieses Paket enthält die C++-Unterstützung für den
GNU-Compiler-Collection. Es unterstützt die aktuelle
C++-Spezifikation, inkl. Templates und Ausnahmeverarbeitung. Eine
C++-Standard-Library ist nicht enthalten - sie ist getrennt
erhältlich.

%description c++ -l es.UTF-8
Este paquete añade soporte de C++ al GCC (colección de compiladores
GNU). Ello incluye el soporte para la mayoría de la especificación
actual de C++, incluyendo plantillas y manejo de excepciones. No
incluye la biblioteca estándar de C++, la que es disponible separada.

%description c++ -l fr.UTF-8
Ce package ajoute un support C++ a la collection de compilateurs GNU.
Il comprend un support pour la plupart des spécifications actuelles de
C++, dont les modéles et la gestion des exceptions. Il ne comprend pas
une bibliothéque C++ standard, qui est disponible séparément.

%description c++ -l pl.UTF-8
Ten pakiet dodaje obsługę C++ do kompilatora GCC. Wspiera większość
obecnej specyfikacji C++, nie zawiera natomiast standardowych
bibliotek C++, które są w oddzielnym pakiecie.

%description c++ -l pt_BR.UTF-8
Este pacote adiciona suporte C++ para o gcc.

%description c++ -l tr.UTF-8
Bu paket, GNU C derleyicisine C++ desteği ekler. 'Template'ler ve
aykırı durum işleme gibi çoğu güncel C++ tanımlarına uyar. Standart
C++ kitaplığı bu pakette yer almaz.

%package c++-multilib-32
Summary:	C++ language 32-bit binaries support for GCC
Summary(pl.UTF-8):	Obsługa 32-bitowych binariów w języku C++ dla GCC
Group:		Development/Languages
Requires:	%{name}-c++ = %{epoch}:%{version}-%{release}
Requires:	%{name}-multilib-32 = %{epoch}:%{version}-%{release}
Obsoletes:	gcc-c++-multilib

%description c++-multilib-32
This package adds 32-bit binaries in C++ language support to the GNU
Compiler Collection.

%description c++-multilib-32 -l pl.UTF-8
Ten pakiet dodaje obsługę 32-bitowych binariów w języku C++ do
kompilatora GCC.

%package c++-multilib-%{multilib2}
Summary:	C++ language %{m2_desc} binaries support for GCC
Summary(pl.UTF-8):	Obsługa %{multilib2}-bitowych binariów C++ dla GCC
Group:		Development/Languages
Requires:	%{name}-c++ = %{epoch}:%{version}-%{release}
Requires:	%{name}-multilib-%{multilib2} = %{epoch}:%{version}-%{release}

%description c++-multilib-%{multilib2}
This package adds %{m2_desc} binaries in C++ language support to the GNU
Compiler Collection.

%description c++-multilib-%{multilib2} -l pl.UTF-8
Ten pakiet dodaje obsługę binariów %{m2_desc} w języku C++ do kompilatora
GCC.

%package -n gcc-java
Summary:	Java language support for GCC
Summary(es.UTF-8):	Soporte de Java para GCC
Summary(pl.UTF-8):	Obsługa języka Java dla GCC
Group:		Development/Languages/Java
Requires:	gcc >= %{epoch}:%{version}-%{release}
Requires:	java-ecj >= %{ecj_ver}
Requires:	libgcj-devel = %{epoch}:%{version}-%{release}
Provides:	gcc-java-tools
Provides:	gcj = %{epoch}:%{version}-%{release}
Obsoletes:	gcc-java-tools
Obsoletes:	java-gnu-classpath-tools

%description -n gcc-java
This package adds experimental support for compiling Java(TM) programs
and bytecode into native code. To use this you will also need the
libgcj package.

%description -n gcc-java -l es.UTF-8
Este paquete añade soporte experimental para compilar programas
Java(tm) y su bytecode en código nativo. Para usarlo también va a
necesitar el paquete libgcj.

%description -n gcc-java -l pl.UTF-8
Ten pakiet dodaje możliwość kompilowania programów w języku Java(TM)
oraz bajtkodu do kodu natywnego. Do używania go wymagany jest
dodatkowo pakiet libgcj.

%package -n gcc-java-aotcompile
Summary:	Java AOT-compiler - compiling bytecode to native
Summary(pl.UTF-8):	Kompilator AOT dla Javy - kompilacja bajtkodu do kodu natywnego
License:	GPL v2+
Group:		Development/Tools
Requires:	gcc-java = %{epoch}:%{version}-%{release}

%description -n gcc-java-aotcompile
aot-compile is a script that searches a directory for Java bytecode
(as class files, or in jars) and uses gcj to compile it to native code
and generate the databases from it.

%description -n gcc-java-aotcompile -l pl.UTF-8
aot-compile to skrypt wyszukujący w katalogu bajtkod Javy (w plikach
class lub jarach) i kompilujący go przy użyciu gcj, a następnie
generujący z niego bazy danych.

%package -n libgcj
Summary:	Java Class Libraries
Summary(es.UTF-8):	Bibliotecas de clases de Java
Summary(pl.UTF-8):	Biblioteki klas Javy
License:	GPL v2+ with limited linking exception
Group:		Libraries
Requires:	jpackage-utils
Requires:	libstdc++ >= %{epoch}:%{version}-%{release}
Requires:	libxml2 >= 1:2.6.8
Requires:	libxslt >= 1.1.11
%if %{with gtk}
Requires:	cairo >= 1.1.8
Requires:	gtk+2 >= 2:2.8
Requires:	libart_lgpl >= 2.1
%endif
%if %{with qt}
Requires:	QtCore >= 4.1.0
Requires:	QtGui >= 4.1.0
%endif
Provides:	java(ClassDataVersion) = %{_classdataversion}
Obsoletes:	libgcj3

%description -n libgcj
Java Class Libraries.

%description -n libgcj -l es.UTF-8
Bibliotecas de clases de Java.

%description -n libgcj -l pl.UTF-8
Biblioteki klas Javy.

%package -n libgcj-devel
Summary:	Development files for Java Class Libraries
Summary(es.UTF-8):	Ficheros de desarrollo para las bibliotecas de clases de Java
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek klas Javy
License:	GPL v2+ with limited linking exception
Group:		Development/Libraries
Requires:	libgcj = %{epoch}:%{version}-%{release}
Requires:	libstdc++-devel >= %{epoch}:%{version}-%{release}
Requires:	zlib-devel
Obsoletes:	libgcj3-devel

%description -n libgcj-devel
Development files for Java Class Libraries.

%description -n libgcj-devel -l es.UTF-8
Ficheros de desarrollo para las bibliotecas de clases de Java.

%description -n libgcj-devel -l pl.UTF-8
Pliki nagłówkowe bibliotek klas Javy.

%package -n libgcj-static
Summary:	Static Java Class Libraries
Summary(es.UTF-8):	Bibliotecas estáticas de clases de Java
Summary(pl.UTF-8):	Statyczne biblioteki klas Javy
License:	GPL v2+ with limited linking exception
Group:		Development/Libraries
Requires:	libgcj-devel = %{epoch}:%{version}-%{release}

%description -n libgcj-static
Static Java Class Libraries.

%description -n libgcj-static -l es.UTF-8
Bibliotecas estáticas de clases de Java.

%description -n libgcj-static -l pl.UTF-8
Statyczne biblioteki klas Javy.

%package gdb-plugin
Summary:	GCC plugin for GDB
Summary(pl.UTF-8):	Wtyczka GCC dla GDB
Group:		Development/Debuggers
Requires:	%{name} = %{epoch}:%{version}-%{release}

%description gdb-plugin
This package contains GCC plugin for GDB C expression evaluation.

%description gdb-plugin -l pl.UTF-8
Ten pakiet zawiera wtyczkę GCC do obliczania wyrażeń języka C w GDB.

%package plugin-devel
Summary:	Support for compiling GCC plugins
Summary(pl.UTF-8):	Obsługa kompilowania wtyczek GCC
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	gmp-devel >= 4.3.2
Requires:	libmpc-devel >= 0.8.1
Requires:	mpfr-devel >= 2.4.2

%description plugin-devel
This package contains header files and other support files for
compiling GCC plugins. The GCC plugin ABI is currently not stable, so
plugins must be rebuilt any time GCC is updated.

%description plugin-devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe oraz inne pozwalające na
kompilowanie wtyczek GCC. ABI wtyczek GCC nie jest obecnie stabilne,
więc wtyczki muszą być przebudowywane przy każdej aktualizacji GCC.

%prep
%setup -q -n gcc-%{version}
%patch100 -p0
%patch0 -p1
%patch2 -p1

%patch7 -p0
%if %{with qt}
%patch8 -p1
%endif
%patch10 -p1

%{__mv} ChangeLog ChangeLog.general

# override snapshot version.
echo %{version} > gcc/BASE-VER
echo "release" > gcc/DEV-PHASE

%build
cd gcc
#{__autoconf}
cd ..
%if %{with qt}
cd libjava/classpath
%{__autoconf}
cd ../..
%endif
cp -f /usr/share/automake/config.sub .

rm -rf builddir && install -d builddir && cd builddir

# http://www.mailinglistarchive.com/java%40gcc.gnu.org/msg02751.html
export JAR=no

CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcxxflags}" \
TEXCONFIG=false \
../configure \
	--prefix=%{_prefix} \
	--with-local-prefix=%{_prefix}/local \
	--libdir=%{_libdir} \
	--libexecdir=%{_libdir} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--x-libraries=%{_libdir} \
	--%{?with_bootstrap:en}%{!?with_bootstrap:dis}able-bootstrap \
	--disable-build-with-cxx \
	--disable-build-poststage1-with-cxx \
	--enable-c99 \
	--enable-checking=release \
%ifarch %{ix86} %{x8664} x32
	--disable-cld \
%endif
	--enable-decimal-float \
	--enable-gnu-indirect-function \
	--enable-gnu-unique-object \
	--enable-initfini-array \
	--disable-isl-version-check \
	--enable-languages="c%{?with_cxx:,c++}%{?with_java:,java}" \
	--disable-libatomic \
	--disable-libcilkrts \
	--disable-libgomp \
	--disable-libitm \
	--disable-libmpx \
	--disable-libquadmath \
	--disable-libsanitizer \
	--disable-libssp \
	--disable-libvtv \
	--enable-linker-build-id \
	--enable-linux-futex \
	--enable-long-long \
	%{!?with_multilib:--disable-multilib} \
	--enable-nls \
	--enable-lto \
	--enable-plugin \
%ifarch ppc ppc64
	--enable-secureplt \
%endif
	--enable-shared \
	--enable-threads=posix \
	--disable-werror \
%ifarch x32
	--with-abi=x32 \
%endif
%ifarch %{x8664} x32
	--with-arch-32=x86-64 \
%endif
%ifarch sparc64
	--with-cpu=ultrasparc \
%endif
	--with-demangler-in-ld \
	--with-ecj-jar=%{_javadir}/ecj.jar \
	--with-gnu-as \
	--with-gnu-ld \
	--with-linker-hash-style=gnu \
	--with-long-double-128 \
%if %{with multilib}
%ifarch %{x8664}
	--with-multilib-list=m32,m64%{?with_multilibx32:,mx32} \
%endif
%ifarch x32
	--with-multilib-list=m32,m64,mx32 \
%endif
%endif
	--with-slibdir=%{_slibdir} \
%ifnarch ia64
	--without-system-libunwind \
%else
	--with-system-libunwind \
%endif
	--with-system-zlib \
	%{!?with_java:--without-x} \
%if %{with cxx}
	--enable-__cxa_atexit \
	--enable-libstdcxx-allocator=new \
	--disable-libstdcxx-pch \
	--enable-libstdcxx-threads \
	--enable-libstdcxx-time=rt \
	--enable-libstdcxx-visibility \
	--enable-symvers=gnu%{?with_symvers:-versioned-namespace} \
	--with-gxx-include-dir=%{_includedir}/c++/%{version} \
	%{?with_vtv:--enable-vtable-verify} \
%endif
%if %{with java}
	%{!?with_alsa:--disable-alsa} \
	%{!?with_dssi:--disable-dssi} \
	--disable-gconf-peer \
	%{?with_gtk:--enable-gtk-cairo} \
%if %{with x}
	--enable-java-awt="xlib%{?with_gtk:,gtk}%{?with_qt:,qt}" \
%endif
	--enable-jni \
	--enable-libgcj \
	--enable-libgcj-database \
	--enable-libgcj-multifile \
	--disable-libjava-multilib \
	%{?with_mozilla:--enable-plugin} \
	--enable-static-libjava \
	--enable-xmlj \
%endif
	--with-pkgversion="PLD-Linux" \
	--with-bugurl="http://bugs.pld-linux.org" \
	--host=%{_target_platform} \
	--build=%{_target_platform}

cd ..

cat << 'EOF' > Makefile
all := $(filter-out all Makefile,$(MAKECMDGOALS))

all $(all):
	$(MAKE) -C builddir $(MAKE_OPTS) $(all) \
		%{?with_bootstrap:%{?with_profiling:profiledbootstrap}} \
		GCJFLAGS="%{rpmcflags}" \
		BOOT_CFLAGS="%{rpmcflags}" \
		STAGE1_CFLAGS="%{rpmcflags} -O1 -g0" \
		GNATLIBCFLAGS="%{rpmcflags}" \
		LDFLAGS_FOR_TARGET="%{rpmldflags}" \
		mandir=%{_mandir} \
		infodir=%{_infodir}
EOF

%{__make}

%if %{with tests}
if [ ! -r /dev/pts/0 ]; then
	echo "You need to have /dev/pts mounted to avoid expect's spawn failures!"
	exit 1
fi
%{__make} -k -C builddir check 2>&1 ||:
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/lib,%{_aclocaldir},%{_datadir},%{_infodir}}

cd builddir

%{__make} -j1 install \
	mandir=%{_mandir} \
	infodir=%{_infodir} \
	DESTDIR=$RPM_BUILD_ROOT

cp -p gcc/specs $RPM_BUILD_ROOT%{gcclibdir}

%if %{with multilib}
# create links
%ifarch sparc64
ln -f $RPM_BUILD_ROOT%{_bindir}/sparc64-pld-linux-gcc \
	$RPM_BUILD_ROOT%{_bindir}/sparc-pld-linux-gcc
ln -f $RPM_BUILD_ROOT%{_bindir}/sparc64-pld-linux-gcc-%{version} \
	$RPM_BUILD_ROOT%{_bindir}/sparc-pld-linux-gcc-%{version}
%if %{with cxx}
ln -f $RPM_BUILD_ROOT%{_bindir}/sparc64-pld-linux-c++ \
	$RPM_BUILD_ROOT%{_bindir}/sparc-pld-linux-c++
ln -f $RPM_BUILD_ROOT%{_bindir}/sparc64-pld-linux-g++ \
	$RPM_BUILD_ROOT%{_bindir}/sparc-pld-linux-g++
%endif
%if %{with java}
ln -f $RPM_BUILD_ROOT%{_bindir}/sparc64-pld-linux-gcj \
	$RPM_BUILD_ROOT%{_bindir}/sparc-pld-linux-gcj
%endif
%endif
%endif

ln -sf %{_bindir}/cpp $RPM_BUILD_ROOT/lib/cpp
ln -sf gcc $RPM_BUILD_ROOT%{_bindir}/cc
echo ".so man1/gcc.1" > $RPM_BUILD_ROOT%{_mandir}/man1/cc.1

cd ..

%if %{with java}
install -d java-doc
cp -f libjava/READ* java-doc
ln -sf libgcj-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/libgcj.jar
%endif

# avoid -L poisoning in *.la - there should be only -L%{_libdir}/gcc/%{_target_platform}/%{version}
# normalize libdir, to avoid propagation of unnecessary RPATHs by libtool
for f in %{?with_cxx:libstdc++.la libstdc++fs.la libsupc++.la} \
%if %{with java}
	libgcj.la libgcj-tools.la libgij.la \
	%{gcjdbexecdir}/libjvm.la \
	%{gcjdbexecdir}/libxmlj.la \
	%{?with_x:lib-gnu-awt-xlib.la} \
	%{?with_gtk:%{gcjdbexecdir}/libgtkpeer.la %{gcjdbexecdir}/libjawt.la} \
	%{?with_qt:%{gcjdbexecdir}/libqtpeer.la} \
	%{?with_alsa:%{gcjdbexecdir}/libgjsmalsa.la} \
	%{?with_dssi:%{gcjdbexecdir}/libgjsmdssi.la} \
%endif
	;
do
	file="$RPM_BUILD_ROOT%{_libdir}/$f"
	%{__perl} %{SOURCE1} "$file" %{_libdir} >"${file}.fixed"
	%{__mv} "${file}.fixed" "$file"

	# normalize /lib/../lib/ path (libjawt.la)
	sed -i -e 's#/%{_lib}/\.\./%{_lib}/#/%{_lib}/#g' "$file"
done
%if %{with multilib}
for f in %{?with_cxx:libstdc++.la libstdc++fs.la libsupc++.la} \
	;
do
	%{__perl} %{SOURCE1} $RPM_BUILD_ROOT%{_libdir32}/$f %{_libdir32} > $RPM_BUILD_ROOT%{_libdir32}/$f.fixed
	%{__mv} $RPM_BUILD_ROOT%{_libdir32}/$f{.fixed,}
done
%if %{with multilib2}
for f in %{?with_cxx:libstdc++.la libstdc++fs.la libsupc++.la} \
	;
do
	%{__perl} %{SOURCE1} $RPM_BUILD_ROOT%{_libdirm2}/$f %{_libdirm2} > $RPM_BUILD_ROOT%{_libdirm2}/$f.fixed
	%{__mv} $RPM_BUILD_ROOT%{_libdirm2}/$f{.fixed,}
done
%endif
%endif

cp -p $RPM_BUILD_ROOT%{gcclibdir}/install-tools/include/*.h $RPM_BUILD_ROOT%{gcclibdir}/include
cp -p $RPM_BUILD_ROOT%{gcclibdir}/include-fixed/syslimits.h $RPM_BUILD_ROOT%{gcclibdir}/include
%{__rm} -r $RPM_BUILD_ROOT%{gcclibdir}/install-tools
%{__rm} -r $RPM_BUILD_ROOT%{gcclibdir}/include-fixed

# plugins, .la not needed
%{__rm} $RPM_BUILD_ROOT%{gcclibdir}/liblto_plugin.la \
	$RPM_BUILD_ROOT%{_libdir}/libcc1.la

%if %{with python}
for LIBDIR in %{_libdir} %{?with_multilib:%{_libdir32}} %{?with_multilib2:%{_libdirm2}} ; do
	LIBPATH="$RPM_BUILD_ROOT%{_datadir}/gdb/auto-load$LIBDIR"
	install -d $LIBPATH
done
install -d $RPM_BUILD_ROOT%{py_sitescriptdir}
%if %{with java}
%{__mv} $RPM_BUILD_ROOT%{_datadir}/gcc-%{version}/python/libjava $RPM_BUILD_ROOT%{py_sitescriptdir}
%{__sed} -i -e '1s,#!/usr/bin/env python,#!/usr/bin/python,' $RPM_BUILD_ROOT%{_bindir}/aot-compile
%endif
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean
%else
%if %{with java}
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/gcc-%{version}/python/libjava
%endif
%endif
# script(s) always installed; see above for builds with python; if no python, just don't package
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libstdc++.so.*-gdb.py
%if %{with multilib}
%{__rm} $RPM_BUILD_ROOT%{_libdir32}/libstdc++.so.*-gdb.py
%if %{with multilib2}
%{__rm} $RPM_BUILD_ROOT%{_libdirm2}/libstdc++.so.*-gdb.py
%endif
%endif

# drop here, use from base gcc:
# libgcc, libgomp, libcilkrts, libstdc++, libasan, liblsan, libtsan, libubsan, libatomic libmpx
%{__rm} $RPM_BUILD_ROOT%{_slibdir}/libgcc_s.so*
%if %{with cxx}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libstdc++.so*
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib{stdc++,stdc++fs,supc++}.la
%{__rm} $RPM_BUILD_ROOT%{_libdir}/lib{stdc++,stdc++fs,supc++}.a
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/gcc-%{version}/python/libstdcxx
%endif
%if %{with multilib}
%{__rm} $RPM_BUILD_ROOT%{_slibdir32}/libgcc_s.so*
%if %{with cxx}
%{__rm} $RPM_BUILD_ROOT%{_libdir32}/libstdc++.so*
%{__rm} $RPM_BUILD_ROOT%{_libdir32}/lib{stdc++,stdc++fs,supc++}.la
%{__rm} $RPM_BUILD_ROOT%{_libdir32}/lib{stdc++,stdc++fs,supc++}.a
%endif
%endif
%if %{with multilib2}
%{__rm} $RPM_BUILD_ROOT%{_slibdirm2}/libgcc_s.so*
%if %{with cxx}
%{__rm} $RPM_BUILD_ROOT%{_libdirm2}/libstdc++.so*
%{__rm} $RPM_BUILD_ROOT%{_libdirm2}/lib{stdc++,stdc++fs,supc++}.la
%{__rm} $RPM_BUILD_ROOT%{_libdirm2}/lib{stdc++,stdc++fs,supc++}.a
%endif
%endif

%find_lang gcc
%find_lang cpplib
cat cpplib.lang >> gcc.lang

%if %{without base}
%{__rm} $RPM_BUILD_ROOT/lib/cpp
%{__rm} $RPM_BUILD_ROOT%{_bindir}/{cc,cpp,gcc*,gcov*,*-pld-linux-gcc*}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libcc1.so*
%{__rm} $RPM_BUILD_ROOT%{gcclibdir}/{cc1,collect2,libgcov.a,lto-wrapper,lto1,specs,vtv_*.o}
%{__rm} $RPM_BUILD_ROOT%{gcclibdir}/include/[!gj]*.h
%{__rm} -r $RPM_BUILD_ROOT%{gcclibdir}/plugin
%{__rm} $RPM_BUILD_ROOT%{_infodir}/{cpp,cppinternals,gcc,gccinstall,gccint}.info
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/{cc,cpp,gcc,gcov*}.1
%{__rm} -r $RPM_BUILD_ROOT%{_mandir}/man7
%if %{with cxx}
%{__rm} $RPM_BUILD_ROOT%{_bindir}/{c++,g++,*-pld-linux-{c,g}++}
%{__rm} $RPM_BUILD_ROOT%{_includedir}/c++/%{version}/{algorithm,array,atomic,bitset,c*,deque,exception,fenv.h,forward_list,fstream,functional,future,initializer_list,io*,istream,iterator,limits,list,locale,map,math.h,memory,mutex,new,numeric,ostream,queue,random,ratio,regex,scoped_allocator,set,shared_mutex,sstream,stack,stdexcept,stdlib.h,streambuf,string,system_error,tgmath.h,thread,tuple,type_traits,typeindex,typeinfo,unordered_*,utility,valarray,vector}
%{__rm} -r $RPM_BUILD_ROOT%{_includedir}/c++/%{version}/{backward,bits,debug,decimal,experimental,ext,*-pld-linux,parallel,profile,tr1,tr2}
%{__rm} $RPM_BUILD_ROOT%{gcclibdir}/cc1plus
%{__rm} $RPM_BUILD_ROOT%{_mandir}/man1/g++.1
%endif
%endif

# always -f, as "dir" is created depending which texlive version is installed
%{__rm} -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	-n gcc-java -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-n gcc-java -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	-p /sbin/ldconfig -n libgcj
%postun	-p /sbin/ldconfig -n libgcj
%post	-p /sbin/ldconfig gdb-plugin
%postun	-p /sbin/ldconfig gdb-plugin

%if %{with base}
%files -f gcc.lang
%defattr(644,root,root,755)
%doc ChangeLog.general MAINTAINERS NEWS
# bugs.html faq.html
%doc gcc/{ChangeLog,ONEWS,README.Portability}
%attr(755,root,root) %{_bindir}/*-gcc*
%attr(755,root,root) %{_bindir}/cc
%attr(755,root,root) %{_bindir}/cpp
%attr(755,root,root) %{_bindir}/gcc
%attr(755,root,root) %{_bindir}/gcc-ar
%attr(755,root,root) %{_bindir}/gcc-nm
%attr(755,root,root) %{_bindir}/gcc-ranlib
%attr(755,root,root) %{_bindir}/gcov
%attr(755,root,root) %{_bindir}/gcov-dump
%attr(755,root,root) %{_bindir}/gcov-tool
%{_mandir}/man1/cc.1*
%{_mandir}/man1/cpp.1*
%{_mandir}/man1/gcc.1*
%{_mandir}/man1/gcov.1*
%{_mandir}/man1/gcov-dump.1*
%{_mandir}/man1/gcov-tool.1*
%{_infodir}/cpp.info*
%{_infodir}/cppinternals.info*
%{_infodir}/gcc.info*
%{_infodir}/gccinstall.info*
%{_infodir}/gccint.info*
%attr(755,root,root) /lib/cpp
%dir %{_libdir}/gcc/%{_target_platform}
%dir %{gcclibdir}
%{gcclibdir}/libgcc.a
%{gcclibdir}/libgcc_eh.a
%{gcclibdir}/libgcov.a
%{gcclibdir}/specs
%{gcclibdir}/crt*.o
%{?with_vtv:%{gcclibdir}/vtv_*.o}
%attr(755,root,root) %{gcclibdir}/cc1
%attr(755,root,root) %{gcclibdir}/collect2
%attr(755,root,root) %{gcclibdir}/lto-wrapper
%attr(755,root,root) %{gcclibdir}/lto1
%attr(755,root,root) %{gcclibdir}/liblto_plugin.so*
%dir %{gcclibdir}/include
%dir %{gcclibdir}/include/sanitizer
%{gcclibdir}/include/sanitizer/common_interface_defs.h
%dir %{gcclibdir}/include/ssp
%{gcclibdir}/include/ssp/*.h
%{gcclibdir}/include/float.h
%{gcclibdir}/include/iso646.h
%{gcclibdir}/include/limits.h
%{gcclibdir}/include/stdalign.h
%{gcclibdir}/include/stdarg.h
%{gcclibdir}/include/stdatomic.h
%{gcclibdir}/include/stdbool.h
%{gcclibdir}/include/stddef.h
%{gcclibdir}/include/stdfix.h
%{gcclibdir}/include/stdint.h
%{gcclibdir}/include/stdint-gcc.h
%{gcclibdir}/include/stdnoreturn.h
%{gcclibdir}/include/syslimits.h
%{gcclibdir}/include/unwind.h
%{gcclibdir}/include/varargs.h
%ifarch %{ix86} %{x8664} x32
%{gcclibdir}/include/adxintrin.h
%{gcclibdir}/include/ammintrin.h
%{gcclibdir}/include/avx2intrin.h
%{gcclibdir}/include/avx512bwintrin.h
%{gcclibdir}/include/avx512cdintrin.h
%{gcclibdir}/include/avx512dqintrin.h
%{gcclibdir}/include/avx512erintrin.h
%{gcclibdir}/include/avx512fintrin.h
%{gcclibdir}/include/avx512ifmaintrin.h
%{gcclibdir}/include/avx512ifmavlintrin.h
%{gcclibdir}/include/avx512pfintrin.h
%{gcclibdir}/include/avx512vbmiintrin.h
%{gcclibdir}/include/avx512vbmivlintrin.h
%{gcclibdir}/include/avx512vlbwintrin.h
%{gcclibdir}/include/avx512vldqintrin.h
%{gcclibdir}/include/avx512vlintrin.h
%{gcclibdir}/include/avxintrin.h
%{gcclibdir}/include/bmi2intrin.h
%{gcclibdir}/include/bmiintrin.h
%{gcclibdir}/include/bmmintrin.h
%{gcclibdir}/include/clflushoptintrin.h
%{gcclibdir}/include/clwbintrin.h
%{gcclibdir}/include/clzerointrin.h
%{gcclibdir}/include/cpuid.h
%{gcclibdir}/include/cross-stdarg.h
%{gcclibdir}/include/emmintrin.h
%{gcclibdir}/include/f16cintrin.h
%{gcclibdir}/include/fma4intrin.h
%{gcclibdir}/include/fmaintrin.h
%{gcclibdir}/include/fxsrintrin.h
%{gcclibdir}/include/ia32intrin.h
%{gcclibdir}/include/immintrin.h
%{gcclibdir}/include/lwpintrin.h
%{gcclibdir}/include/lzcntintrin.h
%{gcclibdir}/include/mm3dnow.h
%{gcclibdir}/include/mmintrin.h
%{gcclibdir}/include/mm_malloc.h
%{gcclibdir}/include/nmmintrin.h
%{gcclibdir}/include/mwaitxintrin.h
%{gcclibdir}/include/pkuintrin.h
%{gcclibdir}/include/pmmintrin.h
%{gcclibdir}/include/popcntintrin.h
%{gcclibdir}/include/prfchwintrin.h
%{gcclibdir}/include/rdseedintrin.h
%{gcclibdir}/include/rtmintrin.h
%{gcclibdir}/include/shaintrin.h
%{gcclibdir}/include/smmintrin.h
%{gcclibdir}/include/tbmintrin.h
%{gcclibdir}/include/tmmintrin.h
%{gcclibdir}/include/wmmintrin.h
%{gcclibdir}/include/x86intrin.h
%{gcclibdir}/include/xmmintrin.h
%{gcclibdir}/include/xopintrin.h
%{gcclibdir}/include/xsavecintrin.h
%{gcclibdir}/include/xsaveintrin.h
%{gcclibdir}/include/xsaveoptintrin.h
%{gcclibdir}/include/xsavesintrin.h
%{gcclibdir}/include/xtestintrin.h
%endif
%ifarch %{arm}
%{gcclibdir}/include/arm_neon.h
%{gcclibdir}/include/mmintrin.h
%endif
%ifarch ia64
%{gcclibdir}/include/ia64intrin.h
%endif
%ifarch m68k
%{gcclibdir}/include/math-68881.h
%endif
%ifarch mips
%{gcclibdir}/include/loongson.h
%endif
%ifarch ppc ppc64
%{gcclibdir}/include/altivec.h
%{gcclibdir}/include/paired.h
%{gcclibdir}/include/ppc-asm.h
%{gcclibdir}/include/ppu_intrinsics.h
%{gcclibdir}/include/si2vmx.h
%{gcclibdir}/include/spe.h
%{gcclibdir}/include/spu2vmx.h
%{gcclibdir}/include/vec_types.h
%endif
%{?with_vtv:%{gcclibdir}/include/vtv_*.h}

%if %{with multilib}
%files multilib-32
%defattr(644,root,root,755)
%dir %{gcclibdir}/32
%{gcclibdir}/32/crt*.o
%{?with_vtv:%{gcclibdir}/32/vtv_*.o}
%{gcclibdir}/32/libgcc.a
%{gcclibdir}/32/libgcc_eh.a
%{gcclibdir}/32/libgcov.a
%endif

%if %{with multilib2}
%files multilib-%{multilib2}
%defattr(644,root,root,755)
%dir %{gcclibdir}/%{multilib2}
%{gcclibdir}/%{multilib2}/crt*.o
%{?with_vtv:%{gcclibdir}/%{multilib2}/vtv_*.o}
%{gcclibdir}/%{multilib2}/libgcc.a
%{gcclibdir}/%{multilib2}/libgcc_eh.a
%{gcclibdir}/%{multilib2}/libgcov.a
%endif
%endif

%if %{with base} && %{with cxx}
%files c++
%defattr(644,root,root,755)
%doc gcc/cp/{ChangeLog,NEWS}
%attr(755,root,root) %{_bindir}/g++
%attr(755,root,root) %{_bindir}/*-g++
%attr(755,root,root) %{_bindir}/c++
%attr(755,root,root) %{_bindir}/*-c++
%attr(755,root,root) %{gcclibdir}/cc1plus
%dir %{_includedir}/c++
%{_includedir}/c++/%{version}
%if %{with java}
%exclude %{_includedir}/c++/%{version}/java
%exclude %{_includedir}/c++/%{version}/javax
%exclude %{_includedir}/c++/%{version}/gcj
%exclude %{_includedir}/c++/%{version}/gnu
%exclude %{_includedir}/c++/%{version}/org
%exclude %{_includedir}/c++/%{version}/sun
%endif
%{_mandir}/man1/g++.1*
%endif

%if %{with java}
%files -n gcc-java
%defattr(644,root,root,755)
%doc gcc/java/ChangeLog java-doc/*
%attr(755,root,root) %{_bindir}/gappletviewer
%attr(755,root,root) %{_bindir}/gc-analyze
%attr(755,root,root) %{_bindir}/gcj
%attr(755,root,root) %{_bindir}/gcj-dbtool
%attr(755,root,root) %{_bindir}/gcjh
%attr(755,root,root) %{_bindir}/gjar
%attr(755,root,root) %{_bindir}/gjarsigner
%attr(755,root,root) %{_bindir}/gjavah
%attr(755,root,root) %{_bindir}/gkeytool
%attr(755,root,root) %{_bindir}/gnative2ascii
%attr(755,root,root) %{_bindir}/gorbd
%attr(755,root,root) %{_bindir}/grmic
%attr(755,root,root) %{_bindir}/grmid
%attr(755,root,root) %{_bindir}/grmiregistry
%attr(755,root,root) %{_bindir}/gserialver
%attr(755,root,root) %{_bindir}/gtnameserv
%attr(755,root,root) %{_bindir}/jcf-dump
%attr(755,root,root) %{_bindir}/jv-convert
%attr(755,root,root) %{_bindir}/rebuild-gcj-db
%attr(755,root,root) %{_bindir}/*-gcj
%dir %{gcclibdir}
%attr(755,root,root) %{gcclibdir}/ecj1
%attr(755,root,root) %{gcclibdir}/jc1
%attr(755,root,root) %{gcclibdir}/jvgenmain
%if %{without base}
%attr(755,root,root) %{gcclibdir}/liblto_plugin.so*
%{gcclibdir}/libgcc.a
%{gcclibdir}/libgcc_eh.a
%{gcclibdir}/crt*.o
%endif
%{_infodir}/cp-tools.info*
%{_infodir}/gcj.info*
%{_mandir}/man1/gappletviewer.1*
%{_mandir}/man1/gc-analyze.1*
%{_mandir}/man1/gcj.1*
%{_mandir}/man1/gcj-dbtool.1*
%{_mandir}/man1/gcjh.1*
%{_mandir}/man1/gjar.1*
%{_mandir}/man1/gjarsigner.1*
%{_mandir}/man1/gjavah.1*
%{_mandir}/man1/gkeytool.1*
%{_mandir}/man1/gnative2ascii.1*
%{_mandir}/man1/gorbd.1*
%{_mandir}/man1/grmic.1*
%{_mandir}/man1/grmid.1*
%{_mandir}/man1/grmiregistry.1*
%{_mandir}/man1/gserialver.1*
%{_mandir}/man1/gtnameserv.1*
%{_mandir}/man1/jcf-dump.1*
%{_mandir}/man1/jv-convert.1*
%{_mandir}/man1/rebuild-gcj-db*

%if %{with python}
%files -n gcc-java-aotcompile
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/aot-compile
%dir %{py_sitescriptdir}/libjava
%{py_sitescriptdir}/libjava/*.py[co]
%{_mandir}/man1/aot-compile.1*
%endif

%files -n libgcj
%defattr(644,root,root,755)
%doc libjava/{ChangeLog,LIBGCJ_LICENSE,NEWS,README,THANKS}
%attr(755,root,root) %{_bindir}/gij
%attr(755,root,root) %{_libdir}/libgcj-tools.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgcj-tools.so.%{gcj_soname_ver}
%attr(755,root,root) %{_libdir}/libgcj.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgcj.so.%{gcj_soname_ver}
%attr(755,root,root) %{_libdir}/libgcj_bc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgcj_bc.so.1
%attr(755,root,root) %{_libdir}/libgcj_bc.so
%attr(755,root,root) %{_libdir}/libgij.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgij.so.%{gcj_soname_ver}
%{?with_x:%attr(755,root,root) %{_libdir}/lib-gnu-awt-xlib.so.*.*.*}
%{?with_x:%attr(755,root,root) %ghost %{_libdir}/lib-gnu-awt-xlib.so.%{gcj_soname_ver}}
%dir %{_libdir}/%{gcjdbexecdir}
%{_libdir}/%{gcjdbexecdir}/classmap.db
%{?with_mozilla:%attr(755,root,root) %{_libdir}/%{gcjdbexecdir}/libgcjwebplugin.so}
%{?with_alsa:%attr(755,root,root) %{_libdir}/%{gcjdbexecdir}/libgjsmalsa.so*}
%{?with_dssi:%attr(755,root,root) %{_libdir}/%{gcjdbexecdir}/libgjsmdssi.so*}
%{?with_gtk:%attr(755,root,root) %{_libdir}/%{gcjdbexecdir}/libgtkpeer.so}
%{?with_gtk:%attr(755,root,root) %{_libdir}/%{gcjdbexecdir}/libjawt.so}
%attr(755,root,root) %{_libdir}/%{gcjdbexecdir}/libjavamath.so
%attr(755,root,root) %{_libdir}/%{gcjdbexecdir}/libjvm.so
%{?with_qt:%attr(755,root,root) %{_libdir}/%{gcjdbexecdir}/libqtpeer.so}
%attr(755,root,root) %{_libdir}/%{gcjdbexecdir}/libxmlj.so*
%{_libdir}/logging.properties
%{_javadir}/libgcj*.jar
%{_mandir}/man1/gij.1*

%files -n libgcj-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgcj-tools.so
%{_libdir}/libgcj-tools.la
%attr(755,root,root) %{_libdir}/libgcj.so
%{_libdir}/libgcj.la
%attr(755,root,root) %{_libdir}/libgij.so
%{_libdir}/libgij.la
%if %{with x}
%attr(755,root,root) %{_libdir}/lib-gnu-awt-xlib.so
%{_libdir}/lib-gnu-awt-xlib.la
%endif
%{_libdir}/libgcj.spec
%dir %{_libdir}/security
%{_libdir}/security/*
%{?with_alsa:%{_libdir}/%{gcjdbexecdir}/libgjsmalsa.la}
%{?with_dssi:%{_libdir}/%{gcjdbexecdir}/libgjsmdssi.la}
%{?with_gtk:%{_libdir}/%{gcjdbexecdir}/libgtkpeer.la}
%{?with_gtk:%{_libdir}/%{gcjdbexecdir}/libjawt.la}
%{_libdir}/%{gcjdbexecdir}/libjavamath.la
%{_libdir}/%{gcjdbexecdir}/libjvm.la
%{?with_qt:%{_libdir}/%{gcjdbexecdir}/libqtpeer.la}
%{?with_mozilla:%{_libdir}/%{gcjdbexecdir}/libgcjwebplugin.la}
%{_libdir}/%{gcjdbexecdir}/libxmlj.la
%dir %{gcclibdir}/include
%{gcclibdir}/include/gcj
%{gcclibdir}/include/jawt.h
%{gcclibdir}/include/jawt_md.h
%{gcclibdir}/include/jni.h
%{gcclibdir}/include/jni_md.h
%{gcclibdir}/include/jvmpi.h
%dir %{_includedir}/c++/%{version}
%{_includedir}/c++/%{version}/java
%{_includedir}/c++/%{version}/javax
%{_includedir}/c++/%{version}/gcj
%{_includedir}/c++/%{version}/gnu
%{_includedir}/c++/%{version}/org
%{_includedir}/c++/%{version}/sun
%{_pkgconfigdir}/libgcj-%{major_ver}.pc

%files -n libgcj-static
%defattr(644,root,root,755)
%{_libdir}/libgcj-tools.a
%{_libdir}/libgcj.a
%{_libdir}/libgcj_bc.a
%{_libdir}/libgij.a
%{?with_x:%{_libdir}/lib-gnu-awt-xlib.a}
%{_libdir}/%{gcjdbexecdir}/libjvm.a
%endif

%if %{with base}
%files gdb-plugin
%defattr(644,root,root,755)
%doc libcc1/ChangeLog*
%attr(755,root,root) %{_libdir}/libcc1.so
%attr(755,root,root) %{_libdir}/libcc1.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcc1.so.0
%attr(755,root,root) %{gcclibdir}/plugin/libcc1plugin.so.*

%files plugin-devel
%defattr(644,root,root,755)
%dir %{gcclibdir}/plugin
%{gcclibdir}/plugin/gengtype
%{gcclibdir}/plugin/gtype.state
%{gcclibdir}/plugin/include
%attr(755,root,root) %{gcclibdir}/plugin/libcc1plugin.la
%attr(755,root,root) %{gcclibdir}/plugin/libcc1plugin.so
%endif
