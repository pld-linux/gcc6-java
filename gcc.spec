#
# Conditional build:
%bcond_without	ada		# build without ADA support
%bcond_without	java		# build without Java support
%bcond_without	objc		# build without objc support
%bcond_with	bootstrap	# don't BR gcc(ada) (temporary for Ac upgrade bootstrap)
#
%define		DASHED_SNAP	%{nil}
%define		SNAP		%(echo %{DASHED_SNAP} | sed -e "s#-##g")
%define		GCC_VERSION	3.3.5
%define		KSI_VERSION	1.1.0.1567

Summary:	GNU Compiler Collection: the C compiler and shared files
Summary(es):	Colecci�n de compiladores GNU: el compilador C y ficheros compartidos
Summary(pl):	Kolekcja kompilator�w GNU: kompilator C i pliki wsp�dzielone
Summary(pt_BR):	Cole��o dos compiladores GNU: o compilador C e arquivos compartilhados
Name:		gcc
Version:	%{GCC_VERSION}
Release:	1
Epoch:		5
License:	GPL
Group:		Development/Languages
Source0:	ftp://gcc.gnu.org/pub/gcc/releases/gcc-%{GCC_VERSION}/%{name}-%{GCC_VERSION}.tar.bz2
# Source0-md5:	70ee088b498741bb08c779f9617df3a5
# Source0-size:	23833856
Source1:	ftp://ftp.pld-linux.org/people/malekith/ksi/ksi-%{KSI_VERSION}.tar.gz
# Source1-md5:	66f07491b44f06928fd95b0e65bb8cd3
Source2:	http://ep09.pld-linux.org/~djrzulf/gcc33/%{name}-non-english-man-pages.tar.bz2
# Source2-md5:	4736f3422ddfb808423b745629acc321
Patch0:		%{name}-info.patch
Patch1:		%{name}-paths.patch
Patch2:		%{name}-nolocalefiles.patch
Patch3:		%{name}-ada-link-new-libgnat.patch
Patch4:		%{name}-nodebug.patch
Patch5:		%{name}-cse-find_best_addr.patch
Patch6:		%{name}-amd64-thunk.patch
# -- stolen patches from RH --
Patch10:	gcc32-ada-link.patch
Patch11:	gcc32-boehm-gc-libs.patch
Patch12:	gcc32-bogus-inline.patch
Patch13:	gcc32-c++-nrv-test.patch
Patch14:	gcc32-c++-tsubst-asm.patch
Patch15:	gcc32-debug-pr7241.patch
Patch16:	gcc32-duplicate-decl.patch
Patch17:	gcc32-dwarf2-pr6381.patch
Patch18:	gcc32-dwarf2-pr6436-test.patch
Patch19:	gcc32-fde-merge-compat.patch
Patch20:	gcc32-i386-memtest-test.patch
Patch21:	gcc32-inline-label.patch
Patch22:	gcc32-java-no-rpath.patch
Patch23:	gcc32-test-rh65771.patch
Patch24:	gcc32-test-rotate.patch
Patch25:	gcc-cmpi.patch
Patch26:	gcc-ffi64.patch
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	binutils >= 2:2.15.90.0.3
BuildRequires:	bison
BuildRequires:	fileutils >= 4.0.41
%{?with_ada:%{!?with_bootstrap:BuildRequires:	gcc(ada)}}
%{?with_ada:BuildRequires: gcc-ada}
BuildRequires:	gettext-devel
BuildRequires:	glibc-devel >= 2.2.5-20
BuildRequires:	perl-devel
BuildRequires:	texinfo >= 4.1
BuildRequires:	zlib-devel
Requires:	binutils >= 2:2.15.90.0.3
Requires:	cpp = %{epoch}:%{GCC_VERSION}-%{release}
Requires:	gcc-dirs
Requires:	libgcc = %{epoch}:%{GCC_VERSION}-%{release}
%{?with_ada:Provides: gcc(ada)}
Conflicts:	glibc-devel < 2.2.5-20
URL:		http://gcc.gnu.org/
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_slibdir	/%{_lib}
%ifarch sparc64
%define		_slibdir64	/lib64
%define		_libdir		/usr/lib
%define		rpmcflags	-O2 -mtune=ultrasparc
%endif

%description
A compiler aimed at integrating all the optimizations and features
necessary for a high-performance and stable development environment.

This package contains the C compiler and some files shared by various
parts of the GNU Compiler Collection. In order to use another GCC
compiler you will need to install the appropriate subpackage.

%description -l es
Un compilador destinado a la integraci�n de todas las optimalizaciones
y caracter�sticas necesarias para un entorno de desarrollo eficaz y
estable.

Este paquete contiene el compilador de C y unos ficheros compartidos
por varias parted de la colecci�n de compiladores GNU (GCC). Para usar
otro compilador de GCC ser� necesario que instale el subpaquete
adecuado.

%description -l pl
Kompilator, posiadaj�cy du�e mo�liwo�ci optymalizacyjne niezb�dne do
wyprodukowania szybkiego i stabilnego kodu wynikowego.

Ten pakiet zawiera kompilator C i pliki wsp�dzielone przez r�ne
cz�ci kolekcji kompilator�w GNU (GCC). �eby u�ywa� innego kompilatora
z GCC, trzeba zainstalowa� odpowiedni podpakiet.

%description -l pt_BR
Este pacote adiciona infraestrutura b�sica e suporte a linguagem C ao
GNU Compiler Collection.

%package -n libgcc
Summary:	Shared gcc library
Summary(es):	Biblioteca compartida de gcc
Summary(pl):	Biblioteka gcc
Summary(pt_BR):	Biblioteca runtime para o GCC
Group:		Libraries
Version:	%{GCC_VERSION}
Obsoletes:	libgcc1

%description -n libgcc
Shared gcc library.

%description -n libgcc -l es
Biblioteca compartida de gcc.

%description -n libgcc -l pl
Biblioteka dynamiczna gcc.

%description -n libgcc -l pt_BR
Biblioteca runtime para o GCC.

%package c++
Summary:	C++ support for gcc
Summary(es):	Soporte de C++ para gcc
Summary(pl):	Obs�uga C++ dla gcc
Summary(pt_BR):	Suporte C++ para o gcc
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{GCC_VERSION}-%{release}
Obsoletes:	egcc-c++
Obsoletes:	egcs-c++

%description c++
This package adds C++ support to the GNU Compiler Collection. It
includes support for most of the current C++ specification, including
templates and exception handling. It does not include a standard C++
library, which is available separately.

%description c++ -l de
Dieses Paket enth�lt die C++-Unterst�tzung f�r den
GNU-Compiler-Collection. Es unterst�tzt die aktuelle
C++-Spezifikation, inkl. Templates und Ausnahmeverarbeitung. Eine
C++-Standard-Library ist nicht enthalten - sie ist getrennt
erh�ltlich.

%description c++ -l es
Este paquete a�ade soporte de C++ al GCC (colecci�n de compiladores
GNU). Ello incluye el soporte para la mayor�a de la especificaci�n
actual de C++, incluyendo plantillas y manejo de excepciones. No
incluye la biblioteca est�ndar de C++, la que es disponible separada.

%description c++ -l fr
Ce package ajoute un support C++ a la collection de compilateurs GNU.
Il comprend un support pour la plupart des sp�cifications actuelles de
C++, dont les mod�les et la gestion des exceptions. Il ne comprend pas
une biblioth�que C++ standard, qui est disponible s�par�ment.

%description c++ -l pl
Ten pakiet dodaje obs�ug� C++ do kompilatora gcc. Ma wsparcie dla
du�ej ilo�ci obecnych specyfikacji C++, nie zawiera natomiast
standardowych bibliotek C++, kt�re s� w oddzielnym pakiecie.

%description c++ -l pt_BR
Este pacote adiciona suporte C++ para o gcc.

%description c++ -l tr
Bu paket, GNU C derleyicisine C++ deste�i ekler. 'Template'ler ve
ayk�r� durum i�leme gibi �o�u g�ncel C++ tan�mlar�na uyar. Standart
C++ kitapl��� bu pakette yer almaz.

%package objc
Summary:	Objective C support for gcc
Summary(de):	Objektive C-Unterst�tzung f�r gcc
Summary(es):	Soporte de Objective C para gcc
Summary(fr):	Gestion d'Objective C pour gcc
Summary(pl):	Obs�uga obiektowego C dla kompilatora gcc
Summary(tr):	gcc i�in Objective C deste�i
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{GCC_VERSION}-%{release}
Requires:	libobjc = %{epoch}:%{GCC_VERSION}-%{release}
Obsoletes:	egcc-objc
Obsoletes:	egcs-objc

%description objc
This package adds Objective C support to the GNU Compiler Collection.
Objective C is a object oriented derivative of the C language, mainly
used on systems running NeXTSTEP. This package does not include the
standard objective C object library.

%description objc -l de
Dieses Paket erg�nzt den GNU-Compiler-Collection durch
Objective-C-Support. Objective C ist ein objektorientiertes Derivat
von C, das zur Hauptsache auf Systemen mit NeXTSTEP zum Einsatz kommt.
Die Standard-Objective-C-Objekt-Library ist nicht Teil des Pakets.

%description objc -l es
Este paquete a�ade soporte de Objective C al GCC (colecci�n de
compiladores GNU). Objective C es un lenguaje orientado a objetos
derivado de C, principalmente usado en sistemas que funcionan bajo
NeXTSTEP. El paquete no incluye la biblioteca de objetos est�ndar de
Objective C.

%description objc -l fr
Ce package ajoute un support Objective C a la collection de
compilateurs GNU. L'Objective C est un langage orient� objetd�riv� du
langage C, principalement utilis� sur les syst�mes NeXTSTEP. Ce
package n'inclue pas la biblioth�que Objective C standard.

%description objc -l pl
Ten pakiet dodaje obs�ug� obiektowego C do kompilatora gcc. Obiektowe
C (objc) jest zorientowan� obiektowo pochodn� j�zyka C, u�ywan�
g��wnie w systemach u�ywaj�cych NeXTSTEP. W pakiecie nie ma
standardowej biblioteki objc (kt�ra znajduje si� w osobnym pakiecie).

%description objc -l tr
Bu paket, GNU C derleyicisine Objective C deste�i ekler. Objective C,
C dilinin nesne y�nelik bir t�revidir ve NeXTSTEP alt�nda �al��an
sistemlerde yayg�n olarak kullan�l�r. Standart Objective C nesne
kitapl��� bu pakette yer almaz.

%package -n libobjc
Summary:	Objective C Libraries
Summary(es):	Bibliotecas de Objective C
Summary(pl):	Biblioteki Obiektowego C
Group:		Libraries
Version:	%{GCC_VERSION}
Obsoletes:	libobjc1

%description -n libobjc
Objective C Libraries.

%description -n libobjc -l es
Bibliotecas de Objective C.

%description -n libobjc -l pl
Biblioteki Obiektowego C.

%package -n libobjc-static
Summary:	Static Objective C Libraries
Summary(es):	Bibliotecas est�ticas de Objective C
Summary(pl):	Statyczne Biblioteki Obiektowego C
Group:		Development/Libraries
Version:	%{GCC_VERSION}
Requires:	libobjc = %{epoch}:%{GCC_VERSION}-%{release}

%description -n libobjc-static
Static Objective C Libraries.

%description -n libobjc-static -l es
Bibliotecas est�ticas de Objective C.

%description -n libobjc-static -l pl
Statyczne biblioteki Obiektowego C.

%package g77
Summary:	Fortran 77 support for gcc
Summary(es):	Soporte de Fortran 77 para gcc
Summary(pl):	Obs�uga Fortranu 77 dla gcc
Summary(pt_BR):	Suporte Fortran 77 para o GCC
Group:		Development/Languages/Fortran
Version:	%{GCC_VERSION}
Requires:	%{name} = %{epoch}:%{GCC_VERSION}-%{release}
Requires:	libg2c = %{epoch}:%{GCC_VERSION}-%{release}
Obsoletes:	egcs-g77

%description g77
This package adds support for compiling Fortran 77 programs with the
GNU compiler.

%description g77 -l es
Este paquete a�ade soporte para compilar programas escritos en Fortran
77 con el compilador GNU.

%description g77 -l pl
Ten pakiet dodaje obs�ug� Fortranu 77 do kompilatora gcc. Jest
potrzebny do kompilowania program�w pisanych w j�zyku Fortran 77.

%description g77 -l pt_BR
Suporte Fortran 77 para o GCC.

%package -n libg2c
Summary:	Fortran 77 Libraries
Summary(es):	Bibliotecas de Fortran 77
Summary(pl):	Biblioteki Fortranu 77
Group:		Libraries
Version:	%{GCC_VERSION}

%description -n libg2c
Fortran 77 Libraries.

%description -n libg2c -l es
Bibliotecas de Fortran 77.

%description -n libg2c -l pl
Biblioteki Fortranu 77.

%package -n libg2c-static
Summary:	Static Fortran 77 Libraries
Summary(es):	Bibliotecas est�ticas de Fortran 77
Summary(pl):	Statyczne Biblioteki Fortranu 77
Group:		Development/Libraries
Version:	%{GCC_VERSION}
Requires:	libg2c = %{epoch}:%{GCC_VERSION}-%{release}

%description -n libg2c-static
Static Fortran 77 Libraries.

%description -n libg2c -l es
Bibliotecas est�ticas de Fortran 77.

%description -n libg2c-static -l pl
Statyczne biblioteki Fortranu 77.

%package java
Summary:	Java support for gcc
Summary(es):	Soporte de Java para gcc
Summary(pl):	Obs�uga Javy dla gcc
Group:		Development/Languages/Java
Version:	%{GCC_VERSION}
Requires:	%{name} = %{epoch}:%{GCC_VERSION}-%{release}
Requires:	libgcj-devel = %{epoch}:%{GCC_VERSION}-%{release}
Requires:	java-shared
Provides:	gcj = %{epoch}:%{GCC_VERSION}-%{release}

%description java
This package adds experimental support for compiling Java(tm) programs
and bytecode into native code. To use this you will also need the
libgcj package.

%description java -l es
Este paquete a�ade soporte experimental para compilar programas
Java(tm) y su bytecode en c�digo nativo. Para usarlo tambi�n va a
necesitar el paquete libgcj.

%description java -l pl
Wsparcie dla kompilowania program�w Java(tm) zar�wno do bajt-kodu jak i
do natywnego kodu. Dodatkowo wymagany jest pakiet libgcj, aby mo�na
by�o przeprowadzi� kompilacj�.

%package java-tools
Summary:	Shared java tools
Summary(es):	Herramientas compartidas de Java
Summary(pl):	Wsp�dzielone narz�dzia javy
Group:		Development/Languages/Java
Version:	%{GCC_VERSION}
Provides:	jar = %{epoch}:%{GCC_VERSION}-%{release}
Provides:	java-shared
Obsoletes:	fastjar
Obsoletes:	jar
Obsoletes:	java-shared

%description java-tools
This package contains tools that are common for every Java(tm)
implementation, such as rmic or jar.

%description java-tools -l es
Este paquete contiene herramientas que son comunes para cada
implementaci�n de Java(tm), como rmic o jar.

%description java-tools -l pl
Pakiet ten zawiera narz�dzia wsp�lne dla ka�dej implementacji
Javy(tm), takie jak rmic czy jar.

%package -n libgcj
Summary:	Java Class Libraries
Summary(es):	Bibliotecas de clases de Java
Summary(pl):	Biblioteki Klas Javy
Group:		Libraries
Version:	%{GCC_VERSION}
Requires:	zlib
Obsoletes:	libgcj3

%description -n libgcj
Java Class Libraries.

%description -n libgcj -l es
Bibliotecas de clases de Java.

%description -n libgcj -l pl
Biblioteki Klas Javy.

%package -n libgcj-devel
Summary:	Development files for Java Class Libraries
Summary(es):	Ficheros de desarrollo para las bibliotecas de clases de Java
Summary(pl):	Pliki nag��wkowe dla Bibliotek Klas Javy
Group:		Development/Libraries
Version:	%{GCC_VERSION}
Requires:	%{name}-java = %{epoch}:%{GCC_VERSION}-%{release}
Requires:	libgcj = %{epoch}:%{GCC_VERSION}-%{release}
Obsoletes:	libgcj3-devel

%description -n libgcj-devel
Development files for Java Class Libraries.

%description -n libgcj-devel -l es
Ficheros de desarrollo para las bibliotecas de clases de Java.

%description -n libgcj-devel -l pl
Pliki nag��wkowe dla Bibliotek Klas Javy.

%package -n libgcj-static
Summary:	Static Java Class Libraries
Summary(es):	Bibliotecas est�ticas de clases de Java
Summary(pl):	Statyczne Biblioteki Klas Javy
Group:		Development/Libraries
Version:	%{GCC_VERSION}
Requires:	libgcj-devel = %{epoch}:%{GCC_VERSION}-%{release}
Requires:	libstdc++-devel = %{epoch}:%{GCC_VERSION}-%{release}

%description -n libgcj-static
Static Java Class Libraries.

%description -n libgcj-static -l es
Bibliotecas est�ticas de clases de Java.

%description -n libgcj-static -l pl
Statyczne Biblioteki Klas Javy.

%package -n libstdc++
Summary:	GNU c++ library
Summary(es):	Biblioteca C++ de GNU
Summary(pl):	Biblioteki GNU C++
Summary(pt_BR):	Biblioteca C++ GNU
Group:		Libraries
Version:	%{GCC_VERSION}
Obsoletes:	libg++
Obsoletes:	libstdc++3

%description -n libstdc++
This is the GNU implementation of the standard C++ libraries, along
with additional GNU tools. This package includes the shared libraries
necessary to run C++ applications.

%description -n libstdc++ -l de
Dies ist die GNU-Implementierung der Standard-C++-Libraries mit
weiteren GNU-Tools. Dieses Paket enth�lt die zum Ausf�hren von
C++-Anwendungen erforderlichen gemeinsam genutzten Libraries.

%description -n libstdc++ -l es
Este es el soporte de las bibliotecas padr�n del C++, junto con
herramientas GNU adicionales. El paquete incluye las bibliotecas
compartidas necesarias para ejecutar aplicaciones C++.

%description -n libstdc++ -l fr
Ceci est l'impl�mentation GNU des librairies C++ standard, ainsi que
des outils GNU suppl�mentaires. Ce package comprend les librairies
partag�es n�cessaires � l'ex�cution d'application C++.

%description -n libstdc++ -l pl
Pakiet ten zawiera biblioteki b�d�ce implementacj� standardowych
bibliotek C++. Znajduj� si� w nim biblioteki dynamiczne niezb�dne do
uruchomienia aplikacji napisanych w C++.

%description -n libstdc++ -l pt_BR
Este pacote � uma implementa��o da biblioteca padr�o C++ v3, um
subconjunto do padr�o ISO 14882.

%description -n libstdc++ -l tr
Bu paket, standart C++ kitapl�klar�n�n GNU ger�eklemesidir ve C++
uygulamalar�n�n ko�turulmas� i�in gerekli kitapl�klar� i�erir.

%package -n libstdc++-devel
Summary:	Header files and documentation for C++ development
Summary(de):	Header-Dateien zur Entwicklung mit C++
Summary(es):	Ficheros de cabecera y documentaci�n para desarrollo C++
Summary(fr):	Fichiers d'en-t�te et biblitoth�ques pour d�velopper en C++
Summary(pl):	Pliki nag��wkowe i dokumentacja do biblioteki standardowej C++
Summary(pt_BR):	Arquivos de inclus�o e bibliotecas para o desenvolvimento em C++
Summary(tr):	C++ ile program geli�tirmek i�in gerekli dosyalar
Group:		Development/Libraries
Version:	%{GCC_VERSION}
Requires:	%{name}-c++ = %{epoch}:%{GCC_VERSION}-%{release}
Requires:	libstdc++ = %{epoch}:%{GCC_VERSION}-%{release}
Obsoletes:	libg++-devel
Obsoletes:	libstdc++3-devel

%description -n libstdc++-devel
This is the GNU implementation of the standard C++ libraries. This
package includes the header files needed for C++ development and
library documentation.

%description -n libstdc++-devel -l es
Este es el soporte de las bibliotecas padr�n del lenguaje C++. Este
paquete incluye los archivos de inclusi�n y bibliotecas necesarios
para desarrollo de programas en lenguaje C++.

%description -n libstdc++-devel -l pl
Pakiet ten zawiera biblioteki b�d�ce implementacj� standardowych
bibliotek C++. Znajduj� si� w nim pliki nag��wkowe wykorzystywane przy
programowaniu w j�zyku C++ oraz dokumentacja biblioteki standardowej.

%description -n libstdc++-devel -l pt_BR
Este pacote inclui os arquivos de inclus�o e bibliotecas necess�rias
para desenvolvimento de programas C++.

%package -n libstdc++-static
Summary:	Static C++ standard library
Summary(es):	Biblioteca est�ndar est�tica de C++
Summary(pl):	Statyczna biblioteka standardowa C++
Group:		Development/Libraries
Version:	%{GCC_VERSION}
Requires:	libstdc++-devel = %{epoch}:%{GCC_VERSION}-%{release}

%description -n libstdc++-static
Static C++ standard library.

%description -n libstdc++-static -l es
Biblioteca est�ndar est�tica de C++.

%description -n libstdc++-static -l pl
Statyczna biblioteka standardowa C++.

%package -n libffi
Summary:	Foreign Function Interface library
Summary(es):	Biblioteca de interfaz de funciones ajenas
Summary(pl):	Biblioteka zewn�trznych wywo�a� funkcji
Group:		Libraries
Version:	%{GCC_VERSION}

%description -n libffi
The libffi library provides a portable, high level programming
interface to various calling conventions. This allows a programmer to
call any function specified by a call interface description at run
time.

%description -n libffi -l es
La biblioteca libffi provee una interfaz portable de programaci�n de
alto nivel para varias convenciones de llamada. Ello permite que un
programador llame una funci�n cualquiera especificada por una
descripci�n de interfaz de llamada en el tiempo de ejecuci�n.

%description -n libffi -l pl
Biblioteka libffi dostarcza przeno�nego, wysokopoziomowego
mi�dzymordzia do r�nych konwencji wywo�a� funkcji. Pozwala to
programi�cie wywo�ywa� dowolne funkcje podaj�c konwencj� wywo�ania w
czasie wykonania.

%package -n libffi-devel
Summary:	Development files for Foreign Function Interface library
Summary(es):	Ficheros de desarrollo para libffi
Summary(pl):	Pliki nag��wkowe dla libffi
Group:		Development/Libraries
Version:	%{GCC_VERSION}
Requires:	libffi = %{epoch}:%{GCC_VERSION}-%{release}

%description -n libffi-devel
Development files for Foreign Function Interface library.

%description -n libffi-devel -l es
Ficheros de desarrollo para libffi.

%description -n libffi-devel -l pl
Pliki nag��wkowe dla libffi.

%package -n libffi-static
Summary:	Static Foreign Function Interface library
Summary(es):	Biblioteca libffi est�tica
Summary(pl):	Statyczna biblioteka libffi
Group:		Development/Libraries
Version:	%{GCC_VERSION}
Requires:	libffi-devel = %{epoch}:%{GCC_VERSION}-%{release}

%description -n libffi-static
Static Foreign Function Interface library.

%description -n libffi-static -l es
Biblioteca libffi est�tica.

%description -n libffi-static -l pl
Statyczna biblioteka libffi.

%package ada
Summary:	Ada support for gcc
Summary(es):	Soporte de Ada para gcc
Summary(pl):	Obs�uga Ady do gcc
Group:		Development/Languages
Version:	%{GCC_VERSION}
Requires:	%{name} = %{epoch}:%{GCC_VERSION}-%{release}
Requires:	libgnat = %{epoch}:%{GCC_VERSION}-%{release}
Obsoletes:	gcc-gnat
Obsoletes:	gnat-devel

%description ada
This package adds experimental support for compiling Ada programs.

%description ada -l es
Este paquete a�ade soporte experimental para compilar programas en
Ada.

%description ada -l pl
Ten pakiet dodaje eksperymentalne wsparcie dla kompilacji program�w w
Adzie.

%package -n libgnat
Summary:	Ada standard libraries
Summary(es):	Bibliotecas est�ndares de Ada
Summary(pl):	Biblioteki standardowe dla Ady
Group:		Libraries
Version:	%{GCC_VERSION}
Obsoletes:	gnat
Obsoletes:	libgnat1

%description -n libgnat
This package contains shared libraries needed to run programs written
in Ada.

%description -n libgnat -l es
Este paquete contiene las bibliotecas compartidas necesarias para
ejecutar programas escritos en Ada.

%description -n libgnat -l pl
Ten pakiet zawiera biblioteki potrzebne do uruchamiania program�w
napisanych w Adzie.

%package -n libgnat-static
Summary:	Static Ada standard libraries
Summary(pl):	Statyczne biblioteki standardowe dla Ady
Group:		Libraries
Version:	%{GCC_VERSION}
Obsoletes:	gnat-static

%description -n libgnat-static
This package contains static libraries for programs written in Ada.

%description -n libgnat-static -l pl
Ten pakiet zawiera biblioteki statyczne dla program�w napisanych w
Adzie.

%package ksi
Summary:	Ksi support for gcc
Summary(es):	Soporte de Ksi para gcc
Summary(pl):	Obs�uga Ksi dla gcc
Version:	%{GCC_VERSION}.%{KSI_VERSION}
Group:		Development/Languages
Requires:	%{name} = %{epoch}:%{GCC_VERSION}-%{release}

%description ksi
This package adds experimental support for compiling Ksi programs into
native code. You proabably don't need it, unless your are going to
develop a compiler using Ksi as intermediate representation or you are
using such compiler (like Gont).

%description ksi -l es
Este paquete a�ade soporte experimental para compilar programas de Ksi
en c�digo nativo. Probablemento no lo necesitar�, a menos que vaya a
desarrollar un compilador que use Ksi como representaci�n intermedia o
use tal compilador (como Gont).

%description ksi -l pl
Ten pakiet dodaje eksperymentalne wsparcie dla kompilacji program�w w
Ksi do kodu maszynowego. Prawdopodobnie nie potrzebujesz go, chyba �e
zamierzasz pisa� kompilator u�ywaj�cy Ksi jako reprezentacji
po�rednicz�cej, lub u�ywasz takiego kompilatora (jak Gont).

%package -n cpp
Summary:	The C Pre Processor
Summary(es):	El preprocesador de C
Summary(pl):	Preprocesor C
Summary(pt_BR):	Preprocessador para a linguagem C
Group:		Development/Languages
Version:	%{GCC_VERSION}
Obsoletes:	egcs-cpp
Obsoletes:	gcc-cpp

%description -n cpp
The C preprocessor is a "macro processor" that is used automatically
by the C compiler to transform your program before actual compilation.
It is called a macro processor because it allows you to define
"macros", which are brief abbreviations for longer constructs.

The C preprocessor provides four separate facilities that you can use
as you see fit:

- Inclusion of header files. These are files of declarations that can
  be substituted into your program.
- Macro expansion. You can define "macros", which are abbreviations
  for arbitrary fragments of C code, and then the C preprocessor will
  replace the macros with their definitions throughout the program.
- Conditional compilation. Using special preprocessing directives, you
  can include or exclude parts of the program according to various
  conditions.
- Line control. If you use a program to combine or rearrange source
  files into an intermediate file which is then compiled, you can use
  line control to inform the compiler of where each source line
  originally came from.

%description -n cpp -l es
El preprocesador de C es un "procesador de macros" que es usado
autom�ticamente por el compilador C para transformar su programa antes
de que �ste se actualmente compile. Se llama procesador de macros
porque permite definir "macros", los que son abreviaciones concisas
para construcciones m�s largas.

El preprocesador C provee cuatro cualidadedes distintas que puede usar
como le convenga:

- Inclusi�n de ficheros de cabecera. �stos son ficheros de
  declaraciones que pueden incorporarse a su programa.
- Expansi�n de macros. Puede definir "macros", los que son
  abreviaciones para fragmentos arbitrarios de c�digo C, y a lo largo
  del programa el preprocesador sustituir� los macros con sus
  definiciones.
- Compilaci�n condicional. Usando especiales directivas del preproceso
  puede incluir o excluir partes del programa seg�n varias condiciones.
- Control de l�neas. Si usa un programa para combinar o reorganizar el
  c�digo fuente en un fichero intermedio que luego es compilado, puede
  usar control de l�neas para informar el compilador de d�nde origina
  cada l�nea.

%description -n cpp -l pl
Preprocesor C jest "makro procesorem" kt�ry jest automatycznie
u�ywany przez kompilator C do obr�bki kompilowanego programu przed
w�a�ciw� kompilacj�. Jest on nazywany makroprocesorem, poniewa�
umo�liwia definiowanie i rozwijanie makr umo�liwiaj�cych skracanie
d�ugich konstrukcji w j�zyku C.

Preprocesor C umo�liwia wykonywanie czterech r�nych typ�w operacji:

- Do��czanie plik�w (np. nag��wkowych). Wstawia pliki w miejscu
  deklaracji polecenia do��czenia innego pliku.
- Rozwijanie makr. Mo�na definiowa� "makra" nadaj�c im identyfikatory,
  kt�rych p�niejsze u�ycie powoduje podczas rozwijania podmienienie
  indentyfikatora deklarowan� wcze�niej warto�ci�.
- Kompilacja warunkowa. W zale�no�ci od obecno�ci symboli i dyrektyw w
  �rodowisku preprocesora s� w��czane warunkowo, b�d� nie, pewne
  fragmenty obrabianego strumienia tekst�w.
- Kontrola linii �r�d�a. Niezale�nie od tego jakim przeobra�eniom
  podlega wynikowy strumie� danych w wyniku rozwijania makr i do��czania
  s� zapami�tywane informacje o tym, kt�rej linii pliku �r�d�owego
  odpowiada fragment pliku wynikowego.

%description -n cpp -l pt_BR
O preprocessador C � um "processador de macros", que � utilizado pelo
compilador C para fazer algumas modifica��es no seu programa, antes da
compila��o em si. Ele � chamado de "processador de macros" porque
permite a voc� definir "macros", que s�o abrevia��es para constru��es
mais complicadas.

O preprocessador C fornece quatro funcionalidades b�sicas: inclus�o de
arquivos de cabe�alho; expans�o de macros; compila��o condicional; e
controle da numera��o das linhas do programa.

%prep
%setup -q -a1 -n %{name}-%{GCC_VERSION}
mv ksi-%{KSI_VERSION} gcc/ksi

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%{!?debug:%patch4 -p1}
%patch5 -p1
%ifarch amd64
# not sure if it wouldn't break x86 (it shouldn't, but better safe than sorry)
%patch6 -p1
%endif

%patch10 -p1
%patch11
%patch12
%patch13
%patch14
%patch15

%patch16
%patch17
%patch18
%patch19
%patch20
%patch21
%patch22
%patch23
%patch24
%patch25 -p1
%patch26 -p2

# because we distribute modified version of gcc...
perl -pi -e 's/(version.*)";/$1 (PLD Linux)";/' gcc/version.c
perl -pi -e 's@(bug_report_url.*<URL:).*";@$1http://bugs.pld-linux.org/>";@' gcc/version.c

%build
# cd gcc && autoconf; cd ..
# autoconf is not needed!
cp /usr/share/automake/config.sub .

rm -rf obj-%{_target_platform} && install -d obj-%{_target_platform} && cd obj-%{_target_platform}

CFLAGS="%{rpmcflags}" \
CXXFLAGS="%{rpmcflags}" \
TEXCONFIG=false ../configure \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--infodir=%{_infodir} \
	--mandir=%{_mandir} \
	--enable-shared \
	--enable-threads=posix \
	--enable-__cxa_atexit \
	--enable-languages="c,c++,f77%{?with_objc:,objc}%{?with_ada:,ada}%{?with_java:,java},ksi" \
	--enable-c99 \
	--enable-long-long \
%ifarch amd64
	--disable-multilib \
%else
	--enable-multilib \
%endif
	--enable-nls \
	--with-gnu-as \
	--with-gnu-ld \
	--with-system-zlib \
	--with-slibdir=%{_slibdir} \
	--without-x \
	%{_target_platform}

PATH=$PATH:/sbin:%{_sbindir}

cd ..
%{__make} -C obj-%{_target_platform} bootstrap-lean \
	GCJFLAGS="%{rpmcflags}" \
	LDFLAGS_FOR_TARGET="%{rpmldflags}" \
	mandir=%{_mandir} \
	infodir=%{_infodir}

%if %{with ada}
for tgt in gnatlib gnattools gnatlib-shared; do
%{__make} -C obj-%{_target_platform}/gcc $tgt \
	LDFLAGS_FOR_TARGET="%{rpmldflags}" \
	mandir=%{_mandir} \
	infodir=%{_infodir}
done
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/lib,%{_datadir},%{_infodir}}

cd obj-%{_target_platform}
PATH=$PATH:/sbin:%{_sbindir}

%{__make} install \
	mandir=%{_mandir} \
	infodir=%{_infodir} \
	DESTDIR=$RPM_BUILD_ROOT

%ifarch sparc64
ln -f $RPM_BUILD_ROOT%{_bindir}/sparc64-pld-linux-gcc \
	$RPM_BUILD_ROOT%{_bindir}/sparc-pld-linux-gcc
%endif

ln -sf gcc $RPM_BUILD_ROOT%{_bindir}/cc
echo ".so gcc.1" > $RPM_BUILD_ROOT%{_mandir}/man1/cc.1

ln -sf g77 $RPM_BUILD_ROOT%{_bindir}/f77
echo ".so g77.1" > $RPM_BUILD_ROOT%{_mandir}/man1/f77.1

%if %{with ada}
# move ada shared libraries to proper place...
mv $RPM_BUILD_ROOT%{_libdir}/gcc-lib/*/*/adalib/*.so.1 \
	$RPM_BUILD_ROOT%{_libdir}
# check if symlink to be made is valid
test -f $RPM_BUILD_ROOT%{_libdir}/libgnat-3.15.so.1
ln -sf libgnat-3.15.so.1 $RPM_BUILD_ROOT%{_libdir}/libgnat-3.15.so
ln -sf libgnarl-3.15.so.1 $RPM_BUILD_ROOT%{_libdir}/libgnarl-3.15.so
ln -sf libgnat-3.15.so $RPM_BUILD_ROOT%{_libdir}/libgnat.so
ln -sf libgnarl-3.15.so $RPM_BUILD_ROOT%{_libdir}/libgnarl.so
%endif

ln -sf %{_bindir}/cpp $RPM_BUILD_ROOT/lib/cpp

cd ..

%if %{with java}
install -d java-doc
cp -f libjava/doc/cni.sgml libjava/READ* java-doc
cp -f fastjar/README java-doc/README.fastjar
cp -f libffi/README java-doc/README.libffi
cp -f libffi/LICENSE java-doc/LICENSE.libffi
%endif

%if %{with objc}
cp -f libobjc/README gcc/objc/README.libobjc
%endif

# avoid -L poisoning in *.la - there should be only -L%{_libdir}/gcc-lib/*/%{version}
for f in libstdc++.la libsupc++.la %{?with_java:libgcj.la} ; do
	perl -pi -e 's@-L[^ ]*[acs.] @@g' $RPM_BUILD_ROOT%{_libdir}/$f
done
# normalize libdir, to avoid propagation of unnecessary RPATHs by libtool
for f in libstdc++.la libsupc++.la libg2c.la \
	%{?with_java:libgcj.la lib-org-w3c-dom.la lib-org-xml-sax.la libffi.la} \
	%{?with_objc:libobjc.la}; do
	perl -pi -e "s@^libdir='.*@libdir='/usr/%{_lib}'@" $RPM_BUILD_ROOT%{_libdir}/$f
done

bzip2 -dc %{SOURCE2} | tar xf - -C $RPM_BUILD_ROOT%{_mandir}
mv -f $RPM_BUILD_ROOT%{_mandir}/ja/man1/{cccp,cpp}.1

# include/ contains install-tools/include/* and headers that were fixed up
# by fixincludes, we don't want former
gccdir=$(echo $RPM_BUILD_ROOT%{_libdir}/gcc-lib/*/*/)
mkdir $gccdir/tmp
# we have to save these however
mv -f $gccdir/include/{%{?with_objc:objc,}g2c.h,syslimits.h%{?with_java:,gcj}} $gccdir/tmp
rm -rf $gccdir/include
mv -f $gccdir/tmp $gccdir/include
cp $gccdir/install-tools/include/*.h $gccdir/include
# but we don't want anything more from install-tools
rm -rf $gccdir/install-tools

%find_lang %{name}
%find_lang libstdc\+\+

%clean
rm -rf $RPM_BUILD_ROOT

%post
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%post g77
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun g77
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%post java
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun java
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%post ksi
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun ksi
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%post -n cpp
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%postun -n cpp
[ ! -x /usr/sbin/fix-info-dir ] || /usr/sbin/fix-info-dir -c %{_infodir} >/dev/null 2>&1

%post   -p /sbin/ldconfig -n libgcc
%postun -p /sbin/ldconfig -n libgcc
%post   -p /sbin/ldconfig -n libstdc++
%postun -p /sbin/ldconfig -n libstdc++
%post   -p /sbin/ldconfig -n libobjc
%postun -p /sbin/ldconfig -n libobjc
%post   -p /sbin/ldconfig -n libg2c
%postun -p /sbin/ldconfig -n libg2c
%post   -p /sbin/ldconfig -n libgcj
%postun -p /sbin/ldconfig -n libgcj
%post   -p /sbin/ldconfig -n libgnat
%postun -p /sbin/ldconfig -n libgnat
%post   -p /sbin/ldconfig -n libffi
%postun -p /sbin/ldconfig -n libffi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc READ* ChangeLog
%dir %{_libdir}/gcc-lib/*/*
%dir %{_libdir}/gcc-lib/*/*/include
%attr(755,root,root) %{_bindir}/*-gcc*
%attr(755,root,root) %{_bindir}/gcc
%attr(755,root,root) %{_bindir}/gccbug
%attr(755,root,root) %{_bindir}/gcov
%attr(755,root,root) %{_bindir}/cc

%{_mandir}/man1/gcc.1*
%{_mandir}/man1/cc.1*
%{_mandir}/man1/gcov.1*
%lang(fr) %{_mandir}/fr/man1/gcc.1*
%lang(ja) %{_mandir}/ja/man1/gcc.1*
%{_infodir}/gcc*

%attr(755,root,root) %{_slibdir}*/lib*.so
%{_libdir}/gcc-lib/*/*/libgcc.a
%{_libdir}/gcc-lib/*/*/libgcc_eh.a
%{_libdir}/gcc-lib/*/*/specs
%{_libdir}*/gcc-lib/*/*/crt*.o
%ifarch sparc64
%{_libdir}/gcc-lib/*/*/*/libgcc.a
%{_libdir}/gcc-lib/*/*/*/libgcc_eh.a
%{_libdir}*/gcc-lib/*/*/*/crt*.o
%endif
%ifarch ppc
%{_libdir}/gcc-lib/*/*/ecrt*.o
%{_libdir}/gcc-lib/*/*/ncrt*.o
%{_libdir}/gcc-lib/*/*/nof
%dir %{_libdir}/nof
%endif
%attr(755,root,root) %{_libdir}/gcc-lib/*/*/cc1
%attr(755,root,root) %{_libdir}/gcc-lib/*/*/collect2

%{_libdir}/gcc-lib/*/*/include/*.h
%exclude %{_libdir}/gcc-lib/*/*/include/g2c.h

%files -n libgcc
%defattr(644,root,root,755)
%attr(755,root,root) %{_slibdir}*/lib*.so.*

%files c++
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/g++
%attr(755,root,root) %{_bindir}/*-g++
%attr(755,root,root) %{_bindir}/c++
%attr(755,root,root) %{_bindir}/*-c++
%attr(755,root,root) %{_libdir}/gcc-lib/*/*/cc1plus
%{_libdir}*/libsupc++.la
%ifarch ppc
%{_libdir}/nof/libsupc++.la
%{_libdir}/nof/libsupc++.a
%endif
%{_libdir}*/libsupc++.a
%{_mandir}/man1/g++.1*
%lang(ja) %{_mandir}/ja/man1/g++.1*

%files -n libstdc++ -f libstdc++.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}*/libstdc++.so.*.*.*
%ifarch ppc
%attr(755,root,root) %{_libdir}/nof/libstdc++.so.*.*.*
%endif

%files -n libstdc++-devel
%defattr(644,root,root,755)
%doc libstdc++-v3/docs/html
%dir %{_includedir}/c++
%{_includedir}/c++/%{GCC_VERSION}
%attr(755,root,root) %{_libdir}*/libstdc++.so
%{_libdir}*/libstdc++.la
%ifarch ppc
%attr(755,root,root) %{_libdir}/nof/libstdc++.so
%{_libdir}/nof/libstdc++.la
%endif

%files -n libstdc++-static
%defattr(644,root,root,755)
%{_libdir}*/libstdc++.a
%ifarch ppc
%{_libdir}/nof/libstdc++.a
%endif

%if %{with objc}
%files objc
%defattr(644,root,root,755)
%doc gcc/objc/READ*
%attr(755,root,root) %{_libdir}/gcc-lib/*/*/cc1obj
%attr(755,root,root) %{_libdir}*/libobjc.so
%{_libdir}*/libobjc.la
%ifarch ppc
%attr(755,root,root) %{_libdir}/nof/libobjc.so
%{_libdir}/nof/libobjc.la
%endif
%{_libdir}/gcc-lib/*/*/include/objc

%files -n libobjc
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}*/libobjc.so.*.*.*
%ifarch ppc
%attr(755,root,root) %{_libdir}/nof/libobjc.so.*.*.*
%endif

%files -n libobjc-static
%defattr(644,root,root,755)
%{_libdir}*/libobjc.a
%ifarch ppc
%{_libdir}/nof/libobjc.a
%endif
%endif

%files g77
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/g77
%attr(755,root,root) %{_bindir}/f77
%{_infodir}/g77*
%attr(755,root,root) %{_libdir}/gcc-lib/*/*/f771
%{_libdir}*/libfrtbegin.a
%{_libdir}*/libg2c.la
%attr(755,root,root) %{_libdir}*/libg2c.so
%ifarch ppc
%{_libdir}/nof/libfrtbegin.a
%{_libdir}/nof/libg2c.la
%attr(755,root,root) %{_libdir}/nof/libg2c.so
%endif
%{_libdir}/gcc-lib/*/*/include/g2c.h
%{_mandir}/man1/g77.1*
%{_mandir}/man1/f77.1*
%lang(ja) %{_mandir}/ja/man1/g77.1*
%lang(ja) %{_mandir}/ja/man1/f77.1*

%files -n libg2c
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}*/libg2c.so.*.*.*
%ifarch ppc
%attr(755,root,root) %{_libdir}/nof/libg2c.so.*.*.*
%endif

%files -n libg2c-static
%defattr(644,root,root,755)
%{_libdir}*/libg2c.a
%ifarch ppc
%{_libdir}/nof/libg2c.a
%endif

%if %{with java}
%files java
%defattr(644,root,root,755)
%doc java-doc/*
%attr(755,root,root) %{_bindir}/gcj*
%attr(755,root,root) %{_bindir}/gij
%attr(755,root,root) %{_bindir}/jcf-dump
%attr(755,root,root) %{_bindir}/jv-*
%attr(755,root,root) %{_bindir}/*-gcj
%attr(755,root,root) %{_libdir}/gcc-lib/*/*/jc1
%attr(755,root,root) %{_libdir}/gcc-lib/*/*/jvgenmain
%{_infodir}/gcj*
%{_mandir}/man1/jcf-*
%{_mandir}/man1/jv-*
%{_mandir}/man1/gij*
%{_mandir}/man1/gcj*

%files java-tools
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/rmi*
%attr(755,root,root) %{_bindir}/jar
%attr(755,root,root) %{_bindir}/grepjar
%{_mandir}/man1/rmi*
%{_mandir}/man1/jar*
%{_mandir}/man1/grepjar*
%{_infodir}/fastjar*

%files -n libgcj
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/addr2name.awk
%attr(755,root,root) %{_libdir}/lib*cj*.so.*.*.*
%attr(755,root,root) %{_libdir}/lib-org*.so.*.*.*
%ifarch ppc
%attr(755,root,root) %{_libdir}/nof/lib*cj*.so.*
%attr(755,root,root) %{_libdir}/nof/lib-org*.so.*
%endif

%files -n libgcj-devel
%defattr(644,root,root,755)
%{_includedir}/java
%{_includedir}/javax
#%%{_includedir}/org
%{_includedir}/gcj
%{_includedir}/j*.h
%{_includedir}/gnu/*
%{_libdir}/gcc-lib/*/*/include/gcj
%dir %{_libdir}/security
%{_libdir}/security/*
%dir %{_datadir}/java
%{_datadir}/java/libgcj*.jar
%{_libdir}/lib*cj.spec
%attr(755,root,root) %{_libdir}/lib*cj*.so
%attr(755,root,root) %{_libdir}/lib-org-*.so
%{_libdir}/lib*cj*.la
%{_libdir}/lib-org-*.la
%ifarch ppc
%attr(755,root,root) %{_libdir}/nof/lib*cj*.so
%attr(755,root,root) %{_libdir}/nof/lib-org-*.so
%{_libdir}/nof/lib*cj*.la
%{_libdir}/nof/lib-org-*.la
%endif

%files -n libgcj-static
%defattr(644,root,root,755)
%{_libdir}/lib*cj*.a
%{_libdir}/lib-org-*.a
%ifarch ppc
%{_libdir}/nof/lib*cj*.a
%{_libdir}/nof/lib-org-*.a
%endif

%files -n libffi
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libffi-*.so
%ifarch ppc
%attr(755,root,root) %{_libdir}/nof/libffi-*.so
%endif

%files -n libffi-devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libffi.so
%{_libdir}/libffi.la
%ifarch ppc
%attr(755,root,root) %{_libdir}/nof/libffi.so
%{_libdir}/nof/libffi.la
%endif
%{_includedir}/ffi*

%files -n libffi-static
%defattr(644,root,root,755)
%{_libdir}/libffi.a
%ifarch ppc
%{_libdir}/nof/libffi.a
%endif
%endif

%if %{with ada}
%files ada
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/gcc-lib/*/*/gnat1
%{_libdir}/gcc-lib/*/*/adainclude
%dir %{_libdir}/gcc-lib/*/*/adalib
%{_libdir}/gcc-lib/*/*/adalib/*.ali
%ifnarch ppc
%{_libdir}/gcc-lib/*/*/adalib/libgmem.a
%endif
%{_libdir}/gcc-lib/*/*/adalib/Makefile.adalib
%attr(755,root,root) %{_bindir}/gnat*
%{_infodir}/gnat*
%attr(755,root,root) %{_libdir}/libgnat*.so
%attr(755,root,root) %{_libdir}/libgnarl*.so

%files -n libgnat
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libgna*.so.1

%files -n libgnat-static
%defattr(644,root,root,755)
%{_libdir}/gcc-lib/*/*/adalib/libgna*.a
%endif

%files ksi
%defattr(644,root,root,755)
%doc gcc/ksi/README gcc/ksi/NEWS gcc/ksi/t/*.{ksi,c,foo}
%{_infodir}/ksi*
%attr(755,root,root) %{_libdir}/gcc-lib/*/*/ksi1

%files -n cpp
%defattr(644,root,root,755)
%attr(755,root,root) /lib/cpp
%attr(755,root,root) %{_bindir}/cpp
%{_mandir}/man1/cpp.1*
%lang(ja) %{_mandir}/ja/man1/cpp.1*
%{_infodir}/cpp*
