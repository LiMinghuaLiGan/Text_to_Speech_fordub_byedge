import os
import shutil
import pysrt
import edge_tts
import asyncio
# import winsound
from math import ceil
from pydub import AudioSegment
from ffmpeg import audio
def main():
    srtpath = "srt/"
    check_mkdir(srtpath)
    mysrt = pysrt.open("srt/1.srt")
    outfile = AudioSegment.empty()
    outfile += AudioSegment.silent(duration=mysrt[0].start.ordinal)
    i = 1
    '''
    辅助文件Auxiliary files
    '''
    tempfile='a.mp3'
    auxfile1='b.wav'
    auxfile2='c.wav'
    for part in mysrt:
        asyncio.get_event_loop().run_until_complete(tospeech(text=part.text, name=tempfile))
        yuyin = AudioSegment.from_mp3(tempfile)
        yuyin.export(auxfile1,format='wav')
        try:
            suitableduration = mysrt[i].start.ordinal - mysrt[i - 1].start.ordinal
            if yuyin.duration_seconds * 1000 > suitableduration:
                desiredincreaserate =ceil(yuyin.duration_seconds * 1000 / suitableduration * 100)
                while desiredincreaserate>200:
                    audio.a_speed(auxfile1,2,auxfile2)
                    shutil.copyfile(auxfile2,auxfile1)
                    desiredincreaserate/=2
                audio.a_speed(auxfile1, round(desiredincreaserate/100,1), auxfile2)
                yuyin=AudioSegment.from_wav(auxfile2)
            outfile += yuyin
            silent_time = mysrt[i].start.ordinal - ceil(outfile.duration_seconds * 1000)
            outfile += AudioSegment.silent(duration=silent_time)
        except:
            suitableduration = mysrt[i - 1].end.ordinal - mysrt[i - 1].start.ordinal
            if yuyin.duration_seconds * 1000 > suitableduration:
                desiredincreaserate = ceil(yuyin.duration_seconds * 1000 / suitableduration * 100)
                while desiredincreaserate > 200:
                    audio.a_speed(auxfile1, 2, auxfile2)
                    shutil.copyfile(auxfile2, auxfile1)
                    desiredincreaserate /= 2
                audio.a_speed(auxfile1, round(desiredincreaserate / 100, 1), auxfile2)
                yuyin = AudioSegment.from_wav(auxfile2)
            outfile += yuyin
        i += 1
    '''
    最终的完整配音导出路径和文件名，默认以wav格式导出为out.wav
    The final full dubbing export path and file name, the default export in wav format as out.wav
    '''
    outfile.export("out.wav", format="wav")


async def tospeech(text, name="a.mp3",setrate="+0%"):
    communicate = edge_tts.Communicate()
    with open(name, 'wb') as f:
        '''
        text:输入的语句Input text
        codec:#输出的音频文件格式编码方式，默认为Mp3，经过测试该编码方式比较稳定The output audio file format encoding method, the default is Mp3,
                after testing the default encoding method is more stable
        voice:语言类型和说话人音色选择Language type and speaker tone selection
        pitch:音调(频率)增加量Tone (frequency)increase amount
        rate:语速增加量speech speed increase amount 
        volume:音量(响度)增加量Volume (loudness) increase amount
        '''
        async for i in communicate.run(text,
        codec="audio-24khz-48kbitrate-mono-mp3",
        voice="Microsoft Server Speech Text to Speech Voice (en-US, AriaNeural)",
        # pitch="+0Hz",
        # rate=setrate,
        # volume="+0%",
        ):
            if i[2] is not None:
                f.write(i[2])
    f.close()

def check_mkdir(path):
    """
    检查一个目录是否存在，不存在则新建
    Check if a directory exists, or create a new one if it does not.
    """
    if not os.path.exists(path):
        os.makedirs(path)

if __name__ == "__main__":
    main()
    # winsound.Beep(500, 1000) #字幕转换语音完成后发出提示音Beep when subtitle to speech is complete

'''
测试过的支持语言
support language that has been test

en-US,AriaNeural
ja-JP,NanamiNeural
zh-CN,YunxiNeural


更多语言请参照edge大声朗读语音选项或参考https://juejin.cn/post/7042569859175022605
For more languages please refer to the edge read aloud voice option or refer tohttps://juejin.cn/post/7042569859175022605
'''