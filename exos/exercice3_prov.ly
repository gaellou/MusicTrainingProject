\version "2.14.1"
\include "event-listener.ly"
\include "italiano.ly" 

\paper {
   paper-width = 8.0\cm
   line-width = 8.0\cm
   paper-height = 2.5\cm
   make-footer=##f
}

global = {
  \clef treble

  \time 4/4
}

notes = \relative do' {do4 re8 mi re2 do1 }

\transpose do lad'{\clef alto \notes}
