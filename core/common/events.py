from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Type, List, Tuple
from pydantic import BaseModel
from datetime import datetime

E = TypeVar('E', bound='Event')

class Event(BaseModel, ABC):
    '''Eventos del programa'''
    created_date: datetime = datetime.now()


class EventSubscriber(Generic[E], ABC):
    '''Suscriptores de eventos'''
    SUPPORTED_EVENTS: Tuple[Type[E], ...] = tuple()
    
    @abstractmethod
    def handle(self, event: E) -> None: ...
    
    def support(self, event: E) -> bool:
        for supported_event in self.SUPPORTED_EVENTS:
            if isinstance(event, supported_event):
                return True
        return False


class EventPublisher:
    '''Publicador de eventos'''
    subscribers : List[EventSubscriber[Event]]= []
    events : List[Event] = []
    
    @classmethod
    def subscribe(cls, subscriber: EventSubscriber[Event]) -> None:
        cls.subscribers.append(subscriber)
    
    @classmethod  
    def publish(cls) -> None:
        for event in cls.events:
            for subscriber in cls.subscribers:
                if subscriber.support(event):
                    subscriber.handle(event)
        cls.clear()
    
    @classmethod
    def add_event(cls, event: Event) -> None:
        cls.events.append(event)
    
    @classmethod
    def get_events(cls) -> List[Event]:
        return cls.events

    @classmethod
    def clear(cls) -> None:
        cls.events.clear()