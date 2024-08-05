# Raw data

## `.json` representations of signals

- "a" for audible: true/false, indicating whether the timestep is audible or silent
- "e" for event: the type of user interaction captured by the interface at that
                    timestamp. Must be one of 'keydown', 'keyup', or 'mousemove'
- "p" for position: the actual y-coordinate of the plunger element
- "t" for time: the time the event was recorded in ms
- "y" for y-position: the y-coordinate, normalized to lie between 0 and 1
- "f" for frequency: the frequency in Hz that the instrument was playing


## `learning_data.zip`

- `trial_type`: was this a whistle played to the participant (`WHISTLE-PLAYBACK`) or was this a whistle the participant recorded (`WHISTLE-RECORD`)?
- `trial_index`
- `time_elapsed`
- `internal_node_id`
- `learning_criterion_reached`: did the participant pass the learning phase?
- `num_correc_lc_guesses`: how many signal-color pairings did the participant correctly guess?
- `screen_resolution`
- `signal`: `.json` representation of signal
- `signal_id`: not used; identical to `referent_id`
- `referent_id`: 0-4 index of referent, corresponding to indices of `["#d9445d", "#ae6c00", "#009069", "#008b98", "#8c6db5"]`
- `block_id`: label for block, where `0` corresponds to `WHISTLE-PLAYBACK` and `6` corresponds to participants' produced signals at the end of the learning phase (for calculating learning score)
- `workerid`
- `hitid`


## `learning_survey_data.zip`

- `age`
- `gender`
- `interface`: `mouse` or `trackpad`
- `pitch`: `yes` or `no` or `don't know`
- `music`: `little` or `moderate` or `lots`
- `color`: `No` or `art` or `design`
- `feedback`: participant written feedback
- `workerid`
- `learningCriterion`: did the participant pass the learning phase?
- `numberCorrect`: number correct (out of 5) out of the learning phase

## `communication_game_data.zip`

- `roundid`
- `gameid`
- `speakerid`
- `listenerid`
- `round`: which round? 1-80
- `blockid`: 1 if round <= 40, 2 if round > 40
- `correctid`: index of target referent, from 0 to 39 (e.g. for indexing into `stimuli` or  `stim/wcs_row_F.json`)
- `correct`: hex of target referent
- `signalproduced`: `.json` representation of signal
- `stimuli`: list of all referents
- `listenerchoiceid`: index of listener chosen referent
- `listenerchoice`: hex of listener chosen referent
- `listenertime`: amount of time it took for listener to choose answer
- `selectioncorrect`: 1 if the listener chose exactly the target referent, 0 otherwise
- `score`: communication score (distance from target to chosen referent, normalized between 0 and 1)

## `communication_metadata.zip`

- `datastring` contains survey data:
    - `human_partner`: did the participant think that they interacted with a real person?
    - `feedback`: participant written feedback
    -  `reason`
    - `score`: final score