from utils.TrajDataset import TrajectoryDataset

#DATASET_FOLDER = './dataset'
#TRAIN_FOLDER ='/train/'


file_path = './dataset/train/biwi/biwi_hotel_0.txt'

dataset = TrajectoryDataset(file_path)


for sample in dataset:
    print(sample)