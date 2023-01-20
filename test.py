# https://github.com/semitable/easing-functions
from easing_functions import *
import numpy as np
import matplotlib.pyplot as plt
from enum import Enum

plt.style.use('_mpl-gallery')

class Easing(Enum):
    LINEAR = 'Linear'
    BOUNCE_IN = 'BounceIn'
    BOUNCE_OUT = 'BounceOut'
    BOUNCE_IN_OUT = 'BounceInOut'
    SINE_IN = 'SineIn'
    SINE_OUT = 'SineOut'
    SINE_IN_OUT = 'SineInOut'
    CIRCULAR_IN = 'CircularEaseIn'
    CIRCULAR_OUT = 'CircularEaseOut'
    CIRCULAR_IN_OUT = 'CircularEaseInOut'
    QUAD_IN = 'QuadEaseIn'
    QUAD_OUT = 'QuadEaseOut'
    QUAD_IN_OUT = 'QuadEaseInOut'
    CUBIC_IN = 'CubicEaseIn'
    CUBIC_OUT = 'CubicEaseOut'
    CUBIC_IN_OUT = 'CubicEaseInOut'
    QUARTIC_IN = 'QuarticEaseIn'
    QUARTIC_OUT = 'QuarticEaseOut'
    QUARTIC_IN_OUT = 'QuarticEaseInOut'
    QUINTIC_IN = 'QuinticEaseIn'
    QUINTIC_OUT = 'QuinticEaseOut'
    QUINTIC_IN_OUT = 'QuinticEaseInOut'
    EXPONENTIAL_IN = 'ExponentialEaseIn'
    EXPONENTIAL_OUT = 'ExponentialEaseOut'
    EXPONENTIAL_IN_OUT = 'ExponentialEaseInOut'
    ELASTIC_IN = 'ElasticEaseIn'
    ELASTIC_OUT = 'ElasticEaseOut'
    ELASTIC_IN_OUT = 'ElasticEaseInOut'
    BACK_IN = 'BackEaseIn'
    BACK_OUT = 'BackEaseOut'
    BACK_IN_OUT = 'BackEaseInOut'


# TODO EaseIn needs work so it ends on the END var
def easing(name: Easing, start: int, end: int):
    if not isinstance(name, Easing): raise TypeError(f'{name} should be Easing not {name.__class__.__name__}')
    f = None
    match name:
        case Easing.LINEAR: f = LinearInOut(start, end, end)
        case Easing.BOUNCE_IN: f = BounceEaseIn(start, end, end)
        case Easing.BOUNCE_OUT: f = BounceEaseOut(start, end-1, end)
        case Easing.BOUNCE_IN_OUT: f = BounceEaseInOut(start, end-1, end)
        case Easing.SINE_IN: f = SineEaseIn(start, end+1, end)
        case Easing.SINE_OUT: f = SineEaseOut(start, end-1, end)
        case Easing.SINE_IN_OUT: f = SineEaseInOut(start, end-1, end)
        case Easing.CIRCULAR_IN: f = CircularEaseIn(start, end+6, end)
        case Easing.CIRCULAR_OUT: f = CircularEaseOut(start, end-1, end)
        case Easing.CIRCULAR_IN_OUT: f = CircularEaseInOut(start, end-1, end)
        case Easing.QUAD_IN: f = QuadEaseIn(start, end+1, end)
        case Easing.QUAD_OUT: f = QuadEaseOut(start, end-1, end)
        case Easing.QUAD_IN_OUT: f = QuadEaseInOut(start, end-1, end)
        case Easing.CUBIC_IN: f = CubicEaseIn(start, end+2, end)
        case Easing.CUBIC_OUT: f = CubicEaseOut(start, end-1, end)
        case Easing.CUBIC_IN_OUT: f = CubicEaseInOut(start, end-1, end)
        case Easing.QUARTIC_IN: f = QuarticEaseIn(start, end+3, end)
        case Easing.QUARTIC_OUT: f = QuarticEaseOut(start, end-1, end)
        case Easing.QUARTIC_IN_OUT: f = QuarticEaseInOut(start, end-1, end)
        case Easing.QUINTIC_IN: f = QuinticEaseIn(start, end+5, end)
        case Easing.QUINTIC_OUT: f = QuinticEaseOut(start, end-1, end)
        case Easing.QUINTIC_IN_OUT: f = QuinticEaseInOut(start, end-1, end)
        case Easing.EXPONENTIAL_IN: f = ExponentialEaseIn(start, end+7, end)
        case Easing.EXPONENTIAL_OUT: f = ExponentialEaseOut(start, end-1, end)
        case Easing.EXPONENTIAL_IN_OUT: f = ExponentialEaseInOut(start, end-1, end)
        case Easing.ELASTIC_IN: f = ElasticEaseIn(start, end, end)
        case Easing.ELASTIC_OUT: f = ElasticEaseOut(start, end-1, end)
        case Easing.ELASTIC_IN_OUT: f = ElasticEaseInOut(start, end-1, end)
        case Easing.BACK_IN: f = BackEaseIn(start, end+9, end)
        case Easing.BACK_OUT: f = BackEaseOut(start, end-1, end)
        case Easing.BACK_IN_OUT: f = BackEaseInOut(start, end-1, end)
        case _: raise NotImplementedError(f'"{name}" is not a valid easing function')
    x = np.arange(start, end, 1, dtype=int)
    return list(map(round,  map(f, x)))

if __name__ == '__main__':
    plots = easing(Easing.ELASTIC_OUT, 0, 11)
    print(plots)
    fig, ax = plt.subplots()
    ax.plot(plots, marker='o')

    ax.scatter(x=[0], y=[0], linewidth=3, color='red', marker='o')
    ax.scatter(x=[10], y=[10], linewidth=3, color='red', marker='o')

    s = min(*plots)-1
    l = max(*plots)+1
    ax.set(xlim=(s, l), ylim=(s, l), xticks=np.arange(
        s, l), yticks=np.arange(s, l))
    plt.tight_layout(pad=0.1, h_pad=0.1, w_pad=0.1)
    plt.show()

    # Should start at 0,0 and end at 10,10
