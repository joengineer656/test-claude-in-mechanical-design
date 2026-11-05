"""Gearbox homing tab (HG_CarrierOut) vs cover stop blocks / skirt / ring at a thigh angle.
python3 gen_tab_check.py THIGH_DEG OUT.json IN_DIR ; solidcraft-cli run OUT.json --quiet --results --json-out R.json
Left gearbox only; the carrier is rotated rigidly about the hip axis (world x 28, z 280, along Y) from the nominal -24.26 deg."""
import sys, math
th, OUT, IN = float(sys.argv[1]), sys.argv[2], sys.argv[3]
C = [{"command": "file.insert_step", "params": {"path": IN + "hip_gearbox.step", "name": "HG", "matrix": [1,0,0,28, 0,0,1,40, 0,-1,0,280]}}]
keep = {"HG_CarrierOut", "HG_Cover", "HG_Skirt", "HG_Ring"}
allb = ["REF_8308_KV130","HG_CarrierIn","HG_AlPlate","B_685ZZ_1","B_685ZZ_2","B_Pin5x45_1","B_685ZZ_3","B_685ZZ_4","B_Pin5x45_2","B_685ZZ_5","B_685ZZ_6","B_Pin5x45_3","B_6806","REF_Encoder_env_D30x8","REF_Magnet_D6x2.5","HG_Sun","HG_Planet_1","HG_Planet_2","HG_Planet_3"]
C.append({"command": "solid.remove", "params": {"bodies": allb}})
d = th + 24.259475   # rotation of the carrier from the nominal pose (the carrier lives in a STEP component, so rotate it through the insert matrix of a 2nd copy, not solid.move; only names that collide get ' (2)')
c, s = math.cos(math.radians(d)), math.sin(math.radians(d)); px, pz = 28, 280
M = [[1,0,0,28],[0,0,1,40],[0,-1,0,280]]
R = [[c,0,s],[0,1,0],[-s,0,c]]   # rotates (x,z) CCW by d about +Y-down; same convention as the pose script
def mm(R, M):
    o = [[sum(R[i][k]*M[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    t = [R[i][0]*(M[0][3]-px) + R[i][1]*M[1][3] + R[i][2]*(M[2][3]-pz) for i in range(3)]
    return [o[0]+[t[0]+px], o[1]+[t[1]], o[2]+[t[2]+pz]]
Mr = mm([[c,0,-s],[0,1,0],[s,0,c]], M)
C.append({"command": "file.insert_step", "params": {"path": IN + "hip_gearbox.step", "name": "HC", "matrix": sum(Mr, [])}})
C.append({"command": "solid.remove", "params": {"bodies": allb + ["HG_Cover (2)", "HG_Skirt (2)", "HG_Ring (2)"]}})
C.append({"command": "inspect.clearance", "params": {"bodies": ["HG_CarrierOut (2)"], "against": ["HG_Cover", "HG_Skirt", "HG_Ring"], "clearance": 10}})
import json; json.dump({"commands": C}, open(OUT, "w"))
