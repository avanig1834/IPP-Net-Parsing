# test NTU120XSub
# python ensemble.py --benchmark NTU120XSub --joint_Score ./Pose/ntu120_XSub_joint.pkl --bone_Score ./Pose/ntu120_XSub_bone.pkl --jointmotion_Score ./Pose/ntu120_XSub_jointmotion.pkl --bonemotion_Score ./Pose/ntu120_XSub_bonemotion.pkl --parsing_Score ./Parsing/ntu120_XSub_best.pkl --val_sample ./Val_sample/NTU120_CTR_CSub_test.txt --match_txt ./Match_txt/ntu120_XSubpair.txt
# test NTU120XSet
# python ensemble.py --benchmark NTU120XSet --joint_Score ./Pose/ntu120_XSet_joint.pkl --bone_Score ./Pose/ntu120_XSet_bone.pkl --jointmotion_Score ./Pose/ntu120_XSet_jointmotion.pkl --bonemotion_Score ./Pose/ntu120_XSet_bonemotion.pkl --parsing_Score ./Parsing/ntu120_XSet_best.pkl --val_sample ./Val_sample/NTU120_CTR_CSet_test.txt --match_txt ./Match_txt/ntu120_XSetpair.txt
# test NTU60XSub
# python ensemble.py --benchmark NTU60XSub --joint_Score ./Pose/ntu60_XSub_joint.pkl --bone_Score ./Pose/ntu60_XSub_bone.pkl --jointmotion_Score ./Pose/ntu60_XSub_jointmotion.pkl --bonemotion_Score ./Pose/ntu60_XSub_bonemotion.pkl --parsing_Score ./Parsing/ntu60_XSub_best.pkl --val_sample ./Val_sample/NTU60_CTR_CSub_test.txt --match_txt ./Match_txt/ntu60_XSubpair.txt
# test NTU60XView
# python ensemble.py --benchmark NTU60XView --joint_Score ./Pose/ntu60_XView_joint.pkl --bone_Score ./Pose/ntu60_XView_bone.pkl --jointmotion_Score ./Pose/ntu60_XView_jointmotion.pkl --bonemotion_Score ./Pose/ntu60_XView_bonemotion.pkl --parsing_Score ./Parsing/ntu60_XView_best.pkl --val_sample ./Val_sample/NTU60_CTR_CView_test.txt --match_txt ./Match_txt/ntu60_XViewpair.txt

import torch
import pickle
import argparse
import numpy as np
import pandas as pd

def get_parser():
    parser = argparse.ArgumentParser(description = 'Parameters of Extract Person Frame') 
    parser.add_argument(
        '--joint_Score', 
        type = str,
        default = './Pose/ntu120_XSub_joint.pkl')
    parser.add_argument(
        '--bone_Score', 
        type = str,
        default = './Pose/ntu120_XSub_bone.pkl')
    parser.add_argument(
        '--jointmotion_Score', 
        type = str,
        default = './Pose/ntu120_XSub_jointmotion.pkl')
    parser.add_argument(
        '--bonemotion_Score', 
        type = str,
        default = './Pose/ntu120_XSub_bonemotion.pkl')
    parser.add_argument(
        '--parsing_Score', 
        type = str,
        default = './Parsing/NTU120_XSub_best.pkl')
    parser.add_argument(
        '--val_sample', 
        type = str,
        default = './Val_sample/NTU120_CTR_CSub_test.txt')
    parser.add_argument(
        '--match_txt', 
        type = str,
        default = './Match_txt/ntu120_XSubpair.txt')
    parser.add_argument(
        '--benchmark', 
        type = str,
        default = 'NTU120XSub')
    return parser

def Cal_Score(File, rgb_score, Rate, ntu60XS_num, Numclass):
    final_score = torch.zeros(ntu60XS_num, Numclass)
    for idx, file in enumerate(File):
        fr = open(file,'rb') 
        inf = pickle.load(fr)

        df = pd.DataFrame(inf)
        df = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
        score = torch.tensor(data = df.values)
        final_score += Rate[idx] * score
    
    final_score += Rate[-1] * rgb_score

    return final_score

def Cal_Acc(final_score, true_label):
    wrong_index = []
    _, predict_label = torch.max(final_score, 1)
    for index, p_label in enumerate(predict_label):
        if p_label != true_label[index]:
            wrong_index.append(index)
            
    wrong_num = np.array(wrong_index).shape[0]
    print('wrong_num: ', wrong_num)

    total_num = true_label.shape[0]
    print('total_num: ', total_num)
    Acc = (total_num - wrong_num) / total_num
    return Acc

def gen_label(val_txt_path):
    true_label = []
    val_txt = np.loadtxt(val_txt_path, dtype = str)
    for idx, name in enumerate(val_txt):
        label = int(name[-3:]) - 1
        true_label.append(label)

    true_label = torch.from_numpy(np.array(true_label))
    return true_label

def swap(rgb_file, pair_file):
    fr = open(rgb_file,'rb') 
    inf = pickle.load(fr)
    df = pd.DataFrame(inf)
    df = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
    rgb_score = torch.tensor(data = df.values)

    pair_txt = np.loadtxt(pair_file)
    target_pos = pair_txt[:, 1]
    target_score = rgb_score[target_pos]
    return target_score

if __name__ == "__main__":
    parser = get_parser()
    args = parser.parse_args()
    j_file = args.joint_Score
    b_file = args.bone_Score
    jm_file = args.jointmotion_Score
    bm_file = args.bonemotion_Score
    p_file = args.parsing_Score
    val_txt_file = args.val_sample
    match_txt_file = args.match_txt

    Pose_File = [j_file, b_file, jm_file, bm_file] 
    if args.benchmark == 'NTU120XSub':
        Rate = [7, 7, 3, 3, 5]
        Numclass = 120
        Sample_Num = 50919
        parsing_score = swap(p_file, match_txt_file)
        final_score = Cal_Score(Pose_File, parsing_score, Rate, Sample_Num, Numclass)
    
    elif args.benchmark == 'NTU120XSet':
        Rate = [6, 6, 4, 4, 6]
        Numclass = 120
        Sample_Num = 59477
        parsing_score = swap(p_file, match_txt_file)
        final_score = Cal_Score(Pose_File, parsing_score, Rate, Sample_Num, Numclass)
    
    elif args.benchmark == 'NTU60XSub':
        Rate = [6, 6, 4, 4, 8]
        Numclass = 60
        Sample_Num = 16487
        parsing_score = swap(p_file, match_txt_file)
        final_score = Cal_Score(Pose_File, parsing_score, Rate, Sample_Num, Numclass)
    
    elif args.benchmark == 'NTU60XView':
        Rate = [6, 6, 4, 4, 6]
        Numclass = 60
        Sample_Num = 18932
        parsing_score = swap(p_file, match_txt_file)
        final_score = Cal_Score(Pose_File, parsing_score, Rate, Sample_Num, Numclass)

    true_label = gen_label(val_txt_file)

    Acc = Cal_Acc(final_score, true_label)

    print('acc:', Acc)