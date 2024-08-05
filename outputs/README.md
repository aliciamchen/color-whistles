# Processed data

## `init_signals_tidy.zip`, `learn_signals_tidy.zip`, `comm_signals_tidy.zip`

NOTE: `signal_id` is now 0 through 4 indices of init referents, in `init_signals_tidy.zip`. `referent_id` is the index corresponding to the 40 referents.

- `referent`: hex of target referent
- `t`: time point
- `val`: pitch value of the trunk (not including whether it is on or off)
- `isOn`: 1 if the signal is playing, 0 otherwise
- `signal`: what is playing (the same as `val`, with `NaN` if the trunk is off)
- `signalWithZeros`: what is playing (the same as `val`, with 0 if the trunk is off - this is what is used for DTW)