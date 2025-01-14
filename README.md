# IPP-Net_Parsing
**Integrating Human Parsing and Pose Network for Human Action Recognition is a Human Activity Recognition Project that that combines two varied approaches for activity identification and analysis. It involves Human Parsing, branch of Semantic Segmentation and Human Pose Estimation.**


# Data Preparation
## Download datasets:
1. **NTU RGB+D 60** Skeleton dataset from [https://rose1.ntu.edu.sg/dataset/actionRecognition/](https://rose1.ntu.edu.sg/dataset/actionRecognition/) <br />
3. **NTU RGB+D 60** Video dataset from [https://rose1.ntu.edu.sg/dataset/actionRecognition/](https://rose1.ntu.edu.sg/dataset/actionRecognition/) <br />
5. Put downloaded skeleton data into the following directory structure:
```
- data/
  - ntu/
  - ntu120/
  - nturgbd_raw/
    - nturgb+d_skeletons
        S001C001P001R001A001.skeleton
        ...
    - nturgb+d_skeletons120/
        S018C001P008R001A061.skeleton
        ...
```
6. Extract person frames from the video dataset according to the following project: [Extract_NTU_Person](https://github.com/liujf69/Extract_NTU_Person) <br />
## Process skeleton data
```
cd ./data/ntu or cd ./data/ntu120
python get_raw_skes_data.py
python get_raw_denoised_data.py
python seq_transformation.py
```
## Extract human parsing data
1. cd ```./Human_parsing```
2. Download checkpoints and put it into the ```./checkpoints/resnet101``` folder: [PSP_Net](https://drive.google.com/file/d/1SGehQsE72odFnqPidK_EWWJjhGI8Ptbk/view?usp=sharing) <br />

**Run:** 
```
python gen_parsing.py --samples_txt_path ./ntu120.txt \
      --ntu60_path person_frame_path \
      --ntu120_path person_frame_path
```
**Example:** 
```
python gen_parsing.py --samples_txt_path ./test_sample.txt \
      --ntu60_path ./dataset/ntu60/ \
      --ntu120_path ./dataset/ntu120/
```
# Training pose branch
## Training NTU60
On the benchmark of XView, using joint modality, run: ```python Pose_main.py --device 0 1 --config ./config/nturgbd-cross-view/joint.yaml``` <br />
On the benchmark of XSub, using joint modality, run: ```python Pose_main.py --device 0 1 --config ./config/nturgbd-cross-subject/joint.yaml``` <br />


# Training parsing branch
## Training NTU60
On the benchmark of XView, run: ```python Parsing_main.py recognition -c ./config/nturgbd-cross-view/parsing_train.yaml``` <br />
On the benchmark of XSub, run: ```python Parsing_main.py recognition -c ./config/nturgbd-cross-subject/parsing_train.yaml``` <br />

# Testing 

## Testing NTU60XSub
```python ensemble.py --benchmark NTU60XSub --joint_Score ./Pose/ntu60_XSub_joint.pkl --bone_Score ./Pose/ntu60_XSub_bone.pkl --jointmotion_Score ./Pose/ntu60_XSub_jointmotion.pkl --bonemotion_Score ./Pose/ntu60_XSub_bonemotion.pkl --parsing_Score ./Parsing/ntu60_XSub_best.pkl --val_sample ./Val_sample/NTU60_CTR_CSub_test.txt --match_txt ./Match_txt/ntu60_XSubpair.txt```

## Testing NTU60XView
```python ensemble.py --benchmark NTU60XView --joint_Score ./Pose/ntu60_XView_joint.pkl --bone_Score ./Pose/ntu60_XView_bone.pkl --jointmotion_Score ./Pose/ntu60_XView_jointmotion.pkl --bonemotion_Score ./Pose/ntu60_XView_bonemotion.pkl --parsing_Score ./Parsing/ntu60_XView_best.pkl --val_sample ./Val_sample/NTU60_CTR_CView_test.txt --match_txt ./Match_txt/ntu60_XViewpair.txt```

}
```

# Contact
For any questions, feel free to contact: ```liujf69@mail2.sysu.edu.cn```
