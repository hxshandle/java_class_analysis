import shelve
from lib import plantuml
from assertpy import assert_that

def test_sequence_diagram():
    db = shelve.open("test_db")
    ret = db['com.successfactors.gm.ui.fb.FBTGMBrowse']
    print('done')
    klass = ret[0]
    uml = plantuml.sequence_diagram(klass)
    assert_that(uml).is_not_none()
