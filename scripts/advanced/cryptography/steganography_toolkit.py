#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Steganography Toolkit
Author: Abdul Haseeb (@h4x33b)
Version: 1.0.0
Description: A comprehensive toolkit for hiding and extracting data within various file types.
             Supports images, audio, video, and text files with multiple steganography techniques.
             For educational and authorized security testing purposes only.
"""

import os
import sys
import argparse
import random
import string
import hashlib
import base64
import binascii
import struct
import wave
import numpy as np
from PIL import Image
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

# ASCII Art Banner
BANNER = """
 ____  _                   _____           _ _    _ _   
/ ___|| |_ ___  __ _  __ _|_   _|__   ___ | | | _(_) |_ 
\___ \| __/ _ \/ _` |/ _` | | |/ _ \ / _ \| | |/ / | __|
 ___) | ||  __/ (_| | (_| | | | (_) | (_) | |   <| | |_ 
|____/ \__\___|\__, |\__,_| |_|\___/ \___/|_|_|\_\_|\__|
               |___/                                     
                                        By: Abdul Haseeb (@h4x33b)
"""

class ImageSteganography:
    """Class for handling image steganography operations"""
    
    @staticmethod
    def hide_lsb(image_path, data, output_path, password=None):
        """
        Hide data in the least significant bits of an image
        
        Args:
            image_path (str): Path to the carrier image
            data (str): Data to hide
            output_path (str): Path to save the output image
            password (str, optional): Password for encryption
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Open the image
            img = Image.open(image_path)
            width, height = img.size
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Encrypt data if password is provided
            if password:
                data = Encryption.encrypt_aes(data, password)
            
            # Convert data to binary
            binary_data = ''.join(format(ord(char), '08b') for char in data)
            binary_data += '00000000'  # Add terminator
            
            # Check if the image has enough pixels to store the data
            if len(binary_data) > width * height * 3:
                print("[!] Error: Data too large for the image")
                return False
            
            # Create a copy of the image
            stego_img = img.copy()
            pixels = stego_img.load()
            
            # Embed data in the image
            idx = 0
            for y in range(height):
                for x in range(width):
                    r, g, b = pixels[x, y]
                    
                    # Modify the least significant bit of each color channel
                    if idx < len(binary_data):
                        r = (r & 0xFE) | int(binary_data[idx])
                        idx += 1
                    
                    if idx < len(binary_data):
                        g = (g & 0xFE) | int(binary_data[idx])
                        idx += 1
                    
                    if idx < len(binary_data):
                        b = (b & 0xFE) | int(binary_data[idx])
                        idx += 1
                    
                    pixels[x, y] = (r, g, b)
                    
                    # Check if all data has been embedded
                    if idx >= len(binary_data):
                        break
                
                if idx >= len(binary_data):
                    break
            
            # Save the output image
            stego_img.save(output_path)
            return True
        
        except Exception as e:
            print(f"[!] Error: {e}")
            return False
    
    @staticmethod
    def extract_lsb(image_path, password=None):
        """
        Extract data hidden in the least significant bits of an image
        
        Args:
            image_path (str): Path to the stego image
            password (str, optional): Password for decryption
            
        Returns:
            str: Extracted data
        """
        try:
            # Open the image
            img = Image.open(image_path)
            width, height = img.size
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            pixels = img.load()
            
            # Extract binary data from the image
            binary_data = ""
            for y in range(height):
                for x in range(width):
                    r, g, b = pixels[x, y]
                    
                    # Extract the least significant bit of each color channel
                    binary_data += str(r & 1)
                    binary_data += str(g & 1)
                    binary_data += str(b & 1)
            
            # Convert binary data to ASCII
            extracted_data = ""
            for i in range(0, len(binary_data), 8):
                byte = binary_data[i:i+8]
                if byte == "00000000":  # Terminator
                    break
                
                extracted_data += chr(int(byte, 2))
            
            # Decrypt data if password is provided
            if password:
                extracted_data = Encryption.decrypt_aes(extracted_data, password)
            
            return extracted_data
        
        except Exception as e:
            print(f"[!] Error: {e}")
            return None
    
    @staticmethod
    def hide_dct(image_path, data, output_path, password=None):
        """
        Hide data using DCT (Discrete Cosine Transform) coefficients
        
        Args:
            image_path (str): Path to the carrier image
            data (str): Data to hide
            output_path (str): Path to save the output image
            password (str, optional): Password for encryption
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # This is a simplified implementation
            # In a real-world scenario, you would use DCT coefficients
            # For now, we'll use a modified LSB approach
            
            # Encrypt data if password is provided
            if password:
                data = Encryption.encrypt_aes(data, password)
            
            # Add a marker to indicate DCT method
            data = "DCT:" + data
            
            # Use LSB method for now
            return ImageSteganography.hide_lsb(image_path, data, output_path)
        
        except Exception as e:
            print(f"[!] Error: {e}")
            return False
    
    @staticmethod
    def extract_dct(image_path, password=None):
        """
        Extract data hidden using DCT coefficients
        
        Args:
            image_path (str): Path to the stego image
            password (str, optional): Password for decryption
            
        Returns:
            str: Extracted data
        """
        try:
            # Extract using LSB method for now
            data = ImageSteganography.extract_lsb(image_path)
            
            # Check for DCT marker
            if data and data.startswith("DCT:"):
                data = data[4:]  # Remove marker
                
                # Decrypt data if password is provided
                if password:
                    data = Encryption.decrypt_aes(data, password)
                
                return data
            
            return None
        
        except Exception as e:
            print(f"[!] Error: {e}")
            return None
    
    @staticmethod
    def hide_metadata(image_path, data, output_path, password=None):
        """
        Hide data in the metadata of an image
        
        Args:
            image_path (str): Path to the carrier image
            data (str): Data to hide
            output_path (str): Path to save the output image
            password (str, optional): Password for encryption
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Open the image
            img = Image.open(image_path)
            
            # Encrypt data if password is provided
            if password:
                data = Encryption.encrypt_aes(data, password)
            
            # Add a marker to indicate metadata method
            data = "META:" + data
            
            # Add data to EXIF metadata
            exif_data = img.info.get('exif', b'')
            comment = f"SteganoComment: {data}".encode('utf-8')
            
            # Save the image with the modified metadata
            img.save(output_path, exif=exif_data, comment=comment)
            return True
        
        except Exception as e:
            print(f"[!] Error: {e}")
            return False
    
    @staticmethod
    def extract_metadata(image_path, password=None):
        """
        Extract data hidden in the metadata of an image
        
        Args:
            image_path (str): Path to the stego image
            password (str, optional): Password for decryption
            
        Returns:
            str: Extracted data
        """
        try:
            # Open the image
            img = Image.open(image_path)
            
            # Extract data from comment
            comment = img.info.get('comment', b'')
            if isinstance(comment, bytes):
                comment = comment.decode('utf-8', errors='ignore')
            
            # Check for metadata marker
            if comment and "SteganoComment: META:" in comment:
                data = comment.split("SteganoComment: META:")[1]
                
                # Decrypt data if password is provided
                if password:
                    data = Encryption.decrypt_aes(data, password)
                
                return data
            
            return None
        
        except Exception as e:
            print(f"[!] Error: {e}")
            return None

class AudioSteganography:
    """Class for handling audio steganography operations"""
    
    @staticmethod
    def hide_lsb(audio_path, data, output_path, password=None):
        """
        Hide data in the least significant bits of an audio file
        
        Args:
            audio_path (str): Path to the carrier audio file
            data (str): Data to hide
            output_path (str): Path to save the output audio file
            password (str, optional): Password for encryption
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Open the audio file
            audio = wave.open(audio_path, 'rb')
            
            # Get audio parameters
            params = audio.getparams()
            nchannels, sampwidth, framerate, nframes = params[:4]
            
            # Read frames
            frames = audio.readframes(nframes)
            audio.close()
            
            # Convert frames to samples
            samples = np.frombuffer(frames, dtype=np.int16)
            
            # Encrypt data if password is provided
            if password:
                data = Encryption.encrypt_aes(data, password)
            
            # Convert data to binary
            binary_data = ''.join(format(ord(char), '08b') for char in data)
            binary_data += '00000000'  # Add terminator
            
            # Check if the audio has enough samples to store the data
            if len(binary_data) > len(samples):
                print("[!] Error: Data too large for the audio file")
                return False
            
            # Embed data in the audio
            for i in range(len(binary_data)):
                if i < len(samples):
                    # Modify the least significant bit
                    samples[i] = (samples[i] & 0xFFFE) | int(binary_data[i])
            
            # Convert samples back to frames
            modified_frames = samples.tobytes()
            
            # Create output audio file
            output_audio = wave.open(output_path, 'wb')
            output_audio.setparams(params)
            output_audio.writeframes(modified_frames)
            output_audio.close()
            
            return True
        
        except Exception as e:
            print(f"[!] Error: {e}")
            return False
    
    @staticmethod
    def extract_lsb(audio_path, password=None):
        """
        Extract data hidden in the least significant bits of an audio file
        
        Args:
            audio_path (str): Path to the stego audio file
            password (str, optional): Password for decryption
            
        Returns:
            str: Extracted data
        """
        try:
            # Open the audio file
            audio = wave.open(audio_path, 'rb')
            
            # Get audio parameters
            nframes = audio.getnframes()
            
            # Read frames
            frames = audio.readframes(nframes)
            audio.close()
            
            # Convert frames to samples
            samples = np.frombuffer(frames, dtype=np.int16)
            
            # Extract binary data from the audio
            binary_data = ""
            for i in range(min(len(samples), 100000)):  # Limit to prevent excessive processing
                # Extract the least significant bit
                binary_data += str(samples[i] & 1)
            
            # Convert binary data to ASCII
            extracted_data = ""
            for i in range(0, len(binary_data), 8):
                if i + 8 <= len(binary_data):
                    byte = binary_data[i:i+8]
                    if byte == "00000000":  # Terminator
                        break
                    
                    extracted_data += chr(int(byte, 2))
            
            # Decrypt data if password is provided
            if password:
                extracted_data = Encryption.decrypt_aes(extracted_data, password)
            
            return extracted_data
        
        except Exception as e:
            print(f"[!] Error: {e}")
            return None
    
    @staticmethod
    def hide_echo(audio_path, data, output_path, password=None):
        """
        Hide data using echo hiding technique
        
        Args:
            audio_path (str): Path to the carrier audio file
            data (str): Data to hide
            output_path (str): Path to save the output audio file
            password (str, optional): Password for encryption
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # This is a simplified implementation
            # In a real-world scenario, you would use echo hiding technique
            # For now, we'll use a modified LSB approach
            
            # Encrypt data if password is provided
            if password:
                data = Encryption.encrypt_aes(data, password)
            
            # Add a marker to indicate echo method
            data = "ECHO:" + data
            
            # Use LSB method for now
            return AudioSteganography.hide_lsb(audio_path, data, output_path)
        
        except Exception as e:
            print(f"[!] Error: {e}")
            return False
    
    @staticmethod
    def extract_echo(audio_path, password=None):
        """
        Extract data hidden using echo hiding technique
        
        Args:
            audio_path (str): Path to the stego audio file
            password (str, optional): Password for decryption
            
        Returns:
            <response clipped><NOTE>To save on context only part of this file has been shown to you. You should retry this tool after you have searched inside the file with `grep -n` in order to find the line numbers of what you are looking for.</NOTE>