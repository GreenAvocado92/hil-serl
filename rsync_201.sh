#!/bin/bash 

# rsync -avz ./* --exclude='*.pth' --exclude='deploy/' --exclude='*.hdf5' cosmo@10.180.76.160:~/skills/
rsync -avz ../hil-serl --exclude='*.pth' --exclude='deploy/' --exclude='*.hdf5' cosmo@10.180.76.160:~/skills/