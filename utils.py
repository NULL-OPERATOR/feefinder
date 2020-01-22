import scipy.interpolate

sample_data = {
    12: {
        'amount': [1000, 2000, 3000, 4000, 5000, 20000],
        'fee': [50, 90, 90, 115, 100, 400]
    },
    24: {
        'amount': [1000, 2000, 3000, 4000, 20000],
        'fee': [70, 100, 120, 160, 800]
    }
}


# just a quick thought
def _get_linear_function(term):
    return scipy.interpolate.interp1d(sample_data[term]['amount'], sample_data[term]['fee'])


# here so they run once
term_linear_functions = {
    12: _get_linear_function(12),
    24: _get_linear_function(24)
}


def calculator(term, amount):
    """
    take the term, amount, and run it through the linear function, then return
    the result rounded to the nearest 5
    """
    fee = term_linear_functions[term](amount)
    return _round_to(fee, 5)


def _round_to(amount, base):
    return amount - amount % base
