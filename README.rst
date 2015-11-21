eduxator
========

Interactive command line interface for `Edux <https://edux.fit.cvut.cz/>`_ classification. 
This is only useful for teachers from `Faculty of Information Technology at Czech Technical University in Prague <http://fit.cvut.cz/en>`_.

Currently, eduxator is in pre-alpha state and **does not work yet**.

The idea
--------

*Here I try to explain what eduxator will do. I'll use present tense so it will be easier in the future to keep the text here.*

Eduxator is a command line tool with interactive console. It's purpose is to give points to students and save those points to Edux. In order to tell eduxator what kind of points are you about to give, you should provide some kind of information, such as:

- course name (e.g. BI-3DT, BI-SAP...)
- what kind of students are we dealing with (e.g. fulltime, parttime)
- what kind of class is happening (e.g. tutorials, labs, lectures, exams)
- what identifier does current class have (e.g. 1, 101...)
- what column in the classification chart are you going to fill this time (such as cv01, tut8...)

You can provide that information as command line arguments and eduxator will try to parse all of it's arguments and determine what to do with them. In case you omit some kind, eduxator will ask you interactively or select the only option available (for example when you only have fulltime students in your course, you don't have to specify it). The following command would be perfect::

    eduxator BI-3DT 3 cv1

Note that BI-3DT has only fulltime tutorials, so this information is omitted without any harm. Order of the arguments is not important, eduxator will first look for any valid course identifier, then fulltime/parttime etc. In case there are multiple arguments that fit as something, you'll be ask interactively. You can just omit everything and let eduxator ask you what you need::

    $ eduxator
    Cannot see Edux cookie in ~./.edux.cookie
    Please provide the name and value of your cookie from Edux. The one where name
    looks like it's random generated is the one. Enter the cookie's name:
    > oihgYftudy654hvkgjgdbytuTGB
    Cookie's value:
    > jkf67HJFKHtg%hh@hjGK67FghjHggqwerty
    Good, I feel your anger. Should I save this to ~./.edux.cookie to save you
    some pain later? (Y/n):
    > y
    What course do you want (use tab to help yourself):
    > B[tab]
    > BI-
    > BI-3[tab]
    > BI-3DT
    What is the identifier for this tutorial (1, 2, 3):
    > 3
    What column you want to edit (use tab to help yourself):
    > [tab]
    > cv
    > cv[tab]
    cv1 cv2 cv3 cv4 cv5 cv8 cv9 cv10 cv11
    > cv1
    All set up. Hint: Use the following command to start eduxator using the same setup:
        eduxator BI-3DT 3 cv1
    You are ready to give points. Type student's username (tab works again) 
    to know what number of points she has. Follow the username by N or +N
    or -N to set points. Type help to see other commands.
    > hr[tab]
    > hroncmir
    hroncmir: (unset)
    > hroncmir +1
    hroncmir: 1
    > hroncmir +1.5
    hroncmir: 2.5
    > hroncmir 1
    hroncmir 1
    > undo
    hroncmir 2.5
    > hroncmir +1
    hroncmir 3.5
    > hroncmir 0
    hroncmir 0
    > unset hroncmir
    hroncmir: (unset)
    > help
    You can use the following commands: undo, unset, stats, info, points, bye, exit.
    Use help <command> to get more info.
    > [Ctrl+D]

Each time, before you add, subtract or change points, the real value form Edux is obtained, so multiple teachers should be able to use eduxator in parallel. However, the ``undo`` feature sets the value to the last known value before the command was run, so it might be dangerous in parallel environment. Especially if you do several of them or you don't run it immediately after the previous command.