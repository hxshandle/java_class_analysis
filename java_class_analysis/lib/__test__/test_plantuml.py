import shelve
from .. import plantuml
from assertpy import assert_that

def test_sequence_diagram():
    db = shelve.open("test_db")
    ret = db['com.successfactors.gm.ui.fb.FBObj5']
    print('done')
    klass = ret[0]
    uml = plantuml.sequence_diagram(klass)
    print(uml)
    assert_that(uml).is_not_none()


def test_mind_diagram():
    db = shelve.open("test_db")
    ret = db['com.successfactors.gm.ui.fb.FBObj5']
    uml = plantuml.mind_diagram(ret[0])
    print(uml)
    assert_that(uml).is_not_none()

