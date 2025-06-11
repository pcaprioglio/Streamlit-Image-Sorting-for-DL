import streamlit as st
import os as os
from math import ceil
from PIL import Image
import skimage.io
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from natsort import natsorted 
import pandas as pd
import cv2
# 
class ImageVisualizer:  # Class containing streamlit page and functions to display images

    def __init__(self, df):
        self.df = df
        # self.save_path = save_path

    def plot_image(self, img, vmin, 
                vmax,
                color_map,
                resize_px = 500,
                cropping_size=None,
                recale_images='No',
                clabel='',
                title='',
                dpi=50,
                
                ):
        px = 1/plt.rcParams['figure.dpi']
        if img.lower().endswith((".tiff", ".tif")):
            img_open = skimage.io.imread(img, plugin='tifffile')
            img_open = cv2.resize(img_open, (resize_px,resize_px), interpolation=cv2.INTER_AREA)
        else:
            img_open = skimage.io.imread(img)
            img_open = cv2.resize(img_open, (resize_px,resize_px), interpolation=cv2.INTER_AREA)

            
        # img_open = skimage.transform.downscale_local_mean(img_open, (4,4))

        # img_open = cv2.imread(img)
        
        if cropping_size:
            height, width, channel = img_open.shape
            img_open = img_open[cropping_size:height-cropping_size, cropping_size:width-cropping_size]
        else:
            img_open = img_open

        if recale_images == 'Yes':
            img_open = cv2.cvtColor(img_open, cv2.COLOR_BGR2GRAY)
            # img_open = img_open[:,:,3]
            # img_open = skimage.color.rgb2gray(img_open)

            plt.rcParams.update({'font.size': 18})
            fig, ax = plt.subplots(dpi=dpi, figsize=((500)*px, (500)*px))
            im = plt.imshow(img_open,
                            vmin=vmin,
                            vmax=vmax,
                            cmap=color_map)
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", "5%", pad="3%")
            cb = fig.colorbar(im, cax=cax)
            cb.set_label(clabel)
            ax.set_title(title)
            ax.set_axis_off()
            return fig
        else:
            fig, ax = plt.subplots(dpi=dpi, figsize=((500)*px, (500)*px))
            plt.imshow(img_open)
            ax.set_axis_off()
            return fig

    def save_processed_images(self, save_path, img, img_class, img_name):
        if not os.path.exists(save_path):
                os.mkdir(save_path)

        class_folder_path = os.path.join(save_path,  img_class)
        if not os.path.exists(class_folder_path):
            os.mkdir(class_folder_path)

        # img.canvas.draw()
        # img = np.array(img.canvas.renderer.buffer_rgba())
        # img_plot=cv2.imread(img)
        # cv2.imwrite(os.path.join(save_path,  img_class), img_plot)
        figure_to_save = img
        figure_to_save.savefig(os.path.join(save_path,  img_class, img_name))
        
    def winapi_path(self, dos_path, encoding=None):   # For Windows users if filepath is too long you can use this functions to shorten your filepath
        if (not isinstance(dos_path, str) and encoding is not None):
            dos_path = dos_path.decode(encoding)
        path = os.path.abspath(dos_path)
        if path.startswith(u"\\\\"):
            return u"\\\\?\\UNC\\" + path[2:]
        return u"\\\\?\\" + path
    
    def visualize(self, resize_px=500):
            ## Control widgets
            header = st.container()
            header2 = st.container(border=True)
            header3 = st.container()

            with header: 
                controls = st.columns(7)
                with controls[0]:
                    image_path_size = st.select_slider("Image batch size:",range(1,31,1))
                with controls[1]:
                    row_size = st.select_slider("Row size:", range(1,6), value = 5)

                num_image_pathes = ceil(len(self.df)/image_path_size)
                with controls[2]:
                    page = st.selectbox("Page", range(1,num_image_pathes+1))

                with controls[5]:
                    sorting = st.selectbox(
                    'How do you want to sort your images?',
                    (self.df.columns))

                with controls[4]:
                    sorting2 = st.selectbox(
                    'How do you want to group your images?',
                    (self.df.columns))

                with controls[3]:
                    image_path_column = st.selectbox(
                    'Select image path column:',
                    (self.df.columns), index=None)

                with controls[6]:
                    sorting_direction = st.selectbox(
                    'Sorting direction:',
                    (['Ascending', 'Descending']))

            with header3:
                options = st.columns(3)          
                with options[1]:
                    with st.popover("Save processed images?"):
                        st.markdown("Copy your save path")
                        save_path = st.text_input("save path")
                        save_images_button = st.button('Save images now')

            with header2:
                controls2 = st.columns(6)
                with controls2[0]:
                    process_images = st.radio("Process images?", ['No', 'Yes'])
                with controls2[1]:
                    cropping = st.number_input(
                    'Crop your image?',
                    value=0,
                    max_value=245,
                     placeholder="Cropping pixel value...")

                with controls2[2]:
                    rescaling = st.selectbox(
                    'Rescale images intensity?',
                    (['No', 'Yes']))

                with controls2[3]:
                    vmin = st.number_input(
                        "Insert Min scaling value", value=1e1, placeholder="Min rescaling value...")
                    
                with controls2[4]:
                    vmax = st.number_input(
                        "Insert Max scaling value", value=1.5e2, placeholder="Max rescaling value...")

                with controls2[5]:
                    color_map = st.selectbox(
                    'Select your color map:',
                    (['inferno', 'viridis', 'turbo', 'gray']))   
                

            if sorting_direction == 'Descending':
                df = self.df.sort_values([sorting], ascending=False)
            else: 
                df = self.df.sort_values([sorting], ascending=True)
                
            ## Images
            col1, col2 = st.columns([1,1], gap="large")
            with col1:
                option = st.selectbox(
                    'Which class would you like to be displayed?',
                    (df[sorting2].unique().tolist()))

                if image_path_column != None:
                    parameter = df[sorting].loc[df[sorting2] == option].values[(page-1)*image_path_size : page*image_path_size]
                    image_path = df[image_path_column].loc[df[sorting2] == option].values[(page-1)*image_path_size : page*image_path_size]

                    grid = st.columns(row_size)
                    col = 0
                    
                    for image, param in zip(image_path,parameter):
                            image = (str(image))
                            image_name = image.split('/')[-1]
                            with grid[col]: 
                                if os.path.exists(image) and '.DS_Store' not in image:
                                    # if rescaling == 'Yes' and image.lower().endswith((".tiff", ".tif")):
                                    if process_images == 'Yes':
                                        if isinstance(param, float)  == True: 
                                            image_open = self.plot_image(image, cropping_size=cropping, recale_images=rescaling, vmin=vmin, vmax=vmax, color_map=color_map, title=param.round(3))
                                        else:
                                            image_open = self.plot_image(image, cropping_size=cropping, recale_images=rescaling, vmin=vmin, vmax=vmax, color_map=color_map, title=param)
                                        st.pyplot(image_open, dpi=100)
                                        if save_images_button:
                                            self.save_processed_images(save_path, image_open, param, image_name)
                                    else: 
                                        image_open = Image.open(image).resize([resize_px, resize_px])
                                        if isinstance(param, float)  == True: 
                                            st.image(image_open, caption=param.round(3), output_format="PNG")
                                        else: 
                                            st.image(image_open, caption=param, output_format="PNG")
                            col = (col + 1) % row_size
            
            with col2:
                option2 = st.selectbox(
                    'Which class would you like to compare?',
                    ( df[sorting2].unique().tolist()))
                
                if image_path_column != None:
                    parameter2 = df[sorting].loc[df[sorting2] == option2].values[(page-1)*image_path_size : page*image_path_size]
                    image_path2 = df[image_path_column].loc[df[sorting2] == option2].values[(page-1)*image_path_size : page*image_path_size]

                    grid = st.columns(row_size)
                    col = 0

                    for image, param in zip(image_path2,parameter2):
                            image = (str(image))
                            image_name = image.split('/')[-1]
                            with grid[col]:
                                if os.path.exists(image) and '.DS_Store' not in image:
                                    # if rescaling == 'Yes' and 'tiff' in image:
                                    if process_images == 'Yes':
                                        if isinstance(param, float)  == True: 
                                            image_open = self.plot_image(image, cropping_size=cropping, recale_images=rescaling, vmin=vmin, vmax=vmax, color_map=color_map, title=param.round(3))
                                        else:
                                            image_open = self.plot_image(image, cropping_size=cropping, recale_images=rescaling, vmin=vmin, vmax=vmax, color_map=color_map, title=param)
                                        st.pyplot(image_open, dpi=100)
                                        if save_images_button:
                                            self.save_processed_images(save_path, image_open, param, image_name)
                                            
                                    else: 
                                        image_open = Image.open(image).resize([resize_px, resize_px])
                                        if isinstance(param, float) == True: 
                                            st.image(image_open, caption=param.round(3), output_format="PNG")
                                        else: 
                                            st.image(image_open, caption=param, output_format="PNG")

                            col = (col + 1) % row_size          

def get_categories(series):       # quick helper function to naturally sort unique values of a series- 
    return list(natsorted(series.unique()))

def initialize_folder(root_path):  # quick helper function to create a dataframe which contains class and filepath from a root folder
    data = []
    for subfolder_name in os.listdir(root_path):
        if subfolder_name != '.DS_Store':
            subfolder_path = os.path.join(root_path, subfolder_name)
            for file_name in os.listdir(subfolder_path):
                file_path = os.path.join(subfolder_path, file_name)
                data.append({
                    'class': subfolder_name,
                    'file_path': file_path,
                })
    df = pd.DataFrame(data)
    return df 

def initialize_file(file):         # quick helper function to read an excel file as a pandas df
    df = pd.read_excel(file)
    return df

