.. _faq:

FAQ
===

There are a number of questions that repeatedly need to be answered.
The following document tries to answer some of them.



Technical FAQ
-------------

Fatal Python error: (pygame parachute) Segmentation Fault
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Most of time, this issue is due to the usage of old graphics drivers. Install the
latest graphics driver available for your graphics card, and it should be ok.

If not, this means you have probably triggered some OpenGL code without an
available OpenGL context. If you are loading images, atlases, using graphics
instructions, you must spawn a Window first::

    # method 1 (preferred)
    from kivy.base import EventLoop
    EventLoop.ensure_window()

    # method 2
    from kivy.core.window import Window

If not, please report a detailed issue on github by following the instructions
in the :ref:`reporting_issues` section of the :doc:`contribute` documentation.
This is very important for us because that kind of error can be very hard
to debug. Give us all the information you can give about your environment and
execution.


undefined symbol: glGenerateMipmap
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You graphics card or its drivers might be too old. Update your graphics drivers to the
latest available version and retry.

ImportError: No module named event
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you use Kivy from our development version, you must compile it before
using it. In the kivy directory, do::

    make force

Pip installation failed
~~~~~~~~~~~~~~~~~~~~~~~

Installing Kivy using Pip is not currently supported. Because Pip forces the
usage of setuptools, setuptools hacks build_ext to use pyrex for generating .c,
meaning there is no clean solution to hack against both weird behaviors to use
Cython. (Reference: http://mail.scipy.org/pipermail/nipy-devel/2011-March/005709.html)

Solution: use `easy_install`, as our documentation said.

.. _gstreamer-compatibility:

GStreamer compatibility
~~~~~~~~~~~~~~~~~~~~~~~

Starting from 1.8.0 version, Kivy now use by default the Gi bindings, on the
platforms that have Gi. We are still in a transition, as Gstreamer 0.10 is now
unmaintained by the Gstreamer team. But 1.0 is not accessible with Python
everywhere. Here is the compatibility table you can use.

    ================= ======== ====== =========================================
    Gstreamer version Bindings Status Remarks
    ----------------- -------- ------ -----------------------------------------
    0.10              pygst    Works  Lot of issues remain with 0.10
    0.10              gi       Buggy  Internal issues with pygobject, and video
                                      doesn't play.
    1.0               pygst    -      No pygst bindings exists for 1.0
    1.0               gi       Works* Linux: works
                                      OSX: works with brew
                                      Windows: No python bindings available
    ================= ======== ====== =========================================

Also, we have no reliable way to check if you have 1.0 installed on your
system. Trying to import gi, and then pygst, will fail.

So currently:

- if you are on Windows: stay on Gstreamer 0.10 with pygst.
- if you are on OSX/Linux: install Gstreamer 1.0.x
- if you are on OSX/Linux and doesn't want to install 1.0:
  `export KIVY_VIDEO=pygst`

If you are on OSX, Brew now have `pygobject3`. You must install it, and
re-install gstreamer with introspection options::

    $ brew install pygobject3
    $ brew install gstreamer --with-gobject-introspection
    $ brew install gst-plugins-base --with-gobject-introspection
    $ brew install gst-plugins-good --with-gobject-introspection
    $ brew install gst-plugins-bad --with-gobject-introspection
    $ brew install gst-plugins-ugly --with-gobject-introspection

    # then add the gi into your PYTHONPATH (as they don't do it for you)
    $ export PYTHONPATH=$PYTHONPATH:/usr/local/opt/pygobject3/lib/python2.7/site-packages

    # test it
    $ python -c 'import gi; from gi.repository import Gst; print Gst.version()'
    (1L, 2L, 1L, 0L)


Android FAQ
-----------

could not extract public data
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This error message can occur under various circumstances. Ensure that:

* you have a phone with an sdcard
* you are not currently in "USB Mass Storage" mode
* you have permissions to write to the sdcard

In the case of the "USB Mass Storage" mode error, and if you don't want to keep
unplugging the device, set the usb option to Power.

Crash on touch interaction on Android 2.3.x
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There have been reports of crashes on Adreno 200/205 based devices.
Apps otherwise run fine but crash when interacted with/through the screen.

These reports also mentioned the issue being resolved when moving to an ICS or
higher rom.

Is it possible to have a kiosk app on android 3.0 ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Thomas Hansen have wrote a detailed answer on the kivy-users mailing list:

    https://groups.google.com/d/msg/kivy-users/QKoCekAR1c0/yV-85Y_iAwoJ

Basically, you need to root the device, remove the SystemUI package, add some
lines to the xml configuration, and you're done.

What's the difference between python-for-android from Kivy and SL4A?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Despite having the same name, Kivy's python-for-android is not related to the 
python-for-android project from SL4A, Py4A, or android-python27. They are 
distinctly different projects with different goals. You may be able to use 
Py4A with Kivy, but no code or effort has been made to do so. The Kivy team 
feels that our python-for-android is the best solution for us going forward, 
and attempts to integrate with and support Py4A is not a good use of our time.


Project FAQ
-----------

Why do you use Python? Isn't it slow?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let us try to give a thorough answer; please bear with us.

Python is a very agile language that allows you to do many things
in a (by comparison) short time.
For many development scenarios, we strongly prefer writing our
application quickly in a high-level language such as Python, testing
it, then optionally optimizing it.

But what about speed?
If you compare execution speeds of implementations for a certain set of
algorithms (esp. number crunching) you will find that Python is a lot
slower than say, C++.
Now you may be even more convinced that it's not a good idea in our
case to use Python. Drawing sophisticated graphics (and we are
not talking about your grandmother's OpenGL here) is computationally
quite expensive and given that we often want to do that for rich user
experiences, that would be a fair argument.
**But**, in virtually every case your application ends up spending
most of the time (by far) executing the same part of the code.
In Kivy, for example, these parts are event dispatching and graphics
drawing. Now Python allows you to do something to make these parts
much faster.

By using Cython, you can compile your code down to the C level,
and from there your usual C compiler optimizes things. This is
a pretty pain free process and if you add some hints to your
code, the result becomes even faster. We are talking about a speed up
in performance by a factor of anything between 1x and up to more
than 1000x (greatly depends on your code). In Kivy, we did this for
you and implemented the portions of our code, where efficiency really
is critical, on the C level.

For graphics drawing, we also leverage today's GPUs which are, for
some tasks such as graphics rasterization, much more efficent than a
CPU. Kivy does as much as is reasonable on the GPU to maximize
performance. If you use our Canvas API to do the drawing, there is
even a compiler that we invented which optimizes your drawing code
automatically. If you keep your drawing mostly on the GPU,
much of your program's execution speed is not determined by the
programming language used, but by the graphics hardware you throw at
it.

We believe that these (and other) optimizations that Kivy does for you
already make most applications fast enough by far. Often you will even
want to limit the speed of the application in order not to waste
resources.
But even if this is not sufficient, you still have the option of using
Cython for your own code to *greatly* speed it up.

Trust us when we say that we have given this very careful thought.
We have performed many different benchmarks and come up with some 
clever optimizations to make your application run smoothly.


Does Kivy support Python 3.x?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

No. Not yet. Python 3 is certainly a good thing; However, it broke
backwards compatibility (for good reasons) which means that some
considerable portion of available Python projects do not yet work
with Python 3. This also applies to some of the projects that Kivy
uses as a dependency, which is why we haven't make the switch yet.
We would also need to switch our own codebase to Python 3. We haven't
done that yet because it's not very high on our priority list, but if
somebody doesn't want to wait for us to do it, please go ahead.
Please note, though, that Python 2.x is still the de facto standard.


How is Kivy related to PyMT?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Our developers are professionals and are pretty savvy in their
area of expertise. However, before Kivy came around there was (and
still is) a project named PyMT that was led by our core developers.
We learned a great deal from that project during the time that we
developed it. In the more than two years of research and development
we found many interesting ways to improve the design of our
framework. We have performed numerous benchmarks and as it turns out, 
to achieve the great speed and flexibility that Kivy has, we had to
rewrite quite a big portion of the codebase, making this a
backwards-incompatible but future-proof decision.
Most notable are the performance increases, which are just incredible.
Kivy starts and operates just so much faster, due to these heavy
optimizations.
We also had the opportunity to work with businesses and associations
using PyMT. We were able to test our product on a large diversity of
setups and made PyMT work on all of them. Writing a system such as
Kivy or PyMT is one thing. Making it work under all these different
conditions is another. We have a good background here, and brought our
knowledge to Kivy.

Furthermore, since some of our core developers decided to drop their full-time
jobs and turn to this project completely, it was decided that a more
professional foundation had to be laid. Kivy is that foundation. It is
supposed to be a stable and professional product.
Technically, Kivy is not really a successor to PyMT because there is
no easy migration path between them. However, the goal is the same:
Producing high-quality applications for novel user interfaces.
This is why we encourage everyone to base new projects on Kivy instead
of PyMT.
Active development of PyMT has stalled. Maintenance patches are still
accepted.


Do you accept patches?
~~~~~~~~~~~~~~~~~~~~~~

Yes, we love patches. In order to ensure a smooth integration of your
precious changes however, please make sure to read our contribution
guidelines.
Obviously we don't accept every patch. Your patch has to be consistent
with our styleguide and, more importantly, make sense.
It does make sense to talk to us before you come up with bigger
changes, especially new features.


Does the Kivy project participate in Google's Summer of Code ?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Potential students ask whether we participate in GSoC.
The clear answer is: Indeed. :-)

If you want to participate as a student and want to maximize your
chances of being accepted, start talking to us today and try fixing
some smaller (or larger, if you can ;-) problems to get used to our
workflow. If we know you can work well with us, that'd be a big plus.

Here's a checklist:

* Make sure to read through the website and at least skim the documentation.
* Look at the source code.
* Read our contribution guidelines.
* Pick an idea that you think is interesting from the ideas list (see link
  above) or come up with your own idea.
* Do some research **yourself**. GSoC is not about us teaching you something
  and you getting paid for that. It is about you trying to achieve agreed upon
  goals by yourself with our support. The main driving force in this should be,
  obviously, yourself.  Many students come up and ask what they should
  do. Well, we don't know because we know neither your interests nor your
  skills. Show us you're serious about it and take initiative.
* Write a draft proposal about what you want to do. Include what you understand
  the current state is (very roughly), what you would like to improve and how,
  etc.
* Discuss that proposal with us in a timely manner. Get feedback.
* Be patient! Especially on IRC. We will try to get to you if we're available.
  If not, send an email and just wait. Most questions are already answered in
  the docs or somewhere else and can be found with some research. If your
  questions don't reflect that you've actually thought through what you're
  asking, it might not be well received.

Good luck! :-)

