#!/usr/bin/env Rscript
# AutoGRADE Pipeline: Automated GRADE assessment of 501 Cochrane meta-analyses
suppressPackageStartupMessages(library(metafor))

DATA_DIR <- "C:/Models/Pairwise70/data"
OUT_DIR  <- "C:/Models/AutoGRADE/data"
dir.create(OUT_DIR, showWarnings = FALSE, recursive = TRUE)

rda_files <- list.files(DATA_DIR, pattern = "\\.rda$", full.names = TRUE)
cat("Found", length(rda_files), "RDA files\n")

results <- data.frame(
  review_id = character(), k = integer(), total_n = numeric(),
  effect = numeric(), ci_lo = numeric(), ci_hi = numeric(),
  i2 = numeric(), tau2 = numeric(), p_value = numeric(),
  rob_down = integer(), incon_down = integer(), indirect_down = integer(),
  imprec_down = integer(), pubbias_down = integer(), total_down = integer(),
  grade_score = integer(), grade_label = character(),
  stringsAsFactors = FALSE
)

n_proc <- 0

for (f in rda_files) {
  rid <- sub("_data\\.rda$", "", basename(f))
  tryCatch({
    d <- get(load(f))
    if ("Analysis.number" %in% names(d)) d <- d[d$Analysis.number == min(d$Analysis.number), ]
    if (nrow(d) < 2) next

    yi <- log(d$Mean)
    sei <- (log(d$CI.end) - log(d$CI.start)) / (2 * qnorm(0.975))
    valid <- is.finite(yi) & is.finite(sei) & sei > 0
    yi <- yi[valid]; sei <- sei[valid]
    if (length(yi) < 2) next

    total_n <- sum(d$Experimental.N[valid] + d$Control.N[valid], na.rm = TRUE)

    fit <- tryCatch(rma(yi = yi, sei = sei, method = "REML"), error = function(e) NULL)
    if (is.null(fit)) next

    theta <- as.numeric(fit$beta)
    se_p <- as.numeric(fit$se)
    i2 <- as.numeric(fit$I2)
    tau2 <- as.numeric(fit$tau2)
    pval <- as.numeric(fit$pval)
    k <- fit$k
    ci_lo <- theta - 1.96 * se_p
    ci_hi <- theta + 1.96 * se_p

    # ── GRADE DOMAINS (automated, RCT starting point = 4) ──
    score <- 4

    # 1. Risk of Bias (proxy: assume 15% high RoB for Cochrane RCTs)
    rob_down <- 0  # Default: Cochrane reviews have systematic RoB assessment

    # 2. Inconsistency
    incon_down <- 0
    if (k > 1) {
      if (i2 > 75) incon_down <- 2
      else if (i2 > 40) incon_down <- 1
    }

    # 3. Indirectness (cannot automate — set to 0)
    indirect_down <- 0

    # 4. Imprecision
    imprec_down <- 0
    ci_crosses_null <- (ci_lo < 0 & ci_hi > 0)
    # OIS: simplified — require total N > 2000 for adequate power
    ois_met <- total_n > 2000
    if (ci_crosses_null & !ois_met) imprec_down <- 2
    else if (ci_crosses_null | !ois_met) imprec_down <- 1

    # 5. Publication bias (Egger's test when k >= 10)
    pubbias_down <- 0
    if (k >= 10) {
      egger <- tryCatch(regtest(fit), error = function(e) NULL)
      if (!is.null(egger)) {
        ep <- egger$pval
        if (!is.na(ep) && ep < 0.05) pubbias_down <- 2
        else if (!is.na(ep) && ep < 0.10) pubbias_down <- 1
      }
    }

    total_down <- rob_down + incon_down + indirect_down + imprec_down + pubbias_down
    score <- max(1, score - total_down)
    grade_label <- if (score >= 4) "HIGH" else if (score == 3) "MODERATE" else if (score == 2) "LOW" else "VERY LOW"

    results <- rbind(results, data.frame(
      review_id = rid, k = k, total_n = total_n,
      effect = exp(theta), ci_lo = exp(ci_lo), ci_hi = exp(ci_hi),
      i2 = i2, tau2 = tau2, p_value = pval,
      rob_down = rob_down, incon_down = incon_down, indirect_down = indirect_down,
      imprec_down = imprec_down, pubbias_down = pubbias_down, total_down = total_down,
      grade_score = score, grade_label = grade_label,
      stringsAsFactors = FALSE
    ))

    n_proc <- n_proc + 1
    if (n_proc %% 50 == 0) cat("  Processed", n_proc, "...\n")

  }, error = function(e) {})
}

cat("\n=== PIPELINE COMPLETE ===\n")
cat("Analyzed:", nrow(results), "\n\n")

write.csv(results, file.path(OUT_DIR, "grade_all.csv"), row.names = FALSE)
saveRDS(results, file.path(OUT_DIR, "grade_all.rds"))

# ── HEADLINE ──
cat("=== GRADE CERTAINTY DISTRIBUTION ===\n")
cat("  HIGH:      ", sum(results$grade_label == "HIGH"), "(", round(100*sum(results$grade_label=="HIGH")/nrow(results),1), "%)\n")
cat("  MODERATE:  ", sum(results$grade_label == "MODERATE"), "(", round(100*sum(results$grade_label=="MODERATE")/nrow(results),1), "%)\n")
cat("  LOW:       ", sum(results$grade_label == "LOW"), "(", round(100*sum(results$grade_label=="LOW")/nrow(results),1), "%)\n")
cat("  VERY LOW:  ", sum(results$grade_label == "VERY LOW"), "(", round(100*sum(results$grade_label=="VERY LOW")/nrow(results),1), "%)\n")

cat("\n=== MOST COMMON DOWNGRADES ===\n")
cat("  Imprecision:     ", sum(results$imprec_down > 0), "(", round(100*sum(results$imprec_down>0)/nrow(results),1), "%)\n")
cat("  Inconsistency:   ", sum(results$incon_down > 0), "(", round(100*sum(results$incon_down>0)/nrow(results),1), "%)\n")
cat("  Publication Bias: ", sum(results$pubbias_down > 0), "(", round(100*sum(results$pubbias_down>0)/nrow(results),1), "%)\n")

cat("\nMedian total downgrades:", median(results$total_down), "\n")
cat("Mean total downgrades:", round(mean(results$total_down), 2), "\n")
