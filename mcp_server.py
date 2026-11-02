"""
MCP Server for Post-Exercise Oxygen Consumption (EPOC) & Metabolic Recovery Kinetics.
Exposes JSON-RPC endpoints for bi-exponential EPOC modeling and heart rate recovery assessment.
"""

import json
import sys
from client import PostExerciseEpocClient

client = PostExerciseEpocClient()


def handle_request(request: dict) -> dict:
    req_id = request.get("id")
    method = request.get("method")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "calculate_epoc_trajectory",
                        "description": "Calculates post-exercise oxygen consumption (EPOC), caloric burn, recovery percentage, and substrate refueling timeline using Gaesser-Brooks bi-exponential kinetics.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "exercise_duration_min": {"type": "number", "description": "Duration of intense training session in minutes"},
                                "vo2_max_ml_kg_min": {"type": "number", "description": "User VO2 max in mL/kg/min"},
                                "exercise_intensity_pct_vo2max": {"type": "number", "description": "Average exercise intensity as % of VO2max (e.g. 80.0 for 80%)"},
                                "body_mass_kg": {"type": "number", "description": "Subject body mass in kilograms"},
                                "post_exercise_time_min": {"type": "number", "default": 60.0, "description": "Elapsed time post workout cessation in minutes"}
                            },
                            "required": ["exercise_duration_min", "vo2_max_ml_kg_min", "exercise_intensity_pct_vo2max", "body_mass_kg"]
                        }
                    },
                    {
                        "name": "evaluate_heart_rate_recovery_kinetics",
                        "description": "Evaluates autonomic vagal reactivation and parasympathetic tone from heart rate recovery kinetics.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "current_hr_bpm": {"type": "number", "description": "Current heart rate in BPM"},
                                "resting_hr_bpm": {"type": "number", "description": "Baseline resting heart rate in BPM"},
                                "peak_exercise_hr_bpm": {"type": "number", "description": "Peak heart rate reached during workout in BPM"},
                                "minutes_post_exercise": {"type": "number", "description": "Minutes elapsed since workout cessation"}
                            },
                            "required": ["current_hr_bpm", "resting_hr_bpm", "peak_exercise_hr_bpm", "minutes_post_exercise"]
                        }
                    }
                ]
            }
        }

    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "calculate_epoc_trajectory":
            res = client.calculate_epoc_trajectory(
                exercise_duration_min=args.get("exercise_duration_min", 45.0),
                vo2_max_ml_kg_min=args.get("vo2_max_ml_kg_min", 45.0),
                exercise_intensity_pct_vo2max=args.get("exercise_intensity_pct_vo2max", 75.0),
                body_mass_kg=args.get("body_mass_kg", 75.0),
                post_exercise_time_min=args.get("post_exercise_time_min", 60.0)
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }

        elif tool_name == "evaluate_heart_rate_recovery_kinetics":
            res = client.evaluate_heart_rate_recovery_kinetics(
                current_hr_bpm=args.get("current_hr_bpm", 95.0),
                resting_hr_bpm=args.get("resting_hr_bpm", 60.0),
                peak_exercise_hr_bpm=args.get("peak_exercise_hr_bpm", 175.0),
                minutes_post_exercise=args.get("minutes_post_exercise", 5.0)
            )
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
            }

        else:
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "error": {"code": -32601, "message": f"Method {tool_name} not found"}
            }

    return {
        "jsonrpc": "2.0",
        "id": req_id,
        "error": {"code": -32600, "message": "Invalid Request"}
    }


def main():
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
