import os
import glob
import cv2
import argparse

def getParser():
    parser = argparse.ArgumentParser(
        description="Resize raw images to uniformed target size."
    )
    parser.add_argument(
        "--raw-dir",
        help="Directory path to raw images.",
        default="./data/raw",
        type=str,
    )
    parser.add_argument(
        "--save-dir",
        help="Directory path to save resized images.",
        default="./data/images",
        type=str,
    )
    parser.add_argument(
        "--in-ext", help="Raw image files extension to resize.", default="jpg,png", type=str
    )
    parser.add_argument(
        "--out-ext", help="Raw image files extension to resize.", default="jpg", type=str
    )
    parser.add_argument(
        "--target-size",
        help="Target size to resize as a tuple of 2 integers.",
        default="(1000, 600)",
        type=str,
    )
    return parser

def main(args):
    raw_dir = args.raw_dir
    save_dir = args.save_dir
    in_ext = args.in_ext
    out_ext = args.out_ext
    target_size = eval(args.target_size)
    msg = "--target-size must be a tuple of 2 integers"
    assert isinstance(target_size, tuple) and len(target_size) == 2, msg
    in_types = in_ext.split(",")
    fnames = []
    for ext in in_types:
        fnames.extend( glob.glob(os.path.join(raw_dir, "*.{}".format(ext.strip() ) ) ) )
    #fnames = glob.glob(os.path.join(raw_dir, "*.{}".format(ext)))
    os.makedirs(save_dir, exist_ok=True)
    print(
        "{} files to resize from directory `{}` to target size:{}".format(
            len(fnames), raw_dir, target_size
        )
    )
    for i, fname in enumerate(fnames):
        print(".", end="", flush=True)
        img = cv2.imread(fname)
        img_small = cv2.resize(img, target_size)
        basename = os.path.basename(fname)
        name, _ = os.path.splitext(basename)
        new_fname = "{}.{}".format(name, out_ext)
        #new_fname = "{}.{}".format(str(i), out_ext)
        small_fname = os.path.join(save_dir, new_fname)
        cv2.imwrite(small_fname, img_small)
    print(
        "\nDone resizing {} files.\nSaved to directory: `{}`".format(
            len(fnames), save_dir
        )
    )

if __name__ == "__main__":

    parser = getParser()
    args = parser.parse_args()
    main(args)

    
