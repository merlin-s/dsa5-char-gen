from globals import *


class RelOp:
    db = None

    @classmethod
    def fromDB(cls, key):
        return cls.db.get(key)

    def op(self, lhs, rhs):
        pass


class LessType(RelOp):
    def op(self, lhs, rhs):
        return lhs < rhs


class LessEqType(RelOp):
    def op(self, lhs, rhs):
        return lhs <= rhs


class EqType(RelOp):
    def op(self, lhs, rhs):
        return lhs == rhs


class NotEqType(RelOp):
    def op(self, lhs, rhs):
        return lhs != rhs


class GreaterType(RelOp):
    def op(self, lhs, rhs):
        return lhs > rhs


class GreaterEqType(RelOp):
    def op(self, lhs, rhs):
        return lhs >= rhs

Less = LessType()
LessEq = LessEqType()
Eq = EqType()
NotEq = NotEqType()
Greater = GreaterType()
GreaterEq = GreaterEqType()

RelOp.db = dict(
    Less=Less,
    LessEq=LessEq,
    Eq=Eq,
    NotEq=NotEq,
    Greater=Greater,
    GreaterEq=GreaterEq,
)