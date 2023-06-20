import os
import cv2

def create_directory_at(path, dir):
    dir_path = os.path.join(path, dir)
    try:
        os.mkdir(dir_path)
    except OSError:
        print ('Error: Directory may already exist or path is invalid')
    return dir_path

def extract_frames_from_video(path_to_video):
    video = cv2.VideoCapture(path_to_video)
    current_frame = 0
    while (True):
        # reading from frame
        ret,frame = video.read()
    
        if ret:
            # if video is still left continue creating images
            frame_name = str(current_frame).zfill(5) + '.jpg'
            # print ('Creating...' + frame_name)
    
            # writing the extracted images
            cv2.imwrite(frame_name, frame)
    
            # increasing counter so that it will
            # show how many frames are created
            current_frame += 1
        else:
            break
    video.release()
    cv2.destroyAllWindows()

def extract_data(input_dir, output_dir, dataset_name, view_points):
    cwd = create_directory_at(output_dir, dataset_name)
    for subdir, dirs, files in os.walk(input_dir):
        for file in files:
            data_dir_list = subdir.split('/')
            if (data_dir_list[-3] == "Sequences" and data_dir_list[-1] == "Undist"):
                file_split = file.split('-')
                keyword = file_split[-1].split('_')[0]  ## check the viewpoint direction
                for view_point in view_points:
                    if (keyword == view_point):
                        dir_name = data_dir_list[-2]   
                        path = create_directory_at(cwd, dir_name)
                        path = create_directory_at(path, keyword)
                        os.chdir(path)
                        print("Extracting data in {}".format(path))
                        path_to_video = os.path.join(subdir, file)
                        extract_frames_from_video(path_to_video)
                    

def main():
    data_dir = '/home/prajwal/Downloads/P3Data'     ## Input directory
    root_dir = '/home/prajwal/EinsteinVision/data'  ## Output directory
    dataset_name = 'Tesla'                          ## Name of the dataset directory
    view_points = ["front"]                         ## List of view points

    extract_data(data_dir, root_dir, dataset_name, view_points)


if __name__ == '__main__':
    main()
