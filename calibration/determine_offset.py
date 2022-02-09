from scenario import monopod as scenario


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


print(f'{bcolors.HEADER}Please refer to calibration docummentation ' +
      f'if confused at any point during the calibration. {bcolors.ENDC}')

input(f'{bcolors.OKBLUE}Set robot leg to be straight (approximately 0) '
      'then reset the Ti evaluation Board. When successful please press '
      f'enter to continue. {bcolors.ENDC}')

world = scenario.World()
world.initialize(scenario.Mode_motor_board)

model_name = world.model_names()[0]
model = world.get_model(model_name)

for joint in model.joints():
    # name = joint.name()
    max = 1.57
    min = -1.57
    scenario.ToMonopodJoint(joint).set_joint_position_limit(max, min)
    # scenario.ToMonopodJoint(joint).set_joint_velocity_limit(max, min)

print(f'{bcolors.OKGREEN}Successfully established connection to robot. {bcolors.ENDC}')
# print('To exit type exit at any input.')
input(f'{bcolors.OKBLUE}Press enter when robot is safe to move. {bcolors.ENDC}')

print(f'{bcolors.WARNING}Searching for the first encoder index position in '
      f'positive direction... Please stay clear of leg. {bcolors.ENDC}')

scenario.ToMonopodModel(model).calibrate(0, 0)

input(f'{bcolors.OKBLUE}Press enter after installing calibration jigs '
              f'onto hip and knee joint {bcolors.ENDC}')

offset_poss = model.joint_positions(['hip_joint', 'knee_joint'])

print(f'{bcolors.OKGREEN}Found calibration offsets [hip_offset, knee_offset]: '
      f'{offset_poss} {bcolors.ENDC}')

input(f'{bcolors.OKBLUE}Testing offset location. Please press enter when '
      f'robot is safe to move and jigs are removed. {bcolors.ENDC}')

scenario.ToMonopodModel(model).calibrate(offset_poss[0], offset_poss[1])

print(f'{bcolors.OKGREEN}Calibration successful if position matches location '
      f'of jig. {bcolors.ENDC}')
