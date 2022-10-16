# Text_to_Speech_for_dub_by_edge
a Subtitle to speech tool
首先要有python运行环境，推荐anaconda+pycharm，之后安装代码中的包依赖，其中edge_tts来自https://github.com/rany2/edge-tts，建议运行pip install edge-tts命令。
然后需要下载ffmpeg，并将其加入到系统的环境变量的path中。
安装完成后克隆仓库到本地，把需要转成配音的字幕复制到srt文件下的1.srt中，再运行代码等待即可，配音文件会输出到代码统一目录下的out.wav中。在字幕的语句与其时间间隔较为不匹配的情况下，配音的语速会出现变快的情况，这是为了保证语音与字幕同步而加速了部分语句的语速的缘故。
电脑需要有edge且应该需要联网，经过测试至少支持中英日三种语言，更多的语言和音色请参照edge大声朗读语音选项或参考https://juejin.cn/post/7042569859175022605，使用过程不会产生任何费用。
本代码借鉴于https://github.com/rany2/edge-tts和https://github.com/kslz/srt-to-speech,在此鸣谢。
