import json
import os


def find_audio_files(directory, extensions, link='https://github.com/DiffPitcher/speech_audio/raw/main/'):
    """
    遍历目录，查找指定扩展名的音频文件，并生成适用的<audio>标签列表。

    :param directory: 要搜索的目录路径。
    :param extensions: 音频文件扩展名列表。
    :return: 适配特定格式的字典列表。
    """
    speakers_list = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                speaker_id = os.path.basename(root)
                # 构造audio标签
                file_path = os.path.join(link+root, file).replace('\\', '/')
                audio_tag = f'<audio controls src=\"{file_path}\"></audio>'
                # 查找或创建speaker条目
                speaker_entry = next((item for item in speakers_list if item["speaker"] == speaker_id), None)
                if speaker_entry is None:
                    speaker_entry = {"speaker": speaker_id}
                    speakers_list.append(speaker_entry)
                    # 根据当前speaker条目中的条目数量决定是否添加autoplay
                sample_key = f"sample{len(speaker_entry)}"
                autoplay_attr = " autoplay" if len(speaker_entry) == 1 else ""  # 第一个文件添加autoplay属性
                audio_tag = f'<audio{autoplay_attr} controls src=\"{file_path}\"></audio>'
                speaker_entry[sample_key] = audio_tag

    return speakers_list


if __name__ == '__main__':
    directory = "vctk"
    extensions = ['mic1.flac', '.wav']

    speakers = find_audio_files(directory, extensions)

    # 将结果保存到JSON文件
    output_file = 'stimuli.js'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("var speakers =\n")
        json.dump(speakers, f, indent=2, ensure_ascii=False)

    print(f"Audio files have been saved to {output_file}.")
