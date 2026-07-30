\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{cv}[2026/07/30 v0.1 Agentic Bilingual CV]

\newif\ifcvchinese
\cvchinesefalse

\DeclareOption{english}{\cvchinesefalse}
\DeclareOption{chinese}{\cvchinesetrue}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}
\ProcessOptions\relax

\LoadClass[10pt,a4paper]{article}

\RequirePackage{fontspec}
\RequirePackage{xcolor}
\RequirePackage{hyperref}
\RequirePackage{array}
\RequirePackage{geometry}

\ifcvchinese
  \geometry{left=1.45cm,right=1.45cm,top=1.15cm,bottom=1.15cm}
\else
  \geometry{left=1.35cm,right=1.35cm,top=1.15cm,bottom=1.15cm}
\fi

\defaultfontfeatures{Ligatures=TeX}

\ifcvchinese
  \IfFontExistsTF{Songti SC}{%
    \setmainfont{Songti SC}
  }{%
    \IfFontExistsTF{Noto Serif CJK SC}{%
      \setmainfont{Noto Serif CJK SC}
    }{%
      \IfFontExistsTF{Source Han Serif SC}{%
        \setmainfont{Source Han Serif SC}
      }{%
        \PackageError{cv}{No supported Chinese serif font found}{%
          Install Songti SC, Noto Serif CJK SC, or Source Han Serif SC.
        }
      }
    }
  }
  \IfFontExistsTF{Heiti SC}{%
    \newfontfamily\cvheadingfont{Heiti SC}
  }{%
    \IfFontExistsTF{Noto Sans CJK SC}{%
      \newfontfamily\cvheadingfont{Noto Sans CJK SC}
    }{%
      \IfFontExistsTF{Source Han Sans SC}{%
        \newfontfamily\cvheadingfont{Source Han Sans SC}
      }{%
        \newfontfamily\cvheadingfont{Latin Modern Sans}
      }
    }
  }
  \XeTeXlinebreaklocale "zh"
  \XeTeXlinebreakskip=0pt plus 1pt
\else
  \setmainfont{lmroman10-regular.otf}[
    Ligatures=NoCommon,
    BoldFont=lmroman10-bold.otf,
    ItalicFont=lmroman10-italic.otf,
    BoldItalicFont=lmroman10-bolditalic.otf
  ]
  \newfontfamily\cvheadingfont{lmroman10-bold.otf}
\fi

\definecolor{cvaccent}{HTML}{174A6E}
\definecolor{cvmuted}{HTML}{4F5963}
\definecolor{cvrule}{HTML}{AEBBC4}

\hypersetup{
  colorlinks=true,
  urlcolor=cvaccent,
  pdfauthor={},
  pdftitle={Resume},
  pdfsubject={},
  pdfkeywords={}
}

\pagestyle{empty}
\setlength{\parindent}{0pt}
\setlength{\parskip}{0pt}
\setlength{\tabcolsep}{0pt}
\linespread{1.0}
\hyphenpenalty=10000
\exhyphenpenalty=10000
\emergencystretch=2em
\urlstyle{same}

\newcommand{\cvsetmetadata}[2]{%
  \hypersetup{pdfauthor={#1},pdftitle={#2}}%
}

\newcommand{\cvsep}{\quad{\color{cvrule}\textbar}\quad}

\newcommand{\cvheader}[3]{%
  \begin{center}
    {\cvheadingfont\fontsize{21}{23}\selectfont\color{cvaccent}#1}\par
    \vspace{2pt}
    {\color{cvmuted}#2}\par
    \vspace{2pt}
    {\small #3}
  \end{center}
  \vspace{-5pt}
}

\ifcvchinese
  \newcommand{\cvsecondary}[1]{{\color{cvmuted}#1}}
  \newcommand{\cvsection}[1]{%
    \vspace{5pt}
    \noindent
    {\color{cvaccent}\rule{3pt}{13pt}}\hspace{6pt}%
    {\color{cvaccent}\cvheadingfont\fontsize{13}{15}\selectfont #1}\hspace{8pt}%
    {\color{cvrule}\leaders\hrule height 0.35pt\hfill\kern0pt}\par
    \vspace{2pt}
  }
\else
  \newcommand{\cvsecondary}[1]{{\color{cvmuted}\itshape #1}}
  \newcommand{\cvsection}[1]{%
    \vspace{5pt}
    {\color{cvaccent}\large\cvheadingfont\MakeUppercase{#1}}\par
    \vspace{1pt}{\color{cvaccent}\hrule height 0.8pt}
    \vspace{2pt}
  }
\fi

\newcommand{\cventry}[4]{%
  \begin{tabular}{@{}p{0.72\textwidth}>{\raggedleft\arraybackslash}p{0.28\textwidth}@{}}
    \bfseries #1 & {\small #2} \\
    \cvsecondary{#3} & {\small\cvsecondary{#4}}
  \end{tabular}\par
}

\newcommand{\cvskill}[2]{%
  \textbf{#1}\hspace{4pt}#2\par
}

\newenvironment{cvitems}{%
  \begin{list}{\color{cvaccent}\raisebox{0.25ex}{\scriptsize\textbullet}}{%
    \setlength{\itemsep}{1pt}%
    \setlength{\parskip}{0pt}%
    \setlength{\parsep}{0pt}%
    \setlength{\topsep}{1pt}%
    \setlength{\partopsep}{0pt}%
    \setlength{\leftmargin}{15pt}%
    \setlength{\labelsep}{6pt}%
    \setlength{\labelwidth}{5pt}%
  }%
}{%
  \end{list}%
}

\endinput
