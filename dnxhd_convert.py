import os
import sys
import subprocess

#version number
ver=0.1

#depending of your system, change this path to ffmpeg executable:
ffmpeg = "/bin/ffmpeg"

#list of consumer video format extensions. this can be extend with further testing
formats = ('.avi','.mp4','.m4v','.mov',)


ascii_art= ("""

     ___  _  _     _  _ ___     ___ ___  _  ___   _____ ___ _____ ___ ___ 
    |   \| \| |_ _| || |   \   / __/ _ \| \| \ \ / / __| _ \_   _| __| _ \ 
    | |) | .` \ \ / __ | |) | | (_| (_) | .` |\ V /| _||   / | | | _||   /
    |___/|_|\_/_\_\_||_|___/   \___\___/|_|\_| \_/ |___|_|_\ |_| |___|_|_\ 
""")

#define functions

class utils:
    def clear():
        """clear system console"""
        os.system('cls' if os.name=='nt' else 'clear')

    def interface(ascii_art, ver):
        """ print ascii art, version number, user instructions"""
        print(ascii_art)
        print("                                                         version: "+f"{ver}"+"\n\n")
        print("           - Batch convert consumer format video (.mp4, .avi...) to professional DNxHD standard")
        print("           - Default Settings create 4K footage ready to use in DaVinci Resolve")
        print("           - Hit enter to keep default values\n\n\n")



    def i_o_folders():
        input_folder_path=input("Enter input folder absolute path: \n")
        output_folder_path=input("Enter output folder absolute path (default: create a folder next to input folder): \n")
        if output_folder_path == "":
            output_folder_path= os.path.join(input_folder_path +"_converted")
        else:
            output_folder_path=output_folder_path
        return input_folder_path, output_folder_path

    def check_output_folder(outfolder):
        if not os.path.exists(outfolder):
            os.mkdir(outfolder)
        return outfolder   

    def grab_user_input():

        def filterInput(message, default):
            user_input = input (message)

            if user_input == "":
                user_input = default
            return user_input
        user_input_dict = {}
        user_input_dict["video_codec"] = filterInput("Video Codec (default = dnxhd): ", "dnxhd")
        user_input_dict["video_profile"] = filterInput("Video Profile (default=dnxhdr_hq: ", "dnxhr_hq")
        user_input_dict["audio_codec"] = filterInput("Audio Codec (default = pcm_s16le): ", "pcm_s16le") 
        #user_input_dict["audio_bitrate"] = filterInput("Audio Bitrate (default = 196k): ", "196k")
        #user_input_dict["sample_rate"] = filterInput("Sample Rate (default = 44100): ", "44100")
        user_input_dict["encoding_speed"] = filterInput("Encoding Speed: (default = fast): ", "fast")
        user_input_dict["crf"] = filterInput("Constant Rate Factor: (default = 22): ", "22")
        user_input_dict["frame_size"] = filterInput("Frame Size (default = 3840x2160: ", "3840x2160")

        return user_input_dict   


class convert:
    def ffmpeg_command(input_file, output_file, final_user_input):
        commands_list = [
            ffmpeg,
            "-i",
            #final_user_input["input_file"],
            input_file,
            "-c:v",
            final_user_input["video_codec"],
            "-profile:v",
            final_user_input["video_profile"],            
            #final_user_input["sample_rate"],
            "-pix_fmt",
            "yuv422p",
            final_user_input["encoding_speed"],
            "-crf",
            final_user_input["crf"],
            "-s",
            final_user_input["frame_size"],
            "-c:a",
            final_user_input["audio_codec"],
            #"-b:a",
            #final_user_input["audio_bitrate"],
            #"-ar",
            output_file
            #final_user_input["output_file"]
            ]

        return commands_list

    def run_ffmpeg(commands):
        print (commands)
        if subprocess.run(commands).returncode == 0:
            print("FFmpeg ran succesfully")
        else:
            print("there was an error, ffmpeg failed to ran")


if __name__ == "__main__":
    
    utils.clear()
    utils.interface(ascii_art ,ver)
    i_o=utils.i_o_folders()
    in_folder=i_o[0]
    out_folder=i_o[1]
    final_user_input = utils.grab_user_input()
    utils.check_output_folder(out_folder)
    for file in os.listdir(in_folder):
        file_path=os.path.join(in_folder,file)
        if os.path.isfile(file_path):
            file_extension = os.path.splitext(file_path)[1]
            if file_extension in formats:
                data_out = os.path.join(out_folder, os.path.splitext(file)[0]+"_converted"+".mov")
                convert.run_ffmpeg(convert.ffmpeg_command(file_path, data_out, final_user_input))
            else:
                print(file, "not an available input")
        else:
            print(file, "not a file")