"""语音识别服务：演示环境返回模拟转写；生产环境可接入 ASR SDK（如 FunASR /  Whisper / 云端语音转文字）。"""


def transcribe(audio_bytes: bytes, fmt: str = "webm") -> str:
    # TODO: 接入真实 ASR。当前返回模拟结果，保证语音答题链路可演示。
    return "我觉得这个岗位挺好的，然后我学过相关技术，然后做过类似项目，就是说比较有经验。"
