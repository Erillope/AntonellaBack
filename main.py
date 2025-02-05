from core.user.domain import UserAccountFactory, UserAccount
from core.user.domain import AccountStatus
import random
from datetime import date, timedelta

start_date = date(date.today().year - 100, date.today().month, date.today().day)
end_date = date(date.today().year - 3, date.today().month, date.today().day)
delta = end_date - start_date
print([start_date - timedelta(days=random.randint(0, delta.days)) for _ in range(10)] + [end_date + timedelta(days=random.randint(0, delta.days)) for _ in range(10)])