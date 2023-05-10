import os
import time
import yaml
import torch
import zipfile
import streamlit as st
st.set_page_config(layout="wide")

from random import shuffle

import subprocess

def run_command(command, **kwargs):
    """Run a command while printing the live output"""
    process = subprocess.Popen(
    command,
    stdout=subprocess.PIPE,
    stderr=subprocess.STDOUT,
    **kwargs,
    )



def remove(path):
    for root, dirs, files in os.walk(path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))

def check_path(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def unzip_data(uploaded_files):
    for path in ['temp','zip','datasets']:  
        check_path(path)
    for uploaded_file in uploaded_files:
        with open('zip/' + uploaded_file.name, "wb") as binary_file:
            # Write bytes to file
            binary_file.write(uploaded_file.getvalue())

        with zipfile.ZipFile('zip/' + uploaded_file.name, 'r') as zip_ref:
            temp_path = 'temp/' + ''.join(uploaded_file.name.split('.')[:-1])
            check_path(temp_path)
            zip_ref.extractall(temp_path)

def make_training_data():
    projects = os.listdir('temp')
    for project in projects:
        with open(os.path.join('temp',project,'train.txt'),'r') as f:
            txts = f.readlines()

        shuffle(txts)
        files = [''.join(txt.replace('\n','')) for txt in txts]

        L = len(files)
        ratio=0.8
        train_files = files[:int(L*ratio)]
        valid_files = files[int(L*ratio):]

        for train_file in train_files:
            pic = os.path.join(*(['temp'] + [project] + train_file.split('/')[1:]))
            pic_name = os.path.basename(pic)

            # pic
            output_path = os.path.join('datasets','train',project,'images')
            check_path(output_path)
            output_pic = os.path.join(output_path,pic_name)
            if not os.path.isfile(output_pic):
                os.rename(pic,output_pic)

            #ann
            ann = pic.replace('png','txt')
            ann_name = os.path.basename(ann)
            output_path = os.path.join('datasets','train',project,'labels')
            check_path(output_path)
            output_ann = os.path.join(output_path,ann_name)
            if not os.path.isfile(output_ann):
                os.rename(ann,output_ann)

        with open(os.path.join('temp',project,'obj.names'),'r') as f:
            names = f.readlines()

        names = [''.join(name.replace('\n','')) for name in names]

        d = {
            'path' : os.path.join(os.getcwd(),'datasets'), 
            'train': [os.path.join('train',project,'images') for project in projects], 
            'val'  : [os.path.join('valid',project,'images') for project in projects],
            'nc'   : len(names)+1,
            'names': {i:n for i,n in enumerate(names)}
            }    

        with open(os.path.join('datasets','coco.yaml'), 'w') as f:
            yaml.dump(d, f, sort_keys=False)

        for valid_file in valid_files:
            pic = os.path.join(*(['temp'] + [project] + valid_file.split('/')[1:]))
            pic_name = os.path.basename(pic)

            # pic
            output_path = os.path.join('datasets','valid',project,'images')
            check_path(output_path)
            output_pic = os.path.join(output_path,pic_name)
            if not os.path.isfile(output_pic):
                os.rename(pic,output_pic)

            #ann
            ann = pic.replace('png','txt')
            ann_name = os.path.basename(ann)
            output_path = os.path.join('datasets','valid',project,'labels')
            check_path(output_path)
            output_ann = os.path.join(output_path,ann_name)
            if not os.path.isfile(output_ann):
                os.rename(ann,output_ann)


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
#Additional Info when using cuda
if device.type == 'cuda':
    t = round((torch.cuda.get_device_properties(0).total_memory)/(1024**3),2)
    r = round((torch.cuda.memory_reserved(0))/1024,2)
    a = round((torch.cuda.memory_allocated(0))/1024,2)
    st.markdown(f'### GPU 型號 : `{torch.cuda.get_device_name(0)}`')
    col1 = st.columns([2,1,1])
    col1[0].markdown(f'### GPU記憶體大小 : `{t}`')
    col1[1].markdown(f'### 已使用 : `{a}` GB')
    col1[2].markdown(f'### 可使用 : `{t-a}` GB')

uploaded_files = st.file_uploader("Choose a file",accept_multiple_files =True)

if len(uploaded_files) != 0:
    unzip_data(uploaded_files)
    make_training_data()

else:
    for path in ['temp','zip','datasets']:  
        remove(path)
        
    
if st.button('Training'):
    run_command(['python', 'train.py' ,'--data','datasets\coco.yaml'])