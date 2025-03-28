---
layout: posts
title: "What happened when your CI is stopping you from releasing?"
date: 2021-04-12
description: "What happened when your CI is stopping you from releasing? An adventure novel about releasing your open-source project."
image: /assets/images/CIbroken.png
author: Cheuk Ting Ho
tags:
  - GitHub

---

I have been wanting to share my funny releasing stories during my short 18 months of maintaining the [TerminusDB Python Client](https://github.com/terminusdb/terminusdb-client-python). I love working in open-source, it has always been my dream to work mainly on GitHub and be part of the community. My journey involves some laughter 🤣, some panic attacks 😱 and tears 😢, but mostly, hugs and support 🙌 from my team and my friends in the community.

This story (or stories) I am going to tell you mainly consists of... laughter? With some sprinkles of panics, I would say.

I have encountered the most annoying situation in a release, not once but twice, both of them happened on a Friday (yes, release on Fridays always ends "well"). The situation is, your CI failed. "It was working a few hours ago," I thought (on a side note, I also think that's the best expression to go with "It works on my computer") so I start looking at the build job log, hoping to get it done so I can start enjoying the weekend. But it's not always that straight forward.

## Chapter 1 - A Tasty Mistake

In the first encounter, I was released with my cool colleague Robin, he is the CI god in my team so I am in good hands. We looked at the log, and we found a slightly weird message: `AttributeError: module 'virtualenv.activation.python' has no attribute 'PestythonActivator'` My first reaction, has it been hacked? `PestythonActivator` sounds ... yummy 😋 ... if you ask me.

We of cause, like all good developers do, put the error message online and look for clues, we quickly found a [GitHub issue](https://github.com/pypa/virtualenv/issues/1857) and boi, we are not the only souls that got crushed by a "timely" release of `virtualenv` just a few hours before us. Since the lastest version of `virtualenv` got installed every time we create the CI build job on Travis, it fails even we have done nothing. Of cause we didn't point fingers at other maintainers, they are just as hardworking as us and it's human to make mistakes. We are faced with 2 options, roll back to the previous release or wait for the patch of `virtualenv` to get released. As the devs of `virtualenv` did a lighting fast patch, we have chosen option 2.

Well, it was... fun and tasty! At least, it is very obvious what had happened and the problem gets solved very quickly and everyone was happy. It's not so... smooth in my second encounter of an "impossible" bug.

## Chapter 2 - You see, but you do not observe

This time there's only one challenger, that's right, ME! I think that' i have grown wiser since the last incident that was like 9 months ago so I am all good "Release is not scary, I got this!" I spoke too soon. This time, it's the notorious `ModuleNotFoundError: No module named 'importlib.metadata'`.

First of all, why is it notorious? Because it is caused by the version difference of `Python<=3.7` and `Python>3.7`. From Python 3.8 it has been added to the Python standard library so this error is EVERYWHERE. When I start to search for it, there are a million threads about this error and I cannot pinpoint a single library that I depend on that causes this error.

So, I took a deep breath and think "Sherlock time! 🔍" I try to make sense out of the situation here, I looked at the status of all my GitHub action (yes we have switched from Travis to GitHub Action) build status and discover it was not a problem 2 days ago, it must be a recent release. So I looked through my list of dependencies and find the suspect. `tox` got the most recent release, I thought I hit the jackpot and do what I think makes the most sense: Open an issue then roll back to a previous version.

I was WRONG! The problem persists even when I roll back to the previous version and a friendly GitHuber (I guess is the maintainer of `tox`?) also confirm that it's not a `tox` error, but suggest I look at `pip-tools` instead. I scratch my head "`pip-tools`? I didn't have `pip-tools` in my dependencies..." But I looked anyway, and found that they actually have an even more recent release and there is indeed a patch fixing that bug coming in. Which means that if I tried to release just slightly later I may not discover the bug! (I can say I am lucky 🍀, right?) I found out that I do have `pip-tools` in the dependency list in my `tox` set up (hence the confusion).

I waited and even ask if the release will be on PyPI soon, and you guess what? GitHub action is down! (I said I am lucky! 🍀) Ok, both `pip-tools` and I cannot release anything at that moment so just drink more coffee ☕ and chill I guess.

In the end, GitHub action is back in action and it's a happy ending for everybody. I feel that I have achieved something. When I figured what is broken I was really happy and feel on top of the world. I guess that's how Sherlock Homes feels if he was real?
