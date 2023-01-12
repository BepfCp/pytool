import os
import shutil
import zipfile

import rarfile


def main(src_dir, tgt_dir):
    # 1. Crete target dir
    if os.path.exists(tgt_dir):
        shutil.rmtree(tgt_dir)
    os.makedirs(tgt_dir)

    # 2. Walk through the source dir
    for _, _, files in os.walk(src_dir):
        for file in files:
            file_path = os.path.join(src_dir, file)
            file_name, file_suffix = os.path.splitext(file)
            if file_suffix == ".mlx":
                # Directly copy the .mlx file
                tgt_file_path = os.path.join(tgt_dir, file)
                shutil.copy(file_path, tgt_file_path)
            elif file_suffix == ".zip":
                z = zipfile.ZipFile(file_path, 'r')
                output_dir = os.path.join(src_dir, file_name)
                z.extractall(path=output_dir)
                # Copy the nested .mlx file
                for _, _, dfiles in os.walk(output_dir):
                    has_mlx = False
                    for df in dfiles:
                        src_file_path = os.path.join(src_dir, output_dir, df)
                        if os.path.isfile(src_file_path) and df.endswith(".mlx"):
                            has_mlx = True
                            tgt_file_path = os.path.join(tgt_dir, file_name + ".mlx")
                            shutil.copy(src_file_path, tgt_file_path)
                    if not has_mlx:
                        print(f"No .mlx file in {file}!")
                    break
                z.close()
                shutil.rmtree(os.path.join(src_dir, output_dir))
            elif file_suffix == ".rar":
                z = rarfile.RarFile(file_path, 'r')
                output_dir = os.path.join(src_dir, file_name)
                try:
                    z.extractall(path=output_dir)
                except:
                    pass
                # Copy the nested .mlx file
                for _, _, dfiles in os.walk(output_dir):
                    has_mlx = False
                    for df in dfiles:
                        src_file_path = os.path.join(src_dir, output_dir, df)
                        if os.path.isfile(src_file_path) and df.endswith(".mlx"):
                            has_mlx = True
                            tgt_file_path = os.path.join(tgt_dir, file_name + ".mlx")
                            shutil.copy(src_file_path, tgt_file_path)
                    if not has_mlx:
                        print(f"No .mlx file in {file}!")
                    break
                z.close()
                shutil.rmtree(os.path.join(src_dir, output_dir))                   
        break

if __name__ == "__main__":
    src_dir = "I://hw2"
    tgt_dir = "I://hw2dec"
    main(src_dir, tgt_dir)