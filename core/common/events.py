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
    
    @classmethod
    def subscribe(cls, subscriber: EventSubscriber) -> None:
        cls.subscribers.append(subscriber)
    
    @classmethod  
    def publish(cls, event: Event) -> None:
        for subscriber in cls.subscribers:
            subscriber.handle(event)