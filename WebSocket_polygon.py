import asyncio
import websockets
import subprocess
import os
import time
import win32com.client as win32



print("hi")
time.sleep(1)

async def connect_websocket():
    url = "wss://socket.polygon.io/forex"
    retry_counter = 0
    max_retries = 30
    retry_delay = 5

    

    while retry_counter < max_retries:
            try:            
                async with websockets.connect(url, timeout=10) as websocket:
                    

                    # Authenticate
                    auth_message = '{"action":"auth","params":"YOURKEY"}'
                    await websocket.send(auth_message)
                    print(f"Sent authentication message: {auth_message}")

                    # Wait for the authentication response
                    auth_response = await websocket.recv()
                    print(f"Received authentication response: {auth_response}")

                    # Subscribe to currency pair
                    subscribe_message = '{"action":"subscribe","params":"C.C:EUR-USD"}'
                    await websocket.send(subscribe_message)
                    print(f"Sent subscribe message: {subscribe_message}")


                    while True:

                        start_time = time.time()  # Start measuring time
                        message = await websocket.recv()
                        elapsed_time = time.time() - start_time  # Calculate elapsed time
                        print(f"Received message: {message}")
                        print(f"Time in Python: {start_time}")
                        print(f"Elapsed time (Python): {elapsed_time} seconds")

                        retry_counter = 0    #reset for each successful message


                        # Pass the message to the Julia script
                        subprocess.run(['julia', r'dirve:filepath+\websocket_feed_processing.jl', message])

            except Exception as e:
                retry_counter += 1
                time.sleep(retry_delay)
                print(f"An error occurred: {e}")

                if retry_counter > max_retries:
                
                    break  # Exit the while loop if retry limit is exceeded

            except asyncio.CancelledError:
                retry_counter += 1
                time.sleep(retry_delay)
                print("Websocket connection canceled. Retrying...")
                if retry_counter > max_retries:

                        break  # Exit the while loop if retry limit is exceeded
    
    # Run the WebSocket connection
    asyncio.get_event_loop().run_until_complete(connect_websocket())
