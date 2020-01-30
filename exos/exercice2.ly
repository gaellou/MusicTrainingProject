\version "2.14.1"
\include "event-listener.ly"
\include "italiano.ly" 

\paper {
   paper-width = 5.0\cm
   line-width = 5.0\cm
   paper-height = 2.5\cm
   make-footer=##f
}


global = {
    \clef treble

  \time 4/4
}

notes = \relative do' {\global do2 mi    }

