from abjad import *
import py.test


def test_path_exists_between_01( ):
   '''Paths exist between all leaves in a voice.'''

   t = Voice(scale(4))

   assert t[0]._navigator._pathExistsBetween(t[1])
   assert t[1]._navigator._pathExistsBetween(t[2])
   assert t[2]._navigator._pathExistsBetween(t[3])

   r'''
   \new Voice {
      c'8
      d'8
      e'8
      f'8
   }
   '''


def test_path_exists_between_02( ):
   '''Paths exist between all notes in a staff.'''

   t = Staff(scale(4))

   assert t[0]._navigator._pathExistsBetween(t[1])
   assert t[1]._navigator._pathExistsBetween(t[2])
   assert t[2]._navigator._pathExistsBetween(t[3])

   r'''
   \new Staff {
      c'8
      d'8
      e'8
      f'8
   }
   '''


def test_path_exists_between_03( ):
   '''Paths exist between all notes in a sequential.'''

   t = Sequential(scale(4))

   assert t[0]._navigator._pathExistsBetween(t[1])
   assert t[1]._navigator._pathExistsBetween(t[2])
   assert t[2]._navigator._pathExistsBetween(t[3])

   r'''
   {
      c'8
      d'8
      e'8
      f'8
   }
   '''


def test_path_exists_between_04( ):
   '''TODO: Determine the correct behavior here.
            Should paths exist between NONE of the leaves in a parallel?
            Should paths exist between ALL of the leaves in a parallel?'''
   ## [VA] None... i think. 
  
   t = Parallel(scale(4))

   #assert not t[0]._navigator._pathExistsBetween(t[1])
   #assert not t[1]._navigator._pathExistsBetween(t[2])
   #assert not t[2]._navigator._pathExistsBetween(t[3])

   r'''
   <<
      c'8
      d'8
      e'8
      f'8
   >>
   '''


def test_path_exists_between_05( ):
   '''Paths exist between tuplet leaves.'''

   t = FixedDurationTuplet((2, 8), scale(3))

   assert t[0]._navigator._pathExistsBetween(t[1])
   assert t[1]._navigator._pathExistsBetween(t[0])

   assert t[1]._navigator._pathExistsBetween(t[2])
   assert t[2]._navigator._pathExistsBetween(t[1])

   r'''
   \times 2/3 {
      c'8
      d'8
      e'8
   }
   '''


def test_path_exists_between_06( ):
   '''Paths exist between all components here.'''

   t = Voice(Sequential(run(4)) * 2)
   diatonicize(t)

   r'''
   \new Voice {
      {
         c'8
         d'8
         e'8
         f'8
      }
      {
         g'8
         a'8
         b'8
         c''8
      }
   }
   '''

   ### paths exist between sequential containers
   assert t[0]._navigator._pathExistsBetween(t[1])
   assert t[1]._navigator._pathExistsBetween(t[0])

   ### paths exist between sequential containers and leaves
   assert t[0]._navigator._pathExistsBetween(t[1][0])
   assert t[0]._navigator._pathExistsBetween(t[1][1])
   assert t[0]._navigator._pathExistsBetween(t[1][2])
   assert t[0]._navigator._pathExistsBetween(t[1][3])
   assert t[1]._navigator._pathExistsBetween(t[0][0])
   assert t[1]._navigator._pathExistsBetween(t[0][1])
   assert t[1]._navigator._pathExistsBetween(t[0][2])
   assert t[1]._navigator._pathExistsBetween(t[0][3])


def test_path_exists_between_07( ):
   '''Paths exist between all components here.'''

   t1 = FixedDurationTuplet((2, 8), [Note(i, (1, 8)) for i in range(3)])
   t2 = FixedDurationTuplet((2, 8), [Note(i, (1, 8)) for i in range(3, 6)])
   t = Voice([t1, t2])

   ### paths exist between tuplets
   assert t[0]._navigator._pathExistsBetween(t[1])
   assert t[1]._navigator._pathExistsBetween(t[0])

   ### paths exist between tuplets and leaves
   assert t[0]._navigator._pathExistsBetween(t[1][0])
   assert t[0]._navigator._pathExistsBetween(t[1][1])
   assert t[0]._navigator._pathExistsBetween(t[1][2])
   assert t[1]._navigator._pathExistsBetween(t[0][0])
   assert t[1]._navigator._pathExistsBetween(t[0][1])
   assert t[1]._navigator._pathExistsBetween(t[0][2])

   r'''
   \new Voice {
      \times 2/3 {
         c'8
         cs'8
         d'8
      }
      \times 2/3 {
         ef'8
         e'8
         f'8
      }
   }
   '''


def test_path_exists_between_08( ):
   '''Paths exist here only within voices and not across voices.'''

   v1 = Voice([Note(i, (1, 8)) for i in range(4)])
   v2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
   t = Staff([v1, v2])

   assert not t[0]._navigator._pathExistsBetween(t[1])
   assert not t[1]._navigator._pathExistsBetween(t[0])
   assert not t[0][0]._navigator._pathExistsBetween(t[1][0])
   assert not t[1][0]._navigator._pathExistsBetween(t[0][-1])

   assert v1[0]._navigator._pathExistsBetween(v1[1])
   assert v1[1]._navigator._pathExistsBetween(v1[2])
   assert v1[2]._navigator._pathExistsBetween(v1[3])

   assert v2[0]._navigator._pathExistsBetween(v2[1])
   assert v2[1]._navigator._pathExistsBetween(v2[2])
   assert v2[2]._navigator._pathExistsBetween(v2[3])

   r'''
   \new Staff {
      \new Voice {
         c'8
         cs'8
         d'8
         ef'8
      }
      \new Voice {
         e'8
         f'8
         fs'8
         g'8
      }
   }
   '''


def test_path_exists_between_09( ):
   r'''Paths exist between all components here.
      Paths can cross the \context-boundary because
      contexts share the same name.'''

   v1 = Voice([Note(i, (1, 8)) for i in range(4)])
   v1.invocation.name = 'foo'
   v2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
   v2.invocation.name = 'foo'
   t = Staff([v1, v2])

   ### path exists between like-named voices
   assert t[0]._navigator._pathExistsBetween(t[1])
   assert t[1]._navigator._pathExistsBetween(t[0])

   ### path exists between like-named voices and voice contents
   assert t[0]._navigator._pathExistsBetween(t[1][0])
   assert t[0]._navigator._pathExistsBetween(t[1][1])
   assert t[0]._navigator._pathExistsBetween(t[1][2])
   assert t[0]._navigator._pathExistsBetween(t[1][3])
   assert t[1]._navigator._pathExistsBetween(t[0][0])
   assert t[1]._navigator._pathExistsBetween(t[0][1])
   assert t[1]._navigator._pathExistsBetween(t[0][2])
   assert t[1]._navigator._pathExistsBetween(t[0][3])

   r'''
   \new Staff {
      \context Voice = "foo" {
         c'8
         cs'8
         d'8
         ef'8
      }
      \context Voice = "foo" {
         e'8
         f'8
         fs'8
         g'8
      }
   }
   '''


def test_path_exists_between_10( ):
   '''Paths exist here only within voices and not across voices.'''

   v1 = Voice([Note(i, (1, 8)) for i in range(4)])
   v1.invocation.name = 'foo'
   v2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
   v2.invocation.name = 'bar'
   t = Staff([v1, v2])

   assert not t[0]._navigator._pathExistsBetween(t[1])
   assert not t[1]._navigator._pathExistsBetween(t[0])

   r'''
   \new Staff {
      \context Voice = "foo" {
         c'8
         cs'8
         d'8
         ef'8
      }
      \context Voice = "bar" {
         e'8
         f'8
         fs'8
         g'8
      }
   }
   '''


def test_path_exists_between_11( ):
   '''Paths exist here only within voices and nowhere else.'''

   v1 = Voice([Note(i, (1, 8)) for i in range(4)])
   v2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
   s1 = Staff([v1])
   s2 = Staff([v2])
   seq = Sequential([s1, s2])
   
   ### paths do not exist between anonymous staves 
   assert not seq[0]._navigator._pathExistsBetween(seq[1])
   assert not seq[1]._navigator._pathExistsBetween(seq[0])

   ### paths do not exist between anonymous voices
   assert not seq[0][0]._navigator._pathExistsBetween(seq[1][0])
   assert not seq[1][0]._navigator._pathExistsBetween(seq[0][0])

   ### paths do not exist between anonymous staves and voices
   assert not seq[0]._navigator._pathExistsBetween(seq[0][0])
   assert not seq[0]._navigator._pathExistsBetween(seq[1][0])
   assert not seq[1]._navigator._pathExistsBetween(seq[0][0])
   assert not seq[1]._navigator._pathExistsBetween(seq[1][0])

   r'''
   {
      \new Staff {
         \new Voice {
            c'8
            cs'8
            d'8
            ef'8
         }
      }
      \new Staff {
         \new Voice {
            e'8
            f'8
            fs'8
            g'8
         }
      }
   }
   '''   


def test_path_exists_between_12( ):
   '''Paths exist here only within voices.'''

   vl1 = Voice([Note(i, (1, 8)) for i in range(4)])
   vl2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
   vh1 = Voice([Note(i, (1, 8)) for i in range(12, 16)])
   vh2 = Voice([Note(i, (1, 8)) for i in range(16, 20)])
   s1 = Staff([vh1, vl1])
   s1.brackets = 'double-angle'
   s2 = Staff([vl2, vh2])
   s2.brackets = 'double-angle'
   seq = Sequential([s1, s2])

   assert not seq[0]._navigator._pathExistsBetween(seq[1])
   assert not seq[0]._navigator._pathExistsBetween(seq[1][0])
   assert not seq[0]._navigator._pathExistsBetween(seq[1][0][0])
   assert not seq[0]._navigator._pathExistsBetween(seq[1][1])
   assert not seq[0]._navigator._pathExistsBetween(seq[1][1][0])

   assert not seq[0][0]._navigator._pathExistsBetween(seq[1])
   assert not seq[0][0]._navigator._pathExistsBetween(seq[1][0])
   assert not seq[0][0]._navigator._pathExistsBetween(seq[1][0][0])
   assert not seq[0][0]._navigator._pathExistsBetween(seq[1][1])
   assert not seq[0][0]._navigator._pathExistsBetween(seq[1][1][0])

   assert not seq[0][0][-1]._navigator._pathExistsBetween(seq[1])
   assert not seq[0][0][-1]._navigator._pathExistsBetween(seq[1][0])
   assert not seq[0][0][-1]._navigator._pathExistsBetween(seq[1][0][0])
   assert not seq[0][0][-1]._navigator._pathExistsBetween(seq[1][1])
   assert not seq[0][0][-1]._navigator._pathExistsBetween(seq[1][1][0])

   assert not seq[0][1]._navigator._pathExistsBetween(seq[1])
   assert not seq[0][1]._navigator._pathExistsBetween(seq[1][0])
   assert not seq[0][1]._navigator._pathExistsBetween(seq[1][0][0])
   assert not seq[0][1]._navigator._pathExistsBetween(seq[1][1])
   assert not seq[0][1]._navigator._pathExistsBetween(seq[1][1][0])

   assert not seq[0][1][-1]._navigator._pathExistsBetween(seq[1])
   assert not seq[0][1][-1]._navigator._pathExistsBetween(seq[1][0])
   assert not seq[0][1][-1]._navigator._pathExistsBetween(seq[1][0][0])
   assert not seq[0][1][-1]._navigator._pathExistsBetween(seq[1][1])
   assert not seq[0][1][-1]._navigator._pathExistsBetween(seq[1][1][0])

   r'''
   {
      \new Staff <<
         \new Voice {
            c''8
            cs''8
            d''8
            ef''8
         }
         \new Voice {
            c'8
            cs'8
            d'8
            ef'8
         }
      >>
      \new Staff <<
         \new Voice {
            e'8
            f'8
            fs'8
            g'8
         }
         \new Voice {
            e''8
            f''8
            fs''8
            g''8
         }
      >>
   }
   '''


def test_path_exists_between_13( ):
   '''Paths exist between all components here.'''

   s1 = Sequential([Note(i, (1, 8)) for i in range(4)])
   s1 = Sequential([s1])
   s2 = Sequential([Note(i, (1, 8)) for i in range(4, 8)])
   s2 = Sequential([s2])
   t = Voice([s1, s2])

   r'''
   \new Voice {
      {
         {
            c'8
            cs'8
            d'8
            ef'8
         }
      }
      {
         {
            e'8
            f'8
            fs'8
            g'8
         }
      }
   }
   '''

   assert t[0]._navigator._pathExistsBetween(t[1])
   assert t[0]._navigator._pathExistsBetween(t[1][0])
   assert t[0]._navigator._pathExistsBetween(t[1][0][0])
   
   assert t[0][0]._navigator._pathExistsBetween(t[1])
   assert t[0][0]._navigator._pathExistsBetween(t[1][0])
   assert t[0][0]._navigator._pathExistsBetween(t[1][0][0])
   
   assert t[0][0][-1]._navigator._pathExistsBetween(t[1])
   assert t[0][0][-1]._navigator._pathExistsBetween(t[1][0])
   assert t[0][0][-1]._navigator._pathExistsBetween(t[1][0][0])


def test_path_exists_between_14( ):
   '''
   Path exists between consecutive like-named staves.
      '''

   t = Sequential(Staff([ ]) * 2)
   t[0].invocation.name = 'foo'
   t[1].invocation.name = 'foo'

   r'''
   {
      \context Staff = "foo" {
      }
      \context Staff = "foo" {
      }
   }
   '''

   assert t[0]._navigator._pathExistsBetween(t[1])
   assert t[1]._navigator._pathExistsBetween(t[0])


def test_path_exists_between_15( ):
   '''
   Path DOES NOT exist between unvoice leaves contained in staves 
   where path does exist.
   '''

   t = Sequential(Staff(run(4)) * 2)
   t[0].invocation.name = 'foo'
   t[1].invocation.name = 'foo'
   diatonicize(t)

   r'''
   {
      \context Staff = "foo" {
         c'8
         d'8
         e'8
         f'8
      }
      \context Staff = "foo" {
         g'8
         a'8
         b'8
         c''8
      }
   }
   '''

   assert t[0]._navigator._pathExistsBetween(t[1])
   assert t[1]._navigator._pathExistsBetween(t[0])

   assert not t[0][0]._navigator._pathExistsBetween(t[1][0])
   assert not t[1][0]._navigator._pathExistsBetween(t[0][1])


def test_path_exists_between_16( ):
   '''LilyPond puts leaves in like-named voices which 
      in turn reside in like-named staves in the same voice.'''

   t = Sequential(Staff([Voice(run(4))]) * 2)
   t[0].invocation.name = 'staff'
   t[0][0].invocation.name = 'voice'
   t[1].invocation.name = 'staff'
   t[1][0].invocation.name = 'voice'
   diatonicize(t)

   r'''{
           \context Staff = "staff" {
                   \context Voice = "voice" {
                           c'8
                           d'8
                           e'8
                           f'8
                   }
           }
           \context Staff = "staff" {
                   \context Voice = "voice" {
                           g'8
                           a'8
                           b'8
                           c''8
                   }
           }
   }'''

   leaves = t.leaves

   assert leaves[0]._navigator._pathExistsBetween(leaves[1])
   assert leaves[0]._navigator._pathExistsBetween(leaves[4])

   assert leaves[4]._navigator._pathExistsBetween(leaves[0])
   assert leaves[4]._navigator._pathExistsBetween(leaves[7])


def test_path_exists_between_17( ):
   '''LilyPond puts leaves in like-named voices that reside,
      however, in differently named (anonymous) staves
      into separate voices.'''

   t = Sequential(Staff([Voice(run(4))]) * 2)
   t[0][0].invocation.name = 'voice'
   t[1][0].invocation.name = 'voice'
   diatonicize(t)

   r'''{
           \new Staff {
                   \context Voice = "voice" {
                           c'8
                           d'8
                           e'8
                           f'8
                   }
           }
           \new Staff {
                   \context Voice = "voice" {
                           g'8
                           a'8
                           b'8
                           c''8
                   }
           }
   }'''

   leaves = t.leaves

   assert leaves[0]._navigator._pathExistsBetween(leaves[1])
   assert not leaves[0]._navigator._pathExistsBetween(leaves[4])

   assert not leaves[4]._navigator._pathExistsBetween(leaves[0])
   assert leaves[4]._navigator._pathExistsBetween(leaves[7])


def test_path_exists_between_18( ):
   '''Path DOES exist between consecutive like-named voices.'''

   t = Sequential(Voice(run(4)) * 2)
   t[0].invocation.name = 'foo'
   t[1].invocation.name = 'foo'
   diatonicize(t)

   r'''
   {
      \context Voice = "foo" {
         c'8
         d'8
         e'8
         f'8
      }
      \context Voice = "foo" {
         g'8
         a'8
         b'8
         c''8
      }
   }
   '''

   assert t[0]._navigator._pathExistsBetween(t[1])
   assert t[1]._navigator._pathExistsBetween(t[0])

   assert t[0][0]._navigator._pathExistsBetween(t[1][0])
   assert t[1][0]._navigator._pathExistsBetween(t[0][1])


def test_path_exists_between_19( ):
   '''Path does not exist from anonymous voice to naked notes.'''

   t = Staff(run(4))
   t.insert(2, Voice(run(2)))
   diatonicize(t)

   r'''\new Staff {
      c'8
      d'8
      \new Voice {
         e'8
         f'8
      }
      g'8
      a'8
   }'''

   assert t[0]._navigator._pathExistsBetween(t[1])
   assert not t[0]._navigator._pathExistsBetween(t[2][0])
   assert t[0]._navigator._pathExistsBetween(t[3])

   assert not t[2][0]._navigator._pathExistsBetween(t[0])
   assert t[2][0]._navigator._pathExistsBetween(t[2][1])
   assert not t[2][0]._navigator._pathExistsBetween(t[3])


def test_path_exists_between_20( ):
   '''
   Path exist between sequential equally named voices inside a 
   parallel container and between all notes contained in the voices.
   '''
   v1 = Voice(run(4))
   v2 = Voice(run(4))
   v1.invocation.name = v2.invocation.name = 'voiceOne'
   t = Parallel([Sequential([v1, v2])])
   diatonicize(t)
   r'''
   <<
           {
                   \context Voice = "voiceOne" {
                           c'8
                           d'8
                           e'8
                           f'8
                   }
                   \context Voice = "voiceOne" {
                           g'8
                           a'8
                           b'8
                           c''8
                   }
           }
   >>
   '''
   assert v1._navigator._pathExistsBetween(v2)
   for n1, n2 in zip(t.leaves[0:-1], t.leaves[1:]):
      assert n1._navigator._pathExistsBetween(n2)


def test_path_exists_between_21( ):
   '''
   Path exists between equally named voices contained in different
   parallel containers.
   '''
   v1 = Voice(run(4))
   v2 = Voice(run(4))
   v1.invocation.name = v2.invocation.name = 'voiceOne'
   t = Sequential([Parallel([v1]), Parallel([v2])])
   diatonicize(t)
   r'''
   {
           <<
                   \context Voice = "voiceOne" {
                           c'8
                           d'8
                           e'8
                           f'8
                   }
           >>
           <<
                   \context Voice = "voiceOne" {
                           g'8
                           a'8
                           b'8
                           c''8
                   }
           >>
   }
   '''
   assert v1._navigator._pathExistsBetween(v2)
   for n1, n2 in zip(t.leaves[0:-1], t.leaves[1:]):
      assert n1._navigator._pathExistsBetween(n2)


def test_path_exists_between_22( ):
   '''
   Path exists between equally named parallel and sequential containers.
   '''
   v1 = Voice(run(4))
   v2 = Voice(run(4))
   v1.invocation.name = v2.invocation.name = 'voiceOne'
   s1 = Staff([v1])
   s2 = Staff([v2])
   s1.invocation.name = s2.invocation.name = 'staffOne'
   s1.brackets = 'double-angle'
   s2.brackets = 'double-angle'
   t = Sequential([s1, s2])
   diatonicize(t)
   r'''
   {
           \context Staff = "staffOne" <<
                   \context Voice = "voiceOne" {
                           c'8
                           d'8
                           e'8
                           f'8
                   }
           >>
           \context Staff = "staffOne" <<
                   \context Voice = "voiceOne" {
                           g'8
                           a'8
                           b'8
                           c''8
                   }
           >>
   }
   '''
   assert v1._navigator._pathExistsBetween(v2)
   assert s1._navigator._pathExistsBetween(s2)
   for n1, n2 in zip(t.leaves[0:-1], t.leaves[1:]):
      assert n1._navigator._pathExistsBetween(n2)


def test_path_exists_between_23( ):
   '''Path exists between equally named StaffGroups.'''
   t = Sequential([StaffGroup([ ]), StaffGroup([ ])])
   t[0].invocation.name = t[1].invocation.name = 'staffGroup'
   r'''{
           \context StaffGroup = "staffGroup" <<
           >>
           \context StaffGroup = "staffGroup" <<
           >>
   }
   '''
   assert t[0]._navigator._pathExistsBetween(t[1])
