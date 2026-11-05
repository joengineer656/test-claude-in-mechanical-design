"""Builds the full robot assembly (headless) at nominal stance (hip 195).
python3 gen_assembly.py OUT.json ; solidcraft-cli run OUT.json --save cad/assembly/robot_assembly.solidcraft --out exports/step/robot_assembly.step
STEP inputs are copied to IN (SolidCraft's sandbox).  Frames: see docs/assembly.md section 2."""
import sys, json, importlib.util
IN = (sys.argv[2] if len(sys.argv) > 2 else "/tmp/solidcraft-mcp-171537-36af69a1/in/")   # dir with the rev 2 part STEPs (body, hip_gearbox, wheel, leg_*, ld19.stp)
SRC = "/run/media/jo_engineer/Engineer files/0- AI Created/Balance Robot with AI/cad/parts/src/build_leg.py"
spec = importlib.util.spec_from_file_location("bl", SRC); bl = importlib.util.module_from_spec(spec); a = sys.argv; sys.argv = ["x"]; spec.loader.exec_module(bl); sys.argv = a
W0x = 28 + bl.pose_h(195.)['W'][0]     # -9.088: the axle of the leg CAD at nominal
C = []
def cmd(c, **p): C.append({"command": c, "params": p})
HG = ["REF_8308_KV130","HG_Sun","HG_Planet_1","HG_Planet_2","HG_Planet_3","HG_CarrierIn","HG_AlPlate","B_685ZZ_1","B_685ZZ_2","B_Pin5x45_1","B_685ZZ_3","B_685ZZ_4","B_Pin5x45_2","B_685ZZ_5","B_685ZZ_6","B_Pin5x45_3","B_6806","REF_Encoder_env_D30x8","REF_Magnet_D6x2.5","HG_Ring","HG_Cover","HG_Skirt","HG_CarrierOut"]
WH = ["WH_Axle","WH_RingSleeve","WH_Sun","WH_Planet_1","WH_Planet_2","WH_Planet_3","WH_CarrierA","WH_CarrierB","WH_Hub","WH_Cover","WH_Tyre","REF_MN5008","B_6806_1","B_6806_2","B_685ZZ_1","B_685ZZ_2","B_Pin5x20_1","B_685ZZ_3","B_685ZZ_4","B_Pin5x20_2","B_685ZZ_5","B_685ZZ_6","B_Pin5x20_3","REF_EncBoard_D30x8","WH_MagHolder","B_Magnet_D6x2.5"]
LG = ["Leg_Thigh","Leg_Coupler","Leg_Shank","Leg_ShankPlate","Leg_KneeStrap","Leg_ArchPlate","Leg_OutriggerBeam","Leg_ArchPost_142","Leg_ArchPost_162","Leg_StopPad_TPU","Leg_Bumper_Thigh_TPU","Leg_Bumper_Shank_TPU","Leg_Dot_TPU","Leg_Pin_K","Leg_Pin_C","Leg_Pin_B","Leg_Pin_Crank","Leg_Pin_Anchor","Leg_Bush_K_shank","Leg_Bush_K_thigh","Leg_Bush_K_strap","Leg_Bush_C_shank","Leg_Bush_C_coupler","Leg_Bush_C_strap","Leg_Bush_B_coupler","Leg_Brg_6806_outer","Leg_Spacer_K","Leg_HexSleeve","Leg_Spring_env"]
def mirror_rename(names, pre, left_sfx="", right_sfx=" (2)", tag=("L", "R")):
    cmd("solid.mirror", bodies=[n + left_sfx for n in names], plane="XZ")
    for n in names: cmd("body.rename", body=n + left_sfx + right_sfx, name=f"{pre}{tag[1]}_{n}")
    for n in names: cmd("body.rename", body=n + left_sfx, name=f"{pre}{tag[0]}_{n}")
cmd("file.insert_step", path=IN + "body.step", name="Body")
cmd("solid.remove", bodies=["REF_HipHousing_L","REF_HipHousing_R","REF_HipRing_L","REF_HipRing_R","REF_Lidar"])
cmd("file.insert_step", path=IN + "hip_gearbox.step", name="HipGearbox_L", matrix=[1,0,0,28, 0,0,1,40, 0,-1,0,280])
mirror_rename(HG, "HG")
cmd("file.insert_step", path=IN + "wheel.step", name="Wheel_L", matrix=[1,0,0,W0x, 0,0,1,80, 0,-1,0,85])
mirror_rename(WH, "WH")
for f in ["thigh","coupler","shank","plate","strap","arch","beam","posts","tpu","hw"]:
    cmd("file.insert_step", path=IN + f"leg_{f}.step", name="Leg_" + f)
mirror_rename(LG, "Leg")   # rev 2 leg STEPs are world coordinates (left): right = true mirror about XZ
cmd("file.insert_step", path=IN + "ld19.stp", name="LD19", matrix=[1,0,0,-40, 0,0,-1,0, 0,1,0,378.2])
cmd("body.rename", body="00_LD19-TOF_WAIFA", name="REF_LD19")
cmd("body.rename", body="PA2X6", name="REF_LD19_part")
cmd("inspect.measure")   # per-body volume/CoM/bbox for com_assembly.py (--json-out)
json.dump({"commands": C}, open(sys.argv[1], "w")); print(len(C))
