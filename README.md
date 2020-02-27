# Sign-Language-Detecttion

Real Time Sign Language Detection Project using WebCam.
Currently working on this project and after completed then move it to mobile devices.

Download link for dataset: https://www.kaggle.com/grassknoted/asl-alphabet/kernels

Here I using the pre-trained model i.e Mobilenet_v2

Due to Hardware restriction I train Model on Kaggle playgroud.
Validation Accuracy = 0.9947917 and Validation Loss = 0.03621217922773212

Main File :- "Sign Language Detection (kaggle).ipynb" and "Real Done.py"

![](validation%20score.JPG)

Now, the Project is on the Real-Time i.e When you capture the image from the web then the model takes that image and predict the Alphabet.
See the code "Real-time.py" or "Real Done.py" for using the model in Real-time Basis.

NOTE :- Here's a important note that when you do real time predictions (by using the Real-time.py or Real Done.py) than you have to keep in mind that the images which you are capturing should be neat having clean background and the intensiy of the light should be moderate NO high and NO low intensity.
