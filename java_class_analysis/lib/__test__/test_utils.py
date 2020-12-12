from .. import utils
from assertpy import assert_that
def test_workspace_root():
    a = utils.workspace_root()
    assert_that(a).is_not_none()
