# Smart Object Recognizer - powered by NVIDIA Jetson Nano
Did you ever want to build your smart solution that could run at the edge, recognise specific objects (or sounds, or human pose) and report summary of its findings directly to your analytics dashboard.

Then search no further. Power of Nvidia's Jetson Nano device, Google's Teachable Machine - visual Machine Learning utility, and Microsoft's PowerBI are combined here to help you on your journey!
<p align="center">
  <img src="/images/JetsonNano_DevKit.jpg" width="100" height="100">
</p>

## Infrastructure Setup:
1. In Azure portal, create and link to each other Azure IoT Hub and Azure IoT Hub Device Provisioning Service (DPS) resources, using the following [Quick Setup guide](https://docs.microsoft.com/en-us/azure/iot-dps/quick-setup-auto-provision).
![Screenshot 1.1](/images/Infra_1.png)
> **Note**: To use Device Twin capability, IoT Hub should be on the Standard pricing tier.
2. In Azure Sphere Developer Command Prompt, download CA certificate from Azure Sphere tenant using the following command:
```
azsphere tenant download-CA-certificate --output CAcertificate.cer
```
You should see confirmation that the CA certificate has been saved.
![Screenshot 1.2](/images/Infra_2.png)
3. In Azure portal, upload certificate to Azure IoT DPS -> Certificates. After upload it will show new entry with an “Unverified” status.
![Screenshot 1.3](/images/Infra_3.png)
4. Then open certificate record and click “Generate Verification Code” button.
![Screenshot 1.4](/images/Infra_4.png)
5. In Azure Sphere Developer Command Prompt, download validation certificate signed with the DPS verification code from Step 4 above using the following command:
```
azsphere tenant download-validation-certificate --output ValidationCertification.cer --verificationcode <DPS_VERIFICATION_CODE>
```
You should see confirmation that the validation certificate has been saved.
![Screenshot 1.5](/images/Infra_5.png)
6. In Azure portal, upload validation certificate into “Verification Certificate” field of the record window from Step 4 and click “Verify” button. After validation, Azure will change the status of your certificate to “Verified”.
![Screenshot 1.6](/images/Infra_6.png)
7. Switch to Azure IoT DPS -> Manage Enrolments menu and add new enrolment group with the primary certificate that we verified in Step 6 above.
![Screenshot 1.7](/images/Infra_7.png)
 
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
