# Lab 2: Closed-Loop Controller
## ME 405 
#### **Authors: Tristan Cavarno, Miloh Padgett, Jon Abraham**

This lab involves implementing a closed-loop motor controller to set the position of a motor's output shaft. 
The performance of the controller is tested by observing the step response for a given positional setpoint
and is tuned by changing the motor gain.

### Motor Controller
Positional (P) control is utilized to control the torque of the motor. The gain, *K<sub>P</sub>*, defines the ratio of 
the output torque (% duty cycle) to positional error (measured in encoder ticks). 

The PController object is defined with methods that allow a user or program to set the gain and setpoint. 
To run the controller, the encoder reading must be passed into the PController.run() method. By multiplying the error (current encoder
reading - last encoder reading) by *K<sub>P</sub>*, a duty cyle is returned to be input into a motor driver. 
The output duty cycle is restricted to a range of [-100, 100].



### Step Response Tests
Step response tests were performed for various values of *K<sub>P</sub>* to help determine an appropriate gain. The goal 
is to maximize the speed of the motor while minimizing overshoot, oscillation, and steady-state error. To achieve nearly a single rotation, 
the setpoint was set at 1000 encoder ticks. ***K<sub>P</sub>* = 0.029** was determined to be the ideal motor gain.
The results of three different cases of step responses are included below. 

![Figure 1. Underdamped Step Response](underdamped_k_01.png)

**Figure 1.** Underdamped Step Response, where *K<sub>P</sub>* = 0.01. There is minimal overshoot but the motor approaches slowly with a large 
steady-state error. This is likely due to the inertia of the flywheel. 

![Figure 2. Overdamped Step Response](overdamped_k_3.png)

**Figure 2.** Overdamped Step Response, where *K<sub>P</sub>* = 0.03. The motor greatly overshoots the setpoint and steadily oscillates
until reaching equilibrium. 

![Figure 3. Well-Performing Step Response](best_performance_k_029.png)

**Figure 3.** Underdamped Step Response, where *K<sub>P</sub>* = 0.029. The motor quickly reaches the setpoint with some overshoot but 
less steady-state error than other cases. 
