\version "2.24.0"

\header {
  tagline = ##f
}

\paper {
  #(set-paper-size "a4" 'landscape)
  indent = 2.5\cm
  top-margin = 1\cm
  bottom-margin = 1\cm
  left-margin = 1\cm
  right-margin = 1\cm
  system-system-spacing.basic-distance = #14
}

\score {
  <<
    \new RhythmicStaff \with {
      instrumentName = "Layer 1"
    } {
      \time 4/4
      \override Score.RehearsalMark.self-alignment-X = #LEFT
      \mark \markup { \concat { \smaller \general-align #Y #DOWN \note {4} #1 " = 120 accel." } }
      \repeat volta 2 {
        \tuplet 7/4 { c'16 c' c' c' c' c' c' } \tuplet 7/4 { c'16 c' c' c' c' c' c' } \tuplet 7/4 { c'16 c' c' c' c' c' c' } \tuplet 7/4 { c'16 c' c' c' c' c' c' } \tuplet 7/4 { c'16 c' c' c' c' c' c' } \tuplet 7/4 { c'16 c' c' c' c' c' c' } \tuplet 7/4 { c'16 c' c' c' c' c' c' } \tuplet 7/4 { c'16 c' c' c' c' c' c' }
      }
      \once \override Score.RehearsalMark.self-alignment-X = #RIGHT
      \once \override Score.RehearsalMark.direction = #UP
      \mark \markup { \concat { \smaller \general-align #Y #DOWN \note {4} #1 " = 210" } }
    }
    \new Dynamics {
      s1\ff\> s1 s1 s1\n
    }
    \new RhythmicStaff \with {
      instrumentName = "Layer 2"
    } {
      \time 4/4
      \repeat volta 2 {
        c'16 c' c' c' c'16 c' c' c' c'16 c' c' c' c'16 c' c' c' c'16 c' c' c' c'16 c' c' c' c'16 c' c' c' c'16 c' c' c'
      }
    }
    \new Dynamics {
      s1\n\< s1 s1 s1\ff
    }
  >>
  \layout {
    \context {
      \Score
      \override SpacingSpanner.base-shortest-duration = #(ly:make-moment 1/16)
    }
  }
}
