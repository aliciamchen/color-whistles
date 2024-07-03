# Discreteness and systematicity in a continuous signal-meaning space

## Setup

`pip install -e .`

First, make sure you have the necessary packages.

For python, create the virtual environment:

```{bash}
conda env create -f environment.yml
conda activate color-sounds
```

For R, open the project in RStudio and run `renv::restore()`.

### Analysis pipeline

To reproduce all calculations:

```{bash}
make clean
make
```

NOTE: this takes a couple hours because of `02_pairwise_dists.py`, which computes the pairwise distances between all combinations of the 1989 signals across all participants.

Finally, run `stats_and_plots.Rmd` to generate the plots and results of the analyses reported in the paper.

## Files

### Tools

[TODO]

### Data

Raw data is in `raw_data`. See [codebook](/raw_data/README.md).

Processed data is in `outputs`. See [codebook](/outputs/README.md).

### Other files

- `extra/plot_embeddings.R`: Plots 2D MDS embeddings for each game. Creates one plot (faceted by participant) per game. The colors of the points correspond to the referent, and the shapes correspond to cluster membership. Communication score, Hopkins statistic, systematicity, and partner alignment are displayed on each facet.
    - This file also contains code to filter and search example yellow signals that have migrated, for visualizing in the paper.
- `plot_signals.py`: Generates `.svg` plots for learning and example communication signals.
- `mds_dims.py`: Visualizes stress vs. number of MDS dimensions. This also takes a while to run

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
[1] stats     graphics  grDevices datasets  utils     methods   base

other attached packages:
 [1] jsonlite_1.8.0  car_3.1-0       carData_3.0-5   broom_1.0.5     tidyboot_0.1.1  forcats_0.5.1   stringr_1.4.0   dplyr_1.0.9     purrr_0.3.4
[10] readr_2.1.2     tidyr_1.2.0     tibble_3.1.7    ggplot2_3.4.4   tidyverse_1.3.1 here_1.0.1      emmeans_1.8.4-1 lmerTest_3.1-3  lme4_1.1-29
[19] Matrix_1.4-1

loaded via a namespace (and not attached):
 [1] httr_1.4.3          viridisLite_0.4.0   bit64_4.0.5         vroom_1.5.7         splines_4.2.0       modelr_0.1.8        assertthat_0.2.1
 [8] renv_1.0.7          cellranger_1.1.0    yaml_2.3.5          numDeriv_2016.8-1.1 pillar_1.7.0        backports_1.4.1     lattice_0.20-45
[15] glue_1.6.2          rvest_1.0.2         minqa_1.2.4         colorspace_2.0-3    pkgconfig_2.0.3     haven_2.5.0         mvtnorm_1.1-3
[22] scales_1.2.0        tzdb_0.3.0          mgcv_1.8-40         generics_0.1.2      farver_2.1.0        ellipsis_0.3.2      withr_2.5.0
[29] pbkrtest_0.5.1      cli_3.6.0           magrittr_2.0.3      crayon_1.5.1        readxl_1.4.0        estimability_1.4.1  fs_1.5.2
[36] fansi_1.0.3         nlme_3.1-157        MASS_7.3-56         xml2_1.3.3          tools_4.2.0         hms_1.1.1           lifecycle_1.0.3
[43] munsell_0.5.0       reprex_2.0.1        compiler_4.2.0      rlang_1.1.2         grid_4.2.0          nloptr_2.0.2        rstudioapi_0.13
[50] labeling_0.4.2      boot_1.3-28         gtable_0.3.0        abind_1.4-5         DBI_1.1.2           R6_2.5.1            lubridate_1.8.0
[57] knitr_1.45          bit_4.0.4           utf8_1.2.2          rprojroot_2.0.3     stringi_1.7.6       parallel_4.2.0      Rcpp_1.0.8.3
[64] vctrs_0.5.2         dbplyr_2.1.1        tidyselect_1.1.2    xfun_0.42
```
