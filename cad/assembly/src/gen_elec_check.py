"""Body electronics vs the hip stack (both sides) and IMU-motor distance; static, nominal.
python3 gen_elec_check.py OUT.json IN_DIR ; solidcraft-cli run OUT.json --quiet --results --json-out R.json"""
import sys, json
IN = sys.argv[2]
gears = ["HG_Sun","HG_Planet_1","HG_Planet_2","HG_Planet_3","HG_CarrierIn","HG_Ring","B_685ZZ_1","B_685ZZ_2","B_685ZZ_3","B_685ZZ_4","B_685ZZ_5","B_685ZZ_6","B_Pin5x45_1","B_Pin5x45_2","B_Pin5x45_3","REF_Encoder_env_D30x8","REF_Magnet_D6x2.5"]
HG = ["HG_Skirt","HG_Cover","HG_AlPlate","REF_8308_KV130","HG_CarrierOut","B_6806"]
C = [{"command": "file.insert_step", "params": {"path": IN + "body.step", "name": "Body"}},
     {"command": "solid.remove", "params": {"bodies": ["REF_HipHousing_L","REF_HipHousing_R","REF_HipRing_L","REF_HipRing_R"]}},
     {"command": "file.insert_step", "params": {"path": IN + "hip_gearbox.step", "name": "HG", "matrix": [1,0,0,28, 0,0,1,40, 0,-1,0,280]}},
     {"command": "solid.remove", "params": {"bodies": gears}},
     {"command": "solid.mirror", "params": {"bodies": HG, "plane": "XZ"}}]
HGall = HG + [n + " (2)" for n in HG]
ELEC = ["REF_Res_L","REF_Res_R","REF_ResBracket_Al1mm","REF_Pi4","REF_Camera3","REF_XDrive_hip_L","REF_XDrive_hip_R","REF_XDrive_whl_L","REF_XDrive_whl_R","REF_ESP32","REF_Battery","B7a_PiDeck","B2b_Cradle","REF_Fan","REF_DrvPlate_hip_L","REF_DrvPlate_hip_R"]
C.append({"command": "inspect.clearance", "params": {"bodies": ELEC, "against": HGall, "clearance": 6}})
C.append({"command": "inspect.clearance", "params": {"bodies": ["REF_IMU"], "against": ["REF_8308_KV130", "REF_8308_KV130 (2)", "REF_Pi4", "REF_ESP32", "B7a_PiDeck"], "clearance": 100}})
C.append({"command": "inspect.clearance", "params": {"bodies": ["B1T_Tie_L", "B1T_Tie_R", "B1_Side_L", "B1_Side_R", "B3_Lid", "B4_Front", "B2_Tray", "B1S_HipSeat_L", "B1S_HipSeat_R"], "against": HGall, "clearance": 3}})
json.dump({"commands": C}, open(sys.argv[1], "w"))
