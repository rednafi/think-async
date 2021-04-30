<div align="center">

![async](https://user-images.githubusercontent.com/30027932/114286121-d4fef400-9a7d-11eb-9e1c-34904ac79aa3.png)


🌿 Exploring Different Concurrency Paradigms in Python

[![Awesome](https://awesome.re/badge-flat.svg)](https://awesome.re)
[![License](https://img.shields.io/cocoapods/l/AFNetworking?style=flat-square)](https://github.com/rednafi/think-asyncio/blob/master/LICENSE)

</div>


<div align="center">

## Description

This repository contains links to some awesome blog posts, books, talks, and docs to get you up and running with Python's asynchronous paradigm. It tries to avoid resources that are outdated or contain deprecated APIs that make the async subspace of Python seem overly complicated, especially for beginners.

</div>

## Table of Contents

* [Concepts &amp; Philosophy](#concepts--philosophy)
* [Asyncio Overview](#asyncio-overview)
* [Asyncio API](#asyncio-api)
* [Examples](#examples)
* [Books](#books)
* [Talks](#talks)
* [Podcasts](#podcasts)
* [Banters](#banters)

## Concepts & Philosophy

* [Why do we need coroutines in Python?](https://stackoverflow.com/questions/40925797/why-do-we-need-coroutines-in-python)
* [Generators & Coroutines - David Beazly](http://www.dabeaz.com/coroutines/Coroutines.pdf) -> This is outdated and uses python 2x but the underlying concept is still relevant


* [Concurrency for People in a Hurry - FastAPI doc](https://fastapi.tiangolo.com/async/) -> Simple high-level overview of concurrency in general
* [How the Heck Does Async/Await Work in Python 3.5?](https://snarky.ca/how-the-heck-does-async-await-work-in-python-3-5/) -> Good intro to async but slightly outdated

* [Unyielding - Why Threads Are Bad?](https://glyph.twistedmatrix.com/2014/02/unyielding.html) -> Glyph, the creator of the Twisted projects argues why writing multi-threaded code correctly is hard

## Asyncio Overview

* [Async IO in Python: A Complete Walkthrough](https://realpython.com/async-io-python/) -> Start grasping the bare-minimum concepts from here
* [Asyncio for the Working Python Developer](https://yeray.dev/python/asyncio/asyncio-for-the-working-python-developer) -> Getting your hands dirty with the async features
* [Calling Sync from Async & Vice Versa](https://www.aeracode.org/2018/02/19/python-async-simplified/) -> Fantastic article on the gradual adoption of Asyncio


## Asyncio API

* [Guide to Concurrency in Python with asyncio](https://www.integralist.co.uk/posts/python-asyncio/#gather) -> Asyncio's *create_task*, *ensure_future*, *wait*, *wait_for*, *gather* APIs

* [Waiting in Asyncio](https://hynek.me/articles/waiting-in-asyncio/) -> Difference between *gather*, *wait*, *wait_for*, *create_task*, *as_completed* etc

* [Latency in Asynchronous Python](https://nullprogram.com/blog/2020/05/24/) -> Using *asyncio.Queue(maxsize=1)* to run blocking code

* [Difference Between Asyncio gather & wait](https://stackoverflow.com/questions/42231161/asyncio-gather-vs-asyncio-wait#:~:text=gather%20mainly%20focuses%20on%20gathering,just%20waits%20on%20the%20futures.)

* [Differences Among Asyncio ensure_future, create_task & simple coroutines](https://stackoverflow.com/questions/36342899/asyncio-ensure-future-vs-baseeventloop-create-task-vs-simple-coroutine#:~:text=ensure_future%20is%20a%20method%20to,implement%20this%20function%20different%20ways.)

* [Does Asyncio gather guarantees execution & result order?](https://stackoverflow.com/questions/54668701/asyncio-gather-scheduling-order-guarantee#:~:text=Yes%2C%20at%20least%20from%20the,of%20them%20one%20by%20one.)


## Examples

* [Asyncio by examples](https://www.pythonsheets.com/notes/python-asyncio.html#) -> A dense example-driven overview of the Asyncio APIs

* [Simple IPv4 TCP Scanner Leveraging Asyncio](https://github.com/rednafi/tcp-port-scanner) -> A complete example of using asynchronous producer-consumer pattern to create a simple TCP scanner


## Books

* [Using Asyncio in Python - Caleb Hattingh](https://www.goodreads.com/book/show/50083143-using-asyncio-in-python?ac=1&from_search=true&qid=Ozrygzthcs&rank=3)


## Tutorials

* [Python Threading Tutorial: Run Code Concurrently Using the Threading Module](https://www.youtube.com/watch?v=IEEhzQoKtQU) -> Corey Schafer explains how to use the built-in threading module in Python to achieve concurrency

* [Python Multiprocessing Tutorial: Run Code Parallelly Using the Multiprocessing Module](https://www.youtube.com/watch?v=fKl2JW_qrso&t=36s) -> Corey Schafer explains how to use the built-in multiprocessing module in Python to achieve parallelism

## Talks

* [Raymond Hettinger - Keynote on Concurrency - PyBay 2017](https://www.youtube.com/watch?v=9zinZmE3Ogk) -> Raymond Rettinger mostly talking about threads, queues, and processes

* [Robert Smallshire - Coroutine Concurrency in Python 3 with asyncio](https://www.youtube.com/watch?v=c5wodlqGK-M&t=2782s) -> Gradually building up the intuition for coroutine driven I/O

* [David Beazley - Fear and Awaiting in Async: A Savage Journey to the Heart of the Coroutine Dream](https://www.youtube.com/watch?v=E-1Y4kSsAFc&list=RDQMFa6jr3zatoc&index=3) -> Reasoning asynchronous programming from first principles

* [Import Asyncio - YouTube Series](https://www.youtube.com/watch?v=Xbl7XjFYsN4&t=18s) -> Łukasz Langa's asyncio videos—from basics to application

* [Yury Selivanov - async/await in Python 3.5 and why it is awesome](https://www.youtube.com/watch?v=m28fiN9y_r8&t=1s) -> An overview of asyncio's high-level APIs

* [Yury Selivanov - Asyncio: What's Next - PyBay2018](https://www.youtube.com/watch?v=vem5GHboRNM) -> Another walkthrough of asyncio APIs and speculations on future improvements

* [Build your own Async - YouTube Screencast](https://www.youtube.com/watch?v=Y4Gt3Xjd7G8) -> David Beazley's takes you through building your own asyncio-like library.

* [John Reese - Thinking Outside the GIL with AsyncIO and Multiprocessing - PyCon 2018](https://www.youtube.com/watch?v=0kXaLh8Fz3k&t=125s) -> Superpowered asyncio with multiprocessing

* [Nathaniel J. Smith - Trio: Async Concurrency for Mere Mortals - PyCon 2018](https://www.youtube.com/watch?v=oLkfnc_UMcE&t=76s) -> Structured concurrency with trio

* [Kavya Joshi - A Tale of Concurrency Through Creativity in Python: A Deep Dive Into How Gevent Works](https://www.youtube.com/watch?v=GunMToxbE0E) -> Implicit cooperative multitasking via Gevent

* [Understanding the Python GIL](https://www.youtube.com/watch?v=Obt-vMVdM8s&t=33s) -> David Beazly explains the behavior of threads in Python why it yields concurrency rather than parallelism


* [The Other Async (Threads + Async = ❤️)](https://www.youtube.com/watch?v=x1ndXuw7S0s) -> David Beazley builds a thread and async compatible queue from scratch

## Podcasts

* [John Reese - Asyncio All the Things with Omnilib](https://talkpython.fm/episodes/show/304/asyncio-all-the-things-with-omnilib) -> Making the fundamental toolsets async in Python

* [David Beazley - Python Concurrency with Curio](https://talkpython.fm/episodes/show/107/python-concurrency-with-curio) -> David Beazley explains the problems with Asyncio and how he built Curio by reasoning from the first principle

* [Nathaniel Smith - Simplifying Python's Async with Trio](https://talkpython.fm/episodes/show/167/simplifying-pythons-async-with-trio) -> Nathaniel Smith talks about why cancellation and exception handling can be difficult in background tasks, and how Trio attempts to solve that


## Banters

* [I Don't Understand Asyncio](https://lucumr.pocoo.org/2016/10/30/i-dont-understand-asyncio/) -> Armin Ronacher complains about baffling complexities in the design decisions of the asyncio module

* [Hackernews Discourse - I Don't Understand Asyncio](https://news.ycombinator.com/item?id=12829759) -> People Complaining About the Design Decisions behind the Asyncio API

* [Reddit Discourse - I Don't Understand Asyncio](https://www.reddit.com/r/Python/comments/5a6gmv/i_dont_understand_pythons_asyncio_armin_ronachers/) -> Armin Ronacher's conversation with a Python core developer

* [I'm Not Feeling the Async Pressure](https://lucumr.pocoo.org/2020/1/1/async-pressure/) -> Armin Ronacher points out how Asyncio API overlooks the complexities imposed by backpressure

* [Hackernews Discourse - I'm Not Feeling the Async Pressure](https://news.ycombinator.com/item?id=21927427) -> Discussion on whether language implementation should deal with backpressure or not

* [Hackernews Discourse - People Comparing Python's Coroutine Driven Concurrency with Golang's Actor Pattern](https://news.ycombinator.com/item?id=23289563) -> People seems to hate asyncio's Twisted inspired design philosophy in general

* [Hackernews Discourse - The Bare Minimum Asyncio](https://news.ycombinator.com/item?id=17714304) -> One Guy's attempt to cover the entire high-level API surface of asyncio in a single Hackernews comment
