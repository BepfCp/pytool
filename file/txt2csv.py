"""Convert .txt to .csv"""
import csv


def main(src_file_path: str, dst_file_path: str):
    with open(src_file_path, 'r') as in_file:
        stripped = (line.strip() for line in in_file)
        lines = (line.split(",") for line in stripped if line)
        with open(dst_file_path, 'w') as out_file:
            writer = csv.writer(out_file, lineterminator = '\n')
            writer.writerow(["第1题", "第2题", "第3题", "第4题", "第5题", "第6题",
                                "第7题", "第8题", "第9题", "第10题", "第11题", "第12题"])
            writer.writerows(lines)

if __name__ == '__main__':
    src_file_path = "./file.txt"
    dst_file_path = "./file.csv"
    main(src_file_path, dst_file_path)