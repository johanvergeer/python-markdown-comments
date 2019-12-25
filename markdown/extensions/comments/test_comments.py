import textwrap

import pytest
from markdown import Markdown

from .comments import CommentsExtension


@pytest.fixture
def markdowner() -> Markdown:
    extension = CommentsExtension()
    return Markdown(extensions=[extension])


@pytest.mark.parametrize(
    "md_input,expected",
    [
        (
            # Inline
            "text <!---inline comment-->",
            "<p>text</p>",
        ),
        (
            # Inline beginning and end
            "<!---inline comment-->text<!---inline comment-->",
            "<p>text</p>",
        ),
        (
            # Full line
            """\
text
<!---this line is ommitted entirely-->
more text""",
            """\
<p>text</p>
<p>more text</p>""",
        ),
        (
            # Multiline
            """\
text  <!---multiline comment
multiline comment
multiline comment-->more text""",
            """\
<p>text</p>
<p>more text</p>""",
        ),
        (
            # Multiline beginning inline
            """\
<!---inline comment-->text<!---multiline commment
multiline comment-->
more text""",
            """\
<p>text</p>
<p>more text</p>""",
        ),
        (
            # Multiline ending inline
            """\
<!---multiline comment
multiline comment-->text<!---inline comment-->""",
            "<p>text</p>",
        ),
        (
            # Multiline ending and beginning on same line
            """\
<!---multiline comment
multiline comment-->text<!---multiline comment
multiline comment-->
more text
""",
            """\
<p>text</p>
<p>more text</p>""",
        ),
        (
            # Comments in HTML
            """\
<pre>
<!--- test --> testing code blocks
    <!--- test --> testing 8 spaces
 <!--- test --> testing 5 spaces
</pre>""",
            """\
<pre>
 testing code blocks
 testing 8 spaces
 testing 5 spaces
</pre>""",
        ),
    ],
)
def test_mkdcomments(md_input, expected, markdowner):
    assert textwrap.dedent(markdowner.convert(md_input)) == textwrap.dedent(expected)
