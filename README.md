# lino_nav_tune

This is an experimental package that hopes to collate set of tools to tune Linorobot's Navigation Stack.

## Calculating maximum acceleration
This requires two inputs - the max velocity of the robot and the axis of movement.

     rosrun lino_nav_tune get_accel.py <axis of movement> <max velocity>

