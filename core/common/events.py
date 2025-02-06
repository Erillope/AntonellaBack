from abc import ABC, abstractmethod
from typing import List
from pydantic import BaseModel
from datetime import datetime


class Event(BaseModel, ABC):
    '''Eventos del programa'''
    created_date: datetime = datetime.now()


class EventSubscriber:
    '''Suscriptores de eventos'''    
    @abstractmethod
    def handle(self, event: Event) -> None: ...


class EventPublisher:
    '''Publicador de eventos'''
    subscribers : List[EventSubscriber]= []
    events : List[Event] = []
    
    @classmethod
    def subscribe(cls, subscriber: EventSubscriber) -> None:
        cls.subscribers.append(subscriber)
    
    @classmethod  
    def publish(cls) -> None:
        for event in cls.events:
            for subscriber in cls.subscribers:
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