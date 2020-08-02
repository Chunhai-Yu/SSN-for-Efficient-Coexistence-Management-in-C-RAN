import scipy.signal as signal
from numpy import *
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.mlab import psd

def selfpsd(x, NFFT=None, Fs=None, Fc=None, detrend=None,
        window=None, noverlap=None, pad_to=None,
        sides=None, scale_by_freq=None):

    if Fc is None:
        Fc = 0

    pxx, freqs = psd(x=x, NFFT=NFFT, Fs=Fs, detrend=detrend,
                          window=window, noverlap=noverlap, pad_to=pad_to,
                          sides=sides, scale_by_freq=scale_by_freq)
    freqs += Fc

    return pxx, freqs

    r"""
        Plot the power spectral density.

        Call signature::

          psd(x, NFFT=256, Fs=2, Fc=0, detrend=mlab.detrend_none,
              window=mlab.window_hanning, noverlap=0, pad_to=None,
              sides='default', scale_by_freq=None, return_line=None, **kwargs)

        The power spectral density :math:`P_{xx}` by Welch's average
        periodogram method.  The vector *x* is divided into *NFFT* length
        segments.  Each segment is detrended by function *detrend* and
        windowed by function *window*.  *noverlap* gives the length of
        the overlap between segments.  The :math:`|\mathrm{fft}(i)|^2`
        of each segment :math:`i` are averaged to compute :math:`P_{xx}`,
        with a scaling to correct for power loss due to windowing.

        If len(*x*) < *NFFT*, it will be zero padded to *NFFT*.

        Parameters
        ----------
        x : 1-D array or sequence
            Array or sequence containing the data

        %(Spectral)s

        %(PSD)s

        noverlap : integer
            The number of points of overlap between segments.
            The default value is 0 (no overlap).

        Fc : integer
            The center frequency of *x* (defaults to 0), which offsets
            the x extents of the plot to reflect the frequency range used
            when a signal is acquired and then filtered and downsampled to
            baseband.

        return_line : bool
            Whether to include the line object plotted in the returned values.
            Default is False.

        Returns
        -------
        Pxx : 1-D array
            The values for the power spectrum `P_{xx}` before scaling
            (real valued)

        freqs : 1-D array
            The frequencies corresponding to the elements in *Pxx*

        line : a :class:`~matplotlib.lines.Line2D` instance
            The line created by this function.
            Only returned if *return_line* is True.

        Other Parameters
        ----------------
        **kwargs :
            Keyword arguments control the :class:`~matplotlib.lines.Line2D`
            properties:

            %(Line2D)s

        See Also
        --------
        :func:`specgram`
            :func:`specgram` differs in the default overlap; in not returning
            the mean of the segment periodograms; in returning the times of the
            segments; and in plotting a colormap instead of a line.

        :func:`magnitude_spectrum`
            :func:`magnitude_spectrum` plots the magnitude spectrum.

        :func:`csd`
            :func:`csd` plots the spectral density between two signals.

        Notes
        -----
        For plotting, the power is plotted as
        :math:`10\log_{10}(P_{xx})` for decibels, though *Pxx* itself
        is returned.

        References
        ----------
        Bendat & Piersol -- Random Data: Analysis and Measurement Procedures,
        John Wiley & Sons (1986)
        """