"""Builds a headless SolidCraft script (left side + body) at hip height H and runs inspect.clearance on the coarse
bodies. usage: python3 gen_pose_checks.py H OUT.json   then   solidcraft-cli run OUT.json --quiet --results --json-out R.json
Poses: thigh/shank/coupler rigid-link moves from the nominal (h195) CAD, from build_leg.py kinematics (no gears, no bushings)."""
import sys, json, math, importlib.util
H = float(sys.argv[1]); OUT = sys.argv[2]; WONLY = len(sys.argv) > 3 and sys.argv[3] == "wheel"; IN_ARG = sys.argv[4] if len(sys.argv) > 4 else None
IN = sys.argv[4] if len(sys.argv) > 4 else "/tmp/solidcraft-mcp-171537-36af69a1/in/"
spec = importlib.util.spec_from_file_location("bl", "/run/media/jo_engineer/Engineer files/0- AI Created/Balance Robot with AI/cad/parts/src/build_leg.py")
bl = importlib.util.module_from_spec(spec); sys.argv = ["x"]; spec.loader.exec_module(bl)
HIP = (28., 280.)
pn, pp = bl.pose_h(195.), bl.pose_h(H)
W0x = HIP[0] + pn['W'][0]                 # axle x at nominal: leg CAD puts it here (not 0)
C = []
def cmd(c, **p): C.append({"command": c, "params": p})
def rot(pt, d):
    c, s = math.cos(math.radians(d)), math.sin(math.radians(d)); return (pt[0]*c - pt[1]*s, pt[0]*s + pt[1]*c)
def rigid(bodies, d, piv_from, piv_to):
    """rotate by d deg (CCW in XZ) about piv_from, ending with piv_from at piv_to"""
    if abs(d) > 1e-9: cmd("solid.move", bodies=bodies, axis=[0, -1, 0], angle=f"{d} deg")
    r = rot(piv_from, d); cmd("solid.move", bodies=bodies, translate=[piv_to[0]-r[0], 0, piv_to[1]-r[1]])
STEP = lambda f: IN + f
cmd("file.insert_step", path=STEP("body.step"), name="Body")
cmd("solid.remove", bodies=["REF_HipHousing_L", "REF_HipHousing_R", "REF_HipRing_L", "REF_HipRing_R"])
cmd("file.insert_step", path=STEP("hip_gearbox.step"), name="HG", matrix=[1,0,0,28, 0,0,1,40, 0,-1,0,280])
cmd("solid.remove", bodies=["HG_Sun","HG_Planet_1","HG_Planet_2","HG_Planet_3","HG_CarrierIn","HG_Ring","B_685ZZ_1","B_685ZZ_2","B_685ZZ_3","B_685ZZ_4","B_685ZZ_5","B_685ZZ_6","B_Pin5x45_1","B_Pin5x45_2","B_Pin5x45_3"])
cmd("file.insert_step", path=STEP("wheel.step"), name="WH", matrix=[1,0,0,W0x, 0,0,1,80, 0,-1,0,85])
cmd("solid.remove", bodies=["WH_Sun","WH_Planet_1","WH_Planet_2","WH_Planet_3","WH_CarrierA","WH_CarrierB","WH_RingSleeve","B_685ZZ_1","B_685ZZ_2","B_685ZZ_3","B_685ZZ_4","B_685ZZ_5","B_685ZZ_6","B_Pin5x20_1","B_Pin5x20_2","B_Pin5x20_3","B_Magnet_D6x2.5","WH_MagHolder"])
for f in ["thigh","coupler","shank","plate","strap","arch","beam","posts","tpu","hw"]:
    cmd("file.insert_step", path=STEP(f"leg_{f}.step"), name="Leg_"+f)
LEG = ["Leg_Thigh","Leg_Coupler","Leg_Shank","Leg_ShankPlate","Leg_KneeStrap","Leg_ArchPlate","Leg_OutriggerBeam","Leg_ArchPost_142","Leg_ArchPost_162","Leg_StopPad_TPU","Leg_Bumper_Thigh_TPU","Leg_Bumper_Shank_TPU","Leg_Dot_TPU","Leg_Pin_K","Leg_Pin_C","Leg_Pin_B","Leg_Pin_Crank","Leg_Pin_Anchor","Leg_Bush_K_shank","Leg_Bush_K_thigh","Leg_Bush_K_strap","Leg_Bush_C_shank","Leg_Bush_C_coupler","Leg_Bush_C_strap","Leg_Bush_B_coupler","Leg_Brg_6806_outer","Leg_Spacer_K"]
cmd("solid.remove", bodies=["Leg_Spring_env"])   # rev 2 leg STEPs are already world coordinates (left)
# links
THIGH = ["Leg_HexSleeve","HG_CarrierOut","Leg_Thigh","Leg_Bush_K_thigh","Leg_Pin_Crank","Leg_Bumper_Thigh_TPU"]
SHANK = ["Leg_Shank","Leg_ShankPlate","Leg_KneeStrap","Leg_Pin_K","Leg_Pin_C","Leg_Bush_K_shank","Leg_Bush_K_strap","Leg_Bush_C_shank","Leg_Bush_C_strap","Leg_Spacer_K","Leg_Bumper_Shank_TPU"]
COUP = ["Leg_Coupler","Leg_Bush_C_coupler","Leg_Bush_B_coupler"]
Kw = lambda p: (HIP[0]+p['K'][0], HIP[1]+p['K'][1])
cang = lambda p: math.degrees(math.atan2(p['C'][1]-bl.B[1], p['C'][0]-bl.B[0]))
if abs(H-195) > 1e-6:
    rigid(THIGH, pp['th']-pn['th'], HIP, HIP)
    rigid(SHANK, pp['sh']-pn['sh'], Kw(pn), Kw(pp))
    # the wheel is a STEP component placed by a matrix: solid.move would use its local axes, so move the occurrence in world space
    cmd("occurrence.move", occurrence="WH:1", space="world", axis=[0,-1,0], angle=f"{pp['sh']-pn['sh']} deg", origin=[Kw(pn)[0], 0, Kw(pn)[1]])
    cmd("occurrence.move", occurrence="WH:1", space="world", translate=[Kw(pp)[0]-Kw(pn)[0], 0, Kw(pp)[1]-Kw(pn)[1]])
    Bw = (HIP[0]+bl.B[0], HIP[1]+bl.B[1])
    rigid(COUP, cang(pp)-cang(pn), Bw, Bw)
# spring: Ø13 cylinder, crank pin (-40 along thigh) to anchor pin, axis y=110
P = (HIP[0]-bl.CRANK*math.cos(math.radians(pp['th'])), HIP[1]-bl.CRANK*math.sin(math.radians(pp['th'])))
A = (HIP[0]+bl.ANCH[0], HIP[1]+bl.ANCH[1]); L = math.hypot(A[0]-P[0], A[1]-P[1])
cmd("solid.cylinder", radius=6.5, height=L, base=[P[0],111,P[1]], axis=[(A[0]-P[0])/L,0,(A[1]-P[1])/L], operation="new", body_name="Spring_cyl")
HOUS = ["HG_Skirt","HG_Cover","HG_AlPlate","REF_8308_KV130","HG_CarrierOut","B_6806"]
BODY = ["B1T_Tie_L","REF_Camera3","REF_IMU","REF_ESP32","REF_XDrive_hip_L","REF_XDrive_whl_L","B1_Side_L","B1S_HipSeat_L","B3_Lid","B4_Front","B5_Rear","B2_Tray","REF_DrvPlate_hip_L","REF_DrvPlate_whl_L","REF_Res_L","REF_Battery","REF_Pi4","REF_Fan","REF_ResBracket_Al1mm"]
WHL = ["WH_Tyre","WH_Hub","WH_Cover","WH_Axle","REF_MN5008"]
LEGB = [n for n in LEG if not any(k in n for k in ["Bush_","Spacer","Dot_"])] + ["Spring_cyl"]
cmd("inspect.clearance", bodies=WHL, against=HOUS+BODY+[n for n in LEG if "Arch" in n or "Beam" in n or "Outrigger" in n], clearance=80)
cmd("inspect.clearance", bodies=WHL, against=LEGB, clearance=8)
if not WONLY:
    cmd("inspect.clearance", bodies=LEGB, against=HOUS+BODY+WHL, clearance=8)
    cmd("inspect.clearance", bodies=LEGB, against=LEGB, clearance=8)
json.dump({"commands": C}, open(OUT, "w"))
print(len(C), "commands; hip x rel axle", -pp['W'][0], "th", pp['th'])
