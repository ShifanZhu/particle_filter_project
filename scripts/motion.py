import random
import math

def Gauss(sigma):
    x1, x2, w = 0.0, 0.0, 0.0
    while w > 1.0 or w == 0.0:
        r = random.random()
        while r == 0.0:
            r = random.random()
        x1 = 2.0 * r - 1.0
        r = random.random()
        while r == 0.0:
            r = random.random()
        x2 = 2.0 * r - 1.0
        w = x1 * x1 + x2 * x2
    return sigma * x2 * math.sqrt(-2.0 * math.log(w) / w)


# Define the angle difference function
def AngleDiff(a, b):
    return math.atan2(math.sin(a - b), math.cos(a - b))

def UpdateMotion(pose0, pose1, pose):
    delta_rot1, delta_trans, delta_rot2 = 0, 0, 0
    delta_rot1_hat, delta_trans_hat, delta_rot2_hat = 0, 0, 0
    delta_rot1_noise, delta_rot2_noise = 0, 0
    alpha1, alpha2, alpha3, alpha4 = 0.01, 0.01, 0.01, 0.01

    delta_pose = [pose1[0]-pose0[0], pose1[1]-pose0[1], pose1[2]-pose0[2]]

    if math.sqrt(delta_pose[1]**2 + delta_pose[0]**2) < 0.01:
        delta_rot1 = 0.0
    else:
        delta_rot1 = AngleDiff(math.atan2(delta_pose[1], delta_pose[0]), pose0[2])

    delta_trans = math.sqrt(delta_pose[0]**2 + delta_pose[1]**2)
    delta_rot2 = AngleDiff(delta_pose[2], delta_rot1)

    delta_rot1_noise = min(abs(AngleDiff(delta_rot1,0.0)), abs(AngleDiff(delta_rot1,math.pi)))
    delta_rot2_noise = min(abs(AngleDiff(delta_rot2,0.0)), abs(AngleDiff(delta_rot2,math.pi)))

    delta_rot1_hat = AngleDiff(delta_rot1, 
                        Gauss(alpha1*delta_rot1_noise*delta_rot1_noise +
                                                  alpha2*delta_trans*delta_trans))
    delta_trans_hat = delta_trans - Gauss(alpha3*delta_trans*delta_trans + alpha4*delta_rot1_noise*delta_rot1_noise + alpha4*delta_rot2_noise*delta_rot2_noise)
    delta_rot2_hat = AngleDiff(delta_rot2, 
                        random.gauss(0.0, math.sqrt(alpha1*delta_rot2_noise*delta_rot2_noise + alpha2*delta_trans*delta_trans)))

    pose[0] += delta_trans_hat * math.cos(pose[2] + delta_rot1_hat)
    pose[1] += delta_trans_hat * math.sin(pose[2] + delta_rot1_hat)
    pose[2] += delta_rot1_hat + delta_rot2_hat
    return pose


pose0 = [10, 20, 0.5]
pose1 = [10, 21, 0.5]
pose = [10, 20, 0.5]

print('old pose: ', pose)
print('new pose: ', UpdateMotion(pose0, pose1, pose))

