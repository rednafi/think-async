<div align="center">

![art](./art.png)

🔰 Contextualizing Python's Asyncio

[![Awesome](https://awesome.re/badge-flat.svg)](https://awesome.re)
[![License](https://img.shields.io/cocoapods/l/AFNetworking?style=flat-square)](https://github.com/rednafi/think-asyncio/blob/master/LICENSE)
[![Twitter](https://img.shields.io/twitter/follow/rednafi?style=flat-square)](https://twitter.com/rednafi)

</div>


<div align="center">

## Description

This repository contains links to some awesome blog posts, books, talks and docs to get you up and running with Python's asynchronous paradigm. It tries to avoid resources that are outdated or contain deprecated APIs that make the async subspace of Python seem overly complicated, especially for the beginners.

</div>

---

## Table of Contents

* [Blogs](#blogs)
    * [Prelude](#prelude)
    * [Overview](#overview)
    * [API](#api)
* [Examples](#examples)
* [Salvation](#salvation)
    * [Concepts](#concepts)
    * [API](#api-1)
* [Books](#books)
* [Talks](#talks)
* [Contributors](#contributors)

---

## Blogs

### Prelude

* [Concurrency for People in a Hurry - FastAPI doc](https://fastapi.tiangolo.com/async/) -> Simple high-level overview of concurrency in general
* [How the Heck Does Async/Await Work in Python 3.5?](https://snarky.ca/how-the-heck-does-async-await-work-in-python-3-5/) -> Good intro to async but slightly outdated


### Overview

* [Async IO in Python: A Complete Walkthrough](https://realpython.com/async-io-python/) -> Start grasping the bare-minimum concepts from here
* [Asyncio for the Working Python Developer](https://yeray.dev/python/asyncio/asyncio-for-the-working-python-developer) -> Getting your hands dirty with the async features
* [Calling Sync from Async & Vice Versa](https://www.aeracode.org/2018/02/19/python-async-simplified/) -> Fantastic article on the gradual adoption of asyncio


### API

* [Guide to Concurrency in Python with asyncio](https://www.integralist.co.uk/posts/python-asyncio/#gather) -> Asyncio's *create_task*, *ensure_future*, *wait*, *wait_for*, *gather* APIs
* [Waiting in Asyncio](https://hynek.me/articles/waiting-in-asyncio/) -> Difference between *gather*, *wait*, *wait_for*, *create_task*, *as_completed* etc
* [Latency in Asynchronous Python](https://nullprogram.com/blog/2020/05/24/) -> Using *asyncio.Queue(maxsize=1)* to run blocking code


## Examples

* [Asyncio by examples](https://www.pythonsheets.com/notes/python-asyncio.html#) -> A dense example driven overview of the asyncio APIs


## Salvation

### Concepts

* [Why do we need coroutines in Python?](https://stackoverflow.com/questions/40925797/why-do-we-need-coroutines-in-python)
* [Generators & Coroutines - David Beazly](http://www.dabeaz.com/coroutines/Coroutines.pdf) -> This is outdated and uses python 2x but the underlying concept is still relevant

### API

* [Difference between asyncio gather & wait](https://stackoverflow.com/questions/42231161/asyncio-gather-vs-asyncio-wait#:~:text=gather%20mainly%20focuses%20on%20gathering,just%20waits%20on%20the%20futures.)
* [Difference among asyncio ensure_future, create_task & simple coroutines](https://stackoverflow.com/questions/36342899/asyncio-ensure-future-vs-baseeventloop-create-task-vs-simple-coroutine#:~:text=ensure_future%20is%20a%20method%20to,implement%20this%20function%20different%20ways.)
* [Does asyncio gather guarantees execution & result order?](https://stackoverflow.com/questions/54668701/asyncio-gather-scheduling-order-guarantee#:~:text=Yes%2C%20at%20least%20from%20the,of%20them%20one%20by%20one.)


## Books

* [Using Asyncio in Python - Caleb Hattingh](https://www.goodreads.com/book/show/50083143-using-asyncio-in-python?ac=1&from_search=true&qid=Ozrygzthcs&rank=3)


## Talks


## Contributors

[![](https://sourcerer.io/fame/rednafi/rednafi/thinking-asyncio/images/0)](https://sourcerer.io/fame/rednafi/rednafi/thinking-asyncio/links/0)[![](https://sourcerer.io/fame/rednafi/rednafi/thinking-asyncio/images/1)](https://sourcerer.io/fame/rednafi/rednafi/thinking-asyncio/links/1)[![](https://sourcerer.io/fame/rednafi/rednafi/thinking-asyncio/images/2)](https://sourcerer.io/fame/rednafi/rednafi/thinking-asyncio/links/2)[![](https://sourcerer.io/fame/rednafi/rednafi/thinking-asyncio/images/3)](https://sourcerer.io/fame/rednafi/rednafi/thinking-asyncio/links/3)[![](https://sourcerer.io/fame/rednafi/rednafi/thinking-asyncio/images/4)](https://sourcerer.io/fame/rednafi/rednafi/thinking-asyncio/links/4)[![](https://sourcerer.io/fame/rednafi/rednafi/thinking-asyncio/images/5)](https://sourcerer.io/fame/rednafi/rednafi/thinking-asyncio/links/5)[![](https://sourcerer.io/fame/rednafi/rednafi/thinking-asyncio/images/6)](https://sourcerer.io/fame/rednafi/rednafi/thinking-asyncio/links/6)[![](https://sourcerer.io/fame/rednafi/rednafi/thinking-asyncio/images/7)](https://sourcerer.io/fame/rednafi/rednafi/thinking-asyncio/links/7)
