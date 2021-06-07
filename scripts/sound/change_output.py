from rofi import Rofi
import pulsectl, sys
import subprocess

SOURCE_ALIASES = {
  'alsa_output.pci-0000_00_1f.3.analog-stereo': "🖥️ Notebook",
  'bluez_sink.78_44_05_84_1E_B0.a2dp_sink': "🔵 Bluetooth",
  'alsa_output.usb-Kingston_Technology_Company_HyperX_Cloud_Flight_Wireless-00.analog-stereo': "🎧 Headphones"
}

def clean_output(output):
    output = str(output).replace("b'","").replace("'","").split("\\n")
    return list(filter(None, output))

def main():
  pulse = pulsectl.Pulse()
  rofi = Rofi()

  # Ask user for a source-output to move

  output = clean_output(subprocess.check_output(("pactl","list","short","sinks")))
  selections = []
  for line in output:
     
     line_separated = line.split("\\t")
     
     name = SOURCE_ALIASES[line_separated[1]] if line_separated[1] in SOURCE_ALIASES else line_separated[1]
     selections.append(line_separated[0] + ": " + name)
  
  source_output_index, _ = rofi.select("Select source-output to move", selections)
  sink_id = selections[source_output_index].split(": ")[0]
  
  sink_inputs = clean_output(subprocess.check_output(("pactl","list","short","sink-inputs")))
  for sinput in sink_inputs:
    sinputid = sinput.split("\\t")[0]   
    subprocess.check_output(("pactl","move-sink-input", "{}".format(sinputid), "{}".format(sink_id)))    

if __name__ == '__main__':
  main()