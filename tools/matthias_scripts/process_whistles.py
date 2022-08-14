import glob
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import argparse


def process_experimental_data(json_data_directory, sampling_frequency):
    """
    """
    for i, file_path in enumerate(glob.glob(json_data_directory + "/*.json")):
        file_name, _ = os.path.splitext(os.path.basename(file_path))
        print(f"Found file {file_name} in {json_data_directory}/. Processing and plotting.")
        with open(file_path) as file:
            raw_signal = np.asarray(json.load(file))
            # print(raw_signal)
            signal = interpolate_signal(raw_signal, sampling_frequency)
            figure_path = json_data_directory + file_name + '.png'
            plot_signal(signal, figure_path)


def plot_signal(signal, figure_path=None, ax=None, lw=1, **plot_kwargs):
    """Plot a single signal.

    Args:
        signal:
            t: np.ndarray [num_timesteps]
            y: np.ndarray [num_timesteps]
            ys_on_off: np.ndarray [num_timesteps]
        **plot_kwargs
    """
    t, y, y_on_off = signal
    if ax is None:
        f, ax = plt.subplots(1, 1, figsize=(t[-1], 2))
    else:
        f = plt.gcf()

    # compute places where signal changes between on and off
    changepoint_indices = np.arange(len(y_on_off))[
        y_on_off != np.concatenate([[True], y_on_off[:-1]])]
    changepoints = np.concatenate([[0.0], t[changepoint_indices], t[-1][None]])
    on = True
    for i in range(len(changepoints) - 1):
        left = changepoints[i]
        right = changepoints[i + 1]
        segment_indicator = (t >= left) & (t <= right)
        if on:
            kwargs = {
                "linestyle": "solid",
                "linewidth": lw,
                "color": "black",
            }
        else:
            kwargs = {
                "linestyle": "dashed",
                "linewidth": lw * 0.5,
                "color": "lightgrey",
            }
        # values in kwargs override plot_kwargs
        kwargs = {**plot_kwargs, **kwargs}

        ax.plot(
            t[segment_indicator], y[segment_indicator], **kwargs,
        )

        on = not on

    if figure_path is not None:
        f.tight_layout(pad=0)
        f.savefig(figure_path, bbox_inches="tight", dpi=300)
        print(f"Saved to {figure_path}")
        plt.close(f)
    else:
        plt.plot()

def smooth(x, window_len=5, window="hanning"):
    """convolution-based method to smooth a signal

    Args:
        x: the input signal
        window_len: the dimension of the smoothing window; should be an odd integer
        window: the type of window from 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'
            flat window will produce a moving average smoothing.

    output:
        the smoothed signal
    """
    if x.size < window_len:
        raise ValueError("Input vector needs to be bigger than window size.")
    if window_len < 3:
        return x
    if window not in ["flat", "hanning", "hamming", "bartlett", "blackman"]:
        raise ValueError(
            "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'")

    s = np.r_[x[window_len - 1: 0: -1], x, x[-2: -window_len - 1: -1]]

    if window == "flat":  # moving average
        w = np.ones(window_len, "d")
    else:
        w = eval("np." + window + "(window_len)")

    y = np.convolve(w / w.sum(), s, mode="valid")
    return y[int(window_len / 2 - 1): -int(window_len / 2)]


def interpolate_signal(raw_signal, sampling_frequency=50):
    """
    Convert raw signal (array of timestamped browser events) to evenly
    sampled signal, 'sampling_frequency' times samples per second.


    """
    if sampling_frequency > 1000:
        raise ValueError("Sampling Frequency cannot be higher than 1000Hz")

    # beginning and end time in ms
    # print(raw_signal)
    # print(raw_signal[0]['t'])
    # print(raw_signal[-1]['t'])
    # TODO: add exception for dealing with empty signals

    t0, tn = int(raw_signal[0]["t"]), int(raw_signal[-1]["t"])

    # sample raw_signal at 1000 Hz
    t = np.arange(tn - t0)
    y = []
    y_on_off = []

    i = 0
    for ms_time_stamp in t:
        y.append(float(raw_signal[i]["y"]))
        y_on_off.append(raw_signal[i]["a"] or raw_signal[i]["e"] == "keyup")
        if raw_signal[i]["t"] <= ms_time_stamp:
            i += 1
    y = np.asarray(y)
    y_on_off = np.asarray(y_on_off)

    # remove noise by smoothing that data
    y = smooth(y, window_len=min(51, len(y)), window="flat")[:len(t)]

    # subsample according to 'sampling_frequency'
    T = int(1000 / sampling_frequency)
    t, y, y_on_off = t[::T], y[::T], y_on_off[::T]
    t = t / 1000  # convert from ms to s

    return t, y, y_on_off


def add_mousemove_for_plotting(raw_signal):
    """
    Make sure that there is at least one 'mousemove' event after every 'keyup' event to ensure consistency in plotting.
    """
    num_inserted_counter = 1
    for i, timestamped_event in enumerate(raw_signal):
        if timestamped_event['e'] == 'keyup':
            filler_event = raw_signal[i+num_inserted_counter-1].copy()
            filler_event['e'] = 'mousemove'
            raw_signal = np.insert(
                raw_signal, i + num_inserted_counter, filler_event)
            num_inserted_counter += 1
    return raw_signal


def get_parser():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description='''
        Code to convert a timestamped json signal file to an interpolated
        (evenly sampled) numpy representation.

        Expects the json representation to contain the following values, per timestamp:

        - "a" for audible: true/false, indicating whether the timestep is audible or silent
        - "e" for event: the type of user interaction captured by the interface at that
                         timestamp. Must be one of 'keydown', 'keyup', or 'mousemove'
        - "p" for position: the actual y-coordinate of the plunger element (optional since
                            it is not used here)
        - "t" for time: the time the event was recorded in ms
        - "y" for y-position: the y-coordinate, normalized to lie between 0 and 1
        - "f" for frequency: the frequency in Hz that the instrument was playing
                             (optional since it is not used here)

        ''',)
    parser.add_argument("--data-path", "-d", type=str, required=True, help="The directory containing the signals to be converted and plotted. E.g., signals")
    parser.add_argument("--sampling-frequency", "-f", type=int, default=50, help="The frequency at which the processed signal will be interpolated. In samples per second (Hz).")
    return parser


if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    json_data_directory = args.data_path
    sampling_frequency = args.sampling_frequency
    process_experimental_data(json_data_directory, sampling_frequency)
