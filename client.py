"""
Post-Exercise Oxygen Consumption (EPOC) & Metabolic Recovery Kinetics Engine.
Provides deterministic, zero-dependency modeling of bi-exponential EPOC decay,
phosphocreatine/lactate clearance phases, thermal load, and post-workout caloric expenditure.
"""

import math
from typing import Dict, Any, List, Optional


class PostExerciseEpocClient:
    """
    Deterministic client for modeling EPOC kinetics and metabolic debt clearance.
    Based on the Gaesser & Brooks bi-exponential model and Margaria recovery kinetics.
    """

    def __init__(self):
        pass

    def calculate_epoc_trajectory(
        self,
        exercise_duration_min: float,
        vo2_max_ml_kg_min: float,
        exercise_intensity_pct_vo2max: float,
        body_mass_kg: float,
        post_exercise_time_min: float = 60.0
    ) -> Dict[str, Any]:
        """
        Calculates EPOC trajectory, cumulative oxygen debt volume, and caloric expenditure.
        Uses bi-exponential recovery equation: VO2(t) = VO2_rest + A_fast * exp(-t/tau_fast) + A_slow * exp(-t/tau_slow).
        """
        if exercise_duration_min <= 0 or vo2_max_ml_kg_min <= 0 or body_mass_kg <= 0:
            return {"error": "Invalid physiological parameters: duration, vo2max, and body mass must be positive"}

        intensity = max(0.20, min(1.20, exercise_intensity_pct_vo2max / 100.0 if exercise_intensity_pct_vo2max > 1.0 else exercise_intensity_pct_vo2max))
        resting_vo2_ml_min = 3.5 * body_mass_kg  # 1 MET baseline
        max_vo2_ml_min = vo2_max_ml_kg_min * body_mass_kg
        exercise_vo2_ml_min = max_vo2_ml_min * intensity

        delta_vo2 = max(0.0, exercise_vo2_ml_min - resting_vo2_ml_min)

        # Fast phase parameters (seconds converted to minutes)
        # Fast phase amplitude scales with intensity (alactacid: PCr & myoglobin resynthesis)
        a_fast = delta_vo2 * (0.65 if intensity > 0.75 else 0.50)
        tau_fast_min = 0.75  # ~45 seconds time constant

        # Slow phase parameters (lactate clearance, elevated temperature Q10 effect, ventilation)
        # Duration exponentially amplifies slow phase amplitude
        duration_factor = min(2.5, 1.0 + (exercise_duration_min / 60.0) * 0.5)
        a_slow = delta_vo2 * (0.25 * (intensity ** 1.8) * duration_factor)
        tau_slow_min = 18.0 + (intensity * 22.0)  # 25 to 40 minutes time constant

        t = max(0.0, post_exercise_time_min)
        vo2_fast_t = a_fast * math.exp(-t / tau_fast_min)
        vo2_slow_t = a_slow * math.exp(-t / tau_slow_min)
        instant_vo2_ml_min = resting_vo2_ml_min + vo2_fast_t + vo2_slow_t

        # Integrated cumulative EPOC volume up to time t in liters
        # Integral of A * exp(-t/tau) from 0 to t = A * tau * (1 - exp(-t/tau))
        vol_fast_liters = (a_fast * tau_fast_min * (1.0 - math.exp(-t / tau_fast_min))) / 1000.0
        vol_slow_liters = (a_slow * tau_slow_min * (1.0 - math.exp(-t / tau_slow_min))) / 1000.0
        cumulative_epoc_liters = round(vol_fast_liters + vol_slow_liters, 3)

        # Total asymptotic EPOC volume (as t -> infinity)
        total_epoc_asymptotic_liters = round(((a_fast * tau_fast_min) + (a_slow * tau_slow_min)) / 1000.0, 3)

        # Energy expenditure: ~4.86 kcal per liter of O2 during post-exercise recovery
        epoc_calories_burned = round(cumulative_epoc_liters * 4.86, 1)
        total_projected_epoc_calories = round(total_epoc_asymptotic_liters * 4.86, 1)

        pct_recovery = round((cumulative_epoc_liters / max(0.01, total_epoc_asymptotic_liters)) * 100.0, 1)
        pct_recovery = min(100.0, pct_recovery)

        # Time to 95% total EPOC clearance (~ 3 * tau_slow)
        t_95_pct_min = round(3.0 * tau_slow_min, 1)

        if pct_recovery < 40.0:
            phase = "RAPID_ALACTACID_AND_LACTATE_CLEARANCE"
            refueling_advice = "Acute recovery window: prioritize fluid rehydration and rapid electrolyte replenishing."
        elif pct_recovery < 85.0:
            phase = "EXTENDED_METABOLIC_EPOC_AND_GLYCOGEN_SYNTHESIS"
            refueling_advice = "Elevated lipid oxidation state. Optimal timing for 3:1 carb-to-protein post-workout nutritional intake."
        else:
            phase = "APPROACHING_RESTING_BASAL_METABOLISM"
            refueling_advice = "Primary physiological homeostasis restored. Transition to passive parasympathetic recovery."

        return {
            "exercise_duration_min": exercise_duration_min,
            "exercise_intensity_pct": round(intensity * 100.0, 1),
            "body_mass_kg": body_mass_kg,
            "elapsed_recovery_min": t,
            "instantaneous_vo2_ml_min": round(instant_vo2_ml_min, 1),
            "resting_baseline_vo2_ml_min": round(resting_vo2_ml_min, 1),
            "cumulative_epoc_o2_liters": cumulative_epoc_liters,
            "total_projected_epoc_o2_liters": total_epoc_asymptotic_liters,
            "epoc_calories_expended_kcal": epoc_calories_burned,
            "total_projected_epoc_kcal": total_projected_epoc_calories,
            "recovery_completion_pct": pct_recovery,
            "estimated_95pct_recovery_min": t_95_pct_min,
            "recovery_phase": phase,
            "nutritional_strategy": refueling_advice
        }

    def evaluate_heart_rate_recovery_kinetics(
        self,
        current_hr_bpm: float,
        resting_hr_bpm: float,
        peak_exercise_hr_bpm: float,
        minutes_post_exercise: float
    ) -> Dict[str, Any]:
        """
        Evaluate heart rate recovery (HRR) clearance curve against expected vagal reactivation standards.
        HRR60 (drop in first 60s) >= 12 bpm is clinically normal; >= 25 bpm indicates superior cardiorespiratory fitness.
        """
        if peak_exercise_hr_bpm <= resting_hr_bpm:
            return {"error": "Peak exercise HR must be greater than resting HR"}

        total_elevation = peak_exercise_hr_bpm - resting_hr_bpm
        current_elevation = max(0.0, current_hr_bpm - resting_hr_bpm)
        hr_drop = peak_exercise_hr_bpm - current_hr_bpm

        fraction_recovered = max(0.0, min(1.0, 1.0 - (current_elevation / total_elevation)))

        if minutes_post_exercise <= 2.0:
            expected_fraction = 0.35
        elif minutes_post_exercise <= 10.0:
            expected_fraction = 0.65
        else:
            expected_fraction = 0.85

        vagal_reactivation_index = round((fraction_recovered / expected_fraction) * 100.0, 1)

        if vagal_reactivation_index >= 115.0:
            vagal_status = "SUPERIOR_VAGAL_REACTIVATION"
        elif vagal_reactivation_index >= 90.0:
            vagal_status = "NORMAL_PARASYMPATHETIC_RECOVERY"
        else:
            vagal_status = "BLUNTED_OR_DELAYED_RECOVERY"

        return {
            "current_hr_bpm": current_hr_bpm,
            "resting_hr_bpm": resting_hr_bpm,
            "peak_exercise_hr_bpm": peak_exercise_hr_bpm,
            "elapsed_minutes": minutes_post_exercise,
            "heart_rate_drop_bpm": round(hr_drop, 1),
            "recovery_fraction_pct": round(fraction_recovered * 100.0, 1),
            "vagal_reactivation_score": min(150.0, vagal_reactivation_index),
            "vagal_status": vagal_status,
            "recommendation": (
                "Parasympathetic reactivation robust. Safe to resume sedentary activities."
                if vagal_reactivation_index >= 90.0 else
                "Elevated cardiac work persists. Practice physiological sighing (double inhale, long exhale) to accelerate vagal brake."
            )
        }
