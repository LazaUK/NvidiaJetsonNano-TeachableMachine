# Smart Object Recogniser - powered by NVIDIA Jetson Nano
NVIDIA Jetson Nano Developer Kit is a compact, yet powerful computer equipped with a GPU (Graphics Processing Unit), which allows running of the Machine Learning models at the edge.

Here I'll show how you can easily train your Machine Learning model in the cloud using Google's Teachable Machine Web site, then bring it over to NVIDIA Jetson Nano and run offline.
<p align="center">
  <img src="/images/JetsonNano_DevKit.jpg" width="300">
</p>
As a further enhancement, you may report some of the findings back to your backend of choice (in my case - Microsoft Azure) to store it in the target data store for the future references or visualise collected data via real time dashboard.


> **Potential areas of implementation**: Imagine a production line equipped with the camera and Jetson Nano -like processing unit. If trained to recognise standard and defective versions of the product, this may enable automatic quality control. Or you can monitor availability of the products on the shelves of the shops to re-order when neeed. Or can detect anomalies in the working engine's sound as the system picks up the changes in the audio signal. And so on and on and on: anywhere you have patterns, such smart solution can detect potential deviations to report or react to.

## Jetson Nano Setup:
1. If you have not purchased NVIDIA Jetson Nano Developer Kit yet, then you can order one from the [Jetson Store](https://www.nvidia.com/en-gb/autonomous-machines/jetson-store/).
2. 

XX. In
```
code sample
```

 
## Data flow configuration:
1. In Azure Sphere Developer Command Prompt, execute the following command to get Azure Sphere tenant’s ID:
```
azsphere tenant show-selected
```
2. In Azure portal, switch to Azure IoT DPS -> Overview and copy DPS ID Scope value.
3. From Azure IoT DPS -> Linked IoT Hubs copy the full name of the linked IoT Hub.
4. Download content of this Git repo.
5. In Visual Studio, click File -> Open -> CMake, navigate to the repo’s Software -> VotingApp and then open app_manifest.json file.
![Screenshot 2.5](/images/Soft_5.png)
6. Update placeholders highlighted in the screenshot below with the values of your Azure Sphere tenant’s ID, DPS ID Scope and IoT Hub names collected in Steps 1, 2 and 3 above.
![Screenshot 2.6](/images/Soft_6.png)
7. Select CMakeLists.txt file and then click Build -> Rebuild Current Document (CMakeLists.txt). Verify that an image package is being generated as shown below.
![Screenshot 2.7](/images/Soft_7.png)
8. In the toolbar, choose “GDB Debugger (HLCore)” as the target.
![Screenshot 2.8](/images/Soft_8.png)
9. In Azure Sphere Developer Command Prompt, enable application development capability on Azure Sphere device:
```
azsphere device enable-development
```
10. Back in Visual Studio, click Debug -> Start (or press F5) to deploy Voting Machine app to the device. If successful, Visual Studio will execute Voting Machine app on Azure Sphere device. In Output window, choose “Device Output” option. If you will press any of 2 buttons, you should see the message updates in the debug window.
![Screenshot 2.10](/images/Soft_10.png)

## Analytics configuration:
1. In Azure, create new Stream Analytics job and add IoT Hub as its stream input
![Screenshot 3.1](/images/Analytics_1.png)
2. Add PowerBI as the output for Stream Analytics job and click Authorize.
![Screenshot 3.2](/images/Analytics_2.png)
3. Provide relevant output alias name, so that you can use it in the Stream Analytics query.
![Screenshot 3.3](/images/Analytics_3.png)
4. Alternatively, you can setup Azure storage account or a database as an output for Azure Stream Analytics job.
![Screenshot 3.4](/images/Analytics_4.png)
5. Last part is to create your dashboard in PowerBI. You may configure it directly at https://powerbi.microsoft.com/en-us/ or use richer functionality with the PowerBI desktop client. This is an example of my PowerBI dashboard, which combines historical data from the database with the live stream from the Azure Sphere device.
![Screenshot 3.5](/images/Analytics_5.png)

## High-Level Design:
The following diagram shows the main components utilised in this project.
![Screenshot 4.1](/images/AzSphere_Schematics.png)

## Working model - YouTube video:
You can find short demo of the working solution here on [YouTube](https://youtu.be/QZcHa6_i7bo)

## Credits:
This solution is based on the original sample code from Microsoft Azure Sphere team, published [here](https://github.com/Azure/azure-sphere-samples)
