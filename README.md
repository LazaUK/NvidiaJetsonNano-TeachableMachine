# Smart Object Recogniser - powered by NVIDIA Jetson Nano
NVIDIA Jetson Nano Developer Kit is a compact, yet powerful computer equipped with a GPU (Graphics Processing Unit), which allows running of the Machine Learning models at the edge.

Here I'll show how you can easily train your Machine Learning model in the cloud using Google's Teachable Machine Web site, then bring it over to NVIDIA Jetson Nano and run offline.
<p align="center">
  <img src="/images/JetsonNano_DevKit.jpg" width="300">
</p>

As a further enhancement, you may report some of the findings back to your backend of choice (in my case - Microsoft Azure) to store it in the target data store for the future references or visualise collected data via real time dashboard.

> **Potential areas of implementation**: Imagine a production line equipped with the camera and Jetson Nano -like processing unit. If trained to recognise standard and defective versions of the product, this may enable automatic quality control. Or you can monitor availability of the products on the shelves of the shops to re-order when neeed. Or can detect anomalies in the working engine's sound as the system picks up the changes in the audio signal. And so on and on and on: anywhere you have patterns, such smart solution can detect potential deviations to report or react to.

## Jetson Nano Setup:
1. If you have not purchased NVIDIA Jetson Nano Developer Kit yet, you can order one from the [Jetson Store](https://www.nvidia.com/en-gb/autonomous-machines/jetson-store/);
2. Flash microSD Card with the latest version of JetPack as per instruction on this [NVIDIA Web site](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit#write);
3. Then deploy Jetson inference libraries, as explained on this [GitHub repo](https://github.com/dusty-nv/jetson-inference/blob/master/docs/building-repo-2.md);
4. And, finally, install TensorFlow framework on your Jetson Nano device as per instruction on this [NVIDIA Web site](https://docs.nvidia.com/deeplearning/frameworks/install-tf-jetson-platform/index.html).
> **Note**: Last step, installation of TensorFlow, is required only for the current version of this package (Version 1). In the future, I can hopefully describe Version 2, where TensorFlow model will be converted into Jetson Nanon optimised TensorRT model / engine. It would then allow more effective use of Jetson's hardware and software capabilities.
 
## Train the model with the Teachable Machine:
Google drastically simplified the process of the Machine Learning through the release of their online "Teachable Machine" platform. It's a no-code environment, where without writing a single line of code you can build a reusable model, capable of recognising your own images, sounds or even human poses !
1. To start, first open [Teachable Machine](https://teachablemachine.withgoogle.com/) Web site and click "Get Started" button;
2. Then create required number of classes (objects that your model should recognise) and either upload images that you have or click Webcam to record with your computer's or attached camera. I usually create 200 images per object, but model will definitely work with less number of images, especially if your objects have distinctive shapes;
3. If you will press the Train button, Teachable Machine will start training the model. By default, it will run through the 50 epochs (training cycles), but if necessary you may adjust the settings;
4. Upon completion of the training process, you will be able to test it in Preview section of the screen, where you can either upload some test images or check how it recognises the objects real-time in the stream of your Webcam, as shown on the screen below;
![Teachable_Machine](/images/TeachableMachine.PNG)
5. If you are happy with the results, in Preview section click "Export Model" button, then switch to TensorFlow tab and save it to your computer.

**Note**: For this tutorial, I trained the model with 3 classes: "Rubik Cube" (to simulate standard product), "Wrong Puzzle" (where another puzzle is used to simulate defective product) and "Nothing" (empty screen, that the system will use when no objects are shown).

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

```
azsphere device enable-development
```

## High-Level Design:
The following diagram shows the main components utilised in this project.
![Screenshot 4.1](/images/AzSphere_Schematics.png)

## Working model - YouTube video:
You can find short demo of the working solution here on [YouTube](https://youtu.be/QZcHa6_i7bo)

## Credits:
This solution is based on the original sample code from Microsoft Azure Sphere team, published [here](https://github.com/Azure/azure-sphere-samples)
