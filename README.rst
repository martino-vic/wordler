solve wordle (https://www.powerlanguage.co.uk/wordle)
=====================================================

A program to support you to solve the wordle puzzles.

installation
------------

::

   $ pip install wordler

alternatively clone or download this repository and run
``python wordler.py`` from the root directory.

usage
-----

Use a pangram like “vogue jacks blitz dwarf nymph” for the first five
guesses. Then run:

.. code:: python

   >>> from wordler import wordler
   >>> wordler.main()

and answer the questions.

dependencies
------------

if you cloned or downloaded this repository, run
``pip install anagram-solver``
(https://github.com/patrickleweryharris/anagram-solver) before you
start.
