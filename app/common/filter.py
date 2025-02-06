from .exceptions import InvalidFieldException, MissingOperationException
from core.common import OrdenDirection
from django.db.models import Q, Model #type: ignore
from typing import List, Type, Tuple, Optional

class BinaryExpresion:
    DJANGO_OPERATIONS = {'>': 'gt', '<': 'lt', '=': 'exact'}
    
    def __init__(self, binary_expresion: str) -> None:
        self.expresion = binary_expresion.lower().strip()
        self.tokens = self.get_tokens()
    
    def get_tokens(self) -> Tuple[str, str, str]:
        for opt in self.DJANGO_OPERATIONS:
            if opt in self.expresion:
                return (self.expresion.split(opt)[0], self.expresion.split(opt)[1], opt)
        raise MissingOperationException.missing_operation(list(self.DJANGO_OPERATIONS.keys()))
                        
    def get_operation(self) -> str:
        return self.DJANGO_OPERATIONS[self.tokens[2]]
    
    def get_field(self) -> str:
        return self.tokens[0]
    
    def get_value(self) -> str:
        return self.tokens[1]


class DjangoFilter:    
    def __init__(self, table: Type[Model], binary_expresion: str, limit: Optional[int], offset: Optional[int],
                 order_by: str, direction: OrdenDirection, fields: List[str]) -> None:
        self.fields = fields
        self.q_filter = self.generate_q_filter(binary_expresion)
        self.limit = limit
        self.offset = offset
        self.verify_field(order_by)
        self.order_by = order_by
        self.direction = direction
        self.table = table
        
    def and_(self, binary_expresion: str) -> None:
        self.q_filter &= self.generate_q_filter(binary_expresion)
    
    def or_(self, binary_expresion: str) -> None:
        self.q_filter |= self.generate_q_filter(binary_expresion) 
    
    def generate_q_filter(self, binary_expresion: str) -> Q:
        binary_expresion = binary_expresion.lower().strip()
        if binary_expresion is None or binary_expresion == "":
            return Q()
        expresion = BinaryExpresion(binary_expresion)
        self.verify_field(expresion.get_field())
        lookup = f"{expresion.get_field()}__{expresion.get_operation()}"
        return Q(**{lookup: expresion.get_value()})
    
    def verify_field(self, field: str) -> None:
        if field not in self.fields:
            raise InvalidFieldException.invalid_field(field, self.fields)

    def filter(self) -> List[Model]:
        models = self.table.objects.filter(self.q_filter)
        if self.direction == OrdenDirection.DESC:
            models = models.order_by(f"-{self.order_by}")
        if self.offset is None:
            if self.limit is None:
                return models
            else:
                return models[:self.limit]
        if self.limit is None:
            if self.offset is not None:
                return models[self.offset:]
        return models[self.offset: self.offset+self.__limit]
    
    @classmethod
    def construct_filter(cls, table: Type[Model], expresion: Optional[str], limit: Optional[int],
                         offset: Optional[int], order_by: str, direction: OrdenDirection, fields: List[str]) -> "DjangoFilter":
        if expresion is None or expresion.strip() == "":
            expresion = ""
        expresion = expresion.lower().strip().replace(' ', ',')
        exps = expresion.split(',')
        _filter = cls(table, exps[0], limit, offset, order_by, direction, fields)
        for i in range(1, len(exps)-2, 2):
            if exps[i] == "and":
                _filter.and_(exps[i+1])
            if exps[i] == "or":
                _filter.or_(exps[i+1])
        return _filter