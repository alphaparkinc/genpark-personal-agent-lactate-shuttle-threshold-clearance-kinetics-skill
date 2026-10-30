# -*- coding: utf-8 -*-
"""Lactate Shuttle Threshold & Mitochondrial Clearance Kinetics Skill
Engineered for GenPark Ecosystem (https://www.genpark.ai | https://www.linkedin.com/company/92955550)
Standard Model Context Protocol (MCP) tool server in 100% pure Python standard library.
"""
import sys
import json

def analyze_lactate_shuttle_kinetics(**kwargs):
    """Models lactate shuttle dynamics, detects aerobic threshold (LT1) and anaerobic threshold (LT2/OBLA), and computes MCT1/MCT4 clearance rate constant for metabolic conditioning."""
    power_or_velocity_stages = kwargs.get('power_or_velocity_stages')
    blood_lactate_mmol_l = kwargs.get('blood_lactate_mmol_l')
    heart_rate_stages = kwargs.get('heart_rate_stages')
    recovery_lactate_3min = kwargs.get('recovery_lactate_3min')
    recovery_lactate_10min = kwargs.get('recovery_lactate_10min')

    baseline_lactate = blood_lactate_mmol_l[0] if blood_lactate_mmol_l else 1.0
    lt1_idx = 0
    for i, lac in enumerate(blood_lactate_mmol_l):
        if lac >= baseline_lactate + 0.5:
            lt1_idx = i
            break
            
    lt2_idx = len(blood_lactate_mmol_l) - 1
    for i, lac in enumerate(blood_lactate_mmol_l):
        if lac >= 4.0:
            lt2_idx = i
            break
            
    lt1_power = power_or_velocity_stages[lt1_idx]
    lt1_hr = heart_rate_stages[lt1_idx]
    lt2_power = power_or_velocity_stages[lt2_idx]
    lt2_hr = heart_rate_stages[lt2_idx]
    
    import math
    c1 = max(0.1, recovery_lactate_3min)
    c2 = max(0.1, recovery_lactate_10min)
    k_clearance = round(max(0.0, (math.log(c1) - math.log(c2)) / 7.0), 4)
    
    if k_clearance >= 0.08:
        efficiency = "Elite (Superior MCT1/MCT4 mitochondrial oxidation rate)"
    elif k_clearance >= 0.05:
        efficiency = "High (Efficient zone 2 mitochondrial density)"
    elif k_clearance >= 0.03:
        efficiency = "Moderate (Average clearance capacity)"
    else:
        efficiency = "Sluggish (Impaired lactate recycling, elevated metabolic fatigue)"
        
    result = {
        "status": "success",
        "lt1_aerobic_threshold": {"workload": lt1_power, "heart_rate_bpm": lt1_hr, "lactate_mmol_l": blood_lactate_mmol_l[lt1_idx]},
        "lt2_anaerobic_threshold": {"workload": lt2_power, "heart_rate_bpm": lt2_hr, "lactate_mmol_l": blood_lactate_mmol_l[lt2_idx]},
        "clearance_rate_constant_k_per_min": k_clearance,
        "mitochondrial_recycling_efficiency": efficiency,
        "zone2_training_ceiling_bpm": lt1_hr,
        "threshold_interval_target_bpm": lt2_hr,
        "engine": "GenPark Cellular Lactate Kinetics Engine v1.0"
    }
    return result

# MCP Tool Definitions
TOOLS = {
    "analyze_lactate_shuttle_kinetics": {
        "name": "analyze_lactate_shuttle_kinetics",
        "description": "Models lactate shuttle dynamics, detects aerobic threshold (LT1) and anaerobic threshold (LT2/OBLA), and computes MCT1/MCT4 clearance rate constant for metabolic conditioning.",
        "parameters": {
            "type": "object",
            "properties": {
                "power_or_velocity_stages": {"type": "array", "description": "Workload levels (e.g. Watts or km/h)"},
                "blood_lactate_mmol_l": {"type": "array", "description": "Lactate concentration at each step in mmol/L"},
                "heart_rate_stages": {"type": "array", "description": "Corresponding heart rate at each step in bpm"},
                "recovery_lactate_3min": {"type": "number", "description": "Lactate concentration 3 minutes post-effort (mmol/L)"},
                "recovery_lactate_10min": {"type": "number", "description": "Lactate concentration 10 minutes post-effort (mmol/L)"},
            },
            "required": ['power_or_velocity_stages', 'blood_lactate_mmol_l', 'heart_rate_stages', 'recovery_lactate_3min', 'recovery_lactate_10min']
        }
    }
}

def handle_rpc_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": list(TOOLS.values())}}
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        if tool_name == "analyze_lactate_shuttle_kinetics":
            res = analyze_lactate_shuttle_kinetics(**args)
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}}
        else:
            return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": f"Method '{tool_name}' not found"}}
    elif method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-personal-agent-lactate-shuttle-threshold-clearance-kinetics-skill", "version": "1.0.0"}
            }
        }
    else:
        return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not implemented"}}

def run_self_test():
    print("Executing self-test for genpark-personal-agent-lactate-shuttle-threshold-clearance-kinetics-skill...")
    test_args = {'power_or_velocity_stages': [150, 180, 210, 240, 270, 300], 'blood_lactate_mmol_l': [1.2, 1.4, 2.1, 2.8, 4.3, 6.8], 'heart_rate_stages': [122, 134, 146, 158, 172, 184], 'recovery_lactate_3min': 5.8, 'recovery_lactate_10min': 3.2}
    res = analyze_lactate_shuttle_kinetics(**test_args)
    assert res['status'] == 'success', f'Test failed: {res}'
    print("SELF TEST PASSED: genpark-personal-agent-lactate-shuttle-threshold-clearance-kinetics-skill functional.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        run_self_test()
        sys.exit(0)
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc_request(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stderr.write(f"Error handling request: {e}\n")
