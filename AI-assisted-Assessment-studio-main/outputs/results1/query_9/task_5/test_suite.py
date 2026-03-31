import pytest
from solution import process_myth_artifacts

@pytest.mark.parametrize("artifacts, expected", [
    ([{'name': 'Mjolnir', 'myth': 'Norse'},
      {'name': 'Aegis', 'myth': 'Greek'},
      {'name': 'Excalibur', 'myth': 'Arthurian'},
      {'name': 'Olympus', 'myth': 'Greek'},
      {'name': 'Gungnir', 'myth': 'Norse'}],
     {
        'Norse': ['Mjolnir', 'Gungnir'],
        'Greek': ['Aegis', 'Olympus'],
        'Arthurian': ['Excalibur'],
        'totals': {'Norse': 2, 'Greek': 2, 'Arthurian': 1, 'total': 5}
     }),

    ([{'name': 'Pandora', 'myth': 'Greek'},
      {'name': 'Avalon', 'myth': 'Arthurian'},
      {'name': 'Fenrir', 'myth': 'Norse'}],
     {
        'Greek': ['Pandora'],
        'Arthurian': ['Avalon'],
        'Norse': ['Fenrir'],
        'totals': {'Greek': 1, 'Arthurian': 1, 'Norse': 1, 'total': 3}
     }),

    ([{'name': 'Fenrir', 'myth': 'Norse'}],
     {
        'Norse': ['Fenrir'],
        'totals': {'Norse': 1, 'total': 1}
     }),

    ([],
     {
        'totals': {'total': 0}
     }),

    ([{'name': 'Thor', 'myth': 'Norse'},
      {'name': 'Odin', 'myth': 'Norse'},
      {'name': 'Zeus', 'myth': 'Greek'},
      {'name': 'Ra', 'myth': 'Egyptian'},
      {'name': 'Horus', 'myth': 'Egyptian'},
      {'name': 'Anubis', 'myth': 'Egyptian'}],
     {
        'Norse': ['Thor', 'Odin'],
        'Greek': ['Zeus'],
        'Egyptian': ['Ra', 'Horus', 'Anubis'],
        'totals': {'Norse': 2, 'Greek': 1, 'Egyptian': 3, 'total': 6}
     })
])
def test_process_myth_artifacts(artifacts, expected):
    assert process_myth_artifacts(artifacts) == expected