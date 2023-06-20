import os
import cv2

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

def extract_data(input_dir, output_dir, view_points):
    input_path = os.path.join(os.getcwd(), input_dir)
    output_path = os.getcwd()
    cwd = os.path.join(output_path, output_dir)
    os.makedirs(cwd, exist_ok=True)
    for subdir, _, files in os.walk(input_path):
        for file in files:
            data_dir_list = subdir.split('/')
            if (data_dir_list[-3] == "Sequences" and data_dir_list[-1] == "Undist"):
                file_split = file.split('-')
                keyword = file_split[-1].split('_')[0]  ## check the viewpoint direction
                for view_point in view_points:
                    if (keyword == view_point):
                        scene_name = data_dir_list[-2]
                        path = os.path.join(cwd, scene_name, keyword)
                        os.makedirs(path, exist_ok=True)
                        os.chdir(path)
                        print("Extracting {} data of {} view".format(scene_name, keyword))
                        path_to_video = os.path.join(subdir, file)
                        extract_frames_from_video(path_to_video)
                    

def main():
    input_dir = 'tesla_raw'             ## Input directory
    output_dir = 'tesla_proc'           ## Name of the output directory
    view_points = ["front"]             ## List of view points

    extract_data(input_dir, output_dir, view_points)


if __name__ == '__main__':
    main()
