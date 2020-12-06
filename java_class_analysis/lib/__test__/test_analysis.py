from lib.analysis import Analyzer
from assertpy import assert_that
from pathlib import Path

from lib.tree import JavaFileMeta


class TestAnalysis:
    def test_analysis(self):
        print("\n")
        # F:\tmp\trunk\au-cdp\au-cdp-service\src\main\java\com\successfactors\learning\service\learningclient\LearningRestClient.java
        analyzer = Analyzer(r"F:\tmp\trunk", enable_method_filter=True)
        # "com.successfactors.learning.service.learningclient.LearningRestClient"
        klass = "com.successfactors.gm.ui.fb.FBTGMBrowse"

        ret = analyzer.parse(klass)
        assert_that(len(ret)).is_equal_to(1)
