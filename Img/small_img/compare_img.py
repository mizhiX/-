from compare_helper import compare
import os
from PIL import Image


def main():
    for i in range(1, 401):
        for n in range(4):
            filename1 = '%d_%d.png' % (i, n + 1)
            for m in range(4):
                try:
                    img_switch = Image.open(filename1).rotate(90)
                    img_switch.save(filename1)
                except:
                    break
                for x in range(i, 401):
                    for y in range(4):
                        try:
                            filename2 = '%d_%d.png' % (x, y + 1)
                        except:
                            print('清理完成!')
                            break
                        if filename2 == filename1:
                            continue
                        try:
                            result = compare(filename1, filename2)
                        except:
                            continue
                        if result == 1:
                            print('%s与%s相同, 删除图片%s' % (filename1, filename2, filename2))
                            # file_list.append(filename2)
                            os.remove(filename2)
    print('图片删除成功!')


if __name__ == '__main__':
    main()
