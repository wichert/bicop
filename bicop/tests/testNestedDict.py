import operator
from unittest import TestCase
from bicop.nestdict import NestedDict

class NestedDictTests(TestCase):
    def testEmptyConstructor(self):
        n=NestedDict()
        self.assertEqual(n.keys(), [])

    def testFlatCopyConstructor(self):
        n=NestedDict(dict(one="one"))
        self.assertEqual(n.items(), [("one", "one")])

    def testNestedCopyConstructor(self):
        n=NestedDict(dict(one=dict(two="two")))
        self.assertEqual(n.items(), [("one", dict(two="two"))])

    def testDirectGetItem(self):
        n=NestedDict(dict(one="one"))
        self.assertEqual(n["one"], "one")

    def testDeepDirectGetItem(self):
        n=NestedDict(dict(one=dict(two="two")))
        self.assertEqual(n["one"]["two"], "two")

    def testDeepSmartGetItem(self):
        n=NestedDict(dict(one=dict(two="two")))
        self.assertEqual(n["one/two"], "two")

    def testDeepSmartGetItemWithDifferentSeparator(self):
        n=NestedDict(dict(one=dict(two="two")), separator=":")
        self.assertEqual(n["one:two"], "two")

    def testGetItemReturnsNestedDict(self):
        n=NestedDict(dict(one=dict(two="two")))
        self.failUnless(isinstance(n["one"], NestedDict))

    def testDirectHasKey(self):
        n=NestedDict(dict(one=dict(two="two")))
        self.failUnless(n.has_key("one"))

    def testDeepHasKey(self):
        n=NestedDict(dict(one=dict(two="two")))
        self.failUnless(n.has_key("one/two"))
        self.failUnless(not n.has_key("one/one"))

    def testDeepHasKeyWithDifferentSeparator(self):
        n=NestedDict(dict(one=dict(two="two")), separator=":")
        self.failUnless(n.has_key("one:two"))
        self.failUnless(not n.has_key("one:one"))

    def testDirectDelItem(self):
        n=NestedDict(dict(one=dict(two="two")))
        del n["one"]
        self.assertEqual(n.keys(), [])

    def testRemoveShallowMissingItem(self):
        n=NestedDict(dict(one=dict(two="two")))
        self.assertRaises(KeyError, operator.__delitem__, n, "two/three")

    def testRemoveDeepMissingItem(self):
        n=NestedDict(dict(one=dict(two="two")))
        self.assertRaises(KeyError, operator.__delitem__, n, "one/three")

    def testDeepDelItem(self):
        n=NestedDict(dict(one=dict(two="two")))
        del n["one"]["two"]
        self.assertEqual(n.keys(), ["one"])
        self.assertEqual(n["one"].keys(), [])

    def testSmartDeepDelItem(self):
        n=NestedDict(dict(one=dict(two="two")))
        del n["one/two"]
        self.assertEqual(n.keys(), ["one"])
        self.assertEqual(n["one"].keys(), [])

    def testSmartDeepDelItemWithDifferentSeparator(self):
        n=NestedDict(dict(one=dict(two="two")), separator=":")
        del n["one:two"]
        self.assertEqual(n.keys(), ["one"])
        self.assertEqual(n["one"].keys(), [])

    def testSetItem(self):
        n=NestedDict()
        n["one"]=1
        self.assertEqual(n["one"], 1)

    def testSetDeepItem(self):
        n=NestedDict()
        n["one/two"]=1
        self.assertEqual(n["one"]["two"], 1)

    def testSetDeepItemWithDifferentSeperator(self):
        n=NestedDict(separator=":")
        n["one:two"]=1
        self.assertEqual(n["one"]["two"], 1)
