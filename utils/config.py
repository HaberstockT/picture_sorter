from pathlib import Path

import load_config

config, local_config = load_config.load()


def read_dirs(conf):
    envir = conf["environment"]
    inp = conf["input"]
    out = conf["output"]
    
    main_dir = Path(envir["main_dir"])
    sub_dir = main_dir / envir["sub_dir"]
    
    watch_dir = sub_dir / inp["watch_dir"]
    
    image_target_dir = sub_dir / out["image_target_dir"]
    video_target_dir = sub_dir / out["video_target_dir"]
    raw_target_dir = sub_dir / out["raw_target_dir"]
    duplicates_dir = sub_dir / out["duplicates_dir"]
    error_dir = sub_dir / out["error_dir"]
    index_db = sub_dir / out["index_db"]
    
    dirs = [
        watch_dir,
        image_target_dir,
        video_target_dir,
        raw_target_dir,
        duplicates_dir,
        error_dir,
        index_db,
    ]
    
    return dirs

def main():
    print(f"config: {config}")
    print(f"local_config: {local_config}")
    
    test_dirs = read_dirs(config)
    for dir in test_dirs:
        print(dir)
    
    
    dirs = read_dirs(local_config)
    for dir in dirs:
        print(dir)
    
if __name__ =="__main__":
    main()
