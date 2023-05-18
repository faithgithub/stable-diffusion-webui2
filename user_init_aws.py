import os
import sys
import shutil

def link_models(models_folder,sdw_models_folder):
    # 创建/mnt/bjcfs/cloud/userid/models/Stable-diffusion文件夹

    os.makedirs(models_folder, exist_ok=True)
    # 遍历/mnt/bjcfs/sdw/models/Stable-diffusion文件夹，并以软链接的方式放到/mnt/bjcfs/cloud/userid/extensions文件夹内

    for filename in os.listdir(sdw_models_folder):
        src_file = f"{sdw_models_folder}/{filename}"
        dst_file = f"{models_folder}/{filename}"
        if os.path.exists(dst_file):
            os.unlink(dst_file)  # 删除已存在的目标文件
        src_path = f"{sdw_models_folder}/{filename}"
        dst_path = f"{models_folder}/"
        abs_dst_path = os.path.abspath(dst_path)
        rel_path = os.path.relpath(src_path, abs_dst_path)
        os.symlink(rel_path, os.path.join(abs_dst_path, os.path.basename(src_path)))

def create_user_folders(userid,reload=0,CFS_DIR='/content/stable-diffusion-webui/mnt'):
    # 创建/mnt/bjcfs/cloud/userid文件夹
    cfs = CFS_DIR
    user_folder = f"{cfs}/cloud/{userid}"
    user_folder_r = f"/cloud/{userid}"
    user_folder_exist = False
    if os.path.exists(user_folder):
        user_folder_exist = True
        if reload == 1:
            print(f"reload {userid}")
        else:
            return user_folder_r
    os.makedirs(user_folder, exist_ok=True)
    model_dir = ["Stable-diffusion","BLIP","Codeformer","dreambooth","ControlNet","deepbooru","deepdanbooru","ESRGAN","GFPGAN",
                 "hed","hypernetworks","LDSR","Lora","openpose","RealESRGAN","SwinIR","torch_deepdanbooru","VAE","VAE-approx"
                 ]
    for i in model_dir:
        models_folder = f"{user_folder}/models/{i}"
        sdw_models_folder = f"{cfs}/sdw/models/{i}"
        try:
            link_models(models_folder,sdw_models_folder)
        except Exception as e:
            print(f"link {models_folder} to {sdw_models_folder} failed",str(e))


    # 创建/mnt/bjcfs/cloud/userid/extensions文件夹
    extensions_folder = f"{user_folder}/extensions"
    os.makedirs(extensions_folder, exist_ok=True)
    # 遍历/mnt/bjcfs/sdw/extensions文件夹，并以软链接的方式放到/mnt/bjcfs/cloud/userid/extensions内
    sdw_extensions_folder = f"{cfs}/sdw/extensions"

    for foldername in os.listdir(sdw_extensions_folder):
        try:
            src_folder = f"{sdw_extensions_folder}/{foldername}"
            dst_folder = f"{extensions_folder}/{foldername}"
            if os.path.exists(dst_folder):
                os.unlink(dst_folder)  # 删除已存在的目标文件
            src_path = f"{sdw_extensions_folder}/{foldername}"
            dst_path = f"{extensions_folder}/"
            abs_dst_path = os.path.abspath(dst_path)
            rel_path = os.path.relpath(src_path, abs_dst_path)
            os.symlink(rel_path, os.path.join(abs_dst_path, os.path.basename(src_path)))
        except Exception as e:
            print(f"link {dst_folder} to {src_folder} failed", str(e))

    # 创建/mnt/bjcfs/cloud/userid/cache文件夹
    cache_folder = f"{user_folder}/cache"
    # os.makedirs(cache_folder, exist_ok=True)

    # 复制/mnt/bjcfs/sdw/cache文件夹内所有内容到/mnt/bjcfs/cloud/userid/cache
    sdw_cache_folder = f"{cfs}/sdw/cache"
    if not user_folder_exist:
        #当用户第一次来的时候  复制配置文件
        try:
            shutil.copytree(sdw_cache_folder, cache_folder,dirs_exist_ok=True)
            shutil.copy(f"{cfs}/sdw/cache.json", f"{user_folder}/")
            shutil.copy(f"{cfs}/sdw/cache.json.lock", f"{user_folder}/")
            shutil.copy(f"{cfs}/sdw/config.json", f"{user_folder}/")
            shutil.copy(f"{cfs}/sdw/params.txt", f"{user_folder}/")
            shutil.copy(f"{cfs}/sdw/ui-config.json", f"{user_folder}/")
        except Exception as e :
            print(str(e))
            os.makedirs(cache_folder, exist_ok=True)
    return user_folder_r
# create_user_folders("wxy-test")
if __name__=="__main__":
    args = sys.argv[1:]
    user_id = args[0]
    reload = int(args[1])
    create_user_folders(user_id,reload=reload)

