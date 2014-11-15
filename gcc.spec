# NOTE: despite lower soname, libffi is newer than standalone 3.0.10
#
# TODO:
# - gconf peer? (but libgcj needs split anyway)
# - package?
#   /usr/bin/gjdoc [BR: antlr.jar] (but see gjdoc package, there are some additional jars?)
#   /usr/share/man/man1/gjdoc.1.gz
#
# Conditional build:
# - languages:
%bcond_without	ada		# build without ADA support
%bcond_without	cxx		# build without C++ support
%bcond_without	fortran		# build without Fortran support
%bcond_without	go		# build without Go support
%bcond_without	java		# build without Java support
%bcond_without	objc		# build without Objective-C support
%bcond_without	objcxx		# build without Objective-C++ support
# - features:
%bcond_without	gomp		# build without OpenMP support
%bcond_without	multilib	# build without multilib support (it needs glibc[32&64]-devel)
%bcond_without	profiling	# build without profiling
%bcond_without	python		# build without libstdc++ printers for gdb and aot-compile for java
%bcond_without	asan		# build without Address Sanitizer library
%bcond_without	tsan		# build without Thread Sanitizer library
%bcond_without	atomic		# build without library for atomic operations not supported by hardware
%bcond_with	gcc_libffi	# packaging gcc libffi for system usage
				# note: libgcj and libgo always have convenience gcc libffi linked in
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

# go, java and objcxx require C++
%if %{without cxx}
%undefine	with_go
%undefine	with_java
%undefine	with_objcxx
%endif
# objcxx requires objc
%if %{without objc}
%undefine	with_objcxx
%endif

%if %{without bootstrap}
%undefine	with_profiling
%endif

%if %{without x}
%undefine	with_gtk
%undefine	with_qt
%endif

%ifnarch %{x8664} ppc64 s390x sparc64
%undefine	with_multilib
%endif

%ifnarch %{ix86} %{x8664} alpha arm ppc ppc64 sh sparc sparcv9 sparc64
%undefine	with_atomic
%endif

%ifnarch %{ix86} %{x8664} ppc ppc64 sparc sparcv9 sparc64
%undefine	with_asan
%endif

%ifnarch %{x8664}
%undefine	with_tsan
%endif

%ifarch sparc64
%undefine	with_ada
%endif

%define		major_ver	4.9
%define		minor_ver	2
%define		major_ecj_ver	4.9
# class data version seen with file(1) that this jvm is able to load
%define		_classdataversion 50.0
%define		gcj_soname_ver	15

Summary:	GNU Compiler Collection: the C compiler and shared files
Summary(es.UTF-8):	Colección de compiladores GNU: el compilador C y ficheros compartidos
Summary(pl.UTF-8):	Kolekcja kompilatorów GNU: kompilator C i pliki współdzielone
Summary(pt_BR.UTF-8):	Coleção dos compiladores GNU: o compilador C e arquivos compartilhados
Name:		gcc
Version:	%{major_ver}.%{minor_ver}
Release:	1
Epoch:		6
License:	GPL v3+
Group:		Development/Languages
Source0:	https://ftp.gnu.org/pub/gnu/gcc/gcc-%{version}/%{name}-%{version}.tar.bz2
# Source0-md5:	4df8ee253b7f3863ad0b86359cd39c43
Source1:	%{name}-optimize-la.pl
Source2:	ftp://sourceware.org/pub/java/ecj-%{major_ecj_ver}.jar
# Source2-md5:	7339f199ba11c941890031fd9981d7be
# check libffi version with libffi/configure.ac
Source3:	libffi.pc.in
# svn diff -x --ignore-eol-style --force svn://gcc.gnu.org/svn/gcc/tags/gcc_4_9_2_release svn://gcc.gnu.org/svn/gcc/branches/gcc-4_9-branch > gcc-branch.diff
Patch100:	%{name}-branch.diff
# Patch100-md5:	66e843617ce0bfe9764059752a9706d6
Patch0:		%{name}-info.patch
Patch1:		%{name}-cloog.patch
Patch2:		%{name}-nodebug.patch
Patch3:		%{name}-ada-link.patch

Patch5:		%{name}-4.9-isl-0.13-hack.patch
Patch6:		%{name}-pr61164.patch
Patch7:		%{name}-libjava-multilib.patch
Patch8:		%{name}-enable-java-awt-qt.patch
Patch10:	%{name}-moresparcs.patch
Patch11:	%{name}-install-libffi.patch
URL:		http://gcc.gnu.org/
BuildRequires:	autoconf >= 2.64
%{?with_tests:BuildRequires:	autogen}
BuildRequires:	automake >= 1:1.9.3
# binutils 2.17.50.0.9 or newer are required for fixing PR middle-end/20218.
BuildRequires:	binutils >= 3:2.17.50.0.9-1
BuildRequires:	bison
BuildRequires:	chrpath >= 0.13-2
BuildRequires:	cloog-isl-devel >= 0.17.0
BuildRequires:	cloog-isl-devel < 0.19
%{?with_tests:BuildRequires:	dejagnu}
BuildRequires:	elfutils-devel >= 0.145-1
BuildRequires:	fileutils >= 4.0.41
BuildRequires:	flex
%if %{with ada}
BuildRequires:	gcc(ada)
BuildRequires:	gcc-ada
%endif
BuildRequires:	gettext-devel
BuildRequires:	glibc-devel >= 6:2.4-1
%if %{with multilib}
BuildRequires:	gcc(multilib)
%ifarch %{x8664}
BuildRequires:	glibc-devel(ix86)
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
BuildRequires:	gmp-c++-devel >= 4.1
BuildRequires:	gmp-devel >= 4.1
BuildRequires:	isl-devel >= 0.13
BuildRequires:	libmpc-devel
BuildRequires:	mpfr-devel >= 2.3.0
BuildRequires:	ppl-devel >= 0.11
%if %{with python}
BuildRequires:	python-devel
BuildRequires:	rpm-pythonprov
%endif
BuildRequires:	rpmbuild(macros) >= 1.211
BuildRequires:	texinfo >= 4.1
BuildRequires:	zlib-devel
%if %{with java}
%{?with_alsa:BuildRequires:	alsa-lib-devel}
%if %{with dssi}
BuildRequires:	dssi-devel
BuildRequires:	jack-audio-connection-kit-devel
%endif
BuildRequires:	libxml2-devel >= 1:2.6.8
BuildRequires:	libxslt-devel >= 1.1.11
BuildRequires:	perl-base
BuildRequires:	perl-tools-pod
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildRequires:	unzip
BuildRequires:	zip
%if %{with gtk}
BuildRequires:	cairo-devel >= 0.5.0
BuildRequires:	gtk+2-devel >= 2:2.4.0
BuildRequires:	libart_lgpl-devel
BuildRequires:	pango-devel
BuildRequires:	xorg-lib-libXt-devel
BuildRequires:	xorg-lib-libXtst-devel
%endif
%if %{with qt}
BuildRequires:	QtGui-devel >= 4.0.1
BuildRequires:	qt4-build >= 4.0.1
%endif
%{?with_mozilla:BuildRequires:	xulrunner-devel >= 1.8.1.3-1.20070321.5}
%endif
BuildConflicts:	pdksh < 5.2.14-50
Requires:	binutils >= 3:2.23
Requires:	libgcc = %{epoch}:%{version}-%{release}
Provides:	cpp = %{epoch}:%{version}-%{release}
%{?with_ada:Provides:	gcc(ada)}
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
# 32-bit environment on x86-64,ppc64,s390x,sparc64
%define		_slibdir32	/lib
%define		_libdir32	/usr/lib
%define		_pkgconfigdir32	%{_libdir32}/pkgconfig
%endif
%define		gcclibdir	%{_libdir}/gcc/%{_target_platform}/%{version}
%define		gcjdbexecdir	gcj-%{version}-%{gcj_soname_ver}

%define		filterout	-fwrapv -fno-strict-aliasing -fsigned-char
%define		filterout_ld	-Wl,--as-needed

# functions with printf format attribute but with special parser and also
# receiving non constant format strings
%define		Werror_cflags	%{nil}

%define		skip_post_check_so	'.*(libgo|libxmlj|lib-gnu-awt-xlib)\.so.*'

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

%package multilib
Summary:	GNU Compiler Collection: the C compiler 32-bit support
Summary(pl.UTF-8):	Kolekcja kompilatorów GNU: obsługa binariów 32-bitowych dla kompilatora C
License:	GPL v3+
Group:		Development/Languages
Requires:	%{name}
Requires:	libgcc-multilib = %{epoch}:%{version}-%{release}
%{?with_multilib:Provides:	gcc(multilib)}
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

%description multilib
A compiler aimed at integrating all the optimizations and features
necessary for a high-performance and stable development environment.

This package contains the C compiler support for producing 32-bit
programs on 64-bit host.

%description multilib -l pl.UTF-8
Kompilator, posiadający duże możliwości optymalizacyjne niezbędne do
wyprodukowania szybkiego i stabilnego kodu wynikowego.

Ten pakiet zawiera rozszerzenie kompilatora C o obsługę tworzenia
programów 32-bitowych na maszynie 64-bitowej.

%package -n libgcc
Summary:	Shared gcc library
Summary(es.UTF-8):	Biblioteca compartida de gcc
Summary(pl.UTF-8):	Biblioteka gcc
Summary(pt_BR.UTF-8):	Biblioteca runtime para o GCC
License:	GPL v2+ with unlimited link permission
Group:		Libraries
Obsoletes:	libgcc1
Obsoletes:	libgcc4

%description -n libgcc
Shared gcc library.

%description -n libgcc -l es.UTF-8
Biblioteca compartida de gcc.

%description -n libgcc -l pl.UTF-8
Biblioteka dynamiczna gcc.

%description -n libgcc -l pt_BR.UTF-8
Biblioteca runtime para o GCC.

%package -n libgcc-multilib
Summary:	Shared gcc library - 32-bit version
Summary(pl.UTF-8):	Biblioteka gcc - wersja 32-bitowa
License:	GPL v2+ with unlimited link permission
Group:		Libraries

%description -n libgcc-multilib
Shared gcc library - 32-bit version.

%description -n libgcc-multilib -l pl.UTF-8
Biblioteka dynamiczna gcc - wersja 32-bitowa.

%package -n libgomp
Summary:	GNU OpenMP library
Summary(pl.UTF-8):	Biblioteka GNU OpenMP
License:	LGPL v2.1+ with unlimited link permission
Group:		Libraries

%description -n libgomp
GNU OpenMP library.

%description -n libgomp -l pl.UTF-8
Biblioteka GNU OpenMP.

%package -n libgomp-multilib
Summary:	GNU OpenMP library - 32-bit version
Summary(pl.UTF-8):	Biblioteka GNU OpenMP - wersja 32-bitowa
License:	LGPL v2.1+ with unlimited link permission
Group:		Libraries

%description -n libgomp-multilib
GNU OpenMP library - 32-bit version.

%description -n libgomp-multilib -l pl.UTF-8
Biblioteka GNU OpenMP - wersja 32-bitowa.

%package -n libgomp-devel
Summary:	Development files for GNU OpenMP library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki GNU OpenMP
License:	LGPL v2.1+ with unlimited link permission
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libgomp = %{epoch}:%{version}-%{release}

%description -n libgomp-devel
Development files for GNU OpenMP library.

%description -n libgomp-devel -l pl.UTF-8
Pliki programistyczne biblioteki GNU OpenMP.

%package -n libgomp-multilib-devel
Summary:	Development files for 32-bit version of GNU OpenMP library
Summary(pl.UTF-8):	Pliki programistyczne wersji 32-bitowej biblioteki GNU OpenMP
License:	LGPL v2.1+ with unlimited link permission
Group:		Development/Libraries
Requires:	libgomp-devel = %{epoch}:%{version}-%{release}

%description -n libgomp-multilib-devel
Development files for 32-bit version of GNU OpenMP library.

%description -n libgomp-multilib-devel -l pl.UTF-8
Pliki programistyczne wersji 32-bitowej biblioteki GNU OpenMP.

%package -n libgomp-static
Summary:	Static GNU OpenMP library
Summary(pl.UTF-8):	Statyczna biblioteka GNU OpenMP
License:	LGPL v2.1+ with unlimited link permission
Group:		Development/Libraries
Requires:	libgomp-devel = %{epoch}:%{version}-%{release}

%description -n libgomp-static
Static GNU OpenMP library.

%description -n libgomp-static -l pl.UTF-8
Statyczna biblioteka GNU OpenMP.

%package -n libgomp-multilib-static
Summary:	Static GNU OpenMP library - 32-bit version
Summary(pl.UTF-8):	Statyczna biblioteka GNU OpenMP - wersja 32-bitowa
License:	LGPL v2.1+ with unlimited link permission
Group:		Development/Libraries
Requires:	libgomp-multilib-devel

%description -n libgomp-multilib-static
Static GNU OpenMP library - 32-bit version.

%description -n libgomp-multilib-static -l pl.UTF-8
Statyczna biblioteka GNU OpenMP - wersja 32-bitowa.

%package -n libcilkrts
Summary:	GCC cilk+ shared support libraries
License:	GPL v2+ with unlimited link permission
Group:		Libraries

%description -n libcilkrts
This package contains the Cilk+ runtime library.

%package -n libcilkrts-multilib
Summary:	GCC cilk+ shared support libraries - 32-bit version
License:	GPL v2+ with unlimited link permission
Group:		Libraries

%description -n libcilkrts-multilib
This package contains the Cilk+ runtime library. This package contains
32-bit version.

%package -n libcilkrts-devel
Summary:	Development files for GCC cilk+ libraries
License:	GPL v2+ with unlimited link permission
Group:		Development/Libraries
Requires:	libcilkrts = %{epoch}:%{version}-%{release}

%description -n libcilkrts-devel
This package contains development files for cilk+ library.

%package -n libcilkrts-multilib-devel
Summary:	Development files for 32-bit version of GCC cilk+ libraries
License:	GPL v2+ with unlimited link permission
Group:		Development/Libraries
Requires:	libcilkrts-devel = %{epoch}:%{version}-%{release}

%description -n libcilkrts-multilib-devel
This package contains development files for 32-bit version of the
cilk+ libraries.

%package -n libcilkrts-static
Summary:	Static GCC cilk+ libraries
License:	GPL v2+ with unlimited link permission
Group:		Development/Libraries
Requires:	libcilkrts-devel = %{epoch}:%{version}-%{release}

%description -n libcilkrts-static
This package contains static cilk+ libraries.

%package -n libcilkrts-multilib-static
Summary:	Static GCC cilk+ libraries - 32-bit version
License:	GPL v2+ with unlimited link permission
Group:		Development/Libraries
Requires:	libcilkrts-multilib-devel = %{epoch}:%{version}-%{release}

%description -n libcilkrts-multilib-static
This package contains 32-bit static cilk+ libraries.
%package ada
Summary:	Ada support for gcc
Summary(es.UTF-8):	Soporte de Ada para gcc
Summary(pl.UTF-8):	Obsługa Ady do gcc
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libgnat = %{epoch}:%{version}-%{release}
Obsoletes:	gcc-gnat
Obsoletes:	gnat-devel

%description ada
This package adds experimental support for compiling Ada programs.

%description ada -l es.UTF-8
Este paquete añade soporte experimental para compilar programas en
Ada.

%description ada -l pl.UTF-8
Ten pakiet dodaje eksperymentalne wsparcie dla kompilacji programów w
Adzie.

%package ada-multilib
Summary:	Ada 32-bit support for gcc
Summary(pl.UTF-8):	Obsługa 32-bitowych binariów Ady dla gcc
Group:		Development/Languages
Requires:	%{name}-ada = %{epoch}:%{version}-%{release}
Requires:	libgnat-multilib = %{epoch}:%{version}-%{release}

%description ada-multilib
This package adds experimental support for compiling 32-bit Ada
programs on 64-bit host.

%description ada-multilib -l pl.UTF-8
Ten pakiet dodaje eksperymentalną obsługę kompilacji programów
32-bitowych w Adzie na maszynie 64-bitowej.

%package -n libgnat
Summary:	Ada standard libraries
Summary(es.UTF-8):	Bibliotecas estándares de Ada
Summary(pl.UTF-8):	Biblioteki standardowe dla Ady
License:	GPL v2+ with linking exception
Group:		Libraries
Obsoletes:	gnat
Obsoletes:	libgnat1

%description -n libgnat
This package contains shared libraries needed to run programs written
in Ada.

%description -n libgnat -l es.UTF-8
Este paquete contiene las bibliotecas compartidas necesarias para
ejecutar programas escritos en Ada.

%description -n libgnat -l pl.UTF-8
Ten pakiet zawiera biblioteki potrzebne do uruchamiania programów
napisanych w Adzie.

%package -n libgnat-multilib
Summary:	Ada standard libraries - 32-bit version
Summary(pl.UTF-8):	Biblioteki standardowe dla Ady - wersja 32-bitowa
License:	GPL v2+ with linking exception
Group:		Libraries

%description -n libgnat-multilib
This package contains 32-bit version of shared libraries needed to run
programs written in Ada.

%description -n libgnat-multilib -l pl.UTF-8
Ten pakiet zawiera wersje 32-bitowe bibliotek potrzebnych do
uruchamiania programów napisanych w Adzie.

%package -n libgnat-static
Summary:	Static Ada standard libraries
Summary(pl.UTF-8):	Statyczne biblioteki standardowe dla Ady
License:	GPL v2+ with linking exception
Group:		Development/Libraries
Obsoletes:	gnat-static

%description -n libgnat-static
This package contains static libraries for programs written in Ada.

%description -n libgnat-static -l pl.UTF-8
Ten pakiet zawiera biblioteki statyczne dla programów napisanych w
Adzie.

%package -n libgnat-multilib-static
Summary:	Static Ada standard libraries - 32-bit version
Summary(pl.UTF-8):	Statyczne biblioteki standardowe dla Ady - wersje 32-bitowe
License:	GPL v2+ with linking exception
Group:		Development/Libraries

%description -n libgnat-multilib-static
This package contains 32-bit version of static libraries for programs
written in Ada.

%description -n libgnat-multilib-static -l pl.UTF-8
Ten pakiet zawiera 32-bitowe wersje bibliotek statycznych dla
programów napisanych w Adzie.

%package c++
Summary:	C++ support for gcc
Summary(es.UTF-8):	Soporte de C++ para gcc
Summary(pl.UTF-8):	Obsługa C++ dla gcc
Summary(pt_BR.UTF-8):	Suporte C++ para o gcc
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
Ten pakiet dodaje obsługę C++ do kompilatora gcc. Ma wsparcie dla
dużej ilości obecnych specyfikacji C++, nie zawiera natomiast
standardowych bibliotek C++, które są w oddzielnym pakiecie.

%description c++ -l pt_BR.UTF-8
Este pacote adiciona suporte C++ para o gcc.

%description c++ -l tr.UTF-8
Bu paket, GNU C derleyicisine C++ desteği ekler. 'Template'ler ve
aykırı durum işleme gibi çoğu güncel C++ tanımlarına uyar. Standart
C++ kitaplığı bu pakette yer almaz.

%package c++-multilib
Summary:	C++ 32-bit support for gcc
Summary(pl.UTF-8):	Obsługa 32-bitowych binariów C++ dla gcc
Group:		Development/Languages
Requires:	%{name}-c++ = %{epoch}:%{version}-%{release}
Requires:	%{name}-multilib = %{epoch}:%{version}-%{release}

%description c++-multilib
This package adds 32-bit C++ support to the GNU Compiler Collection.

%description c++-multilib -l pl.UTF-8
Ten pakiet dodaje obsługę 32-bitowych binariów C++ do kompilatora gcc.

%package -n libstdc++
Summary:	GNU C++ library
Summary(es.UTF-8):	Biblioteca C++ de GNU
Summary(pl.UTF-8):	Biblioteki GNU C++
Summary(pt_BR.UTF-8):	Biblioteca C++ GNU
License:	GPL v2+ with free software exception
Group:		Libraries
# >= instead of = to allow keeping older libstdc++ (with different soname)
Requires:	libgcc >= %{epoch}:%{version}-%{release}
Obsoletes:	libg++
Obsoletes:	libstdc++3
Obsoletes:	libstdc++4

%description -n libstdc++
This is the GNU implementation of the standard C++ libraries, along
with additional GNU tools. This package includes the shared libraries
necessary to run C++ applications.

%description -n libstdc++ -l de.UTF-8
Dies ist die GNU-Implementierung der Standard-C++-Libraries mit
weiteren GNU-Tools. Dieses Paket enthält die zum Ausführen von
C++-Anwendungen erforderlichen gemeinsam genutzten Libraries.

%description -n libstdc++ -l es.UTF-8
Este es el soporte de las bibliotecas padrón del C++, junto con
herramientas GNU adicionales. El paquete incluye las bibliotecas
compartidas necesarias para ejecutar aplicaciones C++.

%description -n libstdc++ -l fr.UTF-8
Ceci est l'implémentation GNU des librairies C++ standard, ainsi que
des outils GNU supplémentaires. Ce package comprend les librairies
partagées nécessaires à l'exécution d'application C++.

%description -n libstdc++ -l pl.UTF-8
Pakiet ten zawiera biblioteki będące implementacją standardowych
bibliotek C++. Znajdują się w nim biblioteki dynamiczne niezbędne do
uruchomienia aplikacji napisanych w C++.

%description -n libstdc++ -l pt_BR.UTF-8
Este pacote é uma implementação da biblioteca padrão C++ v3, um
subconjunto do padrão ISO 14882.

%description -n libstdc++ -l tr.UTF-8
Bu paket, standart C++ kitaplıklarının GNU gerçeklemesidir ve C++
uygulamalarının koşturulması için gerekli kitaplıkları içerir.

%package -n libstdc++-multilib
Summary:	GNU C++ library - 32-bit version
Summary(pl.UTF-8):	Biblioteka GNU C++ - wersja 32-bitowa
License:	GPL v2+ with free software exception
Group:		Libraries
# >= instead of = to allow keeping older libstdc++ (with different soname)
Requires:	libgcc-multilib >= %{epoch}:%{version}-%{release}

%description -n libstdc++-multilib
This is 32-bit version of the GNU implementation of the standard C++
library.

%description -n libstdc++-multilib -l pl.UTF-8
Ten pakiet ten zawiera 32-bitową wersję implementacji GNU biblioteki
standardowej C++.

%package -n libstdc++-gdb
Summary:	libstdc++ pretty printers for GDB
Summary(pl.UTF-8):	Funkcje wypisujące dane libstdc++ dla GDB
Group:		Development/Debuggers

%description -n libstdc++-gdb
This package contains Python scripts for GDB pretty printing of the
libstdc++ types/containers.

%description -n libstdc++-gdb -l pl.UTF-8
Ten pakiet zawiera skrypty Pythona dla GDB służące do ładnego
wypisywania typów i kontenerów libstdc++.

%package -n libstdc++-devel
Summary:	Header files and documentation for C++ development
Summary(de.UTF-8):	Header-Dateien zur Entwicklung mit C++
Summary(es.UTF-8):	Ficheros de cabecera y documentación para desarrollo C++
Summary(fr.UTF-8):	Fichiers d'en-tête et biblitothèques pour développer en C++
Summary(pl.UTF-8):	Pliki nagłówkowe i dokumentacja do biblioteki standardowej C++
Summary(pt_BR.UTF-8):	Arquivos de inclusão e bibliotecas para o desenvolvimento em C++
Summary(tr.UTF-8):	C++ ile program geliştirmek için gerekli dosyalar
License:	GPL v2+ with free software exception
Group:		Development/Libraries
Requires:	%{name}-c++ = %{epoch}:%{version}-%{release}
Requires:	glibc-devel
Requires:	libstdc++ = %{epoch}:%{version}-%{release}
Obsoletes:	libg++-devel
Obsoletes:	libstdc++3-devel
Obsoletes:	libstdc++4-devel

%description -n libstdc++-devel
This is the GNU implementation of the standard C++ libraries. This
package includes the header files needed for C++ development and
library documentation.

%description -n libstdc++-devel -l es.UTF-8
Este es el soporte de las bibliotecas padrón del lenguaje C++. Este
paquete incluye los archivos de inclusión y bibliotecas necesarios
para desarrollo de programas en lenguaje C++.

%description -n libstdc++-devel -l pl.UTF-8
Pakiet ten zawiera biblioteki będące implementacją standardowych
bibliotek C++. Znajdują się w nim pliki nagłówkowe wykorzystywane przy
programowaniu w języku C++ oraz dokumentacja biblioteki standardowej.

%description -n libstdc++-devel -l pt_BR.UTF-8
Este pacote inclui os arquivos de inclusão e bibliotecas necessárias
para desenvolvimento de programas C++.

%package -n libstdc++-multilib-devel
Summary:	Development files for C++ development - 32-bit version
Summary(pl.UTF-8):	Pliki programistyczne biblioteki standardowej C++ - wersja 32-bitowa
License:	GPL v2+ with free software exception
Group:		Development/Libraries
Requires:	%{name}-c++-multilib = %{epoch}:%{version}-%{release}
Requires:	libstdc++-devel = %{epoch}:%{version}-%{release}
Requires:	libstdc++-multilib = %{epoch}:%{version}-%{release}

%description -n libstdc++-multilib-devel
This package contains the development files for 32-bit version of the
GNU implementation of the standard C++ library.

%description -n libstdc++-multilib-devel -l pl.UTF-8
Ten pakiet zawiera pliki programistyczne 32-bitowej wersji
implementacji GNU biblioteki standardowej C++.

%package -n libstdc++-static
Summary:	Static C++ standard library
Summary(es.UTF-8):	Biblioteca estándar estática de C++
Summary(pl.UTF-8):	Statyczna biblioteka standardowa C++
License:	GPL v2+ with free software exception
Group:		Development/Libraries
Requires:	libstdc++-devel = %{epoch}:%{version}-%{release}
Obsoletes:	libstdc++4-static

%description -n libstdc++-static
Static C++ standard library.

%description -n libstdc++-static -l es.UTF-8
Biblioteca estándar estática de C++.

%description -n libstdc++-static -l pl.UTF-8
Statyczna biblioteka standardowa C++.

%package -n libstdc++-multilib-static
Summary:	Static C++ standard library - 32-bit version
Summary(pl.UTF-8):	Statyczna biblioteka standardowa C++ - wersja 32-bitowa
License:	GPL v2+ with free software exception
Group:		Development/Libraries
Requires:	libstdc++-multilib-devel = %{epoch}:%{version}-%{release}

%description -n libstdc++-multilib-static
Static C++ standard library - 32-bit version.

%description -n libstdc++-multilib-static -l pl.UTF-8
Statyczna biblioteka standardowa C++ - wersja 32-bitowa.

%package -n libstdc++-apidocs
Summary:	C++ standard library API documentation
Summary(pl.UTF-8):	Dokumentacja API biblioteki standardowej C++
Group:		Documentation
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n libstdc++-apidocs
API and internal documentation for C++ standard library.

%description -n libstdc++-apidocs -l pl.UTF-8
Dokumentacja API i wewnętrzna biblioteki standardowej C++.

%package fortran
Summary:	Fortran 95 support for gcc
Summary(es.UTF-8):	Soporte de Fortran 95 para gcc
Summary(pl.UTF-8):	Obsługa Fortranu 95 dla gcc
Summary(pt_BR.UTF-8):	Suporte Fortran 95 para o GCC
Group:		Development/Languages/Fortran
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libgfortran = %{epoch}:%{version}-%{release}
Requires:	libquadmath-devel = %{epoch}:%{version}-%{release}
Provides:	gcc-g77 = %{epoch}:%{version}-%{release}
Obsoletes:	egcs-g77
Obsoletes:	gcc-g77

%description fortran
This package adds support for compiling Fortran 95 programs with the
GNU compiler.

%description fortran -l es.UTF-8
Este paquete añade soporte para compilar programas escritos en Fortran
95 con el compilador GNU.

%description fortran -l pl.UTF-8
Ten pakiet dodaje obsługę Fortranu 95 do kompilatora gcc. Jest
potrzebny do kompilowania programów pisanych w języku Fortran 95.

%description fortran -l pt_BR.UTF-8
Suporte Fortran 95 para o GCC.

%package fortran-multilib
Summary:	Fortran 95 32-bit support for gcc
Summary(pl.UTF-8):	Obsługa binariów 32-bitowych Fortranu 95 dla gcc
Group:		Development/Languages/Fortran
Requires:	%{name}-fortran = %{epoch}:%{version}-%{release}
Requires:	libgfortran-multilib = %{epoch}:%{version}-%{release}
Requires:	libquadmath-multilib-devel = %{epoch}:%{version}-%{release}

%description fortran-multilib
This package adds support for compiling 32-bit Fortran 95 programs
with the GNU compiler.

%description fortran-multilib -l pl.UTF-8
Ten pakiet dodaje obsługę 32-bitowych programów w Fortranie 95 do
kompilatora gcc.

%package -n libgfortran
Summary:	Fortran 95 Library
Summary(es.UTF-8):	Biblioteca de Fortran 95
Summary(pl.UTF-8):	Biblioteka Fortranu 95
License:	GPL v2+ with unlimited link permission
Group:		Libraries
Requires:	libquadmath = %{epoch}:%{version}-%{release}
Obsoletes:	libg2c

%description -n libgfortran
Fortran 95 Library.

%description -n libgfortran -l es.UTF-8
Biblioteca de Fortran 95.

%description -n libgfortran -l pl.UTF-8
Biblioteka Fortranu 95.

%package -n libgfortran-multilib
Summary:	Fortran 95 Library - 32-bit version
Summary(pl.UTF-8):	Biblioteka Fortranu 95 - wersja 32-bitowa
License:	GPL v2+ with unlimited link permission
Group:		Libraries
Requires:	libquadmath-multilib = %{epoch}:%{version}-%{release}

%description -n libgfortran-multilib
Fortran 95 Library - 32-bit version.

%description -n libgfortran-multilib -l pl.UTF-8
Biblioteka Fortranu 95 - wersja 32-bitowa.

%package -n libgfortran-static
Summary:	Static Fortran 95 Library
Summary(es.UTF-8):	Bibliotecas estáticas de Fortran 95
Summary(pl.UTF-8):	Statyczna Biblioteka Fortranu 95
License:	GPL v2+ with unlimited link permission
Group:		Development/Libraries
Requires:	libgfortran = %{epoch}:%{version}-%{release}
Obsoletes:	libg2c-static

%description -n libgfortran-static
Static Fortran 95 Library.

%description -n libgfortran-static -l es.UTF-8
Bibliotecas estáticas de Fortran 95.

%description -n libgfortran-static -l pl.UTF-8
Statyczna biblioteka Fortranu 95.

%package -n libgfortran-multilib-static
Summary:	Static Fortran 95 Library - 32-bit version
Summary(pl.UTF-8):	Statyczna Biblioteka Fortranu 95 - wersja 32-bitowa
License:	GPL v2+ with unlimited link permission
Group:		Development/Libraries
Requires:	libgfortran-multilib = %{epoch}:%{version}-%{release}

%description -n libgfortran-multilib-static
Static Fortran 95 Library - 32-bit version.

%description -n libgfortran-multilib-static -l pl.UTF-8
Statyczna biblioteka Fortranu 95 - wersja 32-bitowa.

%package -n libquadmath
Summary:	GCC __float128 shared support library
Summary(pl.UTF-8):	Biblioteka współdzielona do obsługi typu __float128
License:	GPL v2+ with linking exception
Group:		Libraries

%description -n libquadmath
This package contains GCC shared support library which is needed for
__float128 math support and for Fortran REAL*16 support.

%description -n libquadmath -l pl.UTF-8
Ten pakiet zawiera bibliotekę współdzieloną GCC do obsługi operacji
matematycznych na zmiennych typu __float128 oraz typu REAL*16 w
Fortranie.

%package -n libquadmath-multilib
Summary:	GCC __float128 shared support library - 32-bit version
Summary(pl.UTF-8):	Biblioteka współdzielona GCC do obsługi typu __float128 - wersja 32-bitowa
License:	GPL v2+ with linking exception
Group:		Libraries

%description -n libquadmath-multilib
This package contains 32-bit version of GCC shared support library
which is needed for __float128 math support and for Fortran REAL*16
support.

%description -n libquadmath-multilib -l pl.UTF-8
Ten pakiet zawiera 32-bitową bibliotekę współdzieloną GCC do obsługi
operacji matematycznych na zmiennych typu __float128 oraz typu REAL*16
w Fortranie.

%package -n libquadmath-devel
Summary:	Header files for GCC __float128 support library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteka GCC do obsługi typu __float128
License:	GPL v2+ with linking exception
Group:		Development/Libraries
Requires:	libquadmath = %{epoch}:%{version}-%{release}

%description -n libquadmath-devel
This package contains header files for GCC support library which is
needed for __float128 math support and for Fortran REAL*16 support.

%description -n libquadmath-devel -l pl.UTF-8
Ten pakiet zawiera pliki nagłówkowe biblioteki GCC do obsługi operacji
matematycznych na zmiennych typu __float128 oraz typu REAL*16 w
Fortranie.

%package -n libquadmath-multilib-devel
Summary:	Development files for 32-bit GCC __float128 support library
Summary(pl.UTF-8):	Pliki programistyczne 32-bitowej biblioteki do obsługi typu __float128
License:	GPL v2+ with linking exception
Group:		Development/Libraries
Requires:	libquadmath-devel = %{epoch}:%{version}-%{release}
Requires:	libquadmath-multilib = %{epoch}:%{version}-%{release}

%description -n libquadmath-multilib-devel
This package contains development files for 32-bit GCC support library
which is needed for __float128 math support and for Fortran REAL*16
support.

%description -n libquadmath-multilib-devel -l pl.UTF-8
Ten pakiet zawiera pliki programistyczne 32-bitowej biblioteki GCC do
obsługi operacji matematycznych na zmiennych typu __float128 oraz typu
REAL*16 w Fortranie.

%package -n libquadmath-static
Summary:	Static GCC __float128 support library
Summary(pl.UTF-8):	Biblioteka statyczna GCC do obsługi typu __float128
License:	GPL v2+ with linking exception
Group:		Development/Libraries
Requires:	libquadmath-devel = %{epoch}:%{version}-%{release}

%description -n libquadmath-static
Static GCC __float128 support library.

%description -n libquadmath-static -l pl.UTF-8
Biblioteka statyczna GCC do obsługi typu __float128.

%package -n libquadmath-multilib-static
Summary:	Static GCC __float128 support library - 32-bit version
Summary(pl.UTF-8):	32-bitowa biblioteka statyczna GCC do obsługi typu __float128
License:	GPL v2+ with linking exception
Group:		Development/Libraries
Requires:	libquadmath-multilib-devel = %{epoch}:%{version}-%{release}

%description -n libquadmath-multilib-static
Static GCC __float128 support library - 32-bit version.

%description -n libquadmath-multilib-static -l pl.UTF-8
32-bitowa biblioteka statyczna GCC do obsługi typu __float128.

%package java
Summary:	Java support for gcc
Summary(es.UTF-8):	Soporte de Java para gcc
Summary(pl.UTF-8):	Obsługa Javy dla gcc
Group:		Development/Languages/Java
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libgcj-devel = %{epoch}:%{version}-%{release}
Provides:	gcc-java-tools
Provides:	gcj = %{epoch}:%{version}-%{release}
Obsoletes:	eclipse-ecj
Obsoletes:	gcc-java-tools
Obsoletes:	java-gnu-classpath-tools

%description java
This package adds experimental support for compiling Java(TM) programs
and bytecode into native code. To use this you will also need the
libgcj package.

%description java -l es.UTF-8
Este paquete añade soporte experimental para compilar programas
Java(tm) y su bytecode en código nativo. Para usarlo también va a
necesitar el paquete libgcj.

%description java -l pl.UTF-8
Ten pakiet dodaje możliwość kompilowania programów w języku Java(TM)
oraz bajtkodu do kodu natywnego. Do używania go wymagany jest
dodatkowo pakiet libgcj.

%package java-aotcompile
Summary:	Java AOT-compiler - compiling bytecode to native
Summary(pl.UTF-8):	Kompilator AOT dla Javy - kompilacja bajtkodu do kodu natywnego
License:	GPL v2+
Group:		Development/Tools
Requires:	%{name}-java = %{epoch}:%{version}-%{release}

%description java-aotcompile
aot-compile is a script that searches a directory for Java bytecode
(as class files, or in jars) and uses gcj to compile it to native code
and generate the databases from it.

%description java-aotcompile -l pl.UTF-8
aot-compile to skrypt wyszukujący w katalogu bajtkod Javy (w plikach
class lub jarach) i kompilujący go przy użyciu gcj, a następnie
generujący z niego bazy danych.

%package -n libgcj
Summary:	Java Class Libraries
Summary(es.UTF-8):	Bibliotecas de clases de Java
Summary(pl.UTF-8):	Biblioteki Klas Javy
License:	GPL v2+ with limited linking exception
Group:		Libraries
Requires:	jpackage-utils
Requires:	libstdc++ = %{epoch}:%{version}-%{release}
Provides:	java(ClassDataVersion) = %{_classdataversion}
Obsoletes:	libgcj3

%description -n libgcj
Java Class Libraries.

%description -n libgcj -l es.UTF-8
Bibliotecas de clases de Java.

%description -n libgcj -l pl.UTF-8
Biblioteki Klas Javy.

%package -n libgcj-devel
Summary:	Development files for Java Class Libraries
Summary(es.UTF-8):	Ficheros de desarrollo para las bibliotecas de clases de Java
Summary(pl.UTF-8):	Pliki nagłówkowe dla Bibliotek Klas Javy
License:	GPL v2+ with limited linking exception
Group:		Development/Libraries
Requires:	libgcj = %{epoch}:%{version}-%{release}
Requires:	libstdc++-devel = %{epoch}:%{version}-%{release}
Requires:	zlib-devel
Obsoletes:	libgcj3-devel

%description -n libgcj-devel
Development files for Java Class Libraries.

%description -n libgcj-devel -l es.UTF-8
Ficheros de desarrollo para las bibliotecas de clases de Java.

%description -n libgcj-devel -l pl.UTF-8
Pliki nagłówkowe dla Bibliotek Klas Javy.

%package -n libgcj-static
Summary:	Static Java Class Libraries
Summary(es.UTF-8):	Bibliotecas estáticas de clases de Java
Summary(pl.UTF-8):	Statyczne Biblioteki Klas Javy
License:	GPL v2+ with limited linking exception
Group:		Development/Libraries
Requires:	libgcj-devel = %{epoch}:%{version}-%{release}

%description -n libgcj-static
Static Java Class Libraries.

%description -n libgcj-static -l es.UTF-8
Bibliotecas estáticas de clases de Java.

%description -n libgcj-static -l pl.UTF-8
Statyczne Biblioteki Klas Javy.

%package -n libffi
Summary:	Foreign Function Interface library
Summary(es.UTF-8):	Biblioteca de interfaz de funciones ajenas
Summary(pl.UTF-8):	Biblioteka zewnętrznych wywołań funkcji
License:	BSD-like
Group:		Libraries

%description -n libffi
The libffi library provides a portable, high level programming
interface to various calling conventions. This allows a programmer to
call any function specified by a call interface description at run
time.

%description -n libffi -l es.UTF-8
La biblioteca libffi provee una interfaz portable de programación de
alto nivel para varias convenciones de llamada. Ello permite que un
programador llame una función cualquiera especificada por una
descripción de interfaz de llamada en el tiempo de ejecución.

%description -n libffi -l pl.UTF-8
Biblioteka libffi dostarcza przenośnego, wysokopoziomowego
międzymordzia do różnych konwencji wywołań funkcji. Pozwala to
programiście wywoływać dowolne funkcje podając konwencję wywołania w
czasie wykonania.

%package -n libffi-multilib
Summary:	Foreign Function Interface library - 32-bit version
Summary(pl.UTF-8):	Biblioteka zewnętrznych wywołań funkcji - wersja 32-bitowa
License:	BSD-like
Group:		Libraries

%description -n libffi-multilib
The libffi library provides a portable, high level programming
interface to various calling conventions. This allows a programmer to
call any function specified by a call interface description at run
time. This package contains 32-bit version of the library.

%description -n libffi-multilib -l pl.UTF-8
Biblioteka libffi dostarcza przenośnego, wysokopoziomowego
międzymordzia do różnych konwencji wywołań funkcji. Pozwala to
programiście wywoływać dowolne funkcje podając konwencję wywołania w
czasie wykonania. Ten pakiet zawiera wersję 32-bitową biblioteki.

%package -n libffi-devel
Summary:	Development files for Foreign Function Interface library
Summary(es.UTF-8):	Ficheros de desarrollo para libffi
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libffi
License:	BSD-like
Group:		Development/Libraries
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libffi = %{epoch}:%{version}-%{release}

%description -n libffi-devel
Development files for Foreign Function Interface library.

%description -n libffi-devel -l es.UTF-8
Ficheros de desarrollo para libffi.

%description -n libffi-devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libffi.

%package -n libffi-multilib-devel
Summary:	Development files for 32-bit version of Foreign Function Interface library
Summary(pl.UTF-8):	Pliki programistyczne 32-bitowej wersji biblioteki libffi
License:	BSD-like
Group:		Development/Libraries
Requires:	libffi-devel = %{epoch}:%{version}-%{release}
Requires:	libffi-multilib = %{epoch}:%{version}-%{release}

%description -n libffi-multilib-devel
Development files for 32-bit version of Foreign Function Interface
library.

%description -n libffi-multilib-devel -l pl.UTF-8
Pliki programistyczne 32-bitowej wersji biblioteki libffi.

%package -n libffi-static
Summary:	Static Foreign Function Interface library
Summary(es.UTF-8):	Biblioteca libffi estática
Summary(pl.UTF-8):	Statyczna biblioteka libffi
License:	BSD-like
Group:		Development/Libraries
Requires:	libffi-devel = %{epoch}:%{version}-%{release}

%description -n libffi-static
Static Foreign Function Interface library.

%description -n libffi-static -l es.UTF-8
Biblioteca libffi estática.

%description -n libffi-static -l pl.UTF-8
Statyczna biblioteka libffi.

%package -n libffi-multilib-static
Summary:	Static Foreign Function Interface library - 32-bit version
Summary(pl.UTF-8):	Statyczna biblioteka libffi - wersja 32-bitowa
License:	BSD-like
Group:		Development/Libraries
Requires:	libffi-multilib-devel = %{epoch}:%{version}-%{release}

%description -n libffi-multilib-static
Static Foreign Function Interface library - 32-bit version.

%description -n libffi-multilib-static -l pl.UTF-8
Statyczna biblioteka libffi - wersja 32-bitowa.

%package objc
Summary:	Objective C support for gcc
Summary(de.UTF-8):	Objektive C-Unterstützung für gcc
Summary(es.UTF-8):	Soporte de Objective C para gcc
Summary(fr.UTF-8):	Gestion d'Objective C pour gcc
Summary(pl.UTF-8):	Obsługa obiektowego C dla kompilatora gcc
Summary(tr.UTF-8):	gcc için Objective C desteği
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libobjc = %{epoch}:%{version}-%{release}
Obsoletes:	egcc-objc
Obsoletes:	egcs-objc

%description objc
This package adds Objective C support to the GNU Compiler Collection.
Objective C is a object oriented derivative of the C language, mainly
used on systems running NeXTSTEP. This package does not include the
standard objective C object library.

%description objc -l de.UTF-8
Dieses Paket ergänzt den GNU-Compiler-Collection durch
Objective-C-Support. Objective C ist ein objektorientiertes Derivat
von C, das zur Hauptsache auf Systemen mit NeXTSTEP zum Einsatz kommt.
Die Standard-Objective-C-Objekt-Library ist nicht Teil des Pakets.

%description objc -l es.UTF-8
Este paquete añade soporte de Objective C al GCC (colección de
compiladores GNU). Objective C es un lenguaje orientado a objetos
derivado de C, principalmente usado en sistemas que funcionan bajo
NeXTSTEP. El paquete no incluye la biblioteca de objetos estándar de
Objective C.

%description objc -l fr.UTF-8
Ce package ajoute un support Objective C a la collection de
compilateurs GNU. L'Objective C est un langage orienté objetdérivé du
langage C, principalement utilisé sur les systèmes NeXTSTEP. Ce
package n'inclue pas la bibliothéque Objective C standard.

%description objc -l pl.UTF-8
Ten pakiet dodaje obsługę obiektowego C do kompilatora gcc. Obiektowe
C (objc) jest zorientowaną obiektowo pochodną języka C, używaną
głównie w systemach używających NeXTSTEP. W pakiecie nie ma
standardowej biblioteki objc (która znajduje się w osobnym pakiecie).

%description objc -l tr.UTF-8
Bu paket, GNU C derleyicisine Objective C desteği ekler. Objective C,
C dilinin nesne yönelik bir türevidir ve NeXTSTEP altında çalışan
sistemlerde yaygın olarak kullanılır. Standart Objective C nesne
kitaplığı bu pakette yer almaz.

%package objc-multilib
Summary:	32-bit Objective C support for gcc
Summary(pl.UTF-8):	Obsługa 32-bitowych binariów Objective C dla kompilatora gcc
Group:		Development/Languages
Requires:	%{name}-multilib = %{epoch}:%{version}-%{release}
Requires:	libobjc-multilib = %{epoch}:%{version}-%{release}

%description objc-multilib
This package adds 32-bit Objective C support to the GNU Compiler
Collection.

%description objc-multilib -l pl.UTF-8
Ten pakiet dodaje obsługę 32-bitowych binariów Objective C do
kompilatora gcc.

%package objc++
Summary:	Objective C++ support for gcc
Summary(pl.UTF-8):	Obsługa języka Objective C++ dla gcc
Group:		Development/Languages
Requires:	%{name}-c++ = %{epoch}:%{version}-%{release}
Requires:	%{name}-objc = %{epoch}:%{version}-%{release}

%description objc++
This package adds Objective C++ support to the GNU Compiler
Collection.

%description objc++ -l pl.UTF-8
Ten pakiet dodaje obsługę języka Objective C++ do zestawu kompilatorów
GNU Compiler Collection.

%package -n libobjc
Summary:	Objective C Library
Summary(es.UTF-8):	Biblioteca de Objective C
Summary(pl.UTF-8):	Biblioteka Obiektowego C
License:	GPL v2+ with linking exception
Group:		Libraries
Obsoletes:	libobjc1

%description -n libobjc
Objective C Library.

%description -n libobjc -l es.UTF-8
Bibliotecas de Objective C.

%description -n libobjc -l pl.UTF-8
Biblioteka Obiektowego C.

%package -n libobjc-multilib
Summary:	Objective C Library - 32-bit version
Summary(pl.UTF-8):	Biblioteka Obiektowego C - wersja 32-bitowa
License:	GPL v2+ with linking exception
Group:		Libraries

%description -n libobjc-multilib
Objective C Library - 32-bit version.

%description -n libobjc-multilib -l pl.UTF-8
Biblioteka Obiektowego C - wersja 32-bitowa.

%package -n libobjc-static
Summary:	Static Objective C Library
Summary(es.UTF-8):	Bibliotecas estáticas de Objective C
Summary(pl.UTF-8):	Statyczna Biblioteka Obiektowego C
License:	GPL v2+ with linking exception
Group:		Development/Libraries
Requires:	libobjc = %{epoch}:%{version}-%{release}

%description -n libobjc-static
Static Objective C Library.

%description -n libobjc-static -l es.UTF-8
Bibliotecas estáticas de Objective C.

%description -n libobjc-static -l pl.UTF-8
Statyczna biblioteka Obiektowego C.

%package -n libobjc-multilib-static
Summary:	Static Objective C Library - 32-bit version
Summary(pl.UTF-8):	Statyczna Biblioteka Obiektowego C - wersja 32-bitowa
License:	GPL v2+ with linking exception
Group:		Development/Libraries
Requires:	libobjc-multilib = %{epoch}:%{version}-%{release}

%description -n libobjc-multilib-static
Static Objective C Library - 32-bit version.

%description -n libobjc-multilib-static -l pl.UTF-8
Statyczna biblioteki Obiektowego C - wersja 32-bitowa.

%package go
Summary:	Go language support for gcc
Summary(pl.UTF-8):	Obsługa języka Go dla kompilatora gcc
License:	GPL v3+ (gcc), BSD (Go-specific part)
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libgo-devel = %{epoch}:%{version}-%{release}

%description go
This package adds Go language support to the GNU Compiler Collection.

%description go -l pl.UTF-8
Ten pakiet dodaje obsługę języka Go do kompilatora gcc.

%package go-multilib
Summary:	32-bit Go language support for gcc
Summary(pl.UTF-8):	Obsługa 32-bitowych binariów języka Go dla kompilatora gcc
License:	GPL v3+ (gcc), BSD (Go-specific part)
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{version}-%{release}
Requires:	libgo-multilib-devel = %{epoch}:%{version}-%{release}

%description go-multilib
This package adds 32-bit Go language support to the GNU Compiler
Collection.

%description go-multilib -l pl.UTF-8
Ten pakiet dodaje obsługę 32-bitowych binariów języka Go do
kompilatora gcc.

%package -n libgo
Summary:	Go language library
Summary(pl.UTF-8):	Biblioteka języka Go
License:	BSD
Group:		Libraries
Requires:	libgcc >= %{epoch}:%{version}-%{release}

%description -n libgo
Go language library.

%description -n libgo -l pl.UTF-8
Biblioteka języka Go.

%package -n libgo-multilib
Summary:	Go language library - 32-bit version
Summary(pl.UTF-8):	Biblioteka języka Go - wersja 32-bitowa
License:	BSD
Group:		Libraries
Requires:	libgcc-multilib >= %{epoch}:%{version}-%{release}

%description -n libgo-multilib
Go language library - 32-bit version.

%description -n libgo-multilib -l pl.UTF-8
Biblioteka języka Go - wersja 32-bitowa.

%package -n libgo-devel
Summary:	Development files for Go language library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki języka Go
License:	BSD
Group:		Development/Libraries
Requires:	glibc-devel
Requires:	libgo = %{epoch}:%{version}-%{release}

%description -n libgo-devel
Development files for Go language library.

%description -n libgo-devel -l pl.UTF-8
Pliki programistyczne biblioteki języka Go.

%package -n libgo-multilib-devel
Summary:	Development files for Go language library - 32-bit version
Summary(pl.UTF-8):	Pliki programistyczne biblioteki języka Go - wersja 32-bitowa
License:	BSD
Group:		Development/Libraries
Requires:	glibc-devel
Requires:	libgo-multilib = %{epoch}:%{version}-%{release}

%description -n libgo-multilib-devel
Development files for Go language library - 32-bit version.

%description -n libgo-multilib-devel -l pl.UTF-8
Pliki programistyczne biblioteki języka Go - wersja 32-bitowa.

%package -n libgo-static
Summary:	Static Go language library
Summary(pl.UTF-8):	Statyczna biblioteka języka Go
License:	BSD
Group:		Development/Libraries
Requires:	libgo-devel = %{epoch}:%{version}-%{release}

%description -n libgo-static
Static Go language library.

%description -n libgo-static -l pl.UTF-8
Statyczna biblioteka języka Go.

%package -n libgo-multilib-static
Summary:	Static Go language library - 32-bit version
Summary(pl.UTF-8):	Statyczna biblioteka języka Go - wersja 32-bitowa
License:	BSD
Group:		Development/Libraries
Requires:	libgo-multilib-devel = %{epoch}:%{version}-%{release}

%description -n libgo-multilib-static
Static Go language library - 32-bit version.

%description -n libgo-multilib-static -l pl.UTF-8
Statyczna biblioteka języka Go - wersja 32-bitowa.

%package -n libasan
Summary:	The Address Sanitizer library
Summary(pl.UTF-8):	Biblioteka Address Sanitizer do kontroli adresów
Group:		Libraries

%description -n libasan
This package contains the Address Sanitizer library which is used for
-fsanitize=address instrumented programs.

%description -n libasan -l pl.UTF-8
Ten pakiet zawiera bibliotekę Address Sanitizer, służącą do kontroli
adresów w programach kompilowanych z opcją -fsanitize=address.

%package -n libasan-multilib
Summary:	The Address Sanitizer library - 32-bit version
Summary(pl.UTF-8):	Biblioteka Address Sanitizer do kontroli adresów - wersja 32-bitowa
Group:		Libraries

%description -n libasan-multilib
This package contains 32-bit version of the Address Sanitizer library
which is used for -fsanitize=address instrumented programs.

%description -n libasan-multilib -l pl.UTF-8
Ten pakiet zawiera 32-bitową wersję biblioteki Address Sanitizer,
służącej do kontroli adresów w programach kompilowanych z opcją
-fsanitize=address.

%package -n libasan-devel
Summary:	Development files for the Address Sanitizer library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki Address Sanitizer
Group:		Development/Libraries
Requires:	libasan = %{epoch}:%{version}-%{release}

%description -n libasan-devel
This package contains development files for the Address Sanitizer
library.

%description -n libasan-devel -l pl.UTF-8
Ten pakiet zawiera pliki programistyczne biblioteki Address Sanitizer.

%package -n libasan-multilib-devel
Summary:	Development files for the Address Sanitizer library - 32-bit version
Summary(pl.UTF-8):	Pliki programistyczne biblioteki Address Sanitizer - wersja 32-bitowa
Group:		Development/Libraries
Requires:	libasan-multilib = %{epoch}:%{version}-%{release}

%description -n libasan-multilib-devel
This package contains the development files for 32-bit version of the
Address Sanitizer library.

%description -n libasan-multilib-devel -l pl.UTF-8
Ten pakiet zawiera pliki programistyczne 32-bitowej wersji biblioteki
Address Sanitizer.

%package -n libasan-static
Summary:	The Address Sanitizer static library
Summary(pl.UTF-8):	Statyczna biblioteka Address Sanitizer
Group:		Development/Libraries
Requires:	libasan-devel = %{epoch}:%{version}-%{release}

%description -n libasan-static
This package contains Address Sanitizer static library.

%description -n libasan-static -l pl.UTF-8
Ten pakiet zawiera statyczną bibliotekę Address Sanitizer.

%package -n libasan-multilib-static
Summary:	The Address Sanitizer static library - 32-bit version
Summary(pl.UTF-8):	Statyczna biblioteka Address Sanitizer - wersja 32-bitowa
Group:		Development/Libraries
Requires:	libasan-multilib-devel = %{epoch}:%{version}-%{release}

%description -n libasan-multilib-static
This package contains 32-bit version of the Address Sanitizer static
library.

%description -n libasan-multilib-static -l pl.UTF-8
Ten pakiet zawiera 32-bitową wersję statycznej biblioteki Address
Sanitizer.

%package -n liblsan
Summary:	The Leak Sanitizer library
Summary(pl.UTF-8):	Biblioteka Leak Sanitizer do kontroli adresów
Group:		Libraries

%description -n liblsan
This package contains the Leak Sanitizer library which is used for
-fsanitize=leak instrumented programs.

%description -n liblsan -l pl.UTF-8
Ten pakiet zawiera bibliotekę Leak Sanitizer, służącą do
kontroli adresów w programach kompilowanych z opcją
-fsanitize=leak.

%package -n liblsan-devel
Summary:	Development files for the Leak Sanitizer library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki Leak Sanitizer
Group:		Development/Libraries
Requires:	liblsan = %{epoch}:%{version}-%{release}

%description -n liblsan-devel
This package contains development files for the Leak Sanitizer
library.

%description -n liblsan-devel -l pl.UTF-8
Ten pakiet zawiera pliki programistyczne biblioteki Leak Sanitizer.

%package -n liblsan-static
Summary:	The Leak Sanitizer static library
Summary(pl.UTF-8):	Statyczna biblioteka Leak Sanitizer
Group:		Development/Libraries
Requires:	liblsan-devel = %{epoch}:%{version}-%{release}

%description -n liblsan-static
This package contains Leak Sanitizer static library.

%description -n liblsan-static -l pl.UTF-8
Ten pakiet zawiera statyczną bibliotekę Leak Sanitizer.

%package -n libtsan
Summary:	The Thread Sanitizer library
Summary(pl.UTF-8):	Biblioteka Thread Sanitizer do kontroli wielowątkowości
Group:		Libraries

%description -n libtsan
This package contains the Thread Sanitizer library which is used for
-fsanitize=thread instrumented programs.

%description -n libtsan -l pl.UTF-8
Ten pakiet zawiera bibliotekę Thread Sanitizer, służącą do kontroli
wielowątkowości w programach kompilowanych z opcją -fsanitize=thread.

%package -n libtsan-devel
Summary:	Development files for the Thread Sanitizer library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki Thread Sanitizer
Group:		Development/Libraries
Requires:	libtsan = %{epoch}:%{version}-%{release}

%description -n libtsan-devel
This package contains development files for Thread Sanitizer library.

%description -n libtsan-devel -l pl.UTF-8
Ten pakiet zawiera pliki programistyczne biblioteki Address Sanitizer.

%package -n libtsan-static
Summary:	The Thread Sanitizer static library
Summary(pl.UTF-8):	Statyczna biblioteka Thread Sanitizer
Group:		Development/Libraries
Requires:	libtsan-devel = %{epoch}:%{version}-%{release}

%description -n libtsan-static
This package contains Thread Sanitizer static library.

%description -n libtsan-static -l pl.UTF-8
Ten pakiet zawiera statyczną bibliotekę Thread Sanitizer.

%package -n libubsan
Summary:	The Undefined Behavior Sanitizer library
Summary(pl.UTF-8):	Biblioteka Undefined Behavior Sanitizer do kontroli adresów
Group:		Libraries

%description -n libubsan
This package contains the Undefined Behavior Sanitizer library which is used for
-fsanitize=undefined instrumented programs.

%description -n libubsan -l pl.UTF-8
Ten pakiet zawiera bibliotekę Undefined Behavior Sanitizer, służącą do
kontroli adresów w programach kompilowanych z opcją
-fsanitize=undefined.

%package -n libubsan-multilib
Summary:	The Undefined Behavior Sanitizer library - 32-bit version
Summary(pl.UTF-8):	Biblioteka Undefined Behavior Sanitizer do kontroli adresów - wersja 32-bitowa
Group:		Libraries

%description -n libubsan-multilib
This package contains 32-bit version of the Undefined Behavior
Sanitizer library which is used for -fsanitize=undefined instrumented
programs.

%description -n libubsan-multilib -l pl.UTF-8
Ten pakiet zawiera 32-bitową wersję biblioteki Undefined Behavior
Sanitizer, służącej do kontroli adresów w programach kompilowanych z
opcją -fsanitize=undefined.

%package -n libubsan-devel
Summary:	Development files for the Undefined Behavior Sanitizer library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki Undefined Behavior Sanitizer
Group:		Development/Libraries
Requires:	libubsan = %{epoch}:%{version}-%{release}

%description -n libubsan-devel
This package contains development files for the Undefined Behavior
Sanitizer library.

%description -n libubsan-devel -l pl.UTF-8
Ten pakiet zawiera pliki programistyczne biblioteki Undefined Behavior
Sanitizer.

%package -n libubsan-multilib-devel
Summary:	Development files for the Undefined Behavior Sanitizer library - 32-bit version
Summary(pl.UTF-8):	Pliki programistyczne biblioteki Undefined Behavior Sanitizer - wersja 32-bitowa
Group:		Development/Libraries
Requires:	libubsan-multilib = %{epoch}:%{version}-%{release}

%description -n libubsan-multilib-devel
This package contains the development files for 32-bit version of the
Undefined Behavior Sanitizer library.

%description -n libubsan-multilib-devel -l pl.UTF-8
Ten pakiet zawiera pliki programistyczne 32-bitowej wersji biblioteki
Undefined Behavior Sanitizer.

%package -n libubsan-static
Summary:	The Undefined Behavior Sanitizer static library
Summary(pl.UTF-8):	Statyczna biblioteka Undefined Behavior Sanitizer
Group:		Development/Libraries
Requires:	libubsan-devel = %{epoch}:%{version}-%{release}

%description -n libubsan-static
This package contains Undefined Behavior Sanitizer static library.

%description -n libubsan-static -l pl.UTF-8
Ten pakiet zawiera statyczną bibliotekę Undefined Behavior Sanitizer.

%package -n libubsan-multilib-static
Summary:	The Undefined Behavior Sanitizer static library - 32-bit version
Summary(pl.UTF-8):	Statyczna biblioteka Undefined Behavior Sanitizer - wersja 32-bitowa
Group:		Development/Libraries
Requires:	libubsan-multilib-devel = %{epoch}:%{version}-%{release}

%description -n libubsan-multilib-static
This package contains 32-bit version of the Undefined Behavior
Sanitizer static library.

%description -n libubsan-multilib-static -l pl.UTF-8
Ten pakiet zawiera 32-bitową wersję statycznej biblioteki Undefined
Behavior Sanitizer.


%package -n libatomic
Summary:	The GNU Atomic library
Summary(pl.UTF-8):	Biblioteka GNU Atomic
Group:		Libraries

%description -n libatomic
This package contains the GNU Atomic library which is a GCC support
library for atomic operations not supported by hardware.

%description -n libatomic -l pl.UTF-8
Ten pakiet zawiera bibliotekę GNU Atomic, będącą biblioteką GCC
wspierającą operacje atomowe na sprzęcie ich nie obsługującym.

%package -n libatomic-multilib
Summary:	The GNU Atomic library - 32-bit version
Summary(pl.UTF-8):	Biblioteka GNU Atomic - wersja 32-bitowa
Group:		Libraries

%description -n libatomic-multilib
This package contains 32-bit version of the GNU Atomic library which
is a GCC support library for atomic operations not supported by
hardware.

%description -n libatomic-multilib -l pl.UTF-8
Ten pakiet zawiera 32-bitową wersję biblioteki GNU Atomic, będącej
biblioteką GCC wspierającą operacje atomowe na sprzęcie ich nie
obsługującym.

%package -n libatomic-devel
Summary:	Development files for the GNU Atomic library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki GNU Atomic
Group:		Development/Libraries
Requires:	libatomic = %{epoch}:%{version}-%{release}

%description -n libatomic-devel
This package contains development files for the GNU Atomic library.

%description -n libatomic-devel -l pl.UTF-8
Ten pakiet zawiera pliki programistyczne biblioteki GNU Atomic.

%package -n libatomic-multilib-devel
Summary:	Development files for the GNU Atomic static library - 32-bit version
Summary(pl.UTF-8):	Pliki programistyczne biblioteki GNU Atomic - wersja 32-bitowa
Group:		Development/Libraries
Requires:	libatomic-multilib = %{epoch}:%{version}-%{release}

%description -n libatomic-multilib-devel
This package contains the development files for 32-bit version of the
GNU Atomic library.

%description -n libatomic-multilib-devel -l pl.UTF-8
Ten pakiet zawiera pliki programistyczne 32-bitowej wersji biblioteki
GNU Atomic.

%package -n libatomic-static
Summary:	The GNU Atomic static library
Summary(pl.UTF-8):	Statyczna biblioteka GNU Atomic
Group:		Development/Libraries
Requires:	libatomic-devel = %{epoch}:%{version}-%{release}

%description -n libatomic-static
This package contains GNU Atomic static library.

%description -n libatomic-static
Ten pakiet zawiera statyczną bibliotekę GNU Atomic.

%package -n libatomic-multilib-static
Summary:	The GNU Atomic static library - 32-bit version
Summary(pl.UTF-8):	Statyczna biblioteka GNU Atomic - wersja 32-bitowa
Group:		Development/Libraries
Requires:	libatomic-multilib-devel = %{epoch}:%{version}-%{release}

%description -n libatomic-multilib-static
This package contains 32-bit version of the GNU Atomic static library.

%description -n libatomic-multilib-static -l pl.UTF-8
Ten pakiet zawiera 32-bitową wersję statycznej biblioteki GNU Atomic.

%prep
%setup -q
%patch100 -p0
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

%patch5 -p1
%patch6 -p1
%patch7 -p0
%if %{with qt}
%patch8 -p1
%endif
%patch10 -p1
%if %{with gcc_libffi}
%patch11 -p0
%endif

mv ChangeLog ChangeLog.general

%if %{with java}
# see contrib/download_ecj
cp -p %{SOURCE2} ecj.jar
%endif

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
%ifarch %{ix86} %{x8664}
	--disable-cld \
%endif
	%{?with_fortran:--enable-cmath} \
	--enable-decimal-float \
	--enable-gnu-unique-object \
	--enable-gnu-indirect-function \
	--enable-initfini-array \
	--enable-languages="c%{?with_cxx:,c++}%{?with_fortran:,fortran}%{?with_objc:,objc}%{?with_objcxx:,obj-c++}%{?with_ada:,ada}%{?with_java:,java}%{?with_go:,go}" \
	--%{?with_gomp:en}%{!?with_gomp:dis}able-libgomp \
	--enable-libitm \
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
	--with-cloog \
%ifarch %{ix86}
	--with-arch=x86-64 \
%endif
%ifarch %{x8664}
	--with-arch-32=x86-64 \
%endif
%ifarch sparc64
	--with-cpu=ultrasparc \
%endif
	--with-demangler-in-ld \
	--with-gnu-as \
	--with-gnu-ld \
	--with-linker-hash-style=gnu \
	--with-long-double-128 \
	--with-ppl \
	--disable-ppl-version-check \
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
	--enable-libgcj-multifile \
	--enable-libgcj-database \
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

libssp=$(cd $RPM_BUILD_ROOT%{_libdir}; echo libssp.so.*.*.*)
mv $RPM_BUILD_ROOT%{_libdir}/libssp.so.* $RPM_BUILD_ROOT%{_slibdir}
ln -sf %{_slibdir}/$libssp $RPM_BUILD_ROOT%{_libdir}/libssp.so

libitm=$(cd $RPM_BUILD_ROOT%{_libdir}; echo libitm.so.*.*.*)
mv $RPM_BUILD_ROOT%{_libdir}/libitm.so.* $RPM_BUILD_ROOT%{_slibdir}
ln -sf %{_slibdir}/$libitm $RPM_BUILD_ROOT%{_libdir}/libitm.so

libgomp=$(cd $RPM_BUILD_ROOT%{_libdir}; echo libgomp.so.*.*.*)
mv $RPM_BUILD_ROOT%{_libdir}/libgomp.so.* $RPM_BUILD_ROOT%{_slibdir}
ln -sf %{_slibdir}/$libgomp $RPM_BUILD_ROOT%{_libdir}/libgomp.so

%if %{with multilib}
libssp=$(cd $RPM_BUILD_ROOT%{_libdir32}; echo libssp.so.*.*.*)
mv $RPM_BUILD_ROOT%{_libdir32}/libssp.so.* $RPM_BUILD_ROOT%{_slibdir32}
ln -sf %{_slibdir32}/$libssp $RPM_BUILD_ROOT%{_libdir32}/libssp.so

libitm=$(cd $RPM_BUILD_ROOT%{_libdir32}; echo libitm.so.*.*.*)
mv $RPM_BUILD_ROOT%{_libdir32}/libitm.so.* $RPM_BUILD_ROOT%{_slibdir32}
ln -sf %{_slibdir32}/$libitm $RPM_BUILD_ROOT%{_libdir32}/libitm.so

libgomp=$(cd $RPM_BUILD_ROOT%{_libdir32}; echo libgomp.so.*.*.*)
mv $RPM_BUILD_ROOT%{_libdir32}/libgomp.so.* $RPM_BUILD_ROOT%{_slibdir32}
ln -sf %{_slibdir32}/$libgomp $RPM_BUILD_ROOT%{_libdir32}/libgomp.so
%endif

%if %{with fortran}
ln -sf gfortran $RPM_BUILD_ROOT%{_bindir}/g95
echo ".so man1/gfortran.1" > $RPM_BUILD_ROOT%{_mandir}/man1/g95.1
%endif

%if %{with ada}
# move ada shared libraries to proper place...
mv -f	$RPM_BUILD_ROOT%{gcclibdir}/adalib/*.so.1 \
	$RPM_BUILD_ROOT%{_libdir}
# check if symlink to be made is valid
test -f	$RPM_BUILD_ROOT%{_libdir}/libgnat-%{major_ver}.so.1
ln -sf	libgnat-%{major_ver}.so.1 $RPM_BUILD_ROOT%{_libdir}/libgnat-%{major_ver}.so
ln -sf	libgnarl-%{major_ver}.so.1 $RPM_BUILD_ROOT%{_libdir}/libgnarl-%{major_ver}.so
ln -sf	libgnat-%{major_ver}.so $RPM_BUILD_ROOT%{_libdir}/libgnat.so
ln -sf	libgnarl-%{major_ver}.so $RPM_BUILD_ROOT%{_libdir}/libgnarl.so
%if %{with multilib}
mv -f	$RPM_BUILD_ROOT%{gcclibdir}/32/adalib/*.so.1 \
	$RPM_BUILD_ROOT%{_libdir32}
# check if symlink to be made is valid
test -f	$RPM_BUILD_ROOT%{_libdir32}/libgnat-%{major_ver}.so.1
ln -sf	libgnat-%{major_ver}.so.1 $RPM_BUILD_ROOT%{_libdir32}/libgnat-%{major_ver}.so
ln -sf	libgnarl-%{major_ver}.so.1 $RPM_BUILD_ROOT%{_libdir32}/libgnarl-%{major_ver}.so
ln -sf	libgnat-%{major_ver}.so $RPM_BUILD_ROOT%{_libdir32}/libgnat.so
ln -sf	libgnarl-%{major_ver}.so $RPM_BUILD_ROOT%{_libdir32}/libgnarl.so
%endif
%endif

cd ..

%if %{with java}
install -d java-doc
cp -f libjava/READ* java-doc
ln -sf libgcj-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/libgcj.jar
%endif

%if %{with gcc_libffi}
# still not installed by gcc?
[ ! -f $RPM_BUILD_ROOT%{_pkgconfigdir}/libffi.pc ] || exit 1
install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
sed -e 's,@prefix@,%{_prefix},
	s,@exec_prefix@,%{_exec_prefix},
	s,@libdir@,%{_libdir},
	s,@gcclibdir@,%{gcclibdir},' %{SOURCE3} >$RPM_BUILD_ROOT%{_pkgconfigdir}/libffi.pc
%if %{with multilib}
[ ! -f $RPM_BUILD_ROOT%{_pkgconfigdir32}/libffi.pc ] || exit 1
install -d $RPM_BUILD_ROOT%{_pkgconfigdir32}
sed -e 's,@prefix@,%{_prefix},
	s,@exec_prefix@,%{_exec_prefix},
	s,@libdir@,%{_libdir32},
	s,@gcclibdir@,%{gcclibdir},' %{SOURCE3} >$RPM_BUILD_ROOT%{_pkgconfigdir32}/libffi.pc
%endif
%endif

%if %{with objc}
cp -f libobjc/README gcc/objc/README.libobjc
%endif

# avoid -L poisoning in *.la - there should be only -L%{_libdir}/gcc/%{_target_platform}/%{version}
# normalize libdir, to avoid propagation of unnecessary RPATHs by libtool
for f in libitm.la libssp.la libssp_nonshared.la \
	%{?with_cxx:libstdc++.la libsupc++.la} \
	%{?with_fortran:libgfortran.la libquadmath.la} \
	%{?with_gomp:libgomp.la} \
	%{?with_asan:libasan.la} \
	liblsan.la \
	%{?with_tsan:libtsan.la} \
	libubsan.la \
	%{?with_atomic:libatomic.la} \
%if %{with java}
	%{?with_gcc_libffi:libffi.la} \
	libgcj.la libgcj-tools.la libgij.la \
	%{gcjdbexecdir}/libjvm.la \
	%{gcjdbexecdir}/libxmlj.la \
	%{?with_x:lib-gnu-awt-xlib.la} \
	%{?with_gtk:%{gcjdbexecdir}/libgtkpeer.la %{gcjdbexecdir}/libjawt.la} \
	%{?with_qt:%{gcjdbexecdir}/libqtpeer.la} \
	%{?with_alsa:%{gcjdbexecdir}/libgjsmalsa.la} \
	%{?with_dssi:%{gcjdbexecdir}/libgjsmdssi.la} \
%endif
	%{?with_objc:libobjc.la};
do
	%{__perl} %{SOURCE1} $RPM_BUILD_ROOT%{_libdir}/$f %{_libdir} > $RPM_BUILD_ROOT%{_libdir}/$f.fixed
	mv $RPM_BUILD_ROOT%{_libdir}/$f{.fixed,}
done
%if %{with multilib}
for f in libitm.la libssp.la libssp_nonshared.la \
	%{?with_cxx:libstdc++.la libsupc++.la} \
	%{?with_fortran:libgfortran.la libquadmath.la} \
	%{?with_gomp:libgomp.la} \
	%{?with_asan:libasan.la} \
	libubsan.la \
	%{?with_atomic:libatomic.la} \
	%{?with_java:%{?with_gcc_libffi:libffi.la}} \
	%{?with_objc:libobjc.la};
do
	%{__perl} %{SOURCE1} $RPM_BUILD_ROOT%{_libdir32}/$f %{_libdir32} > $RPM_BUILD_ROOT%{_libdir32}/$f.fixed
	mv $RPM_BUILD_ROOT%{_libdir32}/$f{.fixed,}
done
%endif

cp -p $RPM_BUILD_ROOT%{gcclibdir}/install-tools/include/*.h $RPM_BUILD_ROOT%{gcclibdir}/include
cp -p $RPM_BUILD_ROOT%{gcclibdir}/include-fixed/syslimits.h $RPM_BUILD_ROOT%{gcclibdir}/include
%{__rm} -r $RPM_BUILD_ROOT%{gcclibdir}/install-tools
%{__rm} -r $RPM_BUILD_ROOT%{gcclibdir}/include-fixed

# plugin, .la not needed
%{__rm} $RPM_BUILD_ROOT%{gcclibdir}/liblto_plugin.la

%if %{with python}
for LIB in lib lib64; do
	LIBPATH="$RPM_BUILD_ROOT%{_datadir}/gdb/auto-load%{_prefix}/$LIB"
	install -d $LIBPATH
	# basename is being run only for the native (non-biarch) file.
	sed -e 's,@pythondir@,%{_datadir}/gdb,' \
	  -e 's,@toolexeclibdir@,%{_prefix}/'"$LIB," \
	  < libstdc++-v3/python/hook.in	\
	  > $LIBPATH/$(basename $RPM_BUILD_ROOT%{_prefix}/%{_lib}/libstdc++.so.*.*.*)-gdb.py
done
install -d $RPM_BUILD_ROOT%{py_sitescriptdir}
mv $RPM_BUILD_ROOT%{_datadir}/gcc-%{version}/python/libstdcxx $RPM_BUILD_ROOT%{py_sitescriptdir}
%if %{with java}
mv $RPM_BUILD_ROOT%{_datadir}/gcc-%{version}/python/libjava $RPM_BUILD_ROOT%{py_sitescriptdir}
%{__sed} -i -e '1s,#!/usr/bin/env python,#!/usr/bin/python,' $RPM_BUILD_ROOT%{_bindir}/aot-compile
%endif
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}
%py_postclean
%else
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/gcc-%{version}/python/libstdcxx
%if %{with java}
%{__rm} -r $RPM_BUILD_ROOT%{_datadir}/gcc-%{version}/python/libjava
%endif
%endif
# script(s) always installed; see above for builds with python; if no python, just don't package
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libstdc++.so.*-gdb.py
%if %{with multilib}
%{__rm} $RPM_BUILD_ROOT%{_libdir32}/libstdc++.so.*-gdb.py
%endif

%find_lang gcc
%find_lang cpplib
cat cpplib.lang >> gcc.lang

%if %{with cxx}
%find_lang libstdc\+\+
cp -p libstdc++-v3/include/precompiled/* $RPM_BUILD_ROOT%{_includedir}
%endif

# always -f, as "dir" is created depending which texlive version is installed
%{__rm} -f $RPM_BUILD_ROOT%{_infodir}/dir

# is anything using this?
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libvtv*
%{?with_multilib:%{__rm} $RPM_BUILD_ROOT%{_libdir32}/libvtv*}

# svn snap doesn't contain (release does) below files,
# so let's create dummy entries to satisfy %%files.
[ ! -f NEWS ] && touch NEWS
[ ! -f libgfortran/AUTHORS ] && touch libgfortran/AUTHORS
[ ! -f libgfortran/README ] && touch libgfortran/README

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	ada -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	ada -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	fortran -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	fortran -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	java -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	java -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	go -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	go -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	-n libquadmath-devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-n libquadmath-devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post	-n libffi-devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%postun	-n libffi-devel -p /sbin/postshell
-/usr/sbin/fix-info-dir -c %{_infodir}

%post   -p /sbin/ldconfig -n libcilkrts
%postun -p /sbin/ldconfig -n libcilkrts
%post   -p /sbin/ldconfig -n libcilkrts-multilib
%postun -p /sbin/ldconfig -n libcilkrts-multilib
%post	-p /sbin/ldconfig -n libgcc
%postun	-p /sbin/ldconfig -n libgcc
%post	-p /sbin/ldconfig -n libgcc-multilib
%postun	-p /sbin/ldconfig -n libgcc-multilib
%post	-p /sbin/ldconfig -n libgomp
%postun	-p /sbin/ldconfig -n libgomp
%post	-p /sbin/ldconfig -n libgomp-multilib
%postun	-p /sbin/ldconfig -n libgomp-multilib
%post	-p /sbin/ldconfig -n libgnat
%postun	-p /sbin/ldconfig -n libgnat
%post	-p /sbin/ldconfig -n libgnat-multilib
%postun	-p /sbin/ldconfig -n libgnat-multilib
%post	-p /sbin/ldconfig -n libstdc++
%postun	-p /sbin/ldconfig -n libstdc++
%post	-p /sbin/ldconfig -n libstdc++-multilib
%postun	-p /sbin/ldconfig -n libstdc++-multilib
%post	-p /sbin/ldconfig -n libgfortran
%postun	-p /sbin/ldconfig -n libgfortran
%post	-p /sbin/ldconfig -n libgfortran-multilib
%postun	-p /sbin/ldconfig -n libgfortran-multilib
%post	-p /sbin/ldconfig -n libgcj
%postun	-p /sbin/ldconfig -n libgcj
%post	-p /sbin/ldconfig -n libffi
%postun	-p /sbin/ldconfig -n libffi
%post	-p /sbin/ldconfig -n libffi-multilib
%postun	-p /sbin/ldconfig -n libffi-multilib
%post	-p /sbin/ldconfig -n libobjc
%postun	-p /sbin/ldconfig -n libobjc
%post	-p /sbin/ldconfig -n libobjc-multilib
%postun	-p /sbin/ldconfig -n libobjc-multilib
%post	-p /sbin/ldconfig -n libquadmath
%postun	-p /sbin/ldconfig -n libquadmath
%post	-p /sbin/ldconfig -n libquadmath-multilib
%postun	-p /sbin/ldconfig -n libquadmath-multilib
%post	-p /sbin/ldconfig -n libgo
%postun	-p /sbin/ldconfig -n libgo
%post	-p /sbin/ldconfig -n libgo-multilib
%postun	-p /sbin/ldconfig -n libgo-multilib
%post	-p /sbin/ldconfig -n libasan
%postun	-p /sbin/ldconfig -n libasan
%post	-p /sbin/ldconfig -n libasan-multilib
%postun	-p /sbin/ldconfig -n libasan-multilib
%post	-p /sbin/ldconfig -n liblsan
%postun	-p /sbin/ldconfig -n liblsan
%post	-p /sbin/ldconfig -n libtsan
%postun	-p /sbin/ldconfig -n libtsan
%post   -p /sbin/ldconfig -n libubsan
%postun -p /sbin/ldconfig -n libubsan
%post   -p /sbin/ldconfig -n libubsan-multilib
%postun -p /sbin/ldconfig -n libubsan-multilib
%post	-p /sbin/ldconfig -n libatomic
%postun	-p /sbin/ldconfig -n libatomic
%post	-p /sbin/ldconfig -n libatomic-multilib
%postun	-p /sbin/ldconfig -n libatomic-multilib

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
#%attr(755,root,root) %{_bindir}/gccbug
%attr(755,root,root) %{_bindir}/gcov
%{_mandir}/man1/cc.1*
%{_mandir}/man1/cpp.1*
%{_mandir}/man1/gcc.1*
%{_mandir}/man1/gcov.1*
%{_infodir}/cpp.info*
%{_infodir}/cppinternals.info*
%{_infodir}/gcc.info*
%{_infodir}/gccinstall.info*
%{_infodir}/gccint.info*
%{_infodir}/libitm.info*
%attr(755,root,root) /lib/cpp
%attr(755,root,root) %{_slibdir}/libgcc_s.so
%attr(755,root,root) %{_libdir}/libitm.so
%attr(755,root,root) %{_libdir}/libssp.so
%{_libdir}/libitm.la
%{_libdir}/libitm.a
%{_libdir}/libitm.spec
%{_libdir}/libsanitizer.spec
%{_libdir}/libssp.la
%{_libdir}/libssp.a
%{_libdir}/libssp_nonshared.la
%{_libdir}/libssp_nonshared.a
%dir %{_libdir}/gcc
%dir %{_libdir}/gcc/%{_target_platform}
%dir %{gcclibdir}
%{gcclibdir}/libgcc.a
%{gcclibdir}/libgcc_eh.a
%{gcclibdir}/libgcov.a
%{gcclibdir}/specs
%{gcclibdir}/crt*.o
%attr(755,root,root) %{gcclibdir}/cc1
%attr(755,root,root) %{gcclibdir}/collect2
%attr(755,root,root) %{gcclibdir}/lto-wrapper
%attr(755,root,root) %{gcclibdir}/lto1
%attr(755,root,root) %{gcclibdir}/liblto_plugin.so*
%{gcclibdir}/plugin
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
%ifarch %{ix86} %{x8664}
%{gcclibdir}/include/adxintrin.h
%{gcclibdir}/include/ammintrin.h
%{gcclibdir}/include/avx2intrin.h
%{gcclibdir}/include/avx512cdintrin.h
%{gcclibdir}/include/avx512erintrin.h
%{gcclibdir}/include/avx512fintrin.h
%{gcclibdir}/include/avx512pfintrin.h
%{gcclibdir}/include/avxintrin.h
%{gcclibdir}/include/bmi2intrin.h
%{gcclibdir}/include/bmiintrin.h
%{gcclibdir}/include/bmmintrin.h
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
%{gcclibdir}/include/xsaveintrin.h
%{gcclibdir}/include/xsaveoptintrin.h
%{gcclibdir}/include/xtestintrin.h
%endif
%ifarch arm
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
%ifarch powerpc ppc ppc64
%{gcclibdir}/include/altivec.h
%{gcclibdir}/include/paired.h
%{gcclibdir}/include/ppc-asm.h
%{gcclibdir}/include/ppu_intrinsics.h
%{gcclibdir}/include/si2vmx.h
%{gcclibdir}/include/spe.h
%{gcclibdir}/include/spu2vmx.h
%{gcclibdir}/include/vec_types.h
%endif

%if %{with multilib}
%files multilib
%defattr(644,root,root,755)
%attr(755,root,root) %{_slibdir32}/libgcc_s.so
%dir %{gcclibdir}/32
%{gcclibdir}/32/crt*.o
%{gcclibdir}/32/libgcc.a
%{gcclibdir}/32/libgcc_eh.a
%{gcclibdir}/32/libgcov.a
%attr(755,root,root) %{_libdir32}/libitm.so
%attr(755,root,root) %{_libdir32}/libssp.so
%{_libdir32}/libitm.la
%{_libdir32}/libitm.a
%{_libdir32}/libssp.la
%{_libdir32}/libssp.a
%{_libdir32}/libssp_nonshared.la
%{_libdir32}/libssp_nonshared.a
%endif

%files -n libgcc
%defattr(644,root,root,755)
%attr(755,root,root) %{_slibdir}/libgcc_s.so.1
%attr(755,root,root) %{_slibdir}/libitm.so.*.*.*
%attr(755,root,root) %{_slibdir}/libssp.so.*.*.*
%attr(755,root,root) %ghost %{_slibdir}/libitm.so.1
%attr(755,root,root) %ghost %{_slibdir}/libssp.so.0

%if %{with multilib}
%files -n libgcc-multilib
%defattr(644,root,root,755)
%attr(755,root,root) %{_slibdir32}/libgcc_s.so.1
%attr(755,root,root) %{_slibdir32}/libitm.so.*.*.*
%attr(755,root,root) %{_slibdir32}/libssp.so.*.*.*
%attr(755,root,root) %ghost %{_slibdir32}/libssp.so.0
%attr(755,root,root) %ghost %{_slibdir32}/libitm.so.1
%endif

%if %{with gomp}
%files -n libgomp
%defattr(644,root,root,755)
%attr(755,root,root) %{_slibdir}/libgomp.so.*.*.*
%attr(755,root,root) %ghost %{_slibdir}/libgomp.so.1

%if %{with multilib}
%files -n libgomp-multilib
%defattr(644,root,root,755)
%attr(755,root,root) %{_slibdir32}/libgomp.so.*.*.*
%attr(755,root,root) %ghost %{_slibdir32}/libgomp.so.1
%endif

%files -n libgomp-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgomp.so
%{_libdir}/libgomp.la
%{_libdir}/libgomp.spec
%{gcclibdir}/finclude
%{gcclibdir}/include/omp.h
%{_infodir}/libgomp.info*

%if %{with multilib}
%files -n libgomp-multilib-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir32}/libgomp.so
%{_libdir32}/libgomp.la
%{_libdir32}/libgomp.spec
%endif

%files -n libgomp-static
%defattr(644,root,root,755)
%{_libdir}/libgomp.a

%if %{with multilib}
%files -n libgomp-multilib-static
%defattr(644,root,root,755)
%{_libdir32}/libgomp.a
%endif
%endif

%files -n libcilkrts
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcilkrts.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libcilkrts.so.5

%if %{with multilib}
%files -n libcilkrts-multilib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir32}/libcilkrts.so.*.*.*
%attr(755,root,root) %ghost %{_libdir32}/libcilkrts.so.5
%endif

%files -n libcilkrts-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcilkrts.so
%{_libdir}/libcilkrts.la
%{_libdir}/libcilkrts.spec
%{gcclibdir}/include/cilk

%if %{with multilib}
%files -n libcilkrts-multilib-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir32}/libcilkrts.so
%{_libdir32}/libcilkrts.la
%{_libdir32}/libcilkrts.spec
%endif

%files -n libcilkrts-static
%defattr(644,root,root,755)
%{_libdir}/libcilkrts.a

%if %{with multilib}
%files -n libcilkrts-multilib-static
%defattr(644,root,root,755)
%{_libdir32}/libcilkrts.a
%endif

%if %{with ada}
%files ada
%defattr(644,root,root,755)
%doc gcc/ada/ChangeLog
%attr(755,root,root) %{_bindir}/gnat*
%if %{with java}
%exclude %{_bindir}/gnative2ascii
%endif
%attr(755,root,root) %{_libdir}/libgnarl-*.so
%attr(755,root,root) %{_libdir}/libgnarl.so
%attr(755,root,root) %{_libdir}/libgnat-*.so
%attr(755,root,root) %{_libdir}/libgnat.so
%attr(755,root,root) %{gcclibdir}/gnat1
%{gcclibdir}/adainclude
%dir %{gcclibdir}/adalib
%{gcclibdir}/adalib/*.ali
%ifarch %{ix86} %{x8664}
%{gcclibdir}/adalib/libgmem.a
%endif
%{_infodir}/gnat-style.info*
%{_infodir}/gnat_rm.info*
%{_infodir}/gnat_ugn.info*

%if %{with multilib}
%files ada-multilib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir32}/libgnarl-*.so
%attr(755,root,root) %{_libdir32}/libgnarl.so
%attr(755,root,root) %{_libdir32}/libgnat-*.so
%attr(755,root,root) %{_libdir32}/libgnat.so
%{gcclibdir}/32/adainclude
%dir %{gcclibdir}/32/adalib
%{gcclibdir}/32/adalib/*.ali
%ifarch %{ix86} %{x8664}
%{gcclibdir}/32/adalib/libgmem.a
%endif
%endif

%files -n libgnat
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgnarl-*.so.1
%attr(755,root,root) %{_libdir}/libgnarl.so.1
%attr(755,root,root) %{_libdir}/libgnat-*.so.1
%attr(755,root,root) %{_libdir}/libgnat.so.1

%if %{with multilib}
%files -n libgnat-multilib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir32}/libgnarl-*.so.1
%attr(755,root,root) %{_libdir32}/libgnarl.so.1
%attr(755,root,root) %{_libdir32}/libgnat-*.so.1
%attr(755,root,root) %{_libdir32}/libgnat.so.1
%endif

%files -n libgnat-static
%defattr(644,root,root,755)
%{gcclibdir}/adalib/libgnarl.a
%{gcclibdir}/adalib/libgnat.a

%if %{with multilib}
%files -n libgnat-multilib-static
%defattr(644,root,root,755)
%{gcclibdir}/32/adalib/libgnarl.a
%{gcclibdir}/32/adalib/libgnat.a
%endif
%endif

%if %{with cxx}
%files c++
%defattr(644,root,root,755)
%doc gcc/cp/{ChangeLog,NEWS}
%attr(755,root,root) %{_bindir}/g++
%attr(755,root,root) %{_bindir}/*-g++
%attr(755,root,root) %{_bindir}/c++
%attr(755,root,root) %{_bindir}/*-c++
%attr(755,root,root) %{gcclibdir}/cc1plus
%{_libdir}/libsupc++.la
%{_libdir}/libsupc++.a
%{_mandir}/man1/g++.1*

%if %{with multilib}
%files c++-multilib
%defattr(644,root,root,755)
%{_libdir32}/libsupc++.la
%{_libdir32}/libsupc++.a
%endif

%files -n libstdc++ -f libstdc++.lang
%defattr(644,root,root,755)
%doc libstdc++-v3/{ChangeLog,README}
%attr(755,root,root) %{_libdir}/libstdc++.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libstdc++.so.%{cxx_sover}

%if %{with multilib}
%files -n libstdc++-multilib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir32}/libstdc++.so.*.*.*
%attr(755,root,root) %ghost %{_libdir32}/libstdc++.so.%{cxx_sover}
%endif

%if %{with python}
%files -n libstdc++-gdb
%defattr(644,root,root,755)
%dir %{py_sitescriptdir}/libstdcxx
%{py_sitescriptdir}/libstdcxx/*.py[co]
%dir %{py_sitescriptdir}/libstdcxx/v6
%{py_sitescriptdir}/libstdcxx/v6/*.py[co]
%{_datadir}/gdb/auto-load/usr/%{_lib}/libstdc++.so.%{cxx_sover}.*.*-gdb.py
%if %{with multilib}
%{_datadir}/gdb/auto-load/usr/lib/libstdc++.so.%{cxx_sover}.*.*-gdb.py
%endif
%endif

%files -n libstdc++-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libstdc++.so
%{_libdir}/libstdc++.la
%dir %{_includedir}/c++
%{_includedir}/c++/%{version}
%{_includedir}/extc++.h
%{_includedir}/stdc++.h
%{_includedir}/stdtr1c++.h
%if %{with java}
%exclude %{_includedir}/c++/%{version}/java
%exclude %{_includedir}/c++/%{version}/javax
%exclude %{_includedir}/c++/%{version}/gcj
%exclude %{_includedir}/c++/%{version}/gnu
%exclude %{_includedir}/c++/%{version}/org
%exclude %{_includedir}/c++/%{version}/sun
%endif

%if %{with apidocs}
%files -n libstdc++-apidocs
%defattr(644,root,root,755)
%doc libstdc++-v3/doc/html/*
%endif

%if %{with multilib}
%files -n libstdc++-multilib-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir32}/libstdc++.so
%{_libdir32}/libstdc++.la
%endif

%files -n libstdc++-static
%defattr(644,root,root,755)
%{_libdir}/libstdc++.a

%if %{with multilib}
%files -n libstdc++-multilib-static
%defattr(644,root,root,755)
%{_libdir32}/libstdc++.a
%endif
%endif

%if %{with fortran}
%files fortran
%defattr(644,root,root,755)
%doc gcc/fortran/ChangeLog
%attr(755,root,root) %{_bindir}/g95
%attr(755,root,root) %{_bindir}/gfortran
%attr(755,root,root) %{_bindir}/*-gfortran
%attr(755,root,root) %{gcclibdir}/f951
%attr(755,root,root) %{_libdir}/libgfortran.so
%{_libdir}/libgfortran.spec
%{_libdir}/libgfortran.la
%{gcclibdir}/libcaf_single.a
%{gcclibdir}/libcaf_single.la
%{gcclibdir}/libgfortranbegin.la
%{gcclibdir}/libgfortranbegin.a
%{_infodir}/gfortran.info*
%{_mandir}/man1/g95.1*
%{_mandir}/man1/gfortran.1*

%if %{with multilib}
%files fortran-multilib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir32}/libgfortran.so
%{_libdir32}/libgfortran.spec
%{_libdir32}/libgfortran.la
%{gcclibdir}/32/libcaf_single.a
%{gcclibdir}/32/libcaf_single.la
%{gcclibdir}/32/libgfortranbegin.la
%{gcclibdir}/32/libgfortranbegin.a
%endif

%files -n libgfortran
%defattr(644,root,root,755)
%doc libgfortran/{AUTHORS,README,ChangeLog}
%attr(755,root,root) %{_libdir}/libgfortran.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgfortran.so.3

%if %{with multilib}
%files -n libgfortran-multilib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir32}/libgfortran.so.*.*.*
%attr(755,root,root) %ghost %{_libdir32}/libgfortran.so.3
%endif

%files -n libgfortran-static
%defattr(644,root,root,755)
%{_libdir}/libgfortran.a

%if %{with multilib}
%files -n libgfortran-multilib-static
%defattr(644,root,root,755)
%{_libdir32}/libgfortran.a
%endif

%files -n libquadmath
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libquadmath.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libquadmath.so.0

%if %{with multilib}
%files -n libquadmath-multilib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir32}/libquadmath.so.*.*.*
%attr(755,root,root) %ghost %{_libdir32}/libquadmath.so.0
%endif

%files -n libquadmath-devel
%defattr(644,root,root,755)
%{gcclibdir}/include/quadmath.h
%{gcclibdir}/include/quadmath_weak.h
%attr(755,root,root) %{_libdir}/libquadmath.so
%{_libdir}/libquadmath.la
%{_infodir}/libquadmath.info*

%if %{with multilib}
%files -n libquadmath-multilib-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir32}/libquadmath.so
%{_libdir32}/libquadmath.la
%endif

%files -n libquadmath-static
%defattr(644,root,root,755)
%{_libdir}/libquadmath.a

%if %{with multilib}
%files -n libquadmath-multilib-static
%defattr(644,root,root,755)
%{_libdir32}/libquadmath.a
%endif
%endif

%if %{with java}
%files java
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
%attr(755,root,root) %{gcclibdir}/ecj1
%attr(755,root,root) %{gcclibdir}/jc1
%attr(755,root,root) %{gcclibdir}/jvgenmain
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
%files java-aotcompile
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
%{_javadir}/ecj.jar
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
%{gcclibdir}/include/gcj
%{gcclibdir}/include/jawt.h
%{gcclibdir}/include/jawt_md.h
%{gcclibdir}/include/jni.h
%{gcclibdir}/include/jni_md.h
%{gcclibdir}/include/jvmpi.h
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

%if %{with gcc_libffi}
%files -n libffi
%defattr(644,root,root,755)
%doc libffi/{ChangeLog,ChangeLog.libgcj,LICENSE,README}
%attr(755,root,root) %{_libdir}/libffi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libffi.so.4

%if %{with multilib}
%files -n libffi-multilib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir32}/libffi.so.*.*.*
%attr(755,root,root) %ghost %{_libdir32}/libffi.so.4
%endif

%files -n libffi-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libffi.so
%{_libdir}/libffi.la
%{gcclibdir}/include/ffi.h
%{gcclibdir}/include/ffitarget.h
%{_pkgconfigdir}/libffi.pc
%{_mandir}/man3/ffi*.3*
%{_infodir}/libffi.info*

%if %{with multilib}
%files -n libffi-multilib-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir32}/libffi.so
%{_libdir32}/libffi.la
%{_pkgconfigdir32}/libffi.pc
%endif

%files -n libffi-static
%defattr(644,root,root,755)
%{_libdir}/libffi.a

%if %{with multilib}
%files -n libffi-multilib-static
%defattr(644,root,root,755)
%{_libdir32}/libffi.a
%endif
%endif

%if %{with objc}
%files objc
%defattr(644,root,root,755)
%doc gcc/objc/README.libobjc
%attr(755,root,root) %{gcclibdir}/cc1obj
%attr(755,root,root) %{_libdir}/libobjc.so
%{_libdir}/libobjc.la
%{gcclibdir}/include/objc

%if %{with objcxx}
%files objc++
%defattr(644,root,root,755)
%doc gcc/objcp/ChangeLog
%attr(755,root,root) %{gcclibdir}/cc1objplus
%endif

%if %{with multilib}
%files objc-multilib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir32}/libobjc.so
%{_libdir32}/libobjc.la
%endif

%files -n libobjc
%defattr(644,root,root,755)
%doc libobjc/{ChangeLog,README*}
%attr(755,root,root) %{_libdir}/libobjc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libobjc.so.4

%if %{with multilib}
%files -n libobjc-multilib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir32}/libobjc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir32}/libobjc.so.4
%endif

%files -n libobjc-static
%defattr(644,root,root,755)
%{_libdir}/libobjc.a

%if %{with multilib}
%files -n libobjc-multilib-static
%defattr(644,root,root,755)
%{_libdir32}/libobjc.a
%endif
%endif

%if %{with go}
%files go
%defattr(644,root,root,755)
%doc gcc/go/gofrontend/{LICENSE,PATENTS,README}
%attr(755,root,root) %{_bindir}/gccgo
%attr(755,root,root) %{gcclibdir}/go1
%dir %{_libdir}/go
%{_libdir}/go/%{version}
%{_mandir}/man1/gccgo.1*
%{_infodir}/gccgo.info*

%if %{with multilib}
%files go-multilib
%defattr(644,root,root,755)
%dir %{_libdir32}/go
%{_libdir32}/go/%{version}
%endif

%files -n libgo
%defattr(644,root,root,755)
%doc libgo/{LICENSE,PATENTS,README}
%attr(755,root,root) %{_libdir}/libgo.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libgo.so.5

%if %{with multilib}
%files -n libgo-multilib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir32}/libgo.so.*.*.*
%attr(755,root,root) %ghost %{_libdir32}/libgo.so.5
%endif

%files -n libgo-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgo.so
%{_libdir}/libgo.la
%{_libdir}/libgobegin.a

%if %{with multilib}
%files -n libgo-multilib-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir32}/libgo.so
%{_libdir32}/libgo.la
%{_libdir32}/libgobegin.a
%endif

%files -n libgo-static
%defattr(644,root,root,755)
%{_libdir}/libgo.a

%if %{with multilib}
%files -n libgo-multilib-static
%defattr(644,root,root,755)
%{_libdir32}/libgo.a
%endif
%endif

%if %{with asan}
%files -n libasan
%defattr(644,root,root,755)
%doc libsanitizer/ChangeLog* libsanitizer/LICENSE.TXT
%attr(755,root,root) %{_libdir}/libasan.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libasan.so.1

%if %{with multilib}
%files -n libasan-multilib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir32}/libasan.so.*.*.*
%attr(755,root,root) %ghost %{_libdir32}/libasan.so.1
%endif

%files -n libasan-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libasan.so
%{_libdir}/libasan_preinit.o
%{_libdir}/libasan.la
%{gcclibdir}/include/sanitizer/asan_interface.h

%if %{with multilib}
%files -n libasan-multilib-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir32}/libasan.so
%{_libdir32}/libasan_preinit.o
%{_libdir32}/libasan.la
%endif

%files -n libasan-static
%defattr(644,root,root,755)
%{_libdir}/libasan.a

%if %{with multilib}
%files -n libasan-multilib-static
%defattr(644,root,root,755)
%{_libdir32}/libasan.a
%endif
%endif

%files -n liblsan
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblsan.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/liblsan.so.0

%files -n liblsan-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/liblsan.so
%{_libdir}/liblsan.la
%{gcclibdir}/include/sanitizer/lsan_interface.h

%files -n liblsan-static
%defattr(644,root,root,755)
%{_libdir}/liblsan.a

%if %{with tsan}
%files -n libtsan
%defattr(644,root,root,755)
%doc libsanitizer/ChangeLog* libsanitizer/LICENSE.TXT
%attr(755,root,root) %{_libdir}/libtsan.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libtsan.so.0

%files -n libtsan-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libtsan.so
%{_libdir}/libtsan.la

%files -n libtsan-static
%defattr(644,root,root,755)
%{_libdir}/libtsan.a
%endif

%files -n libubsan
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libubsan.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libubsan.so.0

%if %{with multilib}
%files -n libubsan-multilib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir32}/libubsan.so.*.*.*
%attr(755,root,root) %ghost %{_libdir32}/libubsan.so.0
%endif

%files -n libubsan-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libubsan.so
%{_libdir}/libubsan.la

%if %{with multilib}
%files -n libubsan-multilib-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir32}/libubsan.so
%{_libdir32}/libubsan.la
%endif

%files -n libubsan-static
%defattr(644,root,root,755)
%{_libdir}/libubsan.a

%if %{with multilib}
%files -n libubsan-multilib-static
%defattr(644,root,root,755)
%{_libdir32}/libubsan.a
%endif

%if %{with atomic}
%files -n libatomic
%defattr(644,root,root,755)
%doc libatomic/ChangeLog*
%attr(755,root,root) %{_libdir}/libatomic.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libatomic.so.1

%if %{with multilib}
%files -n libatomic-multilib
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir32}/libatomic.so.*.*.*
%attr(755,root,root) %ghost %{_libdir32}/libatomic.so.1
%endif

%files -n libatomic-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libatomic.so
%{_libdir}/libatomic.la

%if %{with multilib}
%files -n libatomic-multilib-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir32}/libatomic.so
%{_libdir32}/libatomic.la
%endif

%files -n libatomic-static
%defattr(644,root,root,755)
%{_libdir}/libatomic.a

%if %{with multilib}
%files -n libatomic-multilib-static
%defattr(644,root,root,755)
%{_libdir32}/libatomic.a
%endif
%endif
