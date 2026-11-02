---
name: genpark-personal-agent-post-exercise-epoc-recovery-skill
description: Deterministic bi-exponential modeling of post-exercise oxygen consumption (EPOC), alactacid/lactacid recovery phases, and post-workout nutritional refueling windows.
version: 1.0.0
author: GenPark Autonomous Agents Ecosystem
license: MIT
tags:
  - personal-agent
  - ai-agent
  - openclaw
  - genpark
  - mcp
  - mcp-server
  - model-context-protocol
  - python
  - zero-dependency
  - wellness
  - productivity
  - production-ready
---

# Post-Exercise EPOC & Metabolic Recovery Kinetics Skill

## Overview
The `genpark-personal-agent-post-exercise-epoc-recovery-skill` provides sovereign personal agents with mathematical modeling of Excess Post-Exercise Oxygen Consumption (EPOC). After intense athletic training or high-intensity interval workouts, cellular metabolism remains elevated above basal levels to clear lactate, resynthesize phosphocreatine (PCr) stores, reload oxymyoglobin, and dissipate exercise-induced heat ($Q_{10}$ effect). This skill tracks the metabolic debt clearance trajectory in real time, computes post-exercise caloric expenditure, and identifies nutritional refueling opportunities.

## Physiological Model & Mathematics
1. **Gaesser-Brooks Bi-Exponential Decay**:
   $$\dot{V}O_2(t) = \dot{V}O_{2,\text{rest}} + A_{\text{fast}} \cdot e^{-t/\tau_{\text{fast}}} + A_{\text{slow}} \cdot e^{-t/\tau_{\text{slow}}}$$
   - **Fast component ($\tau_{\text{fast}} \approx 45\text{ s}$)**: Alactacid recovery (PCr, ATP, myoglobin $O_2$).
   - **Slow component ($\tau_{\text{slow}} \approx 20 - 45\text{ min}$)**: Lactate gluconeogenesis (Cori cycle), elevated core temperature ($Q_{10}$), cardiac/ventilatory elevation.
2. **Integrated Oxygen Debt Volume**:
   $$V_{\text{EPOC}}(t) = A_{\text{fast}}\tau_{\text{fast}}(1 - e^{-t/\tau_{\text{fast}}}) + A_{\text{slow}}\tau_{\text{slow}}(1 - e^{-t/\tau_{\text{slow}}})$$
3. **Caloric Expenditure**:
   $$\text{Calories (kcal)} = V_{\text{EPOC}} (\text{L}) \times 4.86\text{ kcal/L } O_2$$
4. **Heart Rate Recovery (HRR) Vagal Reactivation Index**:
   Evaluates parasympathetic reactivation velocity against standardized normative decay profiles.

## Tools & Endpoints
- `calculate_epoc_trajectory`: Computes instantaneous $\dot{V}O_2$, cumulative $O_2$ debt volume, calories burned, and 95% recovery horizon.
- `evaluate_heart_rate_recovery_kinetics`: Assesses autonomic vagal reactivation from heart rate drop following cessation of exercise.
