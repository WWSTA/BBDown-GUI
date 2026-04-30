
[![img](https://img.shields.io/github/stars/WWSTA/BBDown-GUI?label=星标)](https://github.com/WWSTA/BBDown-GUI)  [![img](https://img.shields.io/github/license/WWSTA/BBDown-GUI?label=许可证)](https://github.com/WWSTA/BBDown-GUI)

> [!WARNING]
>
> 本项目仅供个人学习、研究和非商业性用途。用户在使用本工具时，需自行确保遵守相关法律法规，特别是与版权相关的法律条款。开发者不对因使用本工具而产生的任何版权纠纷或法律责任承担责任。请用户在使用时谨慎，确保其行为合法合规，并仅在有合法授权的情况下使用相关内容。
>

# BBDown GUI

[BBDown](https://github.com/nilaoda/BBDown) 的图形化界面版本，让你更轻松地下载哔哩哔哩视频！



# 注意

- 本软件需要 [BBDown](https://github.com/nilaoda/BBDown) 核心程序，请务必将 `BBDown.exe` 与 `BBDown_GUI.exe` 放在同一目录下
- 混流时需要外部程序：
  * 普通视频：[ffmpeg](https://www.gyan.dev/ffmpeg/builds/) 或 [mp4box](https://gpac.wp.imt.fr/downloads/)
  * 杜比视界：ffmpeg5.0以上或新版mp4box
- 使用 aria2c 下载时，需要将 `aria2c.exe` 放在同一目录下，或者指定地址

# 下载

Release 版本：https://github.com/WWSTA/BBDown-GUI/releases

# 快速开始

1. 下载 BBDown GUI 的最新 Release
2. 确保已下载 [BBDown](https://github.com/nilaoda/BBDown/releases) 并放在同一目录
3. 双击运行 `BBDown_GUI.exe`
4. 粘贴视频链接，配置下载选项
5. 点击「开始下载」，就这么简单！

# 功能

- [x] 支持普通视频、番剧、课程下载
- [x] 支持 WEB/TV/APP/国际版 API 模式
- [x] 交互式选择清晰度和编码格式
- [x] 多线程下载
- [x] 集成 aria2c 下载
- [x] 二维码登录 (WEB/TV)
- [x] 自定义文件名格式
- [x] 选择指定分P下载
- [x] 单独下载视频/音频/弹幕/字幕/封面
- [x] 一键复制生成的命令
- [x] 支持保存和加载配置

# 使用说明

## 基础设置

---

1. **视频链接**：可以直接粘贴完整链接，也可以只输入 BV 号、av 号，或者番剧的 ep/ss 号
2. **选择分P**：如果是多P视频，可以指定要下载哪些，比如 `1,3,5` 或 `1-10`，留空则下载所有
3. **API模式**：
   - WEB：默认模式
   - TV：通常能获取无水印视频
   - APP：适合移动端专属内容
   - 国际版：用于东南亚地区
4. **画质和编码**：选择你想要的画质优先级和编码格式

## 下载选项

---

- **仅解析信息**：只查看视频信息，不真的下载
- **多线程下载**：默认开启，速度更快
- **仅下载类型**：可以只下载视频、音频、弹幕、字幕或封面
- **其他选项**：每个功能后面都有问号按钮，点击即可查看详细说明

## 文件设置

---

- **工作目录**：视频要保存到哪里？留空的话就保存在程序运行目录
- **文件名格式**：可以自定义文件名
- **音频语言代码**：比如 `chi` 是中文，`jpn` 是日文

## 登录账号

---

有些视频需要登录才能下载：

1. 点击「登录(WEB)」或「登录(TV)」按钮
2. 会弹出命令行窗口，同时自动打开二维码图片
3. 用哔哩哔哩 APP 扫码登录
4. 登录成功后就可以下载需要权限的视频了

# 致谢

* [BBDown](https://github.com/nilaoda/BBDown) - 核心下载程序
* https://github.com/codebude/QRCoder
* https://github.com/icsharpcode/SharpZipLib
* https://github.com/protocolbuffers/protobuf
* https://github.com/grpc/grpc
* https://github.com/dotnet/command-line-api
* https://github.com/SocialSisterYi/bilibili-API-collect
* https://github.com/SeeFlowerX/bilibili-grpc-api
* https://github.com/FFmpeg/FFmpeg
* https://github.com/gpac/gpac
* https://github.com/aria2/aria2

# 许可证

本项目遵循 BBDown 的许可证要求。

