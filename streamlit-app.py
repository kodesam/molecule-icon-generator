# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 02:56:08 2022

@author: monar
"""

import streamlit as st
import cirpy
from cirpy import Molecule
import os
import cv2
import molecules_icon_generator as mig


if __name__ == "__main__":
    
    # select the folder with the atom icons:
    atom_icon_dir = "base-icons/"
    icon_map = mig.load_icons(atom_icon_dir)
    
    st.write('''
    # Molecule-icons generator!
    ''')
    
    st.write('''
    Generate icons of molecules from Smiles, Names, Cas-number or standard Inchi.
    For more options, check out the [GitHub repository](https://github.com/lmonari5/molecule-icon-generator.git) with the python module
    ''')
    
    input_type = st.selectbox("Create your icon by", 
                 ['smiles', 'name', 'cas_number', 'stdinchi'], 
                 help= 'Chose the input info of your moleculs')
    
    input_string = st.text_input('Input informations', "CC(=O)Nc1ccc(cc1)O" )

    single_bonds = st.checkbox('Draw just single_bonds')
    remove_H = st.checkbox('remove all Hydrogens') 
    rdkit_draw = st.checkbox('show rdkit structure')

    try:
        if input_type == 'name':
            input_string = cirpy.resolve(input_string, 'smiles')
        mol = Molecule(input_string)
        iupac = mol.iupac_name
        smiles = mol.smiles
    except Exception as e:
        st.write(f'''
        The cirpy python library is not able to resolve your input {input_type}
        You can use the smiles to skip the cirpy use.
        ''')
        if st.button('See full error'):
            st.write(e)
        if input_type == 'smiles':
            smiles = input_string
            iupac = 'not found'
        else:
            exit()
    
    filename = 'molecular-icon' + '.png'
    image = mig.icon_print(smiles, name = 'molecular-icon', rdkit_img = rdkit_draw, 
                            single_bonds = single_bonds, remove_H = remove_H, save=True,
                            symbol_img_dict = icon_map)
    
    im_rgba = cv2.cvtColor(image, cv2.COLOR_BGRA2RGBA)
    img_list = [im_rgba]
    caption_list = ['Iupac name: ' + iupac]
    column_widt = 600 
    
    if rdkit_draw:
        rdkit_img = cv2.imread(os.getcwd() + os.sep + "molecular-icon_rdkit.png", cv2.IMREAD_UNCHANGED)
        rdkit_img = cv2.cvtColor(rdkit_img, cv2.COLOR_BGRA2RGBA)
        img_list.append(rdkit_img)
        caption_list.append('Rdkit 2D conformation')
        column_widt = 300
        
    st.image(img_list, caption = caption_list,  width=column_widt,  channels = 'RGBA')
    
    with open(os.getcwd() + os.sep + filename, "rb") as file:
        btn = st.download_button( label="Download icon",
                                 data=file,
                                 file_name=filename,
                                 mime="image/png" )
    
    st.write('''
    Thanks for using the Molecules icons generators!
    ''')
