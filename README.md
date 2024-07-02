# Discreteness and systematicity in a continuous signal-meaning space

## Setup

`pip install -e .`

## Files

### Data

Raw data is in `raw_data`. See [codebook](/raw_data/README.md).

Processed data is in `outputs`. See [codebook](/outputs/README.md).


### Analysis pipeline

To reproduce all analyses:

First, make sure you have the necessary packages.

For python, create the virtual environment:
```
conda env create -f environment.yml
conda activate color-sounds
```

For R, [TODO: reproducibility stuff]

Second, run `run_analysis.sh`. NOTE: this takes a couple hours because of `02_pairwise_dists.py`, which computes the pairwise distances between all combinations of the 1989 signals across all participants.

Finally, run `stats_and_plots.Rmd` to generate the plots and results of the analyses reported in the paper.


### Other files

- `extra/plot_embeddings.R`: Plots 2D MDS embeddings for each game. Creates one plot (faceted by participant) per game. The colors of the points correspond to the referent, and the shapes correspond to cluster membership. Communication score, Hopkins statistic, systematicity, and partner alignment are displayed on each facet.
    - This file also contains code to filter and search example yellow signals that have migrated, for visualizing in the paper.
- `plot_signals.py`: Generates `.svg` plots for learning and example communication signals.
- `mds_dims.py`: Visualizes stress vs. number of MDS dimensions.


## R session info

```{r}
sessionInfo()
R version 4.2.0 (2022-04-22)
Platform: aarch64-apple-darwin20 (64-bit)
Running under: macOS 14.4.1

Matrix products: default
LAPACK: /Library/Frameworks/R.framework/Versions/4.2-arm64/Resources/lib/libRlapack.dylib

locale:
[1] en_US.UTF-8/en_US.UTF-8/en_US.UTF-8/C/en_US.UTF-8/en_US.UTF-8

attached base packages:
[1] stats     graphics  grDevices utils     datasets  methods   base

other attached packages:
 [1] jsonlite_1.8.0  energy_1.7-10   forcats_0.5.1   stringr_1.4.0   dplyr_1.0.9     purrr_0.3.4     readr_2.1.2     tidyr_1.2.0
 [9] tibble_3.1.7    ggplot2_3.4.4   tidyverse_1.3.1 here_1.0.1

loaded via a namespace (and not attached):
 [1] xfun_0.42        tidyselect_1.1.2 haven_2.5.0      colorspace_2.0-3 vctrs_0.5.2      generics_0.1.2   htmltools_0.5.2
 [8] yaml_2.3.5       utf8_1.2.2       rlang_1.1.2      pillar_1.7.0     glue_1.6.2       withr_2.5.0      DBI_1.1.2
[15] dbplyr_2.1.1     modelr_0.1.8     readxl_1.4.0     lifecycle_1.0.3  munsell_0.5.0    gtable_0.3.0     cellranger_1.1.0
[22] rvest_1.0.2      evaluate_0.15    knitr_1.45       fastmap_1.1.0    tzdb_0.3.0       fansi_1.0.3      broom_1.0.5
[29] Rcpp_1.0.8.3     scales_1.2.0     backports_1.4.1  fs_1.5.2         digest_0.6.29    hms_1.1.1        stringi_1.7.6
[36] gsl_2.1-7.1      grid_4.2.0       rprojroot_2.0.3  cli_3.6.0        tools_4.2.0      magrittr_2.0.3   crayon_1.5.1
[43] pkgconfig_2.0.3  ellipsis_0.3.2   xml2_1.3.3       reprex_2.0.1     lubridate_1.8.0  assertthat_0.2.1 rmarkdown_2.26
[50] httr_1.4.3       rstudioapi_0.13  R6_2.5.1         boot_1.3-28      compiler_4.2.0
```