
# import python modules
import pyvisa
import statistics

try:
    # Open Connection
    rm = pyvisa.ResourceManager()
    
    # Connect to VISA Address
    # GPIB Connection: 'GPIB0::22::INSTR'
    myinst = rm.open_resource("GPIB0::22::INSTR")
    
    # Set Timeout - 5 seconds
    myinst.timeout = 5000
    
    # Set the instrument for 4-wire resistance measurement with additional settings
    myinst.write("END ALWAYS")
    myinst.write("FUNC OHMF")  # Set function to resistance measurement
    myinst.write("OHMF 10,4W")  # Set range and 4-wire mode
    myinst.write("NPLC 100")    # Set number of power line cycles
    myinst.write("OCOMP ON")    # Enable open circuit compensation
    myinst.write("TRIG AUTO")   # Set trigger to auto
    
    # Perform the measurement 10 times and store results
    measurements = []
    for i in range(10):
        myinst.write("TARM HOLD")
        myinst.write("TARM SGL")
        resistance = float(myinst.query("VAL?").strip())
        measurements.append(resistance)
        print(f'Measurement {i+1}: Resistance of the Fluke 742A-1: {resistance} Ohms')
    
    # Calculate and print summary statistics
    average_resistance = statistics.mean(measurements)
    min_resistance = min(measurements)
    max_resistance = max(measurements)
    stddev_resistance = statistics.stdev(measurements)
    
    print('\nSummary Statistics:')
    print(f'Average Resistance: {average_resistance:.6f} Ohms')
    print(f'Minimum Resistance: {min_resistance:.6f} Ohms')
    print(f'Maximum Resistance: {max_resistance:.6f} Ohms')
    print(f'Standard Deviation: {stddev_resistance:.6f} Ohms')
    
    # Close Connection
    myinst.close()
    print('close instrument connection')

except Exception as err:
    print('Exception: ' + str(err))

finally:
    # Perform clean up operations
    print('complete')
