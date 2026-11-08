# Gói R và mẫu code

Cài một lần:

```r
install.packages(c("tidyverse", "haven", "readxl", "janitor", "psych", "lavaan",
                   "semTools", "mice", "effectsize", "parameters", "performance",
                   "pwr", "semPower", "interactions", "papaja", "knitr", "kableExtra"))
```

Gói `papaja` có thể cần cài từ GitHub nếu CRAN không có: `remotes::install_github("crsh/papaja")`.

Để khoá phiên bản gói cho dự án: `renv::init()`.

## Đọc dữ liệu

```r
library(tidyverse)
raw <- readxl::read_excel("nckh/du-lieu/raw/khao-sat.xlsx")   # hoặc haven::read_sav() cho file SPSS
dat <- raw |> janitor::clean_names()
```

## Mã hoá ngược theo codebook

```r
cb <- read_csv("nckh/cong-cu/codebook.csv")
dao <- cb$ten_bien[cb$dao_chieu %in% c(TRUE, "TRUE", "co", 1)]
k <- 5  # số mức Likert
dat <- dat |> mutate(across(all_of(dao), ~ (k + 1) - .x))
```

## Độ tin cậy

```r
items <- dat |> select(starts_with("cas_"))
psych::alpha(items)$total$raw_alpha
psych::omega(items, nfactors = 1, plot = FALSE)$omega.tot
```

## CFA

```r
library(lavaan)
m <- '
  concern   =~ cas_01 + cas_02 + cas_03
  control   =~ cas_04 + cas_05 + cas_06
'
fit <- cfa(m, data = dat, estimator = "MLR", missing = "fiml")
# Biến thứ bậc: cfa(m, data = dat, ordered = TRUE, estimator = "WLSMV")
fitMeasures(fit, c("chisq.scaled", "df", "cfi.robust", "tli.robust", "rmsea.robust", "srmr"))
standardizedSolution(fit)
semTools::AVE(fit); semTools::htmt(m, data = dat)
```

## Bất biến đo lường (ví dụ theo giới)

```r
cfg <- cfa(m, dat, group = "gioi_tinh", estimator = "MLR")
met <- cfa(m, dat, group = "gioi_tinh", estimator = "MLR", group.equal = "loadings")
sca <- cfa(m, dat, group = "gioi_tinh", estimator = "MLR", group.equal = c("loadings", "intercepts"))
lavTestLRT(cfg, met, sca)   # và so sánh ΔCFI ≤ .01
```

## Trung gian với bootstrap

```r
med <- '
  M ~ a*X
  Y ~ b*M + c*X
  gian_tiep := a*b
  tong := c + a*b
'
set.seed(2026)
f <- sem(med, data = dat, se = "bootstrap", bootstrap = 5000)
parameterEstimates(f, boot.ci.type = "perc", standardized = TRUE)
```

## Điều tiết

```r
dat <- dat |> mutate(across(c(X, W), ~ as.numeric(scale(.x, scale = FALSE)), .names = "{.col}_c"))
fm <- lm(Y ~ X_c * W_c + tuoi + gioi_tinh, data = dat)
parameters::model_parameters(fm, standardize = "refit")
interactions::sim_slopes(fm, pred = X_c, modx = W_c, johnson_neyman = TRUE)
```

## Hồi quy và effect size

```r
fit <- lm(Y ~ X1 + X2 + tuoi + gioi_tinh, data = dat)
parameters::model_parameters(fit, standardize = "refit")
performance::check_model(fit)
effectsize::cohens_d(Y ~ nhom, data = dat)
```

## Cỡ mẫu

```r
pwr::pwr.f2.test(u = 4, f2 = 0.05, sig.level = .05, power = .80)  # n = v + u + 1
semPower::semPower.aPriori(effect = .05, effect.measure = "RMSEA", alpha = .05, power = .80, df = 48)
```

## Xuất bảng sang LaTeX cho Prism

```r
tab <- parameters::model_parameters(fit, standardize = "refit") |> as.data.frame()
write_csv(tab, "nckh/ket-qua/bang3-hoi-quy.csv")
knitr::kable(tab, format = "latex", booktabs = TRUE, digits = 2) |>
  writeLines("nckh/ket-qua/bang3-hoi-quy.tex")
```
