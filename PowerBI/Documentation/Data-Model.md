# Project Vortex public Power BI data model

This directory contains the public semantic model only. It consumes approved aggregates from `data/` through a configurable `DataRoot` parameter and does not include a private ledger, raw market archive, account feed or execution connection.

The current PBIP has 14 pages and a 9-table, 24-measure model. The monthly drawdown proxy is not a reconstructed M5 or trade-order equity path. See the repository README and SECURITY_REVIEW.md for metric definitions, exclusions and current release state.
