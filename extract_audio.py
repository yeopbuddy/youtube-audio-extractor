import sys
import subprocess
import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

DEFAULT_FFMPEG_DIR = r"YOUR_FFMPEG_DIR"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("YouTube Audio Extractor (yt-dlp)")
        self.geometry("820x520")

        self.url_var = tk.StringVar()
        self.format_var = tk.StringVar(value="mp3")  # mp3 / m4a
        self.out_dir_var = tk.StringVar(value=str(self.default_out_dir()))
        self.ffmpeg_dir_var = tk.StringVar(value=DEFAULT_FFMPEG_DIR)

        self._build_ui()

    def default_out_dir(self) -> Path: # 스크립트 위치 기준 outputs 고정
        base = Path(__file__).resolve().parent
        return base / "outputs"

    def _build_ui(self):
        pad = {"padx": 10, "pady": 6}

        frm = ttk.Frame(self)
        frm.pack(fill="both", expand=True, **pad)

        ttk.Label(frm, text="YouTube URL").grid(row=0, column=0, sticky="w") # URL
        url_entry = ttk.Entry(frm, textvariable=self.url_var, width=90)
        url_entry.grid(row=1, column=0, columnspan=3, sticky="we")
        url_entry.focus()

        ttk.Label(frm, text="저장 형식").grid(row=2, column=0, sticky="w", **pad) # Format
        fmt_frame = ttk.Frame(frm)
        fmt_frame.grid(row=3, column=0, sticky="w")

        ttk.Radiobutton(fmt_frame, text="MP3 (mp3_mf)", value="mp3", variable=self.format_var).pack(side="left", padx=6)
        ttk.Radiobutton(fmt_frame, text="M4A (추천)", value="m4a", variable=self.format_var).pack(side="left", padx=6)

        ttk.Label(frm, text="저장 경로").grid(row=4, column=0, sticky="w") # Output directory
        out_entry = ttk.Entry(frm, textvariable=self.out_dir_var, width=70)
        out_entry.grid(row=5, column=0, sticky="we")
        ttk.Button(frm, text="폴더 선택", command=self.browse_out_dir).grid(row=5, column=1, sticky="w", padx=8)

        ttk.Label(frm, text="ffmpeg folder (contains ffmpeg.exe/ffprobe.exe)").grid(row=6, column=0, sticky="w") # ffmpeg dir
        ff_entry = ttk.Entry(frm, textvariable=self.ffmpeg_dir_var, width=70)
        ff_entry.grid(row=7, column=0, sticky="we")
        ttk.Button(frm, text="폴더 선택", command=self.browse_ffmpeg_dir).grid(row=7, column=1, sticky="w", padx=8)

        btn_frame = ttk.Frame(frm) # Buttons
        btn_frame.grid(row=8, column=0, columnspan=3, sticky="w", pady=10)
        self.run_btn = ttk.Button(btn_frame, text="추출 시작", command=self.on_extract)
        self.run_btn.pack(side="left", padx=6)
        ttk.Button(btn_frame, text="저장 폴더 열기", command=self.open_output_folder).pack(side="left", padx=6)
        ttk.Button(btn_frame, text="로그 지우기", command=self.clear_log).pack(side="left", padx=6)

        self.progress = ttk.Progressbar(frm, mode="indeterminate") # Progress
        self.progress.grid(row=9, column=0, columnspan=3, sticky="we", pady=6)

        ttk.Label(frm, text="Log").grid(row=10, column=0, sticky="w") # Log
        self.log = tk.Text(frm, height=16, wrap="word")
        self.log.grid(row=11, column=0, columnspan=3, sticky="nsew")

        frm.columnconfigure(0, weight=1) # grid expand
        frm.rowconfigure(11, weight=1)

    def browse_out_dir(self):
        folder = filedialog.askdirectory()
        if folder:
            self.out_dir_var.set(folder)

    def browse_ffmpeg_dir(self):
        folder = filedialog.askdirectory()
        if folder:
            self.ffmpeg_dir_var.set(folder)

    def open_output_folder(self):
        out_dir = Path(self.out_dir_var.get())
        out_dir.mkdir(parents=True, exist_ok=True)
        subprocess.run(["explorer", str(out_dir)])

    def clear_log(self):
        self.log.delete("1.0", "end")

    def append_log(self, text: str):
        self.log.insert("end", text)
        self.log.see("end")

    def on_extract(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning("Missing URL", "유효하지 않은 YouTube URL")
            return

        out_dir = Path(self.out_dir_var.get())
        ffmpeg_dir = Path(self.ffmpeg_dir_var.get())

        if not ffmpeg_dir.exists():
            messagebox.showerror("ffmpeg not found", "ffmpeg 폴더 경로 오류\n(ffmpeg.exe/ffprobe.exe가 있는 폴더를 선택)")
            return

        out_dir.mkdir(parents=True, exist_ok=True)

        self.run_btn.configure(state="disabled")
        self.progress.start(10)
        self.append_log(f"\n=== START ===\nURL: {url}\nFormat: {self.format_var.get()}\nOutput: {out_dir}\nffmpeg: {ffmpeg_dir}\n\n")

        t = threading.Thread(target=self._run_yt_dlp, args=(url, str(out_dir), str(ffmpeg_dir), self.format_var.get()), daemon=True)
        t.start()

    def _run_yt_dlp(self, url: str, out_dir: str, ffmpeg_dir: str, fmt: str):
        try:
            # outputs 템플릿
            output_template = str(Path(out_dir) / "%(title)s [%(id)s].%(ext)s")

            cmd = [
                sys.executable, "-m", "yt_dlp",
                "--ffmpeg-location", ffmpeg_dir,
                "--no-playlist",
                "-x",
                "--audio-format", fmt,
                "--audio-quality", "0",
                "-o", output_template,
                url,
            ]

            if fmt == "mp3": # mp3는 mp3_mf 인코더 강제
                cmd.insert(cmd.index("-o"), "--postprocessor-args")
                cmd.insert(cmd.index("-o"), "ffmpeg:-c:a mp3_mf -b:a 192k")

            self._stream_process(cmd)

            self.after(0, lambda: self.append_log("\n 파일이 outputs 폴더에 저장되었습니다!\n"))
            self.after(0, lambda: messagebox.showinfo("Done", "추출 완료"))

        except subprocess.CalledProcessError as e:
            self.after(0, lambda: self.append_log(f"\nERROR (exit {e.returncode})\n"))
            self.after(0, lambda: messagebox.showerror("Error", "실행 중 오류 발생. Log 확인!"))
        except Exception as e:
            self.after(0, lambda: self.append_log(f"\nEXCEPTION: {e}\n"))
            self.after(0, lambda: messagebox.showerror("Exception", str(e)))
        finally:
            self.after(0, self._stop_ui)

    def _stream_process(self, cmd):
        self.after(0, lambda: self.append_log("Running:\n" + " ".join(cmd) + "\n\n"))

        # stdout/stderr 스트리밍
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, universal_newlines=True)
        for line in p.stdout:
            self.after(0, lambda s=line: self.append_log(s))
        p.wait()

        if p.returncode != 0:
            raise subprocess.CalledProcessError(p.returncode, cmd)

    def _stop_ui(self):
        self.progress.stop()
        self.run_btn.configure(state="normal")


if __name__ == "__main__":
    app = App()
    app.mainloop()