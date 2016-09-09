#!/usr/bin/env python

from time import sleep

from smach import State, StateMachine


class Drive(State):
    def __init__(self, distance):
        State.__init__(self, outcomes=['success'])
        self.distance = distance

    def execute(self, userdata):
        print('Driving', self.distance)
        sleep(1)
        return 'success'


class Turn(State):
    def __init__(self, angle):
        State.__init__(self, outcomes=['success'])
        self.angle = angle

    def execute(self, userdata):
        print('Turning', self.angle)
        sleep(1)
        return 'success'


if __name__ == '__main__':
    triangle = StateMachine(outcomes=['success'])
    with triangle:
        StateMachine.add('SIDE1', Drive(1), transitions={'success': 'TURN1'})
        StateMachine.add('TURN1', Turn(120), transitions={'success': 'SIDE2'})
        StateMachine.add('SIDE2', Drive(1), transitions={'success': 'TURN2'})
        StateMachine.add('TURN2', Turn(120), transitions={'success': 'SIDE3'})
        StateMachine.add('SIDE3', Drive(1), transitions={'success': 'success'})

    square = StateMachine(outcomes=['success'])
    with square:
        StateMachine.add('SIDE1', Drive(1), transitions={'success': 'TURN1'})
        StateMachine.add('TURN1', Turn(90), transitions={'success': 'SIDE2'})
        StateMachine.add('SIDE2', Drive(1), transitions={'success': 'TURN2'})
        StateMachine.add('TURN2', Turn(90), transitions={'success': 'SIDE3'})
        StateMachine.add('SIDE3', Drive(1), transitions={'success': 'TURN3'})
        StateMachine.add('TURN3', Turn(90), transitions={'success': 'SIDE4'})
        StateMachine.add('SIDE4', Drive(1), transitions={'success': 'success'})

    shapes = StateMachine(outcomes=['success'])
    with shapes:
        StateMachine.add('TRIANGLE', triangle,
                         transitions={'success': 'SQUARE'})
        StateMachine.add('SQUARE', square, transitions={'success': 'success'})

    shapes.execute()
