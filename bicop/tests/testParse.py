from unittest import TestCase
from bicop.config import parse
from bicop.config import ParseError


class ParseTests(TestCase):
    def testSingleString(self):
        self.assertEqual(parse('key "value";'), dict(key="value"))

    def testSingleNumber(self):
        self.assertEqual(parse('one 1;'), dict(one=1))

    def testStringList(self):
        self.assertEqual(
                parse('key { "one"; "two"; };'),
                dict(key=["one", "two"]))

    def testNumberList(self):
        self.assertEqual(
                parse('key { 1; 2; };'),
                dict(key=[1, 2]))

    def testCustomDictClass(self):
        class MyDict(dict):
            pass

        result = parse('key { 1; 2; };', dictclass=MyDict)
        self.failUnless(isinstance(result, MyDict))

    def testNestedMap(self):
        self.assertEqual(
                parse('parent { child { key "value"; }; };'),
                dict(parent=dict(child=dict(key="value"))))

    def testMissingSeparatorInList(self):
        try:
            parse('key {1 2};', filename="stdin")
        except ParseError as e:
            self.assertEqual(e.file, "stdin")
            self.assertEqual(e.line, 1)
            self.assertEqual(e.reason, "Required separator missing")
            self.failUnless(str(e), "stdin[1]: Required separator missing")
        else:
            self.fail("ParseError not thrown")

    def testMissingSeparatorInListOnLineTwo(self):
        try:
            parse('key {\n1 2};', filename="stdin")
        except ParseError as e:
            self.assertEqual(e.file, "stdin")
            self.assertEqual(e.line, 2)
            self.assertEqual(e.reason, "Required separator missing")
            self.failUnless(str(e), "stdin[2]: Required separator missing")
        else:
            self.fail("ParseError not thrown")

    def testIllegalValue(self):
        try:
            parse('key {bla};', filename="stdin")
        except ParseError as e:
            self.assertEqual(e.reason, "Illegal value")
        else:
            self.fail("ParseError not thrown")

    def testUnexpectedEndOfFile(self):
        try:
            parse('key ')
        except ParseError as e:
            self.assertEqual(e.reason, "Unexpected end of file")
        else:
            self.fail("ParseError not thrown")

    def testUnexpectedEndOfFileWithoutToken(self):
        try:
            parse('key { "one";')
        except ParseError as e:
            self.assertEqual(e.reason, "Unexpected end of file")
        else:
            self.fail("ParseError not thrown")
