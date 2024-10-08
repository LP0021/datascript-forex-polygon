using DataFrames
using JSON
using CSV
import Base.Threads.@spawn
using Dates
using TimeZones
using Logging
using Base


# Initialize logging

logger = SimpleLogger()
global_logger(logger)

# Checking Execution

println("SCRIPT2 is now open and running")

    try
        # Read the message passed from Python as a command-line argument
        message = ARGS[1]
        # Parse the JSON message
        parsed_message = JSON.parse(message)                

        println("Parsed Message: ", parsed_message)

        now_ns = Dates.now()
        nano_now = time_ns()

        # Check if the key "p" exists in the parsed message
        if haskey(parsed_message[1], "p")
            # Access the value of the key "p" if it exists
            currency_pair = parsed_message[1]["p"]
            println("Currency pair: ", currency_pair)
                      
            # Extract the values for each column
            ev = parsed_message[1]["ev"]
            p = parsed_message[1]["p"]
            i = parsed_message[1]["i"]
            a = parsed_message[1]["a"]
            b = parsed_message[1]["b"]
            x = parsed_message[1]["x"]
            t = parsed_message[1]["t"]

            # Unix Timestamp 
            timestamp = t
            # Convert Unix to DateTime
            datetime = unix2datetime(timestamp / 1000)
            # Format DateTime into a string representation
            datetime_string = Dates.format(datetime, "yyyy-mm-dd'T'HH:MM:SS.s")

            # Create a DataFrame with the extracted values
            df = DataFrame(ev=[ev], p=[p], i=[i], a=[a], b=[b], x=[x], t=[datetime_string], t2=[t], jt3=[now_ns], jt4=[nano_now])

            # Generate the current date string in the format YYYY-MM-DD
            date_string = Dates.format(now(), "yyyy-mm-dd")

            # Construct the output filename with the date prefix
            output_filename = "drive:filepath\\$(date_string)_output.csv"



            # Save the DataFrame to a CSV file or perform other actions
            println(df)
            # Check if the CSV file exists
            if isfile(output_filename)
                # Append the DataFrame to the existing CSV file
                CSV.write(output_filename, df, header=false, append=true)
            else
                # Create a new CSV file and write the DataFrame
                CSV.write(output_filename, df, header=true)
            end

        else
            println("Key 'p' not found in the parsed message.")
        end

    catch e
        throw(e)
        catch_backtrace()


end
