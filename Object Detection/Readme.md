# I apply Object Detection API in this project to Detect the Alphabets in the webcam.

Here First use the "google_object_detection main.rar" - It contatins the "google_object_detection main.ipynb" run this notebook on Google Colab with having the images folder in drive which contains the following files and folder:-

1) train.record file
2) test.record file
3) pipeline.config file
4) ckpt empty folder
5) ig empty folder

Now your question is from where do you get 1, 2 files.

Here your answer:-

First get the anotated dataset with having test and train folder containing annortated images. Then you run the file name "xml_to_csv.py" to convert the xml file to the csv files.

After that run the file "generate_tfrecord.py" to get the train.record and test.record files.

Now you have all files then you start training process in the Google Colab. When the training is done you get some checkpoints from where you can make the inference graph and then download the graph folder from the drive and run the file "object_detection_webcam.py". Here one window will open showing the webcam there you draw the Hand Gestures to get the predictions.

You may have some Questions that how to run the python files and all that for that you may follow this awesome tutoruial:- https://www.youtube.com/watch?v=Rgpfk6eYxJA&t=1323s

