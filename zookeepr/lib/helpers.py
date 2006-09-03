"""
Helper functions

All names available in this module will be available under the Pylons h object.
"""
from routes import request_config
from webhelpers import *

def counter(*args, **kwargs):
    """Return the next cardinal in a sequence.

    Every time ``counter`` is called, the value returned will be the next
    counting number in that sequence.  This is reset to ``start`` on every
    request, but can also be reset by calling ``reset_counter()``.

    You can optionally specify the number you want to start at by passing
    in the ``start`` argument (defaults to 1).

    You can also optionally specify the step size you want by passing in
    the ``step`` argument (defaults to 1).

    Sequences will increase monotonically by ``step`` each time it is
    called, until the heat death of the universe or python explodes.

    This can be used to count rows in a table::

        # In Myghty
        % for item in items:
        <tr>
            <td><% h.counter() %></td>
        </tr>
        % #endfor

    You can used named counters to prevent clashes in nested loops.
    You'll have to reset the inner cycle manually though.  See the
    documentation for ``webhelpers.text.cycle()`` for a similar
    example.
    """
    # optional name of this list
    name = kwargs.get('name', 'default')
    # optional starting value for this sequence
    start = kwargs.get('start', 1)
    # optional step size of this sequence
    step = kwargs.get('step', 1)

    counters = request_config().environ.setdefault('railshelpers.counters', {})

    # ripped off of itertools.count
    def do_counter(start, step):
        while True:
            yield start
            start += step
            
    counter = counters.setdefault(name, do_counter(start, step))

    return counter.next()

def reset_counter(name='default'):
    """Resets a counter.

    Resets the counter so that it starts from the ``start`` cardinal in
    the sequence next time it is used.
    """
    del request_config().environ['railshelpers.counters'][name]
