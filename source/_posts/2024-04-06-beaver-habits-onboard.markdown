---
title: Beaver Habit Tracker Onboard
date: 2024-04-06 12:27:50
tags:
---

When switching from Android to iOS, I was unable to find a light-weighted but handy habit tracking app, so I decided to make one by myself :)

For the name of the project, it came from a game called "[Against the Storm](https://store.steampowered.com/app/1336490/Against_the_Storm/)" (which I spent over 100 hours, highly recommended). In the game, my favorite city builder species is **beaver**, hoping this web app works as a beaver to save ur precious moments in your fleeting life.

<!--more--> 

GitHub: https://github.com/daya0576/beaverhabits/
Demo: https://beaverhabits.com/demo/
![40740423-A4AB-4806-9A6A-6F1B896FC8AE_1_201_a](../images/blog/2021-09-04-jvm-note/40740423-A4AB-4806-9A6A-6F1B896FC8AE_1_201_a.jpeg)


# Tech stacks
Inspired the idea of "web UIs with plain Python" from [Three Python trends in 2023](https://blog.jerrycodes.com/python-trends-in-2023/), finally chose NiceGUI as the full-stack framework (based on [Quasar](https://quasar.dev/), [Tailwind CSS](https://tailwindcss.com/), [FastAPI](https://fastapi.tiangolo.com/), ...). 

So this web app is 100% built with Python <3 

Some thoughts after several weeks development:

1. Good things ✅
    - WebSocket based communication between client and server, works perfectly with Python asyncio.
    - Light-weighted session based storage provided, out of the box to use.
    - Plenty of UI components provided, straightforward and highly customizable.
    - ...
2. Worries 🤔
    - "NiceGUI follows a backend-first philosophy: It handles all the web development details" -> high network latency would be a big issue.
    - ...

## Persistent Storage
As mentioned above, NiceGUI handles everything in server side, high network latency would destroy user experiences.

Some solutions:
1. Global CDN:  Utilizing a global CDN helps mitigate network latency by distributing content across multiple edge servers located strategically worldwide.
2. Self-host option: Providing a self-host option allows users to host the NiceGUI application on their own infrastructure or servers.
3. ...

In order to provide flexible backend storage options, [interfaces](https://github.com/daya0576/beaverhabits/blob/master/beaverhabits/storage/storage.py) were defined with various implementations, e.g. session-based file or user-based file/database.

BTW, the code below leverages the latest features of Python 3.12: [PEP 695: Type Parameter Syntax](https://docs.python.org/3/whatsnew/3.12.html#pep-695-type-parameter-syntax)

```python
class CheckedRecord(Protocol):
    @property
    def day(self) -> datetime.date: ...

    @property
    def done(self) -> bool: ...

    @done.setter
    def done(self, value: bool) -> None: ...

    def __str__(self):
        return f"{self.day} {'[x]' if self.done else '[ ]'}"

    __repr__ = __str__


class Habit[R: CheckedRecord](Protocol):
    @property
    def name(self) -> str: ...

    @name.setter
    def name(self, value: str) -> None: ...

    @property
    def priority(self) -> int: ...

    @priority.setter
    def priority(self, value: int) -> None: ...

    @property
    def records(self) -> List[R]: ...

    def get_records_by_days(self, days: List[datetime.date]) -> List[R]: ...

    async def tick(self, record: R) -> None: ...

    def __str__(self):
        return self.name

    __repr__ = __str__
```

# Future..
1. Pages:
    - [x] Index page
    - [x] Habit list page
    - [ ] Habit detail page, e.g. records over years
2. Storage:
    - [ ] Session-based file storage
    - [ ] User-based file storage
    - [ ] User-based sqlite storage
3. CICD:
    - [x] Custom domain
    - [ ] Global CDN
    - [ ] Self-hosting support
    - [ ] Unit tests & deployment pipeline
4. Others:
    - [ ] Export & Import
    - [x] User management
    - [ ] User timezone



