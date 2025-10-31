pkgs <- c("readr", "dplyr")
to_install <- pkgs[!(pkgs %in% rownames(installed.packages()))]
if (length(to_install)) install.packages(to_install, repos="https://cloud.r-project.org")