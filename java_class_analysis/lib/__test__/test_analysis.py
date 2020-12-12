import pickle
import shelve
from json import dumps, loads

from ..analysis import Analyzer
from assertpy import assert_that
from pathlib import Path

from ..tree import JavaFileMeta


class TestAnalysis:
    def test_analysis(self):
        print("\n")
        # F:\tmp\trunk\au-cdp\au-cdp-service\src\main\java\com\successfactors\learning\service\learningclient\LearningRestClient.java
        analyzer = Analyzer(r"F:\tmp\trunk", enable_method_filter=True)
        # "com.successfactors.learning.service.learningclient.LearningRestClient"
        klass = "com.successfactors.gm.ui.fb.FBObj5"
        ret = analyzer.parse(klass)
        assert_that(len(ret)).is_equal_to(1)
        k = ret[0]
        with shelve.open('test_db') as db:
            db[klass] = ret
        print("done")
