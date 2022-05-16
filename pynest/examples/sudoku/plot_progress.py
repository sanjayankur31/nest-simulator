# -*- coding: utf-8 -*-
#
# plot_progress.py
#
# This file is part of NEST.
#
# Copyright (C) 2004 The NEST Initiative
#
# NEST is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# NEST is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with NEST.  If not, see <http://www.gnu.org/licenses/>.

r"""generates a GIF of the network solving a Sudoku puzzle 
----------------------------------------------------------------
This scripts takes one of the .pkl files generated by 
:doc:`sudoku_solver.py` and generates a GIF showing the progress
of the network solving the puzzle. 

Note that the script generates the images individually, storing
them to disk first, assembling them into a GIF and then,
by default, deleting the images and folder.

For creating the individual images, PIL is used. Because the GIF creation 
tool in PIL is faulty, imageio is required for that step.

See Also
---------

:doc:`sudoku_solver`
:doc:`helpers.py`

:Authors: J Gille
"""
import os
import pickle
import imageio
from glob import glob
from helpers import plot_field
import sys

in_file = "350Hz_puzzle_4.pkl"  # Name of the .pkl file to read from
temp_dir = "tmp"                # Name of directory for temporary files
out_file = "sudoku.gif"         # Name of the output GIF
keep_temps = False              # If True, temporary files will not be deleted

if os.path.exists(out_file):
    print(f"Target file ({out_file}) already exists! Aborting.")
    sys.exit()

try:
    os.mkdir(temp_dir)
except:
    print(f"temporary file folder ({temp_dir}) already exists! Aborting.")
    sys.exit()

with open(in_file, "rb") as f:
    simulation_data = pickle.load(f)

solution_states = simulation_data["solution_states"]

image_count = 0


field = plot_field(simulation_data['puzzle'], simulation_data['puzzle'], False)


for i in range(len(solution_states)):
    current_state = solution_states[i]

    if i == 0:
        # repeat the (colorless) starting configuration several times
        image_repeat = 8
    else:
        field = plot_field(simulation_data['puzzle'], current_state, True)
        image_repeat = 1

    if i == len(solution_states) - 1:
        # repeat the final solution a few more times to make it observable
        # before the gif loops again
        image_repeat = 15

    for j in range(image_repeat):
        field.save(os.path.join(temp_dir, f"{str(image_count).zfill(4)}.png"))
        image_count += 1

filenames = sorted(glob(os.path.join(temp_dir, "*.png")))

with imageio.get_writer(out_file, mode='I', fps=4) as writer:
    for filename in filenames:
        image = imageio.imread(filename)
        writer.append_data(image)
print(f"gif created under: {out_file}")

if not keep_temps:
    print("deleting temporary image files...")
    for in_file in filenames:
        os.unlink(in_file)
    os.rmdir(temp_dir)
