<div align="center">

![async](https://user-images.githubusercontent.com/30027932/114286121-d4fef400-9a7d-11eb-9e1c-34904ac79aa3.png)


🌿 Exploring different concurrency paradigms in Python

[![Awesome](https://awesome.re/badge-flat.svg)](https://awesome.re)
[![License](https://img.shields.io/cocoapods/l/AFNetworking?style=flat-square)](https://github.com/rednafi/think-asyncio/blob/master/LICENSE)

</div>


<div align="center">

## Description

This repository contains links to some awesome blog posts, books, talks, and docs to get you up and running with Python's asynchronous paradigm. It tries to avoid resources that are outdated or contain deprecated APIs that make the async subspace of Python seem overly complicated, especially for beginners.

</div>


## Concepts & philosophy

* [Sync vs. async Python: what is the difference?](https://blog.miguelgrinberg.com/post/sync-vs-async-python-what-is-the-difference) -> Differences between sync and async Python, and when async is the right tool to solve your concurrency problems

* [Why do we need coroutines in Python?](https://stackoverflow.com/questions/40925797/why-do-we-need-coroutines-in-python)

* [Generators & coroutines - David Beazly](http://www.dabeaz.com/coroutines/Coroutines.pdf) -> This is outdated and uses python 2x but the underlying concept is still relevant


* [Concurrency for people in a hurry - FastAPI doc](https://fastapi.tiangolo.com/async/) -> Simple high-level overview of concurrency in general

* [How the heck does async/await work in Python 3.5?](https://snarky.ca/how-the-heck-does-async-await-work-in-python-3-5/) -> Good intro to async but slightly outdated

* [Unyielding - why threads are bad?](https://glyph.twistedmatrix.com/2014/02/unyielding.html) -> Glyph, the creator of the Twisted projects argues why writing multi-threaded code correctly is hard

* [Nathaniel J. Smith - Notes on structured concurrency, or: go statement considered harmful](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/) -> Nataniel Smith argues that Dijkstra's strurctured programming philosophy can show us the correct way of doing concurrent I/O programming

* [Nathaniel J. Smith - Timeouts and cancellation for humans](https://vorpus.org/blog/timeouts-and-cancellation-for-humans/) -> Nathaniel Smith ponders on the ways timeout and cancellation can be handled across different concurrency primitives

* [Some thoughts on asynchronous API design in a post-async/await world](https://vorpus.org/blog/some-thoughts-on-asynchronous-api-design-in-a-post-asyncawait-world/) -> Conundrums of crafting causality-compliant, coroutine-chauffeured concurrency-contraptions—catering callback compliance

## Asyncio overview

* [AsyncIO in Python: A complete walkthrough](https://realpython.com/async-io-python/) -> Start grasping the bare-minimum concepts from here.

* [Asyncio for the working Python developer](https://yeray.dev/python/asyncio/asyncio-for-the-working-python-developer) -> Getting your hands dirty with the async features.

* [Calling sync from async & vice versa](https://www.aeracode.org/2018/02/19/python-async-simplified/) -> Fantastic article on the gradual adoption of Asyncio.


## Asyncio API

* [Guide to concurrency in Python with asyncio](https://www.integralist.co.uk/posts/python-asyncio/#gather) -> Asyncio's *create_task*, *ensure_future*, *wait*, *wait_for*, *gather* APIs.

* [Waiting in asyncio](https://hynek.me/articles/waiting-in-asyncio/) -> Difference between *gather*, *wait*, *wait_for*, *create_task*, *as_completed*, etc.

* [Latency in asynchronous Python](https://nullprogram.com/blog/2020/05/24/) -> Using *asyncio.Queue(maxsize=1)* to run blocking code.

* [Difference between asyncio gather & wait](https://stackoverflow.com/questions/42231161/asyncio-gather-vs-asyncio-wait#:~:text=gather%20mainly%20focuses%20on%20gathering,just%20waits%20on%20the%20futures.)

* [Differences among asyncio ensure_future, create_task & simple coroutines](https://stackoverflow.com/questions/36342899/asyncio-ensure-future-vs-baseeventloop-create-task-vs-simple-coroutine#:~:text=ensure_future%20is%20a%20method%20to,implement%20this%20function%20different%20ways.)

* [Does asyncio gather guarantees execution & result order?](https://stackoverflow.com/questions/54668701/asyncio-gather-scheduling-order-guarantee#:~:text=Yes%2C%20at%20least%20from%20the,of%20them%20one%20by%20one.)


## Examples

* [Asynchronous I/O examples](https://github.com/rednafi/think-async/tree/master/examples) -> Self contained examples of how to perform a few common asynchronous I/O tasks

* [Asyncio by examples](https://www.pythonsheets.com/notes/python-asyncio.html#) -> A dense example-driven overview of the Asyncio APIs

* [Simple IPv4 TCP scanner leveraging asyncio](https://github.com/rednafi/tcp-port-scanner) -> A complete example of using asynchronous producer-consumer pattern to create a simple TCP scanner


## Books

* [Using asyncio in Python - Caleb Hattingh](https://www.goodreads.com/book/show/50083143-using-asyncio-in-python?ac=1&from_search=true&qid=Ozrygzthcs&rank=3)


## Tutorials

* [Python threading tutorial: Run code concurrently using the 'threading' module](https://www.youtube.com/watch?v=IEEhzQoKtQU) -> Corey Schafer explains how to use the built-in threading module in Python to achieve concurrency

* [Python multiprocessing tutorial: Run code parallelly using the 'multiprocessing' module](https://www.youtube.com/watch?v=fKl2JW_qrso&t=36s) -> Corey Schafer explains how to use the built-in multiprocessing module in Python to achieve parallelism

## Talks

* [Understanding async and await in Python - Jonathan Slenders](https://www.youtube.com/watch?v=a_wWnxH2o0Y) -> A succinct introduction to asyncio in Python.

* [Raymond Hettinger - Keynote on concurrency - PyBay 2017](https://www.youtube.com/watch?v=9zinZmE3Ogk) -> Raymond Rettinger mostly talking about threads, queues, and processes.

* [Robert Smallshire - Coroutine concurrency in Python 3 with asyncio](https://www.youtube.com/watch?v=c5wodlqGK-M&t=2782s) -> Gradually building up the intuition for coroutine driven I/O.

* [David Beazley - Fear and awaiting in async: A savage journey to the heart of the coroutine dream](https://www.youtube.com/watch?v=E-1Y4kSsAFc&list=RDQMFa6jr3zatoc&index=3) -> Reasoning asynchronous programming from first principles.

* [Import asyncio - YouTube series](https://www.youtube.com/watch?v=Xbl7XjFYsN4&t=18s) -> Łukasz Langa's asyncio videos—from basics to application.

* [Yury Selivanov - High performance networking in Python](https://www.youtube.com/watch?v=pi49aiLBas8) -> The talk covers the async/await syntax in Python, asyncio library and ecosystem around it, and ways to use them for creating high performance servers.

* [Yury Selivanov - Async/await in Python 3.5 and why it is awesome](https://www.youtube.com/watch?v=m28fiN9y_r8&t=1s) -> An overview of asyncio's high-level APIs

* [Yury Selivanov - Asyncio: what's next - PyBay2018](https://www.youtube.com/watch?v=vem5GHboRNM) -> Another walkthrough of asyncio APIs and speculations on future improvements.

* [Yury Selivanov - Asyncio in Python 3.7 and 3.8 || A guide to asynchronous programming in Python with asyncio](https://www.youtube.com/watch?v=5ZUXg5uzrGU&t=4s) -> Asyncio's past, present and future.

* [Build your own async - YouTube screencast](https://www.youtube.com/watch?v=Y4Gt3Xjd7G8) -> David Beazley's takes you through building your own asyncio-like library.

* [John Reese - Thinking outside the GIL with asyncio and multiprocessing - PyCon 2018](https://www.youtube.com/watch?v=0kXaLh8Fz3k&t=125s) -> Superpowered asyncio with multiprocessing.

* [Nathaniel J. Smith - Trio: Async concurrency for mere mortals - PyCon 2018](https://www.youtube.com/watch?v=oLkfnc_UMcE&t=76s) -> Structured concurrency with trio.

* [Kavya Joshi - A tale of concurrency through creativity in Python: A deep dive into how gevent works](https://www.youtube.com/watch?v=GunMToxbE0E) -> Implicit cooperative multitasking via Gevent.

* [Understanding the Python GIL](https://www.youtube.com/watch?v=Obt-vMVdM8s&t=33s) -> David Beazly explains the behavior of threads in Python why it yields concurrency rather than parallelism.

* [The other async (threads + async = ❤️)](https://www.youtube.com/watch?v=x1ndXuw7S0s) -> David Beazley builds a thread and async compatible queue from scratch.

* [Łukasz Langa – Thinking in coroutines](https://www.youtube.com/watch?v=cvwrkOnn9xo) -> Understanding event loop, task cancellation, and exception handling in Asyncio.

## Podcasts

* [John Reese - Asyncio all the things with Omnilib](https://talkpython.fm/episodes/show/304/asyncio-all-the-things-with-omnilib) -> Making the fundamental toolsets async in Python.

* [David Beazley - Python concurrency with Curio](https://talkpython.fm/episodes/show/107/python-concurrency-with-curio) -> David Beazley explains the problems with Asyncio and how he built Curio by reasoning from the first principle.

* [Nathaniel Smith - Simplifying Python's async with Trio](https://talkpython.fm/episodes/show/167/simplifying-pythons-async-with-trio) -> Nathaniel Smith talks about why cancellation and exception handling can be difficult in background tasks, and how Trio attempts to solve that.

* [Lukasz Langa - AsyncIO + music, origins of Black, and managing Python releases](https://realpython.com/podcasts/rpp/7/) -> Lukasz Langa talks about analog synthesizers, AsyncIO and the Black code formatter.

## Banters

* [I don't understand asyncio](https://lucumr.pocoo.org/2016/10/30/i-dont-understand-asyncio/) -> Armin Ronacher complains about baffling complexities in the design decisions of the asyncio module.

* [Hackernews discourse - I don't understand asyncio](https://news.ycombinator.com/item?id=12829759) -> People Complaining About the Design Decisions behind the Asyncio API.

* [Reddit discourse - I don't understand asyncio](https://www.reddit.com/r/Python/comments/5a6gmv/i_dont_understand_pythons_asyncio_armin_ronachers/) -> Armin Ronacher's conversation with a Python core developer.

* [I'm not feeling the async pressure](https://lucumr.pocoo.org/2020/1/1/async-pressure/) -> Armin Ronacher points out how Asyncio API overlooks the complexities imposed by backpressure.

* [Hackernews discourse - I'm not feeling the async pressure](https://news.ycombinator.com/item?id=21927427) -> Discussion on whether language implementation should deal with backpressure or not.

* [Hackernews discourse - People comparing Python's coroutine driven concurrency with Golang's actor pattern](https://news.ycombinator.com/item?id=23289563) -> People seems to hate asyncio's Twisted inspired design philosophy in general.

* [Hackernews discourse - The bare minimum asyncio](https://news.ycombinator.com/item?id=17714304) -> One Guy's attempt to cover the entire high-level API surface of asyncio in a single Hackernews comment.

## Reactive programming & microservices

* [Redis Streams Featuring Salvatore Sanfilippo - Redis Labs](https://www.youtube.com/watch?v=qXEyuUxQXZM) -> Introduction to the Redis streams data structure and how can it be used as a safer alternative to Pub-Sub.


## Python enhancement proposals (PEPs)

* [PEP 255 -- Simple generators](https://www.python.org/dev/peps/pep-0255/)
* [PEP 342 -- Coroutines via enhanced generators](https://www.python.org/dev/peps/pep-0342/)
* [PEP 380 -- Syntax for delegating to a subgenerator](https://www.python.org/dev/peps/pep-0380/)
* [PEP 3156 -- Asynchronous i/o support rebooted: the "asyncio" module](https://www.python.org/dev/peps/pep-3156/)
* [PEP 492 -- Coroutines with async and await syntax](https://www.python.org/dev/peps/pep-0492/)
* [PEP 654 -- Exception groups and except*](https://www.python.org/dev/peps/pep-0654/)
