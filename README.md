# YouTube Audio Extractor (yt-dlp + Tkinter)

개인 PC에서 **YouTube 링크를 입력하면 음원을 MP3 또는 M4A로 추출**하는 간단한 GUI 프로그램입니다.  
내부적으로 `yt-dlp`와 `ffmpeg`를 사용합니다.

> ⚠️ **주의 / 면책**
> - 본 프로젝트는 **개인 학습/개인 사용 목적**의 예시입니다.
> - 저작권 및 각 플랫폼(YouTube 등)의 이용약관을 준수하세요.
> - **본인이 다운로드/변환할 권한이 있는 콘텐츠에 한해** 사용하세요.

---

## 1) 준비물

- Windows 10/11 (권장)
- Anaconda 또는 Miniconda 설치
- 인터넷 연결

---

## 2) 레포 구성 (최소)

이 레포는 단일 파이썬 파일로 구성됩니다.

```
.
├─ extract_audio.py                # (이 파일) GUI 실행 파일
└─ README.md
```

> 예시 코드에서는 `DEFAULT_FFMPEG_DIR = r"YOUR_FFMPEG_DIR"` 값을 본인 PC 경로로 바꿔야 합니다.

---

## 3) 가상환경 생성 및 활성화 (Anaconda Prompt)

### 3-1. 가상환경 만들기

Anaconda Prompt를 열고 아래를 실행하세요.

```bat
conda create -n yt_audio python=3.10 -y
conda activate yt_audio
```

> Python 3.10~3.12 중 편한 버전 사용 가능하지만, 처음엔 3.10 권장합니다.

---

## 4) ffmpeg 설치

### conda로 설치

```bat
conda install ffmpeg -y
```

설치 확인:

```bat
where ffmpeg
where ffprobe
ffmpeg -version
ffprobe -version
```

보통 아래처럼 가상환경 폴더 안에 설치됩니다.

- `...\envs\yt_audio\Library\bin\ffmpeg.exe`
- `...\envs\yt_audio\Library\bin\ffprobe.exe`

### 코드에 ffmpeg 경로 반영

`extract_audio.py` 상단의 `DEFAULT_FFMPEG_DIR`를 내 환경에 맞게 수정합니다.

예)
```python
DEFAULT_FFMPEG_DIR = r"C:\Users\<USER>\anaconda3\envs\yt_audio\Library\bin"
```

> `where ffmpeg` 결과에 나온 경로에서 `...\Library\bin` 폴더를 그대로 넣으면 됩니다.

---

## 5) yt-dlp 설치

⚠️ **중요:** pip는 반드시 `python -m pip` 방식으로 설치하세요. (환경 꼬임 방지)

```bat
python -m pip install -U yt-dlp
```

설치 확인:

```bat
python -c "import yt_dlp; print('yt_dlp OK')"
python -m yt_dlp --version
```

---

## 6) 실행 방법

### 6-1. extract_audio.py 실행

Anaconda Prompt에서 프로젝트 폴더로 이동 후:

```bat
conda activate yt_audio
python extract_audio.py
```

GUI가 뜨면:

1. YouTube URL 입력
2. 저장 형식 선택 (MP3 / M4A)
3. 저장 경로 확인/변경
4. **추출 시작**

추출 파일은 기본적으로 `extract_audio.py` 파일이 있는 폴더의 `outputs/`에 저장됩니다.

---

## 7) 자주 발생하는 문제 (Troubleshooting)

### 7-1. `ModuleNotFoundError: No module named 'yt_dlp'`

- `pip install`을 했는데도 안 되면, 아래처럼 다시 설치하세요:

```bat
conda activate yt_audio
python -m pip uninstall -y yt-dlp
python -m pip install -U yt-dlp
python -c "import yt_dlp; print('yt_dlp OK')"
```

> `pip`만 쓰면 다른 파이썬/pip가 잡히는 경우가 많습니다.  
> 항상 `python -m pip`를 사용하세요.

---

### 7-2. `ffprobe and ffmpeg not found`

- `DEFAULT_FFMPEG_DIR`가 잘못된 경우입니다.
- 아래로 확인하고 `Library\bin` 폴더를 코드에 넣으세요.

```bat
where ffmpeg
where ffprobe
```

예시 경로:
- `C:\Users\<USER>\anaconda3\envs\yt_audio\Library\bin\ffmpeg.exe`

코드에는 폴더까지만:
- `C:\Users\<USER>\anaconda3\envs\yt_audio\Library\bin`

---

### 7-3. MP3 추출이 실패함 (mp3 codec 관련)

환경에 따라 ffmpeg가 `libmp3lame`을 포함하지 않는 경우가 있어 MP3 인코딩이 실패할 수 있습니다.  
이 프로젝트는 그런 경우를 대비해 `mp3_mf`(Windows MediaFoundation) 인코더를 강제 사용합니다.

그래도 MP3가 실패하면:
- M4A로 추출해보세요 (대개 더 안정적)

---

### 7-4. 저장 경로에 파일이 안 생김

- 저장 경로에 **쓰기 권한**이 없을 수 있습니다.
- OneDrive 동기화 폴더/권한 제한 폴더에서 문제가 날 수 있으니, 임시로 `C:\Temp\outputs` 같은 경로로 바꿔서 테스트해보세요.

---

## 8) 라이선스

개인 프로젝트용으로 자유롭게 수정/사용하되, **yt-dlp / ffmpeg의 라이선스 및 배포 정책**은 각 프로젝트의 안내를 따르세요.

---

## 9) 참고

- yt-dlp: YouTube 등에서 미디어 정보를 가져오는 도구
- ffmpeg: 오디오/비디오 변환 도구

(이 레포는 설치/실행 방법을 쉽게 제공하는 것을 목표로 합니다.)
