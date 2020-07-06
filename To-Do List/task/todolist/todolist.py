from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker

from datetime import date, datetime, timedelta
from typing import Any, Callable, Dict, List, Tuple, Iterator

engine = create_engine('sqlite:///todo.db?'
                       'check_same_thread=False')
session = sessionmaker(bind=engine)()
Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"id='{self.id}', "
            f"task={self.task}, "
            f"deadline={self.deadline})>"
        )


Base.metadata.create_all(engine)

Choice = Tuple[str, Callable[..., Any]]
MenuOptions = Dict[str, Choice]


class TodoList:
    def __init__(self, session) -> None:
        self.session = session
        self.run = True
        # has to be date as all stored values are date type
        self.today = datetime.today().date()
        self.menu: MenuOptions = {
            "1": ("Today's tasks", self.get_today_tasks),
            "2": ("Week's tasks", self.get_week_tasks),
            "3": ("All tasks", self.get_all_tasks),
            "4": ("Missed tasks", self.get_missed_tasks),
            "5": ("Add task", self.add_task),
            "6": ("Delete task", self.delete_task),
            "0": ("Exit", self.exit),
        }

    @staticmethod
    def get_user_choice(menu: MenuOptions) -> Choice:
        print(*(f'{num}) {item[0]}' for num, item in menu.items()), sep='\n')
        user_choice = input()
        while user_choice not in menu.keys():
            user_choice = input()
        return menu[user_choice]

    @staticmethod
    def _print_tasks(tasks: Iterator['Task'], verbose: bool = False) -> None:
        if tasks:
            for num, task in enumerate(tasks, start=1):
                print(f'{num}. {task.task}'
                      f'{task.deadline.strftime("%d %b") if verbose else ""}'
                      )
        else:
            print('Nothing to do!')
        print()

    def get_today_tasks(self) -> None:
        tasks: List['Task'] = (
            self.session.query(Task)
                .filter(Task.deadline == self.today)
                .all()
        )
        day_month = self.today.strftime('%d %m')
        print(f'Today {day_month}:')
        self._print_tasks(tasks)

    def get_week_tasks(self) -> None:
        # week_date duration is 6 days after today
        week_date: date = self.today + timedelta(7)
        tasks: List['Task'] = (
            self.session.query(Task)
                .filter(Task.deadline.between(self.today, week_date))
                .order_by(Task.deadline)
                .all()
        )
        date_range = [self.today + timedelta(x) for x in range((week_date-self.today).days)]
        for today_date in date_range:
            dow_day_mon: str = today_date.strftime('%A %d %b')
            print(f'\n{dow_day_mon}:')
            # generator comprehension filter out current date
            # prev implementation used pop, more efficient if smaller date_range but less clean
            self._print_tasks((task for task in tasks if task.deadline == today_date))

    def get_all_tasks(self) -> List['Task']:
        tasks: List['Task'] = (
            self.session.query(Task)
                .filter(Task.deadline >= self.today)
                .order_by(Task.deadline)
                .all()
        )
        print('All tasks:')
        self._print_tasks(tasks, verbose=True)
        return tasks

    def get_missed_tasks(self):
        tasks: List['Task'] = (
            self.session.query(Task)
                .filter(Task.deadline < self.today)
                .order_by(Task.deadline)
                .all()
        )
        print("Missed tasks:")
        self._print_tasks(tasks, verbose=True)

    def add_task(self) -> None:
        task: str = input('Enter task')
        deadline: str = input('Enter deadline')
        new_row: 'Task' = Task(task=task, deadline=date.fromisoformat(deadline))

        self.session.add(new_row)
        self.session.commit()
        print('The task has been added!')

    def delete_task(self):
        print('Chose the number of the task you want to delete:')
        tasks = self.get_all_tasks()
        num_delete: int = int(input())
        item: 'Task' = tasks[num_delete-1]

        self.session.delete(item)
        self.session.commit()

    def exit(self) -> None:
        print('Bye!')
        self.run = False
        self.session.close()

    def run_todo(self) -> None:
        while self.run:
            choice: Choice = self.get_user_choice(self.menu)
            print()
            choice[1]()


todo = TodoList(session)
todo.run_todo()
