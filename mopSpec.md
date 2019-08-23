# 2019-08-23 Specification mop

Use uvcdynctrl to interact with the camera (http://manpages.org/uvcdynctrl-023).

SET: uvcdynctrl -d VAR_CameraID -s 'VAR_ParamId' VALUE.

GET: uvcdynctrl -d VAR_CameraID -g 'VAR_ParamId'

## 0. Before you code
Measure the behavior for the motor because it automatically switches to fast after VAR_StepsBeforeMotorSpeedsUp time.
The other Things seem to work linearly at a certain speed.

Measure after how much relative change in absolute numbers it speeds up!
-> set this in VAR_StepsBeforeMotorSpeedsUp

## 1. Variables
Create for each setting three variables:

- VAR_ParamId: (from UVC -vc)
- VAR_CurrentState: current value element of {AUTO; a value in its range} (you read those from uvcctrl -vc)
- VAR_Stepping (you read those from uvcctrl -vc)
- VAR_MaxValue (you read those from uvcctrl -vc)
- VAR_MonValue (you read those from uvcctrl -vc)
- boolean VAR_IamIncreasing; determines if you want to count up or down

In addition the static variables:

- VAR_ControllerID
- VAR_CameraID
- VAR_StepsBeforeMotorSpeedsUp: N
- VAR_MovementThreshold: 30%
- VAR_MovementFastThreshold: 90%
- VAR_StorePresetTimeout: 2s

And:

- Array of arrays for the presets.

## 2. Determining Current Values
The program has to know the cameras current values for all settings when it does changes.

a) read it out if possible and reflect it to the variables while changes happen via the controller.

b) (obsolete as it should work) FallBack: Model it according to the measured behavior relative to the reset.
If you cannot read the current value:
Write a simulator for each of them The simulator should always give you the current value.
If you can get the current value you can skip this BUT for the Pan/ Tilt as you have to know when it switches state!

## 3 GUI (ALL Command line?!)
Show All analog inputs in one line each:

- TOP Left/Right | SettingName | CurrentValue
- LEFT Joystick Left/Right | SettingName | CurrentValue
- LEFT Joystick Up/Down | SettingName | CurrentValue
- RIGHT Joystick Left/Right | SettingName | CurrentValue
- RIGHT Joystick Up/Down | SettingName | CurrentValue

- Use the Start button to switch between the control elements. Make the currently selected bold.
- Use the Select button to switch between the controlled feature (update the info on the right accordingly!)
- - Use the third button to switch between AUTO and manual (if switched to manual just keep the current value)

- If a preset is stored display "PRESET %Name% stored"
with %Name% of {ControllerSetting1-5, SceneSetting1-5}.
- If a preset is called display "PRESET %Name% called"
with %Name% of {ControllerSetting1-5, SceneSetting1-5}.

- Display the last 5 commands issued as history.

## 3 Control Logic
### Start
Reset()

### Reset
- LED -> off
- -> all settings auto => set to auto
- -> exec reset => set position to 0,0 (uvc and model)

### Changes
Changes happen via the analog inputs.

- if above 30%:
  - set localVarThisSetting_isChanging = 1
  - set uvc value of ThisSetting to MAX and keep the MODEL going (or READING the current which would be better).
- if (below 30% && localVarThisSetting_isChanging == 1):
  - set uvc value of ThisSetting to currentValue +1 (if currently increasing) or -1 (if decreasing); Do not set higher than MAX = if at max leave it.
  - set localVarThisSetting_isChanging = 0
  
The only ones that are tricky are those that change speed on their own (only PAN/TILT?):
For that you know when it will change speed.
If the analog control is pressed between 30% and 90% PREVENT the change!

To do so set a target to currentValue +/- VAR_StepsBeforeMotorSpeedsUp.
The wait until the current position is there and the set it to +/- VAR_StepsBeforeMotorSpeedsUp again until the max is reached.

### Presets
All remaining buttons that are not used by the interface (analog, select button, select feature) are for presets.

Preset = store all current settings.

- Store preset = Press button for longer than VAR_StorePresetTimeout.
- Call preset = Press button for less than VAR_StorePresetTimeout:
Reflect all values from this Preset to the camera (and the model).

Use the left five binary buttons  for controller configs and the right five for camera positions.

Store All Presets ON DISK to keep them persistent over script restarts (Filename PRESET_{CTRL_VAR_ControllerID,SCNE_VAR_CameraID}).
