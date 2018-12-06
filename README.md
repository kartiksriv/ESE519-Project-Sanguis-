# ESE519-Project-Sanguis-
Device to measure count of neutrophil from blood sample using image processing.


Button.py -> starts the thread which continously waits for the button press. If button is pressed, it starts the main thread.

sanguis_main.py -> does image processsing, syringe action, led lightining, image capture from raspberry pi camera, push the data to MQTT broker.

app_yaml and SanguisMQTT.html -> these are run on the google cloud server for getting the live data.
