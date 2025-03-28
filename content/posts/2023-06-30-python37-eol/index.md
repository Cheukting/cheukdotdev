---
layout: posts
title: "What does Python 3.7 End-of-life mean?"
date: 2023-06-30
description: "You have probably seen everyone has been talking about the end-of-life of Python 3.7 recently. Do you know what does it mean? What happened if you are still using Python 3.7?"
image: /assets/images/andy-holmes-zUor3ZmVbss-unsplash.jpg
author: Cheuk Ting Ho
tags:
  - Python

---

You have probably seen everyone has been talking about the end-of-life of Python 3.7 recently. Do you know what does it mean? What happened if you are still using Python 3.7?

## What does it mean?

According to [the status of Python versions](https://devguide.python.org/versions/), each Python version will have a "lifespan" of its own. From its "birth" - when it got released, to when it will stop getting bug fixes and when we get to the stage that there will no longer be any security bug fixes, that version of Python is considered "dead".

Is it a good idea to upgrade to using more modern Python versions? Absolutely yes! It is never a good idea to use a piece of software that will not receive security fixes - it carries potential risks, if there is a vulnerability found, it will not be fixed and baddies will be able to exploit that vulnerability and potentially do you harm.

## Why can't Python 3.x be maintained for ever?

It is very common that software will have a life cycle like Python does. As the number of engineers and resources is limited. It is simply impossible to maintain a piece of software forever. It is even more so for open-source projects when the software is maintained mostly by volunteers. It is better to put resources to improve Python and maintain newer versions of it. That's why each Python version will have its life cycle.

It is also easier for library maintainer to also maintain their library similarly, supporting only a set of newer versions of the libraries and newer versions of the releases will no longer support old, especially end-of-life versions of Python. In this case, it is possible to publish new features if it does not need to be compatible with Python versions that are very old and are quite different from the newest version.

## How I am affected?

You will probably need to make sure that all your projects are compatible with Python 3.8+ - time to upgrade old and dusty projects, show them some love or make the hard decision to achieve them.

After upgrading to Python 3.7, check if your dependencies are also upgraded. There are also popular Python libraries, or frameworks that will stop supporting Python 3.7. It will happen again in 3.8 in a year and so on, so it is always a good idea to keep up to date. Ideally, you should be using Python 3.11 right now and is ready to move on to Python 3.12 once it is released.

There is also a good thing about the Python 3.7 end-of-life, you can now stop testing again Python 3.7 in your CI/CD pipeline. And now you can also use the following cool features that are introduced in Python 3.8 without worrying about breaking backward compatibility.

## What are the coolest features in Python 3.8?

Take this session with a grain of salt! It is my personal opinion! Python 3.8 has been out for a while so everyone will have their own opinion. Here are my top 3 features:

#### Walrus operator

This is a very controversial one when it came out! However, now people are starting to get more and more used to it and now after Ptyhon 3.7 is retired you will see them more often. In my opinion,  the most useful way to use it when we have a while loop like this:

```Python
while content := fetch_from_source(url) is not None:
    do_somthing_with_it(content)
```

compare it to the older version which will be:

```Python
content = fetch_from_source(url)
while content is not None:
    do_somthing_with_it(content)
    content = fetch_from_source(url)
```

we do not have to write the same line `content = fetch_from_source(url)` twice and can keep things consistent easily.

#### Enforced positional argument

Now you can enforce arguments to be positional only:

```Python
def my_func(arg1, /, arg2):
    do_something(arg1, arg2)
```

Here you can only call `my_func(1, 2)` or `my_func(1, arg2=2)` but not `my_func(arg1=1, arg2=2)` anymore.

I can imagine this will affect how we use our favourite libraries in the future. As more and more libraries will use enforced positional arguments. Time to double-check their documentation if you are not sure if certain arguments are positional only.

#### Using = in f-strings

f-string was introduced in Python 3.6 and it was a game changer in how we print things. It has been more powerful and convenient over time. In Python 3.8, you can now use `=` in f-strings like `f"Account info: {user_name=}"` and it will print out something like "Account info: user_name=user1". It is extremely useful for debugging and error messages.

---

To know more about what's introduced in Python 3.8, you can check out [this page at the official documentation](https://docs.python.org/3/whatsnew/3.8.html).


## What if my work is still using Python 3.7?

As I said, it is crucial and beneficial to be using an updated version of Python. I understand that sometimes there are reasons Python 3.7 is still needed.

If it is for compatibility of a certain piece of software. Look for if a newer version of that piece of software is available. If it is a commercial piece of software, contact the publisher to ask for an update. If it is an open-source piece of software, report the issue and see what you can do to help. I am happily offering my help to any open-source project that may need help in updating the dependencies and removing Python 3.7 from their dependencies (I cannot promise I can solve your problem 100% but I will try)

If you are required to use Python 3.7 internally, mention the potential concern to the decision makers and explain the importance, like for security reasons, to upgrade to a newer version of Python.

---

I hope you found this blog post useful If you have any comments, feel free to get in touch with me on social media and I am happy to chat.  

---

Cover Photo by <a href="https://unsplash.com/@andyjh07?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Andy Holmes</a> on <a href="https://unsplash.com/photos/zUor3ZmVbss?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText">Unsplash</a>
