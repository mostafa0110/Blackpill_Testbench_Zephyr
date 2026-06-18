#!/usr/bin/env bash
# Bootstrap the GitHub Issues board for the Blackpill Testbench:
# creates labels, 3 phase milestones, and 14 issues split by layer.
#
# Requirements: GitHub CLI authenticated  ->  gh auth login
# Usage:        edit SEIF below, then:  bash scripts/create_github_issues.sh
set -euo pipefail

REPO="mostafa0110/Blackpill_Testbench_Zephyr"
MOSTAFA="mostafa0110"
SEIF="Seif-Gama1"   # <-- set Seif's GitHub username (must be a repo collaborator)

echo ">> Labels"
mklabel() { gh label create "$1" --color "$2" --description "$3" --repo "$REPO" --force >/dev/null; }
mklabel firmware        "1d76db" "Zephyr firmware layer"
mklabel host            "0e8a16" "Python host driver layer"
mklabel tests           "5319e7" "Robot Framework test layer"
mklabel shared          "fbca04" "Shared / integration"
mklabel "owner:mostafa" "c2e0c6" "Owned by Mostafa"
mklabel "owner:seif"    "bfd4f2" "Owned by Seif"

echo ">> Milestones"
mkmilestone() {
  gh api -X POST "repos/$REPO/milestones" -f title="$1" -f description="$2" >/dev/null 2>&1 || true
}
mkmilestone "Phase 1 - Foundation"            "Week 1: Zephyr workspace, UART + Shell, pyserial connection"
mkmilestone "Phase 2 - Hardware Control"      "Week 2: devicetree overlay, GPIO/PWM/ADC commands, Python API"
mkmilestone "Phase 3 - Automation Integration" "Week 3: Robot library, keywords, self-validation suite"

echo ">> Issues"
mkissue() { # title body milestone layer who
  local title="$1" body="$2" milestone="$3" layer="$4" who="$5"
  local args=(--repo "$REPO" --title "$title" --body "$body" --milestone "$milestone" --label "$layer")
  local owner_label="" assignee=""
  case "$who" in
    mostafa) owner_label="owner:mostafa"; assignee="$MOSTAFA" ;;
    seif)    owner_label="owner:seif";    assignee="$SEIF" ;;
    shared)  owner_label="";              assignee="$MOSTAFA" ;;
  esac
  [ -n "$owner_label" ] && args+=(--label "$owner_label")
  if [ -n "$assignee" ] && [ "$assignee" != "REPLACE_WITH_SEIF_GITHUB_USERNAME" ]; then
    args+=(--assignee "$assignee")
  fi
  gh issue create "${args[@]}"
}

# ---- Phase 1 ----
mkissue "Set up Zephyr/west workspace and build for blackpill_f401ce" \
  "Init west workspace, fetch Zephyr + STM32 HAL, build hello-world for the Blackpill (f401cc=256K / f401ce=512K)." \
  "Phase 1 - Foundation" firmware mostafa
mkissue "Configure USART2 + Zephyr Shell over UART (115200 8N1)" \
  "Enable shell + serial backend on USART2; confirm the 'uart>' prompt and 'tb' command tree respond." \
  "Phase 1 - Foundation" firmware mostafa
mkissue "Establish pyserial connection + base send/parse loop" \
  "Open the serial port, send a line, read the response; handle echo/prompt/blank-line filtering." \
  "Phase 1 - Foundation" host seif
mkissue "Finalize protocol v1 (command tree + OK/VAL/ERROR format)" \
  "Lock the tb command syntax and response/error grammar in docs/Protocol_Spec.md. Shared firmware+host sign-off." \
  "Phase 1 - Foundation" shared shared

# ---- Phase 2 ----
mkissue "Create app.overlay devicetree aliases" \
  "Define tb_out_1..4, tb_in_1..4, tb_pwm_1..2, tb_adc_1..2 in the zephyr,user node per docs/Hardware_Pinout.md." \
  "Phase 2 - Hardware Control" firmware mostafa
mkissue "Implement tb gpio set/get" \
  "Wire the GPIO handlers in src/tb_shell.c to the gpio_dt_spec arrays; return OK / VAL:." \
  "Phase 2 - Hardware Control" firmware mostafa
mkissue "Implement tb pwm set" \
  "Convert freq+duty to period/pulse ns and call pwm_set_dt; validate ranges." \
  "Phase 2 - Hardware Control" firmware mostafa
mkissue "Implement tb adc read" \
  "Read the ADC channel and convert raw->millivolts; return 'VAL: <n> mV'." \
  "Phase 2 - Hardware Control" firmware mostafa
mkissue "Implement Python API methods + parsing + exceptions" \
  "set_gpio/get_gpio/set_pwm/read_adc with response parsing and Testbench*Error exceptions." \
  "Phase 2 - Hardware Control" host seif
mkissue "Add host reliability: timeouts, retries, reconnect" \
  "Harden _send with the retry loop and reconnect-on-drop (the TODO in client.py)." \
  "Phase 2 - Hardware Control" host seif

# ---- Phase 3 ----
mkissue "Build Robot Framework library wrapping the Python API" \
  "Flesh out tests/TestbenchLibrary.py against the finished host driver." \
  "Phase 3 - Automation Integration" tests seif
mkissue "Author high-level Robot keywords" \
  "Set Testbench Pin High/Low, Testbench Input Should Be, Generate Testbench PWM, Verify Testbench ADC Voltage." \
  "Phase 3 - Automation Integration" tests seif
mkissue "Write self-validation suite with loopback harness" \
  "Loopback wiring (tb_out_1->tb_in_1, divider->tb_adc_1); expand tests/smoke.robot to validate the bench." \
  "Phase 3 - Automation Integration" tests seif
mkissue "Integration pass + documentation wrap-up" \
  "End-to-end run across all layers; finalize README and docs. Shared firmware+host+tests." \
  "Phase 3 - Automation Integration" shared shared

echo ">> Done."
