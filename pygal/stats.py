from math import log, pi, sqrt


def erfinv(x, a=.147):
    """Approximation of the inverse error function
    https://en.wikipedia.org/wiki/Error_function
    #Approximation_with_elementary_functions
    """
    lnx = log(1 - x * x)
    part1 = (2 / (a * pi) + lnx / 2)
    part2 = lnx / a
    sgn = 1 if x > 0 else -1
    return sgn * sqrt(sqrt(part1 * part1 - part2) - part1)


def norm_ppf(x):
    if not 0 < x < 1:
        raise ValueError("Can't compute the percentage point for value %d" % x)
    return sqrt(2) * erfinv(2 * x - 1)


def ppf(x, n):
    try:
        from scipy import stats
    except ImportError:
        stats = None

    if stats:
        if n < 30:
            return stats.t.ppf(x, n)
        return stats.norm.ppf(x)
    else:
        if n < 30:
            # TODO: implement power series:
            # http://eprints.maths.ox.ac.uk/184/1/tdist.pdf
            raise ImportError(
                'You must have scipy installed to use t-student '
                'when sample_size is below 30'
            )
        return norm_ppf(x)


# According to http://sphweb.bumc.bu.edu/otlt/MPH-Modules/BS/
# BS704_Confidence_Intervals/BS704_Confidence_Intervals_print.html


def confidence_interval_continuous(
        point_estimate, stddev, sample_size, confidence=.95, **kwargs
):
    """Continuous confidence interval from sample size and standard error"""
    alpha = ppf((confidence + 1) / 2, sample_size - 1)

    margin = stddev / sqrt(sample_size)
    return (point_estimate - alpha * margin, point_estimate + alpha * margin)


def confidence_interval_dichotomous(
        point_estimate,
        sample_size,
        confidence=.95,
        bias=False,
        percentage=True,
        **kwargs
):
    """Dichotomous confidence interval from sample size and maybe a bias"""
    alpha = ppf((confidence + 1) / 2, sample_size - 1)
    p = point_estimate
    if percentage:
        p /= 100

    margin = sqrt(p * (1 - p) / sample_size)
    if bias:
        margin += .5 / sample_size
    if percentage:
        margin *= 100

    return (point_estimate - alpha * margin, point_estimate + alpha * margin)


def confidence_interval_manual(point_estimate, low, high):
    return (low, high)
