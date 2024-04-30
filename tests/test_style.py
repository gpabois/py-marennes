import pytest

from pymarennes import html as H
from pymarennes import style as S

__author__ = "G. PABOIS"
__copyright__ = "G. PABOIS"
__license__ = "MIT"

def test_001_simple_rules():
    tree = H.e("div", {"class": "red bold"}, [H.e("p", {"class": "red"})])
    sheet = S.StyleSheet(
        S.rule().select(S.by("class", "red")).decl("background-color": "red").build()
    )