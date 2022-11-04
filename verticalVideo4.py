#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Convert all media assets located in a specified directory."""
import glob
import os
from optparse import OptionParser

from moviepy.editor import VideoFileClip
from moviepy.editor import CompositeVideoClip
from skimage.filters import gaussian_filter



def get_dir_files(dir_path, patterns=None):
    """Get all absolute paths for pattern matched files in a directory.

    Args:
        dir_path (str): The path to of the directory containing media assets.
        patterns (list of str): The list of patterns/file extensions to match.

    Returns:
        (list of str): A list of all pattern-matched files in a directory.
    """
    if not patterns or type(patterns) != list:
        print('No patterns list passed to get_dir_files, defaulting to patterns.')
        patterns = ['*.mp4', '*.avi', '*.mov', '*.flv']

    files = []
    for pattern in patterns:
        dir_path = os.path.abspath(dir_path) + '/' + pattern
        files.extend(glob.glob(dir_path))

    return files

def blur(image):
    return gaussian_filter(image.astype(float),sigma=20)

def modify_clip(path, output):
    """Handle conversion of a video file.

    Args:
        path (str): The path to the directory of video files to be converted.
        output (str): The filename to associate with the converted file.
    """
    clip = VideoFileClip(path)
    clip1 = clip.rotate(270)
    clip2 = clip1.crop(x_center=540, y_center=960, width=1080, height=608)
    clip3 = clip2.resize(width=1920)
    clip_blurred = clip3.fl_image(blur)
    clip_blurred = clip_blurred.set_opacity(0.5)
    video = clip1.resize(height=1080)
    render = CompositeVideoClip([clip_blurred,video.set_position("center")])
    render = render.set_duration(68)
    render.write_videofile(output, codec='libx264', audio_codec='aac', temp_audiofile='temp-audio.m4a', remove_temp=True)
    print('File: {} should have been created.'.format(output))


if __name__ == '__main__':
    status = 'Failed!'
    parser = OptionParser(version='%prog 1.0.0')
    parser.add_option('-p', '--path', action='store', dest='dir_path',
                      default='.', type='string',
                      help='the path of the directory of assets, defaults to .')

    options, args = parser.parse_args()
    print('Running against directory path: {}'.format(options.dir_path))
    path_correct = raw_input('Is that correct?').lower()

    if path_correct.startswith('y'):
        dir_paths = get_dir_files(options.dir_path)
        for dir_path in dir_paths:
            output_filename = 'converted_' + os.path.basename(dir_path)
            modify_clip(path=dir_path, output=output_filename)

        status = 'Successful!'

    print('Conversion {}'.format(status))
