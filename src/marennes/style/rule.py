from __future__ import annotations
from collections.abc import Iterator

from . import StyleSheet, Selector, Declaration
from .. import html as H


def rule() -> RuleBuilder:
    return RuleBuilder()


class RuleBuilder:
    def __init__(self, sheet: StyleSheet):
        self.sheet = StyleSheet
        self.selectors = []
        self.declarations = []

    def select(self, selector: Selector) -> RuleBuilder:
        self.selectors.append(selector)
        return self

    def declare(self, declaration: Declaration) -> RuleBuilder:
        self.declarations.append(declaration)
        return self

    def build(self) -> Rule:
        return Rule(selectors=self.selectors, declarations=self.declarations)


class Rule:
    def __init__(self,
                 selectors: Iterator[Selector],
                 declarations: Iterator[Declaration]):
        self.selectors = list(selectors)
        self.declarations = list(declarations)

    def select(self, node: H.Node) -> Iterator[H.Node]:
        already_selected = []
        for selector in self.selectors:
            for selected in filter(lambda s: s not in already_selected, selector(node)):
                already_selected.append(selected)
                yield selected

    def apply(self, node: H.Node):
        for decl in self.declarations:
            decl(node)

    def __call__(self, node: H.Node):
        for node in self.select(node):
            self.apply(node)

