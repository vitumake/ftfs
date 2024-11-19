# Filename to folder structur

I made a small script to create a folder structure from list of filenames. It's a simple script that reads a list of filenames and creates a folder structure based on different classes found in the name of the file. It was made to help me import data to keras for image classification because keras has a handy function to import data and labels from a certain folder structure.

The script will create a folder with each class having a subfolder with the images of that class. The script can also create a test train split of the data if you provide a split ratio.

The code itself has comments to explain what each part does. The parameters are hardcoded in the script, so you need to change the parameters in the script to fit your needs.

*Note:* I can't imagine the script is very optimized as its a quick and dirty script I made for my own use with rather small amount of data, so it might not be too suitable for massive datasets.

You are free to steal the code and use it as you like. If you have any suggestions for improvements, feel free to fix it yourself.

:)
