"""Hex sleeve / thigh vs gearbox output carrier (hex 26 A/F, sleeve inner 26.3 A/F), nominal pose (the pair rotates together, so the fit is the same at every hip height).
python3 gen_hex_check.py OUT.json IN_DIR ; solidcraft-cli run OUT.json --quiet --results --json-out R.json"""
import sys, json
IN = sys.argv[2]
rm = ["REF_8308_KV130","HG_CarrierIn","HG_AlPlate","B_685ZZ_1","B_685ZZ_2","B_Pin5x45_1","B_685ZZ_3","B_685ZZ_4","B_Pin5x45_2","B_685ZZ_5","B_685ZZ_6","B_Pin5x45_3","B_6806","REF_Encoder_env_D30x8","REF_Magnet_D6x2.5","HG_Sun","HG_Planet_1","HG_Planet_2","HG_Planet_3","HG_Ring","HG_Skirt"]
C = [{"command": "file.insert_step", "params": {"path": IN + "hip_gearbox.step", "name": "HG", "matrix": [1,0,0,28, 0,0,1,40, 0,-1,0,280]}},
     {"command": "solid.remove", "params": {"bodies": rm}},
     {"command": "file.insert_step", "params": {"path": IN + "leg_thigh.step", "name": "Leg_thigh"}},
     {"command": "file.insert_step", "params": {"path": IN + "leg_hw.step", "name": "Leg_hw"}},
     {"command": "solid.remove", "params": {"bodies": [b for b in ["Leg_Pin_K","Leg_Pin_C","Leg_Pin_B","Leg_Pin_Crank","Leg_Pin_Anchor","Leg_Bush_K_shank","Leg_Bush_K_thigh","Leg_Bush_K_strap","Leg_Bush_C_shank","Leg_Bush_C_coupler","Leg_Bush_C_strap","Leg_Bush_B_coupler","Leg_Spacer_K","Leg_Spring_env"]]}},
     {"command": "inspect.clearance", "params": {"bodies": ["Leg_HexSleeve", "Leg_Thigh", "Leg_Brg_6806_outer"], "against": ["HG_CarrierOut", "HG_Cover"], "clearance": 3}}]
json.dump({"commands": C}, open(sys.argv[1], "w"))
