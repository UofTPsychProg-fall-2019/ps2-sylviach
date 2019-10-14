#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scene-cat problem set for PSY 1210 - Fall 2018

@author: Michael Mack
### Assignment completed by Xiao Min Chang
"""

#%% import block 
import numpy as np
import scipy as sp
import scipy.stats
import os
import shutil


#%%
# copy files from testing room folders to raw data, rename files to include
# testing room letter in the filename
#
testingrooms = ['A','B','C']
for room in testingrooms:
    os.chdir('C:/Users/XiaoMin/Documents/GitHub/ps2-sylviach')
    path="/Users/XiaoMin/Documents/GitHub/ps2-sylviach/"+"testingroom"+ room +"/experiment_data.csv"
    newpath="/Users/XiaoMin/Documents/GitHub/ps2-sylviach/"+"rawdata/"+"experiemtn_data_"+ room +".csv"
    shutil.copyfile(path,newpath)

...


#%%
# read in all the data files in rawdata directory using a for loop
# columns: subject, stimulus, pairing, accuracy, median RT
#
data = np.empty((0,5))
for room in testingrooms:
    newpath="/Users/XiaoMin/Documents/GitHub/ps2-sylviach/"+"rawdata/"+"experiemtn_data_"+ room +".csv"
    tmp = sp.loadtxt(newpath,delimiter=',')
    data = np.vstack([data,tmp])
...


#%%
# calculate overall average accuracy and average median RT
#
acc_avg = np.mean(data[:, 3])   # 91.48%
mrt_avg = np.mean(data[:, 4])   # 477.3ms


#%%
# calculate averages (accuracy & RT) split by stimulus using a for loop and an 
# if statement. (i.e., loop through the data to make a sum for each condition, 
# then divide by the number of data points going into the sum)
#
word_count = 0
face_count = 0
word_acc_sum = 0
word_mrt_sum = 0
face_acc_sum = 0
face_mrt_sum = 0

for i in range(len(data)): 
    if data[i, 1] == 1:
        word_count = word_count + 1
        word_acc_sum = word_acc_sum + data[i,3]
        word_mrt_sum = word_mrt_sum + data[i,4]
    elif data[i, 1] == 2:
        face_count = face_count + 1
        face_acc_sum = face_acc_sum + data[i,3]
        face_mrt_sum = face_mrt_sum + data[i,4]
    else:
        break

word_acc_avg = word_acc_sum/word_count
word_mrt_avg = word_mrt_sum/word_count
face_acc_avg = face_acc_sum/face_count
face_mrt_avg = face_mrt_sum/word_count

print(word_acc_avg, word_mrt_avg)
print(face_acc_avg, face_mrt_avg)
# words: 88.6%, 489.4ms   faces: 94.4%, 465.3ms


#%%
# calculate averages (accuracy & RT) split by congruency using indexing, 
# slicing, and numpy's mean function 
# wp - white/pleasant, bp - black/pleasant
# (hint: only one line of code is needed per average)
#
acc_wp = np.mean(data[(data[:,2] == 1), 3])  # 94.0%
acc_bp = np.mean(data[(data[:,2] == 2), 3])  # 88.9%
mrt_wp = np.mean(data[(data[:,2] == 1), 4])  # 469.6ms
mrt_bp = np.mean(data[(data[:,2] == 2), 4])  # 485.1ms


#%% 
# calculate average median RT for each of the four conditions
# use for loops, indexing/slicing, or both!
# (hint: might be easier to slice data into separate words and faces datasets)
#
words_wp_mrt = np.mean(data[(data[:,1] == 1) & (data[:,2] == 1), 4])
words_bp_mrt = np.mean(data[(data[:,1] == 1) & (data[:,2] == 2), 4])
faces_wp_mrt = np.mean(data[(data[:,1] == 2) & (data[:,2] == 1), 4])
faces_bp_mrt = np.mean(data[(data[:,1] == 2) & (data[:,2] == 2), 4])

print(words_wp_mrt, words_bp_mrt, faces_wp_mrt, faces_bp_mrt)

# words - white/pleasant: 478.4ms
# words - black/pleasant: 500.3ms
# faces - white/pleasant: 460.8ms
# faces - black/pleasant: 469.9ms


#%%        
# compare pairing conditions' effect on RT within stimulus using scipy's 
# paired-sample t-test: scipy.stats.ttest_rel()
#
import scipy.stats

words_wp_mrt2 = data[(data[:,1] == 1) & (data[:,2] == 1), 4]
words_bp_mrt2 = data[(data[:,1] == 1) & (data[:,2] == 2), 4]
words_t = scipy.stats.ttest_rel(words_wp_mrt2, words_bp_mrt2)

faces_wp_mrt2 = data[(data[:,1] == 2) & (data[:,2] == 1), 4]
faces_bp_mrt2 = data[(data[:,1] == 2) & (data[:,2] == 2), 4]
faces_t = scipy.stats.ttest_rel(faces_wp_mrt2, faces_bp_mrt2)

print(words_t, faces_t)

# words: t=-5.36, p=2.19e-5
# faces: t=-2.84, p=0.0096


#%%
# print out averages and t-test results
# (hint: use the ''.format() method to create formatted strings)
#
print('\nOVERALL: {:.2f}%, {:.1f} ms'.format(100*acc_avg,mrt_avg))
print('\nWORDS: {:.2f}%, {:.1f} ms'.format(100*word_acc_avg,word_mrt_avg))
print('\nFACES: {:.2f}%, {:.1f} ms'.format(100*face_acc_avg,face_mrt_avg))
print('\nWHITE/PLEASANT: {:.2f}%, {:.1f} ms'.format(100*acc_wp,mrt_wp))
print('\nBLACK/PLEASANT: {:.2f}%, {:.1f} ms'.format(100*acc_bp,mrt_bp))
print('\nWORDS - WHITE/PLEASANT: {:.1f} ms'.format(words_wp_mrt))
print('\nWORDS - BLACK/PLEASANT: {:.1f} ms'.format(words_bp_mrt))
print('\nFACES - WHITE/PLEASANT: {:.1f} ms'.format(faces_wp_mrt))
print('\nFACES - BLACK/PLEASANT: {:.1f} ms'.format(faces_bp_mrt))
print('\nWORDS T-TEST: t = {:.2f}, p = {:.4f}'.format(words_t[0], words_t[1]))
print('\nFACES T-TEST: t = {:.2f}, p = {:.4f}'.format(faces_t[0], faces_t[1]))
...