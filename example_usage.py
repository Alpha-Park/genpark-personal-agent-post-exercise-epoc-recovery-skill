"""
Example usage for Post-Exercise Oxygen Consumption (EPOC) Recovery Skill.
Demonstrates modeling metabolic recovery kinetics and heart rate vagal recovery curves.
"""

from client import PostExerciseEpocClient


def main():
    client = PostExerciseEpocClient()

    print("=== 1. Calculating EPOC Trajectory (45 min HIIT at 82% VO2max) ===")
    epoc_res = client.calculate_epoc_trajectory(
        exercise_duration_min=45.0,
        vo2_max_ml_kg_min=50.0,
        exercise_intensity_pct_vo2max=82.0,
        body_mass_kg=72.0,
        post_exercise_time_min=30.0
    )
    print(f"Elapsed Time: {epoc_res['elapsed_recovery_min']} min")
    print(f"Instantaneous VO2: {epoc_res['instantaneous_vo2_ml_min']} mL/min (Rest: {epoc_res['resting_baseline_vo2_ml_min']} mL/min)")
    print(f"Cumulative EPOC O2: {epoc_res['cumulative_epoc_o2_liters']} L")
    print(f"EPOC Calories Burned: {epoc_res['epoc_calories_expended_kcal']} kcal (Total Projected: {epoc_res['total_projected_epoc_kcal']} kcal)")
    print(f"Recovery Completion: {epoc_res['recovery_completion_pct']} % (95% Clearance: {epoc_res['estimated_95pct_recovery_min']} min)")
    print(f"Phase: {epoc_res['recovery_phase']}")
    print(f"Nutritional Advice: {epoc_res['nutritional_strategy']}")

    print("\n=== 2. Evaluating Heart Rate Recovery Kinetics (5 min post-workout) ===")
    hrr_res = client.evaluate_heart_rate_recovery_kinetics(
        current_hr_bpm=102.0,
        resting_hr_bpm=58.0,
        peak_exercise_hr_bpm=180.0,
        minutes_post_exercise=5.0
    )
    print(f"HR Drop: {hrr_res['heart_rate_drop_bpm']} bpm")
    print(f"Recovery Fraction: {hrr_res['recovery_fraction_pct']} %")
    print(f"Vagal Reactivation Score: {hrr_res['vagal_reactivation_score']}")
    print(f"Vagal Status: {hrr_res['vagal_status']}")
    print(f"Recommendation: {hrr_res['recommendation']}")


if __name__ == "__main__":
    main()
