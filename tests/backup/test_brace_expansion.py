import pytest
from mkdf.fs.brace_expansion import brace_expand

def test_simple_expansion():
    assert sorted(brace_expand("test/{a,b,c}")) == sorted(["test/a", "test/b", "test/c"])

def test_nested_expansion():
    expected = [
        "app/api/models/",
        "app/api/views/",
        "app/frontend/"
    ]
    assert sorted(brace_expand("app/{api/{models/,views/},frontend/}")) == sorted(expected)

def test_no_braces():
    assert brace_expand("simple/path") == ["simple/path"]

def test_empty_braces():
    assert brace_expand("test/{}") == ["test/"]

def test_multiple_brace_groups():
    expected = [
        "a-x-1", "a-x-2", "a-y-1", "a-y-2",
        "b-x-1", "b-x-2", "b-y-1", "b-y-2"
    ]
    assert sorted(brace_expand("{a,b}-{x,y}-{1,2}")) == sorted(expected)