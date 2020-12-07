import shelve


def test_sequence_diagram():
    db = shelve.open("test_db")
    ret = db['com.successfactors.gm.ui.fb.FBTGMBrowse']
    print('done')
