# -*- encoding: utf-8 -*-
from abjad import *


def test_datastructuretools_TypedOrderedDict_01():
    r'''Implements __cmp__().
    '''
    
    dictionary_1 = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary_1['soprano'] = 'treble'

    dictionary_2 = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary_2['soprano'] = 'treble'

    dictionary_3 = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary_3['bass'] = 'bass'

    assert cmp(dictionary_1, dictionary_1) == 0
    assert cmp(dictionary_1, dictionary_2) == 0
    assert cmp(dictionary_1, dictionary_3) == 1
    assert cmp(dictionary_2, dictionary_1) == 0
    assert cmp(dictionary_2, dictionary_2) == 0
    assert cmp(dictionary_2, dictionary_3) == 1
    assert cmp(dictionary_3, dictionary_1) == -1
    assert cmp(dictionary_3, dictionary_2) == -1
    assert cmp(dictionary_3, dictionary_3) == 0


def test_datastructuretools_TypedOrderedDict_02():
    r'''Implements __contains__().
    '''
    
    dictionary = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary['soprano'] = 'treble'
    dictionary['alto'] = 'alto'
    dictionary['tenor'] = 'tenor'
    dictionary['bass'] = 'bass'

    assert 'soprano' in dictionary
    assert 'treble' not in dictionary
    assert [_ for _ in dictionary] == ['soprano', 'alto', 'tenor', 'bass']


def test_datastructuretools_TypedOrderedDict_03():
    r'''Implements __delitem__().
    '''
    
    dictionary_1 = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary_1['soprano'] = 'treble'
    del(dictionary_1['soprano'])

    dictionary_2 = datastructuretools.TypedOrderedDict(item_class=Clef)
    assert dictionary_1 == dictionary_2


def test_datastructuretools_TypedOrderedDict_04():
    r'''Implements __eq__().
    '''
    
    dictionary_1 = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary_1['soprano'] = 'treble'

    dictionary_2 = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary_2['soprano'] = 'treble'

    dictionary_3 = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary_3['bass'] = 'bass'

    assert dictionary_1 == dictionary_1
    assert dictionary_1 == dictionary_2
    assert not dictionary_1 == dictionary_3
    assert dictionary_2 == dictionary_1
    assert dictionary_2 == dictionary_2
    assert not dictionary_2 == dictionary_3
    assert not dictionary_3 == dictionary_1
    assert not dictionary_3 == dictionary_2
    assert dictionary_3 == dictionary_3


def test_datastructuretools_TypedOrderedDict_05():
    r'''Implements __format__().
    '''
    
    dictionary = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary['soprano'] = 'treble'
    dictionary['alto'] = 'alto'
    dictionary['tenor'] = 'tenor'
    dictionary['bass'] = 'bass'

    assert systemtools.TestManager.compare(
        format(dictionary),
        r'''
        datastructuretools.TypedOrderedDict(
            {
                'alto': indicatortools.Clef(
                    name='alto',
                    ),
                'bass': indicatortools.Clef(
                    name='bass',
                    ),
                'soprano': indicatortools.Clef(
                    name='treble',
                    ),
                'tenor': indicatortools.Clef(
                    name='tenor',
                    ),
                },
            item_class=indicatortools.Clef,
            )
                '''
        )


def test_datastructuretools_TypedOrderedDict_06():
    r'''Initializes from dictionary items.
    '''
    
    items = [
        ('soprano', Clef('treble')), 
        ('alto', Clef('alto')),
        ('tenor', Clef('tenor')),
        ('bass', Clef('bass')),
        ]
    dictionary_1 = datastructuretools.TypedOrderedDict(
        item_class=Clef, 
        tokens=items,
        )

    dictionary_2 = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary_2['soprano'] = 'treble'
    dictionary_2['alto'] = 'alto'
    dictionary_2['tenor'] = 'tenor'
    dictionary_2['bass'] = 'bass'

    assert dictionary_1 == dictionary_2


def test_datastructuretools_TypedOrderedDict_07():
    r'''Implements __len__().
    '''
    
    dictionary = datastructuretools.TypedOrderedDict(item_class=Clef)
    assert len(dictionary) == 0

    dictionary = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary['soprano'] = 'treble'
    assert len(dictionary) == 1


def test_datastructuretools_TypedOrderedDict_08():
    r'''Implements __ne__().
    '''
    
    dictionary_1 = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary_1['soprano'] = 'treble'

    dictionary_2 = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary_2['soprano'] = 'treble'

    dictionary_3 = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary_3['bass'] = 'bass'

    assert not dictionary_1 != dictionary_1
    assert not dictionary_1 != dictionary_2
    assert dictionary_1 != dictionary_3
    assert not dictionary_2 != dictionary_1
    assert not dictionary_2 != dictionary_2
    assert dictionary_2 != dictionary_3
    assert dictionary_3 != dictionary_1
    assert dictionary_3 != dictionary_2
    assert not dictionary_3 != dictionary_3


def test_datastructuretools_TypedOrderedDict_09():
    r'''Implements __reversed__().
    '''
    
    dictionary = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary['soprano'] = 'treble'
    dictionary['alto'] = 'alto'
    dictionary['tenor'] = 'tenor'
    dictionary['bass'] = 'bass'

    generator = reversed(dictionary)
    assert [_ for _ in generator] == ['bass', 'tenor', 'alto', 'soprano']


def test_datastructuretools_TypedOrderedDict_10():
    r'''Implements clear().
    '''
    
    dictionary_1 = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary_1['soprano'] = 'treble'
    dictionary_1['alto'] = 'alto'
    dictionary_1['tenor'] = 'tenor'
    dictionary_1['bass'] = 'bass'
    dictionary_1.clear()

    dictionary_2 = datastructuretools.TypedOrderedDict(item_class=Clef)
    assert dictionary_1 == dictionary_2


def test_datastructuretools_TypedOrderedDict_11():
    r'''Implements copy().
    '''
    
    dictionary_1 = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary_1['soprano'] = 'treble'
    dictionary_1['alto'] = 'alto'
    dictionary_1['tenor'] = 'tenor'
    dictionary_1['bass'] = 'bass'

    dictionary_2 = dictionary_1.copy()
    assert dictionary_1 == dictionary_2


def test_datastructuretools_TypedOrderedDict_12():
    r'''Implements get().
    '''
    
    dictionary = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary['soprano'] = 'treble'
    dictionary['alto'] = 'alto'
    dictionary['tenor'] = 'tenor'
    dictionary['bass'] = 'bass'

    assert dictionary.get('soprano') == Clef('treble')
    assert dictionary.get('foo') is None
    assert dictionary.get('foo', 'bar') == 'bar'


def test_datastructuretools_TypedOrderedDict_13():
    r'''Implements has_key().
    '''
    
    dictionary = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary['soprano'] = 'treble'
    dictionary['alto'] = 'alto'
    dictionary['tenor'] = 'tenor'
    dictionary['bass'] = 'bass'

    assert dictionary.has_key('soprano')
    assert not dictionary.has_key('treble')
    assert not dictionary.has_key('foo')


def test_datastructuretools_TypedOrderedDict_14():
    r'''Implements items().
    '''
    
    dictionary = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary['soprano'] = 'treble'
    dictionary['alto'] = 'alto'
    dictionary['tenor'] = 'tenor'
    dictionary['bass'] = 'bass'

    assert dictionary.items() == [
        ('soprano', Clef('treble')), 
        ('alto', Clef('alto')),
        ('tenor', Clef('tenor')),
        ('bass', Clef('bass')),
        ]


def test_datastructuretools_TypedOrderedDict_15():
    r'''Implements keys().
    '''
    
    dictionary = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary['soprano'] = 'treble'
    dictionary['alto'] = 'alto'
    dictionary['tenor'] = 'tenor'
    dictionary['bass'] = 'bass'

    assert dictionary.keys() == ['soprano', 'alto', 'tenor', 'bass']


def test_datastructuretools_TypedOrderedDict_16():
    r'''Implements pop().
    '''
    
    dictionary_1 = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary_1['soprano'] = 'treble'
    dictionary_1['alto'] = 'alto'
    dictionary_1['tenor'] = 'tenor'
    dictionary_1['bass'] = 'bass'

    dictionary_2 = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary_2['alto'] = 'alto'
    dictionary_2['tenor'] = 'tenor'
    dictionary_2['bass'] = 'bass'

    assert dictionary_1.pop('soprano') == Clef('treble')
    assert dictionary_1 == dictionary_2


#def test_datastructuretools_TypedOrderedDict_17():
#    r'''Implements popitem().
#    '''
#    
#    dictionary_1 = datastructuretools.TypedOrderedDict(item_class=Clef)
#    dictionary_1['soprano'] = 'treble'
#    dictionary_1['alto'] = 'alto'
#    dictionary_1['tenor'] = 'tenor'
#    dictionary_1['bass'] = 'bass'
#
#    dictionary_2 = datastructuretools.TypedOrderedDict(item_class=Clef)
#    dictionary_2['alto'] = 'alto'
#    dictionary_2['tenor'] = 'tenor'
#    dictionary_2['bass'] = 'bass'
#
#    item = dictionary_1.popitem('soprano')
#    assert item == ('soprano', Clef('treble'))
#    assert dictionary_1 == dictionary_2


def test_datastructuretools_TypedOrderedDict_18():
    r'''Implements update().
    '''
    
    dictionary_1 = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary_1['soprano'] = 'treble'
    dictionary_1['alto'] = 'alto'

    dictionary_2 = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary_2['tenor'] = 'tenor'
    dictionary_2['bass'] = 'bass'

    dictionary_3 = datastructuretools.TypedOrderedDict(item_class=Clef)
    dictionary_3['soprano'] = 'treble'
    dictionary_3['alto'] = 'alto'
    dictionary_3['tenor'] = 'tenor'
    dictionary_3['bass'] = 'bass'

    dictionary_1.update(dictionary_2)
    assert dictionary_1 == dictionary_3