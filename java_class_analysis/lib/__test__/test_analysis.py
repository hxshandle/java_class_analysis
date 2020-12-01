from lib.analysis import analysis
from assertpy import assert_that
from pathlib import Path

from lib.tree import JavaFileMeta


class TestAnalysis:
    def test_analysis(self):
        java_file_path = ""
        ret = analysis(java_file_path)
        assert_that(ret).is_none()
        ## Given a valid java file path
        file_path = r"F:\tmp\trunk\au-cdp\au-cdp-service\src\main\java\com\successfactors\learning\service\LearningPopulateCompetenciesRating.java"
        ret = analysis(file_path)
        assert_that(ret.path).is_equal_to(file_path)
        assert_that(len(ret.types)).is_equal_to(1)
        assert_that(ret.types[0].name).is_equal_to("LearningPopulateCompetenciesRating")
        assert_that(ret).is_not_none()
