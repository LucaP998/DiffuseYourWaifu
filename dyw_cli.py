import random
import argparse
from src.diffuse_your_waifu import diffuse_your_waifu_client

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path" ,help="Path to a WAIFU", default=None)
    #BUG: if we write argument that start with #
    parser.add_argument("-e", "--extra", nargs="+", help="Add a list of extra hashtag", default=[])
    args = parser.parse_args()
    extra_hashtags = diffuse_your_waifu_client.correct_hashtags(args.extra)
    diffuse_your_waifu_client.upload_photo(args.path, extra_hashtags)
    
