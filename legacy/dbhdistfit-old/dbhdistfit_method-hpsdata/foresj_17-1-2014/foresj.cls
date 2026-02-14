\newcommand\classname{Foresj}
\newcommand\lastmodifieddate{2004/07/05}
\newcommand\versionnumber{0.1}

% Are we printing crop marks?%%
\newif\if@cropmarkson \@cropmarksontrue

\NeedsTeXFormat{LaTeX2e}[2012/06/15]
\ProvidesClass{\classname}[\lastmodifieddate\space G-Series,
                           Version \versionnumber^^J%
                           (C) 2004 Techset Composition Pvt. Ltd.^^J^^J]

\special{papersize=216mm,279mm}
\setlength{\paperheight}{279truemm}
\setlength{\paperwidth}{216truemm}

\newif\if@numberedref \@numberedreftrue
\newif\if@endproofbox \@endproofboxtrue
\newif\ifcopyedit
\newif\ifbreaklink
\newif\ifunarticle
\newif\ifnoquery
\newif\ifnocolfig
\newif\iflink
\newif\ifpap
\newif\iftrack
\newif\ifrevises
\newif\ifdiscussion
\newif\ifbkreview
\newif\ifcolorfigs
\newif\ifgcopyright
\newif\iffproof\fprooffalse %to make surname in magenta color
\newif\iffinal

\DeclareOption{final}{\finaltrue}
\DeclareOption{track}{\tracktrue}
\DeclareOption{copyedit}{\copyedittrue}
\DeclareOption{link}{\linktrue}
\DeclareOption{pap}{\paptrue}
\DeclareOption{revises}{\revisestrue}
\DeclareOption{fproof}{\fprooftrue}
\DeclareOption{noquery}{\noquerytrue}
\DeclareOption{nocolfig}{\nocolfigtrue}
\DeclareOption{breaklink}{\breaklinktrue}
\DeclareOption{draft}{\PassOptionsToPackage{draft}{graphicx}}
\DeclareOption{a3paper}{\PassOptionsToPackage{a3}{crop}}
\DeclareOption{centre}{\PassOptionsToPackage{center}{crop}}
\DeclareOption{crop}{\PassOptionsToPackage{cam}{crop}\global\@cropmarksontrue}
\DeclareOption{nocrop}{\PassOptionsToPackage{off}{crop}\global\@cropmarksonfalse}
\DeclareOption{info}{\PassOptionsToPackage{info}{crop}}
\DeclareOption{noinfo}{\PassOptionsToPackage{noinfo}{crop}}
\DeclareOption{numbered}{\global\@numberedreftrue}
\DeclareOption{named}{\global\@numberedreffalse}
\DeclareOption{noproofbox}{\global\@endproofboxfalse}
\DeclareOption{proofbox}{\global\@endproofboxtrue}
\DeclareOption{courier}{\def\verbatim@font{\normalfont\ttfamily}}
\DeclareOption{times}{\def\verbatim@font{\normalfont\rmfamily}}
\DeclareOption{bookreview}{\global\unarticletrue}
\DeclareOption{discussion}{\global\discussiontrue}
\DeclareOption{colorfigs}{\colorfigstrue}
\DeclareOption{bkreview}{\global\bkreviewtrue}
\DeclareOption{gcopyright}{\global\gcopyrighttrue}

\ProcessOptions

% Load all necessary packages
\RequirePackage{crop,graphicx,array,amsthm,amsmath,amssymb,amsfonts,upref,endnotes,rotating,upgreek}
\RequirePackage{boxedminipage}
\RequirePackage{stfloats}
\usepackage{setspace}

\usepackage{multicol}

\usepackage{dcolumn}
\newcolumntype{d}[1]{D{.}{.}{#1}}

% Not sure if needed.
\newcommand\@ptsize{0}

% Set twoside printing
\@twosidetrue

% Marginal notes are on the outside edge
\@mparswitchtrue

% Default font sizes
\renewcommand\normalsize{%
  \@setfontsize\normalsize{9\p@}{11\p@}%
  \abovedisplayskip 13\p@ \@plus 3\p@ \@minus2\p@
  \abovedisplayshortskip 9\p@ \@plus 2\p@ \@minus1\p@
  \belowdisplayshortskip 8\p@ \@plus 2\p@ \@minus2\p@
  \belowdisplayskip \abovedisplayskip
  \let\@listi\@listI}
\normalsize
\let\@bls\baselineskip

\newcommand\small{%
  \@setfontsize\small{8\p@}{10\p@}%
  \abovedisplayskip 6\p@ \@plus1\p@ \@minus1\p@
  \abovedisplayshortskip 3\p@ \@plus 2\p@ \@minus1\p@
  \belowdisplayshortskip 2\p@ \@plus 1\p@ \@minus1\p@
  \def\@listi{\leftmargin\leftmargini
              \listparindent \parindent
              \topsep 6\p@ \@plus2\p@ \@minus1\p@
              \parsep \z@ \itemsep \z@}%
  \belowdisplayskip \abovedisplayskip}

\newcommand\footnotesize{%
 \@setfontsize\footnotesize{9\p@}{10\p@}%
  \abovedisplayskip 6\p@ \@plus2\p@ \@minus4\p@
  \abovedisplayshortskip \z@ \@plus \p@
  \belowdisplayshortskip 1\p@ \@plus2\p@ \@minus2\p@
  \def\@listi{\leftmargin\leftmargini
              \listparindent 1em
              \topsep 5\p@ \@plus 2\p@ \@minus 1\p@
              \parsep \z@ \itemsep \z@}%
  \belowdisplayskip \abovedisplayskip}

\def\scriptsize{\@setfontsize\scriptsize{7\p@}{9\p@}}
\def\tiny{\@setfontsize\tiny{6\p@}{7\p@}}
\def\little{\@setfontsize\little{5\p@}{6\p@}}
\def\large{\@setfontsize\large{12\p@}{14\p@}}
\def\Large{\@setfontsize\Large{14\p@}{16\p@}}
\def\LARGE{\@setfontsize\LARGE{16\p@}{18\p@}}
\def\huge{\@setfontsize\huge{24\p@}{26\p@}}
\def\Huge{\@setfontsize\Huge{25\p@}{27\p@}}
\gdef\rec#1{\gdef\@rec{#1}}\rec{}
\gdef\rev#1{\gdef\@rev{#1}}\rev{}
\gdef\acc#1{\gdef\@acc{#1}}\acc{}
\gdef\pub#1{\gdef\@pub{#1}}\pub{}


\DeclareOldFontCommand{\rm}{\normalfont\rmfamily}{\mathrm}
\DeclareOldFontCommand{\sf}{\normalfont\sffamily}{\mathsf}
\DeclareOldFontCommand{\tt}{\normalfont\ttfamily}{\mathtt}
\DeclareOldFontCommand{\bf}{\normalfont\bfseries}{\mathbf}
\DeclareOldFontCommand{\it}{\normalfont\itshape}{\mathit}
\DeclareOldFontCommand{\sl}{\normalfont\slshape}{\@nomath\sl}
\DeclareOldFontCommand{\sc}{\normalfont\scshape}{\@nomath\sc}

% Line spacing
\setlength\lineskip{1\p@}
\setlength\normallineskip{1\p@}
\renewcommand\baselinestretch{}

% Paragraph dimensions and inter-para spacing
\setlength\parskip{0\p@}
\setlength\parindent{12pt}

% Set inter-para skips
\setlength\smallskipamount{3\p@ \@plus 1\p@ \@minus 1\p@}
\setlength\medskipamount{6\p@ \@plus 2\p@ \@minus 2\p@}
\setlength\bigskipamount{12\p@ \@plus 4\p@ \@minus 4\p@}

% Page break penalties
\@lowpenalty   51
\@medpenalty  151
\@highpenalty 301

% Disallow widows and orphans
\clubpenalty 10000
\widowpenalty 10000

% Disable page breaks before equations, allow pagebreaks after
% equations and discourage widow lines before equations.
\displaywidowpenalty 100
\predisplaypenalty   10000
\postdisplaypenalty  2500

% Allow breaking the page in the middle of a paragraph
\interlinepenalty 0

% Disallow breaking the page after a hyphenated line
\brokenpenalty 10000

% Hyphenation; don't split words into less than three characters
\lefthyphenmin=3
\righthyphenmin=3

%
% Set page layout dimensions
%
\setlength\headheight{7\p@}          % height of running head
\setlength\topmargin{48.5pt}            % top margin 3pc, 9pt
\addtolength\topmargin{0\p@}         %
\addtolength\topmargin{-1in}         % subtract out the 1 inch driver margin

\setlength\topskip{8\p@}            % height of first line of text%% {10\p@}
\setlength\headsep{42\p@}          % space below running head --
\addtolength\headsep{-\topskip}      %   base to base with first line of text

%%%%%%%%%update%%%%%%%%%
\setlength\footskip{34\p@}           % space above footer line
\setlength\maxdepth{.5\topskip}      % pages can be short or deep by half a line?

\setlength\textwidth{186mm}           % text measure excluding margins
%\addtolength\textwidth{9.89\p@}      % -> textwidth of 30pc, 9.89pt!

\setlength\textheight{58\@bls}       % text height of 50pc,
\addtolength\textheight{\topskip}    %  - including first line of text

% Set the margins
\setlength\marginparsep{6\p@} \setlength\marginparpush{18\p@}
\setlength\marginparwidth{14pt}

\setlength\oddsidemargin{15mm}
\addtolength\oddsidemargin{-1in}    % subtract out the 1 inch driver margin
\setlength\@tempdima{\paperwidth}
\addtolength\@tempdima{-\textwidth}
\addtolength\@tempdima{-15mm}
\setlength\evensidemargin{\@tempdima}
\addtolength\evensidemargin{-1in}

\setlength\columnsep{12\p@}          % space between columns for double-column text
\setlength\columnseprule{0\p@}      % width of rule between two columns

% Footnotes
\setlength\footnotesep{0\p@}     % space between footnotes
% space between text and footnote
\setlength{\skip\footins}{22\p@ \@plus 0\p@ \@minus 0\p@}

% Float placement parameters

% The total number of floats that can be allowed on a page.
\setcounter{totalnumber}{10}
% The maximum number of floats at the top and bottom of a page.
\setcounter{topnumber}{5}
\setcounter{bottomnumber}{5}
% The maximum part of the top or bottom of a text page that can be
% occupied by floats. This is set so that at least four lines of text
% fit on the page.
\renewcommand\topfraction{.921}
\renewcommand\bottomfraction{.921}
% The minimum amount of a text page that must be occupied by text.
% This should accomodate four lines of text.
\renewcommand\textfraction{.079}
% The minimum amount of a float page that must be occupied by floats.
\renewcommand\floatpagefraction{.887}

% The same parameters repeated for double column output
\renewcommand\dbltopfraction{.88}
\renewcommand\dblfloatpagefraction{.88}

% Space between floats
\setlength\floatsep    {20\p@ \@plus 2\p@ \@minus 2\p@}
% Space between floats and text
\setlength\textfloatsep{20\p@ \@plus 2\p@ \@minus 4\p@}
% Space above and below an inline figure
\setlength\intextsep   {20\p@ \@plus 2\p@ \@minus 2\p@}

% For double column floats
\setlength\dblfloatsep    {20\p@ \@plus 2\p@ \@minus 2\p@}
\setlength\dbltextfloatsep{20\p@ \@plus 2\p@ \@minus 4\p@}

% Space left at top, bottom and inbetween floats on a float page.
\setlength\@fptop{0\p@}         % no space above float page figures
\setlength\@fpsep{12\p@ \@plus 2fil}
\setlength\@fpbot{0\p@ \@plus 1fil}

% The same for double column
\setlength\@dblfptop{0\p@}
\setlength\@dblfpsep{12\p@ \@plus 1fil}
\setlength\@dblfpbot{0\p@ \@plus 2fil}

%%%%%%%%%%%%%%%%%%%%%%%%%%%% Article Identification %%%%%%%%%%%%%%%%%%%%%%%%%%%%
\def\@default@journal@title{Journal Title}
\let\@journal@title\@default@journal@title
\def\month@info{Month~}
\def\year@info{\the\year}
\def\vol@info{00}
\def\issue@info{00}
\def\@print@issn{0000-0000}
\def\@online@issn{0000-0000}
\def\ceby@info{}
\def\qaby@info{}
\def\mcby@info{}
\newcommand{\page@extent@info}{%
  \thepage--\pageref{LastPage}}

\newcommand{\totalpage}{%
  \pageref{LastPage}}

\newcommand{\issn@line}{ISSN \@print@issn\ print$/$ISSN \@online@issn\ online}
\newcommand{\copyright@line}{\textcopyright\ \year@info\ International Association for Hydro-Environment Engineering and Research}
\gdef\doi@string{0000000000}

\gdef\backack#1{\gdef\@backack{#1}}\backack{}

\newcommand{\journal}[1]{%
  \makeatletter
  \InputIfFileExists{#1.cfg}{%
    \message{Journal identification loaded from #1.cfg}}%
  {\message{No configuration file for #1}}%
  \makeatother}

% Article information user commands
\def\Year#1{\gdef\year@info{#1}}
\def\Vol#1{\gdef\vol@info{#1}}
\def\Issue#1{\gdef\issue@info{#1}}
\def\Month#1{\gdef\month@info{#1}}
\def\ceby#1{\gdef\ceby@info{#1}}
\def\qaby#1{\gdef\qaby@info{#1}}
\def\mcby#1{\gdef\mcby@info{#1}}
\newcommand\DOI[2][\@doi@fixed@field]{%
  \gdef\@doi@variable@field{#1}%
  \setDOI{#1}{#2}}
\newcommand{\setDOI}[2]{%
  \gdef\doi@string{#1#2}}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Firstpage %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcommand{\firstpage}[1]{%
  \setcounter{page}{#1}}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%% Page Styles %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\def\slinf{\raise 0pc\hbox to 40pc{\artname \hfill Page\#:\quad \totalpage\hfill  Printed:\ \today}}

\def\ps@titlepage{%
  \def\@evenfoot{\titlepagefootline}%\slinf}%
 \def\@evenhead{\fontsize{10}{12}\selectfont \titlepageheadline}
 \def\@oddhead{\fontsize{10}{12}\selectfont \titlepageheadline}%
  \def\@oddfoot{\titlepagefootline}%
  \def\authormark##1{\def\leftmark{##1}}%
  \def\titlemark##1{\markboth{##1}{##1}}}

\def\ps@headings{%
  \def\@oddfoot{\vbox{\rule{\textwidth}{.5pt}\vskip21pt}
  \vbox{\hspace*{\fill}\thepage}}%
  \def\@evenfoot{\vbox{\rule{\textwidth}{.5pt}\vskip21pt}\vbox{\hspace*{-260pt}\thepage}}%
  \def\@evenhead{\vbox{\let\etal=\etal\fontsize{9}{11}\selectfont{{\itshape\rightmark}}\hfill\\[2.85\p@]
  \rule{\textwidth}{0.5\p@}}}%
  \def\@oddhead{\vbox{\hsize\textwidth\let\etal=\etal\fontsize{9}{11}\selectfont{\hspace*{\fill}{\leftmark}}\\[2.85\p@]
\rule{\textwidth}{0.5\p@}}}%
  \def\authormark##1{\def\leftmark{##1}}%
  \def\titlemark##1{\markboth{##1}{##1}}}

\def\ps@myheadings{%
  \let\@oddfoot\@empty%
  \let\@evenfoot\@empty%
  \def\@evenhead{\hfil}%
  \def\@oddhead{\hfil}%
  \def\authormark##1{\def\leftmark{##1}}%
  \def\titlemark##1{\markboth{##1}{##1}}}

\newcommand{\titlepageheadline}{\vbox to 81pt{\vspace*{-31.4pt}\fontsize{10}{12}\selectfont
\vbox{\hbox to \textwidth{{\fontsize{35}{38}\selectfont\sf Forestry} {\itshape An International Journal of Forest Research\hspace*{\fill}}}}
\vspace*{19.2pt}
\vbox{\hbox to \textwidth{{\itshape\@journal@title}\ \jourinf\ doi:\doi@string\hfill}}
\vspace*{-5.5pt}
\vbox{\noindent\rule{\textwidth}{.5pt}}
}}

\def\today{\number\day/\ifcase\month\or
 1\or 2\or 3\or 4\or 5\or 6\or 7\or 8\or 9\or 10\or 11\or 12\fi/\number\year}

\newcommand{\titlepagefootline}{%
  \fontsize{8.5}{11}\itshape\selectfont
  \vbox{\vskip 12\p@ \@plus 3\p@%
\hbox to \textwidth{\noindent\rule{\textwidth}{.5pt}\hfill}\vskip3pt
\hbox to \textwidth{Institute of Chartered Foresters, 2012. All rights reserved. For Permissions, please e-mail: journals.permissions@oup.com\hfill}
\vspace*{2pt}
\hbox to \textwidth{{\hfill\rm\thepage}}
}}


\setcounter{footnote}{1}
\renewcommand\thefootnote{\@fnsymbol\c@footnote}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newcounter{part}
\newcounter{section}
\newcounter{rsection}
\newcounter{subsection}[section]
\newcounter{rsubsection}[section]
\newcounter{subsubsection}[subsection]
\newcounter{paragraph}[subsubsection]
\newcounter{subparagraph}[paragraph]
\newcounter{refsection}[section]
\newcounter{acksection}[section]
\newcounter{figure}
\newcounter{scheme}
\newcounter{table}

% Form of the numbers
\newcommand\thepage{\arabic{page}}
\renewcommand\thesection{\arabic{section}}
\renewcommand\thersection{\arabic{section}}
\renewcommand\thesubsection{{\thesection.\arabic{subsection}}}
\renewcommand\thersubsection{{\thersection.\arabic{subsection}}}
\renewcommand\thersubsection{{\thersection.\arabic{subsection}}}
\renewcommand\thesubsubsection{{\thesubsection.\arabic{subsubsection}}}
\renewcommand\theparagraph{\thesubsubsection.\arabic{paragraph}}
\renewcommand\thesubparagraph{\theparagraph.\arabic{subparagraph}}
\renewcommand\theequation{\arabic{equation}}

% Form of the words
\newcommand\contentsname{Contents}
\newcommand\guestname{GUEST EDITORS}
\newcommand\listfigurename{List of Figures}
\newcommand\listtablename{List of Tables}
\newcommand\partname{Part}
\newcommand\appendixname{Appendix}
\newcommand\abstractname{\MakeUppercase{\bf Abstract}}
\newcommand\refname{References}
\newcommand\bibname{{{\bf References}\vskip4pt}}%{{\bf References}\vskip4pt}
\newcommand\normsname{Norms}
\newcommand\indexname{Index}
\newcommand\figurename{Figure}
\newcommand\schemename{Scheme}
\newcommand\tablename{Table}

% Clearemptydoublepage should really clear the running heads too
\newcommand{\clearemptydoublepage}{\newpage{\pagestyle{empty}\cleardoublepage}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Titling Macros %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Reset default command signatures

\def\title{\@ifnextchar[{\@title@wst@}{\@title@nst@}}
\def\@title@wst@[#1]{\titlemark{#1}\@title@assign@}
\def\@title@nst@#1{\titlemark{\@journal@title}\@title@assign@{#1}}
\def\@title@assign@#1{\def\@title{#1}}

\def\author{\@ifnextchar[{\@author@wst@}{\@author@nst@}}
\def\@author@wst@[#1]{\authormark{#1}\@author@assign@}
\def\@author@nst@#1{\authormark{#1}\@author@assign@{#1}}
\def\@author@assign@#1{\gdef\@author{#1}\global\@author@providedtrue}


\def\and{\MakeLowercase{and}\space\ignorespaces}

\newif\if@supertitle@provided \@supertitle@providedfalse
\newif\if@specialissue@provided \@specialissue@providedfalse
\newif\if@guesteditor@provided \@guesteditor@providedfalse
\newif\if@subtitle@provided \@subtitle@providedfalse
\newif\if@author@provided \@author@providedfalse
\newif\if@date@provided \@date@providedfalse
\newif\if@corres@provided \@corres@providedfalse
\newif\if@classification@provided \@classification@providedfalse
\newif\if@abstract@provided \@abstract@providedfalse %%5/7/2004
\newif\if@keywords@provided \@keywords@providedfalse
\newif\if@discussion@provided \@discussion@providedfalse
\newif\if@bkreview@provided \@bkreview@providedfalse

\def\keywordsname{Keywords}

\def\address#1{\gdef\@address{#1}}\address{}
\def\date#1{\gdef\@date{#1}\global\@date@providedtrue}
\def\corres#1{\def\@corres{#1}\global\@corres@providedtrue}
\def\keywords#1{\gdef\@keywords{#1}\global\@keywords@providedtrue}
\def\discussion#1{\gdef\@discussion{#1}\global\@discussion@providedtrue}
\def\bkreview#1{\gdef\@bkreview{#1}\global\@bkreview@providedtrue}
\def\subtitle#1{\def\@subtitle{{#1}}\global\@subtitle@providedtrue}
\def\supertitle#1{\def\@supertitle{{\noindent #1}}\global\@supertitle@providedtrue}
\def\specialissue#1{\def\@specialissue{{\noindent SPECIAL ISSUE:~#1}}\global\@specialissue@providedtrue}
\def\guesteditor#1{\def\@guesteditor{{\noindent \guestname:~#1}}\global\@guesteditor@providedtrue}
\def\@abbreviations{}
\def\@classification{}
\newcommand\classification[2][Jel Classification]{%
     \global\@classification@providedtrue
     \gdef\@classification{{\leftskip=2pc\rightskip=2pc \noindent\textit{#1}:\enskip #2\par}}}

\newbox\@abstractbox
\newenvironment{abstract}{\global\@abstract@providedtrue%%% 5/7/2004
  \global\setbox\@abstractbox\vbox\bgroup\fontsize{9}{11}\selectfont\leftskip46\p@\rightskip46\p@%
  \@afterindentfalse\@afterheading}{\par\egroup}%

\def\@fnsymbol#1{\ifcase#1\or *\or \dagger\or \ddagger\or
    \S\or \P\or \|\or **\or \dagger\dagger
    \or \ddagger\ddagger \else\@ctrerr\fi}


\mathchardef\Register="20AE%
\mathchardef\ter="099%
\def\titdagger{\hbox{$\dagger$}}
\def\titddagger{\hbox{$\ddagger$}}
\def\titS{\hbox{$\S$}}
\def\titP{\hbox{$\P$}}

\def\affpunct{,}

%% Reimplement Titling Layout
\newcommand\maketitle{\par
   \begingroup
\renewcommand{\@fnsymbol}[1]{\ifcase##1\or \hbox{*}\or \titdagger\or \titddagger\or
    \titS\or \titP\or \|\or \hbox{**}\or \titdagger\titdagger
    \or \titddagger\titddagger \else\@ctrerr\fi}
    \thispagestyle{titlepage}%
    \setcounter{footnote}{0}
    \renewcommand\thefootnote{\@fnsymbol\c@footnote}%
    \def\@makefnmark{\hbox{\rm\@thefnmark}}%
    \long\def\@makefntext##1{%\noindent
      {${\@thefnmark}$}{##1}}%
    \global\@topnum\z@   % Prevents figures from going at top of page.
\iffinal
\twocolumn[\@maketitle]
\else
    \@maketitle
\fi
  \endgroup
  \enlargethispage{-6pt}
  \@afterindentfalse
  \@afterheading
  \setcounter{footnote}{1}%
  \global\let\maketitle\relax
  \global\let\@maketitle\relax}
%%%
\def\@maketitle{%
\vspace*{24pt}
     \if@supertitle@provided%
       {\fontsize{10}{12}\selectfont\@supertitle\par}
    \else
       \vskip1pt%
     \fi
  \begingroup
        {\fontsize{16}{19}\selectfont\bfseries
      \mathversion{bold}%
      \begin{center}{\@title}\end{center}%
      \par}%
     \if@subtitle@provided%
       \vspace{12.5\p@}%
       {\fontsize{12}{14}\fontseries{b}\selectfont\@subtitle\par
        %\vspace{1.5\p@}%
        }%
     \else
       \vspace{0\p@}%
     \fi
    \vspace{2.5pt}%
    {\normalsize\raggedright\centering
     \begingroup
     \if@author@provided%
      {\fontsize{10}{12}\bfseries\selectfont\mathversion{bold}\@author}\par
      \vskip13.25pt
      {\fontseries{m}\fontshape{it}\fontsize{9}{11}\selectfont\@address}%
    \vspace{10\p@}%
     \else
    \vspace{0\p@}%
      \fi
      \endgroup
      \par}%
     \if@corres@provided%
       {\fontsize{8}{10}\fontseries{m}\selectfont\centering \@corres\par
        \vspace{13.25\p@}}%
     \else
       \vspace{0\p@}%
     \fi
     \if@date@provided%
    {\fontsize{8}{10}\fontshape{it}\selectfont\centering\@date\ifx\@rec\empty\else Received \@rec\fi \ifx\@pub\empty\else , Advance Access publication \@pub\fi\par}%
\vspace{1.5\p@}%%        \vspace{9.25\p@}%
     \else
    \vspace{0\p@}%
     \fi
\endgroup
\if@abstract@provided%
    \vskip12pt%
    {\fontsize{9}{10}\selectfont\noindent%
    \unvbox\@abstractbox\par}%
    \vspace{1.5\p@}%
    \else
       \vspace{0\p@}%
     \fi
    \if@classification@provided
      {\leftskip\z@\parfillskip=\z@ plus1fill%
        \fontsize{8}{9}\selectfont\@classification\par}%
    \fi
  \par
  \ifunarticle%
  \vspace{-.8pc plus 6\p@}%
  \else%
  \if@bkreview@provided
\vspace{4pt}%
  \else
  \vspace{2.8pc plus 4\p@}%
  \fi
  \fi
}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\usepackage{color}
\definecolor{gray}{cmyk}{0,0,0,.2}% #1 50pt width

%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Lastpage %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\def\lastpage@putlabel{\addtocounter{page}{-1}%
   \immediate\write\@auxout{\string
   \newlabel{LastPage}{{}{\thepage}}}%
   \addtocounter{page}{1}
   }
\AtEndDocument{%
   \message{Setting LastPage}%
   \clearpage\lastpage@putlabel
   \ifcolorfigs%
\clearpage
\onecolumn%
\input \jobname_colorfig.tex
\clearpage
\fi}%

\AtBeginDocument{\ifcolorfigs%
\usepackage{watermark}
\renewcommand{\thispageheading}[1]{%
  \def\@tempa{#1}%
  \ifx\@tempa\@empty
    \global\let\WMK@thishead\@empty
  \else
    \gdef\WMK@thishead{%
    \rotatebox{60}{\vbox to 20pc{\vfill\hbox to \textheight{\sf\fontsize{60}{60}\selectfont\raggedright \textbf{\textcolor{gray}{#1}}\hfill}\vfill}}
    }%
  \fi%
}
\long\def\Printfig#1{%
\clearpage
\thispageheading{PRINT USE ONLY}
\ \vfill
\centerline{{\includegraphics{#1}}}
\ \vfill}%
\fi}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%% Sectioning macros %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Lowest level heading that takes a number by default
\setcounter{secnumdepth}{0}

% Reset the default section macros to help with title casing
\def\@sect#1#2#3#4#5#6[#7]#8{%
  \ifnum #2>\c@secnumdepth
    \let\@svsec\@empty
  \else
    \refstepcounter{#1}%
    \protected@edef\@svsec{\@seccntformat{#1}\relax}%
  \fi
  \@tempskipa #5\relax
  \ifdim \@tempskipa>\z@
    \begingroup
      #6{%
        \@hangfrom{\hskip #3\relax\@svsec}%
          \interlinepenalty \@M
% Modified to uppercase H1's and titlecase the rest
          \ifnum #2=1\relax
            {#8}%
          \else
            {#8}%
          \fi
        \@@par}%
    \endgroup
    \csname #1mark\endcsname{#7}%
    \addcontentsline{toc}{#1}{%
      \ifnum #2>\c@secnumdepth \else
        \protect\numberline{\csname the#1\endcsname}%
      \fi
      #7}%
  \else
    \def\@svsechd{%
      #6{\hskip #3\relax
      \@svsec #8}%
      \csname #1mark\endcsname{#7}%
      \addcontentsline{toc}{#1}{%
        \ifnum #2>\c@secnumdepth \else
          \protect\numberline{\csname the#1\endcsname}%
        \fi
        #7}}%
  \fi
  \@xsect{#5}}

% H1
\def\section{%
\renewcommand{\@seccntformat}[1]{{{\csname the##1\endcsname\quad}}}
  \@startsection{section}{1}{\z@}
  {-20\p@ plus -3\p@ minus -3\p@}{6\p@}
  {\reset@font\fontsize{12}{14}\selectfont\fontseries{b}\selectfont
    \mathversion{bold}\raggedright%\setcounter{thm}{0}%
}}

% H2
\def\subsection{%
\renewcommand{\@seccntformat}[1]{{{\rm\csname the##1\endcsname\quad}}}
  \@startsection{subsection}{2}{\z@}
  {-18.5\p@ plus -1\p@ minus -2\p@}{7\p@}
  {\reset@font\normalsize\fontshape{it}\selectfont
    \raggedright}}

% H3
\def\subsubsection{%
\renewcommand{\@seccntformat}[1]{{{\rm\csname the##1\endcsname\quad}}}
  \@startsection{subsubsection}{3}{\z@}
  {-13\p@ plus -1\p@ minus -2\p@}{3\p@}
  {\reset@font\normalsize\itshape\selectfont
    \raggedright}}

\def\paragraph{%
\renewcommand{\@seccntformat}[1]{{{\csname the##1\endcsname.\quad}}}
  \@startsection{paragraph}{4}{\z@}
  {-9\p@ plus -1\p@}{-1em}
  {\reset@font\normalfont\normalsize\itshape}}


 % H5
 \def\subparagraph{%
   \@startsection{subparagraph}{5}{\z@}
   {-12\p@ plus -1\p@}{-1em}
   {\indent\reset@font\normalfont\normalsize%\bfseries
   }}

\def\acksection{%
 \@startsection{section}{1}{\z@}
  {-18\p@ plus -3\p@ minus -3\p@}{2\p@}%
  {\noindent\raisebox{4.5pt}{\rule{258pt}{.5pt}}\vskip-1.5pt\reset@font\fontsize{12}{14}\selectfont\fontseries{b}\selectfont
    \mathversion{bold}\raggedright
}}

\def\refsection{%
  \@startsection{section}{1}{\z@}
  {-19\p@ plus -2\p@ minus -1\p@}{8.5\p@}
  {\reset@font\normalsize\fontseries{b}\selectfont
    \mathversion{bold}\raggedright}}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Footnotes %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\def\@makefnmark{$^{\@thefnmark}$}%

\ifunarticle
\renewcommand\footnoterule{}
\else
\renewcommand\footnoterule{\begingroup\leftskip\z@\noindent
\rule{\textwidth}{0.5\p@}\vspace{2.5\p@}\setcounter{footnote}{1}\endgroup}
\fi
\newcommand\@makefntext[1]{%
 \begingroup
    \leftskip=\z@\rightskip=\z@
    \footnotesize
    \setlength\parindent{1em}%
    \@makefnmark\ignorespaces\,#1%
  \endgroup}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% From ifmtarg.sty
% Copyright Peter Wilson and Donald Arseneau, 2000
\begingroup
\catcode`\Q=3
\long\gdef\@ifmtarg#1{\@xifmtarg#1QQ\@secondoftwo\@firstoftwo\@nil}
\long\gdef\@xifmtarg#1#2Q#3#4#5\@nil{#4}
\long\gdef\@ifnotmtarg#1{\@xifmtarg#1QQ\@firstofone\@gobble\@nil}
\endgroup
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%% PostScript Rotation Macros %%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newif\if@rotate \@rotatefalse
\newif\if@rotatecenter \@rotatecenterfalse
\def\rotatecenter{\global\@rotatecentertrue}
\def\rotateendcenter{\global\@rotatecenterfalse}
\def\rotate{\global\@rotatetrue}
\def\endrotate{\global\@rotatefalse}
\newdimen\rotdimen
\def\rotstart#1{\special{ps: gsave currentpoint currentpoint translate
    #1 neg exch neg exch translate}}
\def\rotfinish{\special{ps: currentpoint grestore moveto}}
\def\rotl#1{\rotdimen=\ht#1\advance\rotdimen by \dp#1
    \hbox to \rotdimen{\vbox to\wd#1{\vskip \wd#1
    \rotstart{270 rotate}\box #1\vss}\hss}\rotfinish}
\def\rotr#1{\rotdimen=\ht #1\advance\rotdimen by \dp#1
    \hbox to \rotdimen{\vbox to \wd#1{\vskip \wd#1
    \rotstart{90 rotate}\box #1\vss}\hss}\rotfinish}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%% Figures and Tables %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newlength{\abovecaptionskip}
\newlength{\belowcaptionskip}
\setlength{\abovecaptionskip}{10\p@}
\setlength{\belowcaptionskip}{4\p@}

\newbox\figurecaptionbox
\long\def\@makecaption#1#2{\vspace{\abovecaptionskip}\par%
\let\query\figquery%
  \setbox\figurecaptionbox=\hbox{\fontsize{8}{10}\selectfont
    {\bf#1}\hskip1em#2}%
  \ifdim\wd\figurecaptionbox<\hsize
{\box\figurecaptionbox}
  \else
    \fontsize{8}{10}\selectfont
    \unhbox\figurecaptionbox
    \par
  \fi}

\newbox\schemecaptionbox
\long\def\@schemecaption#1#2{\vspace{\abovecaptionskip}\par%
\let\query\figquery%
  \setbox\schemecaptionbox=\hbox{#1\quad #2}%
  \ifdim\wd\schemecaptionbox<\hsize
{\box\schemecaptionbox}
  \else
\fontsize{8}{9}\selectfont
    \unhbox\schemecaptionbox
    \par
  \fi}

\newbox\tablecaptionbox
\long\def\@tablecaption#1#2{\par%
\let\query\tabquery%
\setbox\tablecaptionbox=\hbox{\fontsize{8}{10}\selectfont
    {\bf #1}\enskip #2\strut}%
  \ifdim\wd\tablecaptionbox<\hsize
{\box\tablecaptionbox}
  \else
    \fontsize{8}{10}\selectfont
    \unhbox\tablecaptionbox
    \par
  \fi
  \vspace{\belowcaptionskip}}

\def\thefigure{\@arabic\c@figure}
\def\fps@figure{tbp}
\def\ftype@figure{1}
\def\ext@figure{lof}
\def\fnum@figure{{\figurename}~\thefigure}
\def\figure{\@float{figure}}
\def\endfigure{\end@float}
\@namedef{figure*}{\@dblfloat{figure}}
\@namedef{endfigure*}{\end@dblfloat}

\def\thescheme{\@arabic\c@scheme}
\def\fps@scheme{h}
\def\ftype@scheme{2}
\def\ext@scheme{los}
\def\fnum@scheme{\MakeUppercase{\schemename}~\thescheme}
\def\scheme{\let\@makecaption\@schemecaption\@float{scheme}}
\def\endscheme{\end@float}
\@namedef{scheme*}{\let\@makecaption\@schemecaption\@dblfloat{scheme}}
\@namedef{endscheme*}{\end@dblfloat}

\def\thetable{\@arabic\c@table}
\def\fps@table{tbp}
\def\ftype@table{3}
\def\ext@table{lot}
\def\fnum@table{{\tablename}\hskip1em\thetable}
\def\table{\let\@makecaption\@tablecaption\@float{table}}
\def\endtable{\end@float}
\@namedef{table*}{\let\@makecaption\@tablecaption\@dblfloat{table}}
\@namedef{endtable*}{\end@dblfloat}

\newdimen\tempdime
\newbox\temptbox

\newlength{\abovefigskip}
\newlength{\belowfigskip}
\setlength{\abovefigskip}{\z@}
\setlength{\belowfigskip}{\z@}

\def\toprule{\noalign{\ifnum0=`}\fi
  \hrule \@height 0.5\p@
  \hrule \@height 1\p@ \@width \z@
  \futurelet \@tempa\@xhline}

\def\midrule{\noalign{\ifnum0=`}\fi
  \hrule \@height 2.5\p@ \@width \z@
  \hrule \@height 0.5\p@
  \hrule \@height 7\p@ \@width\z@
  \futurelet \@tempa\@xhline}

\def\botrule{\noalign{\ifnum0=`}\fi
  \hrule \@height 7\p@ \@width \z@
  \hrule \@height 0.5\p@
  \futurelet \@tempa\@xhline}

% Table and array parameters
\setlength\arraycolsep{.5em} \setlength\tabcolsep{.5em}
\setlength\arrayrulewidth{.25pt}
\setlength\doublerulesep{2.5pt}
\renewcommand\arraystretch{1}

\def\hrulefill{\leavevmode\leaders\hrule height .25pt\hfill\kern\z@}

\newcolumntype{P}[1]{>{\raggedright\let\\\@arraycr\hangindent1em}p{#1}}

\def\tablebodyfont{\fontsize{8}{11}\selectfont}
\def\resettablebodyfont{\def\tablebodyfont{\fontsize{8}{11}\selectfont}}
\newenvironment{processtable}[3]{\setbox\temptbox=\hbox{{\tablebodyfont #2}}%
\tempdime\wd\temptbox\@processtable{#1}{#2}{#3}{\tempdime}}%
{\relax}

\newenvironment{fwprocesstable}[3]{\setbox\temptbox=\hbox{{\tablebodyfont #2}}%
\tempdime\wd\temptbox\@fwprocesstable{#1}{#2}{#3}{\tempdime}}%
{\relax}%


\newenvironment{@processtable}[4]{%
\if!#1!%
\addtocounter{table}{-1}%%
\def\fnum@table{}%
\else%
\def\fnum@table{{\tablename}\enspace\thetable}%
\fi%
\setbox4=\hbox to 84mm{{\hfill\begin{minipage}[t]{#4}%
\caption{#1}{\tablebodyfont #2}
\@ifmtarg{#3}{}{\vskip6pt\noindent
\parbox{#4}{\fontsize{8}{10}\selectfont #3\par}}%
\end{minipage}\hfill}}%
\box4}{\relax}

\newenvironment{@fwprocesstable}[4]{%
\if!#1!%
\addtocounter{table}{-1}%
\def\fnum@table{}%
\else%
\def\fnum@table{{\tablename}\enspace\thetable}%
\fi%
\setbox4=\hbox to \textwidth{{\hfil\begin{minipage}[t]{#4}%
\caption{#1}{\tablebodyfont #2}%
\@ifmtarg{#3}{}{\vskip6pt\noindent%
\parbox{#4}{\fontsize{8}{10}\selectfont #3\par}}%
\end{minipage}\hfil}}%
\centering\box4}%
{\relax}%

\newcommand{\tabhead}[1]{#1}%
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Lists %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\def\labelenumi{{\rm(\arabic{enumi})}}
\def\theenumi{\arabic{enumi}}
\def\labelenumii{{\rm(\alph{enumii})}}
\def\theenumii{\alph{enumii}}
\def\p@enumii{\theenumi}
\def\labelenumiii{{\rm(\arabic{enumiii})}}
\def\theenumiii{\roman{enumiii}}
\def\p@enumiii{\theenumi(\theenumii)}
\def\labelenumiv{{\rm(\arabic{enumiv})}}
\def\theenumiv{\Alph{enumiv}}
\def\p@enumiv{\p@enumiii\theenumiii}
\def\labelitemi{$\bullet$}
\def\labelitemii{$\bullet$}
\def\labelitemiii{$\bullet$}
\def\labelitemiv{$\bullet$}

\setlength{\leftmargini}{\z@}
\setlength{\leftmarginii}{\z@}
\setlength{\leftmarginiii}{\z@}
\setlength{\leftmarginiv}{\z@}

\def\enumargs{%
   \partopsep     \z@
   \itemsep       \z@
   \parsep        \z@
   \rightmargin   \z@
   \labelsep      0.5em
   \listparindent \parindent
   \itemindent    \z@}

\def\enumerate{%
    \@ifnextchar[{\@numerate}{\@numerate[(3)]}}

\def\@numerate[#1]{%
     \ifnum \@enumdepth >3 \@toodeep\else
     \advance\@enumdepth \@ne
     \edef\@enumctr{enum\romannumeral\the\@enumdepth}
     \list{\csname label\@enumctr\endcsname}{%
       \enumargs
       \setlength{\leftmargin}{\csname leftmargin\romannumeral\the\@listdepth\endcsname}
       \usecounter{\@enumctr}
       \settowidth\labelwidth{#1}
       \addtolength{\leftmargin}{\labelwidth}
       \addtolength{\leftmargin}{\labelsep}
       \def\makelabel##1{\hss \llap{##1}}}%
     \fi
   }
\def\endenumerate{\endlist\advance \@listdepth -1}

% Changes to the list parameters for itemize
\def\itemargs{%
   \partopsep     \z@
   \itemsep       \z@
   \parsep        \z@
   \rightmargin   \z@
   \labelsep      0.5em
   \listparindent \parindent
   \itemindent    \z@}

\def\itemize{%
    \@ifnextchar[{\@itemize}{\@itemize[$\bullet$]}}

\def\@itemize[#1]{%
     \ifnum \@itemdepth >3 \@toodeep\else
     \advance\@itemdepth \@ne
     \edef\@itemctr{item\romannumeral\the\@itemdepth}
     \list{\csname label\@itemctr\endcsname}{%
       \itemargs
       \setlength{\leftmargin}{\csname leftmargin\romannumeral\the\@listdepth\endcsname}
       \settowidth\labelwidth{#1}
       \addtolength{\leftmargin}{\labelwidth}
       \addtolength{\leftmargin}{\labelsep}
       \def\makelabel##1{\hss \llap{##1}}}%
     \fi
   }
\let\enditemize\endlist

\setlength{\topsep}{6\p@}% \@plus 1\p@ \@minus 1\p@}
\setlength{\itemsep}{\z@}

\def\@listI{\leftmargin\leftmargini\topsep12\p@ plus 4\p@ minus 2\p@}
\let\@listi\@listI
\@listi
\def\@listii{\leftmargin\leftmarginii\topsep\z@}
\def\@listiii{\leftmargin\leftmarginiii\topsep\z@}
\def\@listiv{\leftmargin\leftmarginiv\topsep\z@}
\def\@listv{\leftmargin\leftmarginv\topsep\z@}
\def\@listvi{\leftmargin\leftmarginvi\topsep\z@}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% unnumbered list %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newenvironment{description}{%
  \begin{list}{}{%
      \usecounter{enumi}%
      \setlength{\itemsep}{\z@}%
      \setlength{\labelwidth}{\z@}%
      \setlength{\leftmargin}{2em}%
      \setlength{\itemindent}{-2em}}}%
{\end{list}}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Extracts %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\def\quotation{\par\begin{list}{}{\footnotesize%  Extracts in small type
      \setlength{\topsep}{\medskipamount}%
      \setlength{\itemsep}{\z@}%
      \setlength\labelwidth{\z@}%
      \setlength\labelsep{\z@}%
      \setlength\leftmargin{12pt}%
      \setlength\rightmargin{12pt}%
      \listparindent \parindent}%
  \item[\vrule width\z@ height 9\p@]}
\def\endquotation{\end{list}}
\let\quote\quotation
\let\endquote\endquotation
\newcommand{\source}[1]{\newline\hbox{}{#1}}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% programs %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

{\obeyspaces\global\let =\ }

\newskip\cmskipamount%
\cmskipamount=12pt plus 6pt minus 3pt%

\def\cmskip{\removelastskip\vskip\cmskipamount}

\long\def\bCM{\begingroup\parindent=0pt\cmskip\ttfamily%
\obeylines\obeyspaces}%

\def\eCM{\cmskip\endgroup}%

\long\def\tbCM{\begingroup\parindent=0pt\cmskip%
\obeylines\obeyspaces}%

\def\teCM{\cmskip\endgroup}%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\renewcommand{\qedsymbol}{\ensuremath{\blacksquare}}
\renewenvironment{proof}[1][\proofname]{\par
  \if@endproofbox\pushQED{\qed}\fi%
  \normalfont
  \topsep\bigskipamount
  \labelsep=1em\relax
  \trivlist
  \item[\hskip\labelsep
        \itshape
    #1]\ignorespaces
}{%
  \if@endproofbox\popQED\fi
  \endtrivlist\@endpefalse
}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


% Counter for saving the section numbering depth
\newcounter{savesecnumdepth}

%%%%%%%%%%%%%%%%%%%%%%%%%% Acknowledgments %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newif\ifack
\providecommand{\ackname}{Acknowledgements}
\newcommand{\ack}[1][\ackname]{\small\par%
\let\section\acksection
  \setcounter{savesecnumdepth}{\value{secnumdepth}}%
  \setcounter{secnumdepth}{0}%
  \acksection{\bf #1}%
  \setcounter{secnumdepth}{\value{savesecnumdepth}}%
}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%% Notations %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\providecommand{\notationname}{Notation}
\newcommand{\notation}[1][\notationname]{\par%
  \setcounter{savesecnumdepth}{\value{secnumdepth}}%
  \setcounter{secnumdepth}{0}%
  \acksection{\bf #1\vskip2.5pt}%
  \setcounter{secnumdepth}{\value{savesecnumdepth}}%
}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\providecommand{\nomenname}{Nomenclature}
\newcommand{\nomen}[1][\nomenname]{\normalsize%
  \setcounter{secnumdepth}{0}%
  \section{#1}%
}%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Notes %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\def\enoteheading{\section*{\notesname
  \@mkboth{\uppercase{\notesname}}{\uppercase{\notesname}}}%
     \leavevmode\par}

\def\enoteformat{\rightskip\z@ \leftskip=16pt\parindent=0pt
     \leavevmode\llap{\hbox{${\@theenmark}$}.\enskip}}


\newenvironment{notes}[1][99]{%
  \begingroup%
 }%
{\endgroup}%

\newenvironment{thebibliography}[1][99]{%
  \begingroup
  \small
  \setcounter{secnumdepth}{0}
  \acksection{\bibname\vspace*{-4pt}}%
  \begin{list}{\@biblabel{\theenumi}}{%
      \usecounter{enumi}%
\itemsep3pt
      }}%
{\end{list}\endgroup}

\usepackage[authoryear]{natbib}
\bibpunct[, ]{(}{)}{;}{a}{,}{;}

\def\@biblabel#1{{\bf#1\hskip4.5pt}}
\renewenvironment{thebibliography}[1]{%
  \begingroup
  \small
  \setcounter{secnumdepth}{0}
  \acksection{\bibname\vspace*{-4pt}}%
  \begin{list}{}{%
      \usecounter{enumi}%
\itemsep3pt
            \setlength\leftmargin{12pt}
            \setlength\itemindent{-12pt}
      }}%
{\end{list}\endgroup}


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  NORMES  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newskip\normskip
\setlength\normskip{6pt}

\newenvironment{normes}{%
  \begingroup
  \footnotesize\parindent=0pt
  \setcounter{secnumdepth}{0}
  \vskip\normskip
  {\fontsize{10}{12}\selectfont\bf\normsname}%
  \begin{list}{}{%
      \usecounter{enumi}%
      \setlength{\itemsep}{\z@}%
      \setlength{\labelwidth}{0pt}%
      \setlength{\leftmargin}{2em}%
      \setlength{\itemindent}{-2em}}}%
{\end{list}\endgroup}

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Index %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
\newif\if@restonecol
\def\theindex{\@mainmatterfalse
  \@restonecoltrue\if@twocolumn\@restonecolfalse\fi
  \begingroup\parindent \z@
  \addcontentsline{toc}{section}{Index}
  \columnseprule \z@
  \columnsep 1pc\section*{\indexname} %Subject or Author here
  \parskip\z@ plus .3\p@\relax\let\item\idxitem\fontsize{8\p@}{10\p@}\selectfont}
\def\idxitem{\par\raggedright\hangindent 3em}
\def\subitem{\par\penalty1000\raggedright\hangindent 3em\hspace*{1em}}
\def\subsubitem{\par\penalty1000\raggedright\hangindent 3em\hspace*{2em}}
\def\endtheindex{\if@restonecol\endgroup\onecolumn\else\clearpage\fi}
\def\indexspace{\par \vskip 18\p@ plus 12\p@ minus 12\p@\relax}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%% Appendix %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

\newif\ifappend % Are we in the Appendix?
\def\appendix{%
\renewcommand\footnotesize{%
  \@setfontsize\footnotesize{9\p@}{10\p@}%
  \abovedisplayskip 8\p@ \@plus2\p@ \@minus4\p@
  \abovedisplayshortskip 8\p@ \@plus2\p@ \@minus2\p@
  \belowdisplayshortskip 8\p@ \@plus2\p@ \@minus2\p@
  \def\@listi{\leftmargin\leftmargini
              \listparindent 1em
              \topsep 5\p@ \@plus 2\p@ \@minus 1\p@
              \parsep \z@ \itemsep \z@}%
  \belowdisplayskip \abovedisplayskip}
\footnotesize\par%
  \setcounter{secnumdepth}{3}
  \renewcommand{\thesection}{\Alph{section}}
  \renewcommand{\@seccntformat}[1]{{\csname
  the##1\endcsname}\quad}
%\def\thetable{\Alph{section}.\@arabic\c@table}
\def\thetable{\thesection\@arabic\c@table}
\def\thefigure{\thesection\@arabic\c@figure}
\renewcommand\theequation{\thesection\arabic{equation}}
        \setcounter{section}{0}
        \setcounter{table}{0}
        \setcounter{equation}{0}
        \setcounter{subsection}{0}
        \appendtrue}
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

% Override settings in MathTime back to TeX defaults
\DeclareMathSizes{5}     {5}   {5}  {5}
\DeclareMathSizes{6}     {6}   {5}  {5}
\DeclareMathSizes{7}     {7}   {5}  {5}
\DeclareMathSizes{8}     {8}   {6}  {5}
\DeclareMathSizes{9}     {9}   {7}  {5}
\DeclareMathSizes{10}   {10}   {7}  {5}
\DeclareMathSizes{12}   {12}   {9}  {7}

%Math parameters
\setlength{\jot}{5\p@}
\skip\@mpfootins = \skip\footins
\fboxsep=6\p@
\fboxrule=.25\p@

\medmuskip=4mu% plus 2mu minus 4mu
\thickmuskip=5mu% plus 5mu

\vbadness=9999
\tolerance=9999
\doublehyphendemerits=10000
\doublehyphendemerits 640000
\finalhyphendemerits  1000000

\flushbottom
\frenchspacing
\onecolumn
\pagestyle{headings}

% Short-form coding
\newcommand\tetal{{{\rm et~al.}}}
\newcommand\etal{\textit{et~al.}}
\newcommand\eg{\textit{e.g.}}
\newcommand\ie{\textit{i.e.}}
\let\endash\textendash

\def\dbond{\raise0.18ex\hbox{$=$}}
\def\bond{\raise0.18ex\hbox{$-$}}

\def\endash{--}
\def\emdash{\,--\,}
\def\sdot#1{{\buildrel{\scriptscriptstyle\bullet}\over{\hbox{$#1$}}}}
\def\ssdot#1{{\buildrel{\scriptscriptstyle\bullet\bullet}\over{\hbox{$#1$}}}}


\hyphenation{Table}
\hyphenation{Figure}
\hyphenation{Section}
\hyphenation{equation}
\hyphenation{Theorem}
\hyphenation{Lemma}
\hyphenation{Algorithm}
\hyphenation{Definition}
\hyphenation{Corollary}
\hyphenation{Proof}
\hyphenation{Remark}

\def\bcontinued{({\it Continued\/})}
\def\tcontinued{Continued}

\def\dd{{\rm d}}
\def\ee{{\rm e}}
\def\cir#1{{\accent"17 #1}}

\newdimen\p@renwd

\def\spbordermatrix#1{\begingroup \m@th
  \setbox\z@\vbox{\def\cr{\crcr\noalign{\kern2\p@\global\let\cr\endline}}%
    \ialign{$##$\hfil\kern2\p@\kern\p@renwd&\thinspace\hfil$##$\hfil
      &&\quad\hfil$##$\hfil\crcr
      \omit\strut\hfil\crcr\noalign{\kern-\baselineskip}%
      #1\crcr\omit\strut\cr}}%
  \setbox\tw@\vbox{\unvcopy\z@\global\setbox\@ne\lastbox}%
  \setbox\tw@\hbox{\unhbox\@ne\unskip\global\setbox\@ne\lastbox}%
  \setbox\tw@\hbox{$\kern\wd\@ne\kern-\p@renwd\left[\kern-\wd\@ne
    \global\setbox\@ne\vbox{\box\@ne\kern2\p@}%
    \vcenter{\kern-\ht\@ne\unvbox\z@\kern-\baselineskip}\,\hskip-\bmskip\right]$}%
  \null\;\vbox{\kern\ht\@ne\box\tw@}\endgroup}


\def\sqbordermatrix#1{\begingroup \m@th
  \setbox\z@\vbox{\def\cr{\crcr\noalign{\kern2\p@\global\let\cr\endline}}%
    \ialign{$##$\hfil\kern2\p@\kern\p@renwd&\thinspace\hfil$##$\hfil
      &&\quad\hfil$##$\hfil\crcr
      \omit\strut\hfil\crcr\noalign{\kern-\baselineskip}%
      #1\crcr\omit\strut\cr}}%
  \setbox\tw@\vbox{\unvcopy\z@\global\setbox\@ne\lastbox}%
  \setbox\tw@\hbox{\unhbox\@ne\unskip\global\setbox\@ne\lastbox}%
  \setbox\tw@\hbox{$\kern\wd\@ne\kern-\p@renwd\left[\kern-\wd\@ne
    \global\setbox\@ne\vbox{\box\@ne\kern2\p@}%
    \vcenter{\kern-\ht\@ne\unvbox\z@\kern-\baselineskip}\,\right]$}%
  \null\;\vbox{\kern\ht\@ne\box\tw@}\endgroup}

\def\llbordermatrix#1{\begingroup \m@th
  \setbox\z@\vbox{\def\cr{\crcr\noalign{\kern2\p@\global\let\cr\endline}}%
    \ialign{$##$\hfil\kern2\p@\kern\p@renwd&\thinspace\hfil$##$\hfil
      &&\quad\hfil$##$\hfil\crcr
      \omit\strut\hfil\crcr\noalign{\kern-\baselineskip}%
      #1\crcr\omit\strut\cr}}%
  \setbox\tw@\vbox{\unvcopy\z@\global\setbox\@ne\lastbox}%
  \setbox\tw@\hbox{\unhbox\@ne\unskip\global\setbox\@ne\lastbox}%
  \setbox\tw@\hbox{$\kern\wd\@ne\kern-\p@renwd\left[\kern-\wd\@ne
    \global\setbox\@ne\vbox{\box\@ne\kern2\p@}%
    \vcenter{\kern-\ht\@ne\unvbox\z@\kern-\baselineskip}\,\right.$}%
  \null\;\vbox{\kern\ht\@ne\box\tw@}\endgroup}

\def\lbordermatrix#1{\begingroup \m@th
  \setbox\z@\vbox{\def\cr{\crcr\noalign{\kern2\p@\global\let\cr\endline}}%
    \ialign{$##$\hfil\kern2\p@\kern\p@renwd&\thinspace\hfil$##$\hfil
      &&\quad\hfil$##$\hfil\crcr
      \omit\strut\hfil\crcr\noalign{\kern-\baselineskip}%
      #1\crcr\omit\strut\cr}}%
  \setbox\tw@\vbox{\unvcopy\z@\global\setbox\@ne\lastbox}%
  \setbox\tw@\hbox{\unhbox\@ne\unskip\global\setbox\@ne\lastbox}%
  \setbox\tw@\hbox{$\left[\kern\wd\@ne\kern-\p@renwd\kern-\wd\@ne
    \global\setbox\@ne\vbox{\box\@ne\kern2\p@}%
    \vcenter{\kern-\ht\@ne\unvbox\z@\kern-\baselineskip}\,\right.$}%
  \null\;\vbox{\kern\ht\@ne\box\tw@}\endgroup}

\newdimen\bmskip
\bmskip=0pt

\def\rbordermatrix#1{\begingroup \m@th
  \setbox\z@\vbox{\def\cr{\crcr\noalign{\kern2\p@\global\let\cr\endline}}%
    \ialign{\hfil$##$\hfil\kern6\p@\kern\p@renwd&\thinspace\hfil$##$\hfil
      &&\quad\hfil$##$\hfil\crcr
      \omit\strut\hfil\crcr\noalign{\kern-\baselineskip}%
      #1\crcr\omit\strut\cr}}%
  \setbox\tw@\vbox{\unvcopy\z@\global\setbox\@ne\lastbox}%
  \setbox\tw@\hbox{\unhbox\@ne\unskip\global\setbox\@ne\lastbox}%
  \setbox\tw@\hbox{$\left.\kern\wd\@ne\kern-\p@renwd\kern-\wd\@ne
    \global\setbox\@ne\vbox{\box\@ne\kern2\p@}
    \vcenter{\kern-\ht\@ne\unvbox\z@\kern-\baselineskip}\hskip-\bmskip\right]$}%
  \null\;\vbox{\kern\ht\@ne\box\tw@}\endgroup}

\chardef\permil="89%

\newtheorem{mythm}{mythm}[section]

\def\bktitle#1{{\bfseries #1}}
\def\au#1{\vskip6pt\hfill#1}
\def\aff#1{\hspace*{\fill}{\it #1}}
\def\email#1{\par{\it Email: #1}}
\def\cyear#1{\hspace*{\fill} $\copyright$ 2008, #1}
\usepackage{url}
\urlstyle{rm}
\def\UrlSpecials{\do\<{\langle}\do\>{\mathbin{\rangle}}\do\_{\_%
 \penalty\@m}\do\|{\mid}\do\{{\lbrace}\do\}{\mathbin{\rbrace}}\do
 \\{\mathbin{\backslash}}\do\~{\raise0ex\hbox{\m@th$\scriptstyle\sim$}}\do
 \ {\ }}%

\newenvironment{tabenumerate}[1][10pc]{
\begin{minipage}[t]{#1}
\begin{enumerate}
}{\end{enumerate}
\end{minipage}}

\newenvironment{tabitemize}[1][10pc]{
\begin{minipage}[t]{#1}
\begin{itemize}
}{\end{itemize}
\end{minipage}}

\def\tabspace#1{\protect\raisebox{-#1pt}[0pt][0pt]}
\def\figspace#1{\protect\raisebox{#1pt}[0pt][0pt]}

\def\edau#1{\vskip12pt{\fontsize{10}{12}\selectfont\hspace*{\fill}#1\par}}
\def\edaff#1{{\fontsize{10}{12}\selectfont\itshape\hspace*{\fill}#1\par}}

\def\weblink#1{#1}

\newcommand{\lastpage}[1]{{#1}}

\def\replyby#1{#1\vskip16pt}

\def\discussname{Discussers}

\usepackage{color}
\definecolor{mag}{cmyk}{0,1,0,0}
\iffproof%
\def\surname#1{\fboxsep=1pt\colorbox{mag}{#1}}%
\else%
\def\surname#1{#1}%
\fi%

\def\aopadjust#1{$^{\vphantom{\vrule height#1}}$}
\def\@journal@title{Forestry}
\def\@print@issn{0022-1686}
\def\@online@issn{1814-2079}
\def\@doi@fixed@field{10.1093$/$forestry$/$}
\def\@doi@variable@field{00000000000000000000}


\def\add#1{#1\par}

\def\aoppages{pp}

\def\jourinf{\year@info; {\bfseries \vol@info}, \page@extent@info,}

\def\runheadinfo{Vol.~\vol@info, No.~\issue@info\ (\year@info), \aoppages.~\page@extent@info}

\providecommand{\materialname}{Material and methods}
\newcommand{\material}[1][\materialname]{\small\par%
  \setcounter{savesecnumdepth}{\value{secnumdepth}}%
  \setcounter{secnumdepth}{0}%
  \section{#1}%
  \setcounter{secnumdepth}{\value{savesecnumdepth}}%
}

\iffinal
\usepackage[switch,columnwise]{lineno}
\linenumbers
\else
\renewcommand{\baselinestretch}{1.5}
\usepackage{lineno}
\linenumbers
\fi

\newcommand\linenomathWithnumbersforams{%
  \ifLineNumbers
  %\ifx\@@par\@@@par\else
    \ifnum\interlinepenalty>-\linenopenaltypar
      \global\holdinginserts\thr@@
      \advance\interlinepenalty \linenopenalty
     \ifhmode                                   % v4.3
      \advance\predisplaypenalty \linenopenalty
     \fi
      %\advance\postdisplaypenalty \linenopenalty
      \advance\interdisplaylinepenalty \linenopenalty
    \fi
  \fi
  \ignorespaces
  }

\newcommand\linenomathWithnumbersformultline{%
  \ifLineNumbers
  %\ifx\@@par\@@@par\else
    \ifnum\interlinepenalty>-\linenopenaltypar
      \global\holdinginserts\thr@@
      \advance\interlinepenalty \linenopenalty
     \ifhmode                                   % v4.3
      %\advance\predisplaypenalty \linenopenalty
     \fi
      %\advance\postdisplaypenalty \linenopenalty
      \advance\interdisplaylinepenalty \linenopenalty
    \fi
  \fi
  \ignorespaces
  }



\newcommand*\patchAmsMathEnvironmentForLineno[1]{%
\expandafter\let\csname old#1\expandafter\endcsname\csname #1\endcsname
\expandafter\let\csname oldend#1\expandafter\endcsname\csname end#1\endcsname
\renewenvironment{#1}%
{\def\linenomath{\linenomathWithnumbersforams}%added
 \@namedef{linenomath*}{\linenomathNonumbers}%added
\linenomath\csname old#1\endcsname}%
{\csname oldend#1\endcsname\endlinenomath}}%
\newcommand*\patchBothAmsMathEnvironmentsForLineno[1]{%
\patchAmsMathEnvironmentForLineno{#1}%
\patchAmsMathEnvironmentForLineno{#1*}%
}%

\AtBeginDocument{%
%\patchBothAmsMathEnvironmentsForLineno{equation}% deleted
\patchBothAmsMathEnvironmentsForLineno{align}%
\patchBothAmsMathEnvironmentsForLineno{flalign}%
\patchBothAmsMathEnvironmentsForLineno{alignat}%
\patchBothAmsMathEnvironmentsForLineno{gather}%
%\patchBothAmsMathEnvironmentsForLineno{multline}%
%\patchBothAmsMathEnvironmentsForLineno{split}%
\patchAmsMathEnvironmentForLineno{array}%
%\patchAmsMathEnvironmentForLineno{split}%
}

\renewenvironment{multline}{\linenomathWithnumbersformultline%
  \start@multline\st@rredfalse
}{%
  \iftagsleft@ \@xp\lendmultline@ \else \@xp\rendmultline@ \fi
  \ignorespacesafterend
\endlinenomath}
\renewenvironment{multline*}{\linenomathWithnumbersformultline\start@multline\st@rredtrue}{\endmultline\endlinenomath}

\def\insplit@{%
  \global\setbox\z@\vbox\bgroup
    \Let@ \chardef\dspbrk@context\@ne \restore@math@cr
    \default@tag % disallow use of \tag here
    \ialign\bgroup
      \hfil%
      \strut@
       $\m@th\displaystyle{##}$%
     &$\m@th\displaystyle{{}##}$%
      \hfill % Why not \hfil?---dmj, 1994/12/28
      \crcr\noalign{\global\advance\c@linenumber\@ne}%
}

\endinput
