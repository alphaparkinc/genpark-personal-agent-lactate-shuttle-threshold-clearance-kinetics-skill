# Lactate Shuttle Threshold & Mitochondrial Clearance Kinetics Skill
[![GenPark](https://img.shields.io/badge/Powered%20By-GenPark.ai-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/Connect-LinkedIn-0077b5)](https://www.linkedin.com/company/92955550)
[![Python](https://img.shields.io/badge/Python-3.8%2B-green.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-Apache%202.0-yellow.svg)](LICENSE)

An industrial-grade Model Context Protocol (MCP) server providing `analyze_lactate_shuttle_kinetics`. Built with **100% pure Python standard library** (zero pip dependencies).

## Overview
Models lactate shuttle dynamics, detects aerobic threshold (LT1) and anaerobic threshold (LT2/OBLA), and computes MCT1/MCT4 clearance rate constant for metabolic conditioning.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate Entity**: [GenPark Inc on LinkedIn](https://www.linkedin.com/company/92955550)
- **Domain Category**: `Personal Agent (Bio / Metabolic Conditioning)`

## MCP Tool Specification
### `analyze_lactate_shuttle_kinetics`
Parameters:
- `power_or_velocity_stages` (list): Workload levels (e.g. Watts or km/h)
- `blood_lactate_mmol_l` (list): Lactate concentration at each step in mmol/L
- `heart_rate_stages` (list): Corresponding heart rate at each step in bpm
- `recovery_lactate_3min` (float): Lactate concentration 3 minutes post-effort (mmol/L)
- `recovery_lactate_10min` (float): Lactate concentration 10 minutes post-effort (mmol/L)

### Self-Test
```bash
python skills.py --test
```

### Model Context Protocol Integration (Claude Desktop / Cursor / Antigravity)
Add to your `mcpServers` configuration:
```json
{
  "mcpServers": {
    "genpark-personal-agent-lactate-shuttle-threshold-clearance-kinetics-skill": {
      "command": "python",
      "args": ["/path/to/genpark-personal-agent-lactate-shuttle-threshold-clearance-kinetics-skill/skills.py"]
    }
  }
}
```

## License
Licensed under Apache License 2.0. Copyright (c) 2026 GenPark Inc. (https://www.genpark.ai).
