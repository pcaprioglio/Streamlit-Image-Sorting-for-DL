# Image-visualizer-app
An intuitive Streamlit application tailored for deep learning practitioners, offering powerful tools to visualize, sort, and explore large image datasets with ease. Designed with flexibility in mind, the app supports high-resolution TIFF files and provides advanced options for image rescaling, color mapping, and cropping.

On the sidebar of the app your are reuired to provoide as input either:
1) a root folder with the following structure:
                    root_folder:
                        class_folder_1:
                            img1
                            img2
                            ...
                        class_folder_2:
                            img1
                            img2
                            ...
                        ...
2) or an excel file where classes and image paths are contained in different columns. Every information of additional columns can be easily used to sort and group the images on the main page.

In both case the app with create a pandas df where classes, optional additional features and file paths are stored in individual columns. 

You have now the possibility to display, group and sort all images per class (or any additional features) on a convenient webpage. The app allows for comparing two different groups by dispalying them side to side.

You can additionally crop, rescale and plots the images as heatmaps choosing between different colors. Once your happy with your modifications, you can conveniently save the modified images in a new folder while keeping the same subfolder structure where images are sorted by class. 

![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1")


I packeged the project in UV. So if you have UV installed you can simply run:
1) uv sync
2) uv run streamlit run app.py

if you're using conda or any other environment be sure to have all the packages listen in the pyproject.toml installed and then just run:
streamlit run app.py

NOTE: Since I was working with large images, the displayed images are by default resized to 500x500 px. If you want to change the resize value you can do that in the functions.py file by modifying the argument of the functions: plot_image and visualize inside the ImageVisualizer class. 

