import pytest
from recoup.core import *
def test_normalize_integer_money(): assert normalize({"source":"bank","reference":" A ","amount_paise":100,"timestamp":1}).reference=="A"
def test_match_same_amount_reference():
    a=normalize({"source":"a","reference":"X","amount_paise":100,"timestamp":1}); b=normalize({"source":"b","reference":"X","amount_paise":100,"timestamp":2}); assert match([a],[b])[0].score==1
def test_window():
    a=normalize({"source":"a","reference":"X","amount_paise":100,"timestamp":1}); b=normalize({"source":"b","reference":"X","amount_paise":100,"timestamp":1000}); assert not match([a],[b])
def test_recovery_gate(): assert recovery_allowed("amount_mismatch",10000); assert not recovery_allowed("amount_mismatch",9999)
def test_negative_rejected():
    with pytest.raises(ValueError): normalize({"source":"a","reference":"x","amount_paise":-1,"timestamp":1})
