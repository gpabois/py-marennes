import pytest

from pymarennes import html as H
from pymarennes import layout as L
from pymarennes import style as S

__author__ = "G. PABOIS"
__copyright__ = "G. PABOIS"
__license__ = "MIT"

def test_anonymous_block_boxes():
    sheet = S.StyleSheet(
        [
            S.Rule([])
        ]
    )
    html = H.e("div", {}, [
        "Some text",
        h.e("p", {}, ["More text"])
    ])
    
    


def test_main(capsys):
    """CLI Tests"""
    # capsys is a pytest fixture that allows asserts against stdout/stderr
    # https://docs.pytest.org/en/stable/capture.html
    main(["7"])
    captured = capsys.readouterr()
    assert "The 7-th Fibonacci number is 13" in captured.out
