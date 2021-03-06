# clize -- A command-line argument parser for Python
# Copyright (C) 2011-2015 by Yann Kaiser <kaiser.yann@gmail.com>
# See COPYING for details.

from clize import util
from clize.tests import util as testutil


def formatter(**kwargs):
    kwargs.setdefault('max_width', 50)
    return util.Formatter(**kwargs)


@testutil.testfunc
def formatter_tests(self, func, expected_ret):
    f = formatter(max_width=50)
    ret = func(self, f)
    if ret is None:
        ret = f
    self.assertEqual(expected_ret, str(f))


def equal(s):
    def _deco(func):
        return func, s
    return _deco


lorem = (
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam finibus '
    'erat mi, eget accumsan metus.')
slorem = 'Lorem ipsum dolor sit amet'


@formatter_tests
class FormatterTests(object):
    @equal('')
    def empty(self, f):
        pass

    @equal('hello')
    def line(self, f):
        f.append('hello')

    @equal('hello\nworld')
    def lines(self, f):
        f.append('hello')
        f.append('world')

    @equal('hello\n\nworld')
    def paragraph(self, f):
        f.append('hello')
        f.new_paragraph()
        f.append('world')

    @equal('hello\n\nworld')
    def paragraph_dupe(self, f):
        f.append('hello')
        f.new_paragraph()
        f.new_paragraph()
        f.append('world')

    @equal('hello\nworld')
    def extend(self, f):
        f.extend(['hello', 'world'])

    @equal('')
    def extend_empty(self, f):
        f.extend([])

    @equal('hello\n\nworld')
    def extend_ewp(self, f):
        f.append('hello')
        f.new_paragraph()
        f.extend(['', 'world'])

    @equal('hello\nworld')
    def extend_f(self, f):
        f1 = formatter()
        f1.append('hello')
        f1.append('world')
        f.extend(f1)

    @equal('hello\n\nworld')
    def extend_f_newp(self, f):
        f.append('hello')
        f.new_paragraph()
        f1 = formatter()
        f1.new_paragraph()
        f1.append('world')
        f.extend(f1)

    @equal('Lorem ipsum dolor sit amet, consectetur adipiscing\n'
           'elit. Etiam finibus erat mi, eget accumsan metus.')
    def wrap(self, f):
        f.append(lorem)

    @equal('  hello\n  world')
    def indent(self, f):
        with f.indent():
            f.append('hello')
            f.append('world')

    @equal('  hello\nworld')
    def indent_individual(self, f):
        with f.indent():
            f.append('hello')
            f.append('world', indent=-2)

    @equal('  hello\n    world')
    def indent_extend(self, f):
        with f.indent():
            f.append('hello')
            f1 = formatter()
            with f1.indent():
                f1.append('world')
            f.extend(f1)

    @equal('   hello\n   world')
    def indent_custom(self, f):
        with f.indent(3):
            f.append('hello')
            f.append('world')

    @equal('  Lorem ipsum dolor sit amet, consectetur\n'
           '  adipiscing elit. Etiam finibus erat mi, eget\n'
           '  accumsan metus.')
    def indent_wrap(self, f):
        with f.indent():
            f.append(lorem)

    @equal('col1      col2\ncolumn1   column2')
    def columns(self, f):
        with f.columns() as cols:
            cols.append('col1', 'col2')
            cols.append('column1', 'column2')

    @equal('   col1 | col2    |    col3\ncolumn1 | column2 | column3')
    def columns_opts(self, f):
        with f.columns(3, spacing=' | ', align='><>') as cols:
            cols.append('col1', 'col2', 'col3')
            cols.append('column1', 'column2', 'column3')

    @equal('col1      col2\n\nheading\ncolumn1   column2')
    def columns_iterleaved(self, f):
        with f.columns() as cols:
            cols.append('col1', 'col2')
            f.new_paragraph()
            f.append('heading')
            cols.append('column1', 'column2')


    @equal('col1   Lorem ipsum dolor sit amet, consectetur\n'
           '       adipiscing elit. Etiam finibus erat mi,\n'
           '       eget accumsan metus.')
    def columns_wrap_second(self, f):
        with f.columns() as cols:
            cols.append('col1', lorem)
        self.assertEqual([4, 43], cols.widths)

    @equal('Lorem ipsum   Lorem ipsum dolor sit amet,\n'
           'dolor sit     consectetur adipiscing elit. Etiam\n'
           'amet,         finibus erat mi, eget accumsan\n'
           'consectetur   metus.\n'
           'adipiscing\n'
           'elit. Etiam\n'
           'finibus\n'
           'erat mi,\n'
           'eget\n'
           'accumsan\n'
           'metus.')
    def columns_wrap_both(self, f):
        with f.columns(wrap=[True, True]) as cols:
            cols.append(lorem, lorem)
        self.assertEqual(cols.widths, [11, 36])

    @equal('Lorem ipsum dolor sit amet\n'
           '     Lorem ipsum dolor sit amet, consectetur\n'
           '     adipiscing elit. Etiam finibus erat mi, eget\n'
           '     accumsan metus.')
    def columns_nowrap_first(self, f):
        with f.columns() as cols:
            cols.append(slorem, lorem)
        self.assertEqual([2, 45], cols.widths)

    def test_match_lines_no_empty_ends(self):
        f = formatter(max_width=50)
        cols = f.columns()
        cols.widths = [4, 4]
        cols.wrap = [True, False]
        self.assertEqual(
            list(cols.match_lines(['col1', 'word word word'])),
            [['col1', 'word word word']]
            )

    @equal('row1col1 is long\n'
           '       word word word\n'
           'col1   word word word word')
    def columns_nowrap_multiline(self, f):
        with f.columns() as cols:
            cols.append('row1col1 is long', 'word word word')
            cols.append('col1', 'word word word word')
