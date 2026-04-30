import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import subprocess
import threading
import os
import configparser


class ModernBBDownGUI:
    def __init__(self, root):
        self.root = root
        self.root.title('BBDown GUI v1.0.0 - 哔哩哔哩下载器')
        self.root.geometry('1000x700')
        self.root.minsize(900, 600)
        
        self.gui_config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'BBDownGUI.config')
        
        self.setup_theme()
        self.create_main_interface()
        self.load_config()
        
        # 绑定窗口大小变化事件
        self.root.bind('<Configure>', self.on_window_resize)
    
    def show_help(self, title, content):
        """显示帮助弹窗"""
        help_window = tk.Toplevel(self.root)
        help_window.title(f'帮助 - {title}')
        help_window.geometry('600x400')
        help_window.minsize(400, 300)
        
        text = scrolledtext.ScrolledText(help_window, wrap=tk.WORD, font=("Microsoft YaHei UI", 10))
        text.pack(fill='both', expand=True, padx=10, pady=10)
        text.insert('1.0', content)
        text.config(state='disabled')
        
        close_btn = ttk.Button(help_window, text='关闭', command=help_window.destroy)
        close_btn.pack(pady=5)
    
    def on_window_resize(self, event):
        """窗口大小变化时的处理"""
        if event.widget == self.root:
            # Canvas 自动处理滚动
            pass
    
    def setup_theme(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        default_font = ("Microsoft YaHei UI", 9)
        
        style.configure('.', font=default_font, background='#f8f9fa', foreground='#212529')
        style.configure('Main.TFrame', background='#f8f9fa')
        style.configure('Card.TFrame', background='#ffffff')
        style.configure('Title.TLabel', font=("Microsoft YaHei UI", 18, "bold"), 
                       background='#f8f9fa', foreground='#212529')
        style.configure('Header.TLabel', font=("Microsoft YaHei UI", 11, "bold"), 
                       background='#ffffff', foreground='#343a40')
        style.configure('Normal.TLabel', font=default_font, 
                       background='#ffffff', foreground='#495057')
        style.configure('Small.TLabel', font=("Microsoft YaHei UI", 8), 
                       background='#ffffff', foreground='#6c757d')
        style.configure('TButton', font=default_font, padding=8)
        style.configure('Primary.TButton', font=("Microsoft YaHei UI", 9, "bold"), padding=8)
        style.configure('TCheckbutton', font=default_font, background='#ffffff')
        style.configure('TRadiobutton', font=default_font, background='#ffffff')
        style.configure('TEntry', font=default_font)
        style.configure('TCombobox', font=default_font)
        style.configure('TSpinbox', font=default_font)
        style.configure('TSeparator', background='#dee2e6')
        style.configure('Help.TButton', font=("Microsoft YaHei UI", 8, "bold"), 
                       padding=2, background='#e9ecef', borderwidth=1)
        
        style.configure('Card.TLabelframe', background='#ffffff', borderwidth=2, relief='groove')
        style.configure('Card.TLabelframe.Label', font=("Microsoft YaHei UI", 10, "bold"), 
                       background='#ffffff', foreground='#495057')
    
    def create_main_interface(self):
        self.canvas = tk.Canvas(self.root, background='#f8f9fa', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.root, orient='vertical', command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style='Main.TFrame')
        
        self.scrollable_frame.bind(
            '<Configure>',
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        )
        
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        self.canvas.bind('<Configure>', self._on_canvas_configure)
        self.canvas.bind_all('<MouseWheel>', self._on_mousewheel)
        
        self.canvas.pack(side='left', fill='both', expand=True)
        self.scrollbar.pack(side='right', fill='y')
        
        main_container = ttk.Frame(self.scrollable_frame, style='Main.TFrame')
        main_container.pack(fill='both', expand=True, padx=10, pady=10)
        
        header_frame = ttk.Frame(main_container, style='Main.TFrame')
        header_frame.pack(fill='x', pady=(0, 10))
        
        title_label = ttk.Label(header_frame, text='🎬 BBDown GUI', style='Title.TLabel')
        title_label.pack(side='left')
        
        notebook = ttk.Notebook(main_container)
        notebook.pack(fill='both', expand=True)
        
        self.create_basic_tab(notebook)
        self.create_download_tab(notebook)
        self.create_advanced_tab(notebook)
        self.create_about_tab(notebook)
        
        bottom_frame = ttk.Frame(main_container, style='Main.TFrame')
        bottom_frame.pack(fill='x', pady=(10, 0))
        
        self.create_command_preview(bottom_frame)
        self.create_action_buttons(bottom_frame)
    
    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_window, width=event.width)
    
    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
    
    def create_card_frame(self, parent, title, help_content=None):
        card_frame = ttk.Frame(parent, style='Card.TFrame')
        card_frame.pack(fill='x', pady=5)
        
        header_frame = ttk.Frame(card_frame, style='Card.TFrame')
        header_frame.pack(fill='x', anchor='w')
        
        ttk.Label(header_frame, text=title, style='Header.TLabel').pack(side='left')
        
        if help_content:
            help_btn = ttk.Button(header_frame, text='?', width=3, style='Help.TButton',
                                command=lambda: self.show_help(title, help_content))
            help_btn.pack(side='left', padx=5)
        
        content_frame = ttk.LabelFrame(card_frame, text='', style='Card.TLabelframe', padding=15)
        content_frame.pack(fill='x')
        
        return content_frame
    
    def create_basic_tab(self, parent):
        tab = ttk.Frame(parent, style='Main.TFrame')
        parent.add(tab, text='  基础设置  ', padding=15)
        
        self.create_url_card(tab)
        ttk.Separator(tab, orient='horizontal').pack(fill='x', pady=15)
        self.create_api_card(tab)
        ttk.Separator(tab, orient='horizontal').pack(fill='x', pady=15)
        self.create_quality_card(tab)
    
    def create_url_card(self, parent):
        help_text = """📺 视频输入帮助

【视频链接】
- 支持多种链接格式：
  - 标准 B 站视频链接（https://www.bilibili.com/video/BV...）
  - 番剧/电影链接（https://www.bilibili.com/bangumi/play/...）
  - 直接输入 BV 号或 av 号（例如：BV1xx411c7mD）
  - ep/ss 号（番剧专用）

【选择分P】
- 选择指定分P或分P范围
- 示例：
  - 单个分P：5
  - 多个分P：1,3,5
  - 范围：3-7
  - 所有分P：ALL
  - 最新分P：LAST
  - 组合：3,5,7-10

- 如果不填，默认下载所有分P
"""
        card = self.create_card_frame(parent, '📺 视频输入', help_text)
        
        url_frame = ttk.Frame(card, style='Card.TFrame')
        url_frame.pack(fill='x', pady=(0, 10))
        ttk.Label(url_frame, text='视频链接:', style='Normal.TLabel').pack(anchor='w')
        self.url_entry = ttk.Entry(url_frame, font=("Microsoft YaHei UI", 10))
        self.url_entry.pack(fill='x', pady=(5, 0))
        
        page_frame = ttk.Frame(card, style='Card.TFrame')
        page_frame.pack(fill='x')
        ttk.Label(page_frame, text='选择分P:', style='Normal.TLabel').pack(side='left')
        self.page_entry = ttk.Entry(page_frame)
        self.page_entry.pack(side='left', fill='x', expand=True, padx=(10, 0))
        ttk.Label(page_frame, text='(示例: 1,2,3-5,ALL,LAST)', style='Small.TLabel').pack(side='left', padx=(10, 0))
    
    def create_api_card(self, parent):
        help_text = """🔌 API模式帮助

【WEB 模式】
- 默认解析模式
- 使用网页端接口
- 适合普通视频下载

【TV 模式】
- 使用电视端接口
- 通常提供无水印视频
- 画质选择更丰富

【APP 模式】
- 使用手机端接口
- 某些视频可能只能通过此模式下载
- 适合移动端专属内容

【国际版】
- 用于下载东南亚地区的内容
- 需要配合区域设置使用
"""
        card = self.create_card_frame(parent, '🔌 API 模式', help_text)
        
        api_frame = ttk.Frame(card, style='Card.TFrame')
        api_frame.pack(fill='x')
        
        self.api_mode = tk.StringVar(value='web')
        
        ttk.Radiobutton(api_frame, text='🌐 WEB 模式 (默认)', variable=self.api_mode, value='web').pack(side='left', padx=(0, 30))
        ttk.Radiobutton(api_frame, text='📺 TV 模式 (无水印)', variable=self.api_mode, value='tv').pack(side='left', padx=(0, 30))
        ttk.Radiobutton(api_frame, text='📱 APP 模式', variable=self.api_mode, value='app').pack(side='left', padx=(0, 30))
        ttk.Radiobutton(api_frame, text='🌍 国际版', variable=self.api_mode, value='intl').pack(side='left')
    
    def create_quality_card(self, parent):
        help_text = """🎨 画质和编码帮助

【画质优先级】
- 指定首选画质，用逗号分隔
- 例如：8K 超高清,4K 超清,1080P 高码率,1080P 高清,720P 高清
- 程序会按顺序尝试下载，直到找到可用画质

【编码优先级】
- 指定视频编码格式优先级
- 常用编码：
  - hevc (H.265，压缩率高，文件小)
  - av1 (新一代编码，压缩率更高)
  - avc (H.264，兼容性好)
- 例如：hevc,av1,avc

【交互式选择清晰度】
- 开启后，下载前会弹出窗口让您手动选择清晰度
- 适合需要精确控制画质的情况
"""
        card = self.create_card_frame(parent, '🎨 画质和编码', help_text)
        
        left_frame = ttk.Frame(card, style='Card.TFrame')
        left_frame.pack(side='left', fill='both', expand=True)
        
        ttk.Label(left_frame, text='画质优先级:', style='Normal.TLabel').pack(anchor='w')
        self.dfn_entry = ttk.Entry(left_frame)
        self.dfn_entry.insert(0, '8K 超高清,4K 超清,1080P 高码率,1080P 高清,720P 高清')
        self.dfn_entry.pack(fill='x', pady=(5, 15))
        
        right_frame = ttk.Frame(card, style='Card.TFrame')
        right_frame.pack(side='right', fill='both', expand=True, padx=(20, 0))
        
        ttk.Label(right_frame, text='编码优先级:', style='Normal.TLabel').pack(anchor='w')
        self.encoding_entry = ttk.Entry(right_frame)
        self.encoding_entry.insert(0, 'hevc,av1,avc')
        self.encoding_entry.pack(fill='x', pady=(5, 0))
        
        self.interactive_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(card, text='交互式选择清晰度', variable=self.interactive_var).pack(anchor='w', pady=(10, 0))
    
    def create_download_tab(self, parent):
        tab = ttk.Frame(parent, style='Main.TFrame')
        parent.add(tab, text='  下载选项  ', padding=15)
        
        self.create_download_options_card(tab)
        ttk.Separator(tab, orient='horizontal').pack(fill='x', pady=15)
        self.create_file_card(tab)
        ttk.Separator(tab, orient='horizontal').pack(fill='x', pady=15)
        self.create_aria2c_card(tab)
    
    def create_download_options_card(self, parent):
        help_text = """⚙️ 下载设置帮助

【仅解析信息】
- 只解析视频信息，不实际下载
- 适合查看视频详情、分P列表等

【多线程下载】
- 默认开启
- 使用多个线程同时下载，速度更快

【仅下载类型】
- 可以只下载视频、音频、弹幕、字幕或封面
- 互斥选项，最多选一个

【其他选项】
- 下载弹幕：同时下载视频的弹幕文件
- 跳过字幕：不下载字幕文件
- 跳过封面：不下载视频封面
- 跳过混流：只下载音视频文件，不合并为MP4
- 跳过AI字幕：不下载自动生成的字幕（默认开启）
- 使用MP4Box：用MP4Box而不是FFmpeg混流
- 视频/音频升序：优先选择码率最低的版本（小体积优先）
- 允许PCDN：不替换PCDN域名（通常不推荐）
- 强制HTTP：强制使用HTTP协议下载（默认开启）
- 保存记录到文件：保存下载记录，后续跳过已下载
"""
        card = self.create_card_frame(parent, '⚙️ 下载设置', help_text)
        
        top_frame = ttk.Frame(card, style='Card.TFrame')
        top_frame.pack(fill='x', pady=(0, 10))
        
        self.only_info_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(top_frame, text='仅解析信息', variable=self.only_info_var).pack(side='left', padx=(0, 20))
        
        self.mt_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(top_frame, text='多线程下载', variable=self.mt_var).pack(side='left', padx=(0, 20))
        
        type_frame = ttk.LabelFrame(card, text='仅下载类型', style='Card.TLabelframe', padding=10)
        type_frame.pack(fill='x', pady=(10, 0))
        
        self.video_only_var = tk.BooleanVar(value=False)
        self.audio_only_var = tk.BooleanVar(value=False)
        self.danmaku_only_var = tk.BooleanVar(value=False)
        self.sub_only_var = tk.BooleanVar(value=False)
        self.cover_only_var = tk.BooleanVar(value=False)
        
        ttk.Checkbutton(type_frame, text='仅视频', variable=self.video_only_var).pack(side='left', padx=(0, 15))
        ttk.Checkbutton(type_frame, text='仅音频', variable=self.audio_only_var).pack(side='left', padx=(0, 15))
        ttk.Checkbutton(type_frame, text='仅弹幕', variable=self.danmaku_only_var).pack(side='left', padx=(0, 15))
        ttk.Checkbutton(type_frame, text='仅字幕', variable=self.sub_only_var).pack(side='left', padx=(0, 15))
        ttk.Checkbutton(type_frame, text='仅封面', variable=self.cover_only_var).pack(side='left')
        
        other_frame = ttk.LabelFrame(card, text='其他选项', style='Card.TLabelframe', padding=10)
        other_frame.pack(fill='x', pady=(10, 0))
        
        self.download_danmaku_var = tk.BooleanVar(value=False)
        self.skip_subtitle_var = tk.BooleanVar(value=False)
        self.skip_cover_var = tk.BooleanVar(value=False)
        self.skip_mux_var = tk.BooleanVar(value=False)
        self.skip_ai_var = tk.BooleanVar(value=True)
        self.use_mp4box_var = tk.BooleanVar(value=False)
        self.video_ascending_var = tk.BooleanVar(value=False)
        self.audio_ascending_var = tk.BooleanVar(value=False)
        self.allow_pcdn_var = tk.BooleanVar(value=False)
        self.force_http_var = tk.BooleanVar(value=True)
        self.save_archives_var = tk.BooleanVar(value=False)
        
        # 固定分组多行布局 - 更稳定可靠
        # 第一行
        row1 = ttk.Frame(other_frame, style='Card.TFrame')
        row1.pack(fill='x', pady=2)
        ttk.Checkbutton(row1, text='下载弹幕', variable=self.download_danmaku_var).pack(side='left', padx=(0, 15))
        ttk.Checkbutton(row1, text='跳过字幕', variable=self.skip_subtitle_var).pack(side='left', padx=(0, 15))
        ttk.Checkbutton(row1, text='跳过封面', variable=self.skip_cover_var).pack(side='left', padx=(0, 15))
        ttk.Checkbutton(row1, text='跳过混流', variable=self.skip_mux_var).pack(side='left', padx=(0, 15))
        ttk.Checkbutton(row1, text='跳过AI字幕', variable=self.skip_ai_var).pack(side='left', padx=(0, 15))
        
        # 第二行
        row2 = ttk.Frame(other_frame, style='Card.TFrame')
        row2.pack(fill='x', pady=2)
        ttk.Checkbutton(row2, text='使用MP4Box', variable=self.use_mp4box_var).pack(side='left', padx=(0, 15))
        ttk.Checkbutton(row2, text='视频升序(小体积优先)', variable=self.video_ascending_var).pack(side='left', padx=(0, 15))
        ttk.Checkbutton(row2, text='音频升序(小体积优先)', variable=self.audio_ascending_var).pack(side='left', padx=(0, 15))
        
        # 第三行
        row3 = ttk.Frame(other_frame, style='Card.TFrame')
        row3.pack(fill='x', pady=2)
        ttk.Checkbutton(row3, text='允许PCDN', variable=self.allow_pcdn_var).pack(side='left', padx=(0, 15))
        ttk.Checkbutton(row3, text='强制HTTP', variable=self.force_http_var).pack(side='left', padx=(0, 15))
        ttk.Checkbutton(row3, text='保存下载记录', variable=self.save_archives_var).pack(side='left')
    
    def create_file_card(self, parent):
        help_text = """📁 文件设置帮助

【工作目录】
- 指定下载文件保存的目录
- 如果不填，默认保存到程序运行目录
- 建议设置一个专门的下载目录

【单P文件名格式】
- 自定义单个视频的文件名
- 可用变量：
  <videoTitle> 视频标题
  <pageNumber> 分P序号
  <pageNumberWithZero> 分P序号（补零）
  <pageTitle> 分P标题
  <bvid> BV号
  <aid> aid
  <cid> cid
  <dfn> 清晰度
  <res> 分辨率
  <fps> 帧率
  <videoCodecs> 视频编码
  <videoBandwidth> 视频码率
  <audioCodecs> 音频编码
  <audioBandwidth> 音频码率
  <ownerName> 作者名
  <ownerMid> 作者ID
  <publishDate> 发布日期
  <videoDate> 视频日期
  <apiType> API类型

- 示例：<videoTitle> - <pageTitle>

【多P文件名格式】
- 自定义多P视频的文件名
- 默认：<videoTitle>/[P<pageNumberWithZero>]<pageTitle>
- 会创建一个以视频标题命名的文件夹，分P放在里面

【音频语言代码】
- 指定混流时使用的音频语言
- 例如：chi（中文）、jpn（日文）
- 如果不填，使用默认音轨
"""
        card = self.create_card_frame(parent, '📁 文件设置', help_text)
        
        dir_frame = ttk.Frame(card, style='Card.TFrame')
        dir_frame.pack(fill='x', pady=(0, 10))
        ttk.Label(dir_frame, text='工作目录:', style='Normal.TLabel').pack(anchor='w')
        dir_input = ttk.Frame(dir_frame, style='Card.TFrame')
        dir_input.pack(fill='x', pady=(5, 0))
        self.work_dir_entry = ttk.Entry(dir_input)
        self.work_dir_entry.pack(side='left', fill='x', expand=True)
        ttk.Button(dir_input, text='浏览', command=self.browse_work_dir).pack(side='left', padx=(10, 0))
        
        file_frame = ttk.Frame(card, style='Card.TFrame')
        file_frame.pack(fill='x', pady=(0, 10))
        ttk.Label(file_frame, text='单P文件名格式:', style='Normal.TLabel').pack(anchor='w')
        self.file_pattern_entry = ttk.Entry(file_frame)
        self.file_pattern_entry.insert(0, '<videoTitle>')
        self.file_pattern_entry.pack(fill='x', pady=(5, 0))
        
        multi_frame = ttk.Frame(card, style='Card.TFrame')
        multi_frame.pack(fill='x')
        ttk.Label(multi_frame, text='多P文件名格式:', style='Normal.TLabel').pack(anchor='w')
        self.multi_file_pattern_entry = ttk.Entry(multi_frame)
        self.multi_file_pattern_entry.insert(0, '<videoTitle>/[P<pageNumberWithZero>]<pageTitle>')
        self.multi_file_pattern_entry.pack(fill='x', pady=(5, 0))
        
        lang_frame = ttk.Frame(card, style='Card.TFrame')
        lang_frame.pack(fill='x', pady=(10, 0))
        ttk.Label(lang_frame, text='音频语言代码:', style='Normal.TLabel').pack(anchor='w')
        ttk.Label(lang_frame, text='例如: chi(中文), jpn(日文)', style='Small.TLabel').pack(anchor='w')
        self.language_entry = ttk.Entry(lang_frame)
        self.language_entry.pack(fill='x', pady=(5, 0))
    
    def create_aria2c_card(self, parent):
        help_text = """🚀 Aria2c 设置帮助

【启用Aria2c下载】
- 使用aria2c下载器进行下载
- 适合大文件或需要更稳定下载的情况
- 需要自行准备aria2c可执行文件

【连接数 (-x)】
- 单个文件的连接数
- 建议：8-16
- 数值越大，下载越快，但可能被服务器限制
- 注意：aria2c 限制最大为 16

【服务器连接数 (-s)】
- 同时连接到服务器的数量
- 建议：8-16
- 注意：aria2c 限制最大为 16

【并发任务数 (-j)】
- 同时下载的任务数
- 建议：1-16

【分片大小 (-k)】
- 每个分片的大小
- 例如：1M、2M、5M、10M、20M
- 分片越小，连接数利用越充分，但开销稍大

【Aria2c路径】
- 指定aria2c可执行文件的路径
- 如果不填，尝试从系统PATH中查找

【自定义参数】
- 可添加其他aria2c参数
- 多个参数用空格分隔
"""
        card = self.create_card_frame(parent, '🚀 Aria2c 设置', help_text)
        
        self.use_aria2_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(card, text='启用 Aria2c 下载', variable=self.use_aria2_var, command=self.toggle_aria2c_options).pack(anchor='w', pady=(0, 10))
        
        self.aria2c_options_frame = ttk.Frame(card, style='Card.TFrame')
        self.aria2c_options_frame.pack(fill='x')
        
        left_col1 = ttk.Frame(self.aria2c_options_frame, style='Card.TFrame')
        left_col1.pack(side='left', fill='both', expand=True)
        
        ttk.Label(left_col1, text='连接数 (-x):', style='Normal.TLabel').pack(anchor='w')
        self.aria2c_x = tk.StringVar(value='16')
        x_spin = ttk.Spinbox(left_col1, from_=1, to=16, textvariable=self.aria2c_x, width=10)
        x_spin.pack(anchor='w', pady=(5, 10))
        self.aria2c_x.trace_add('write', lambda *args: self.validate_aria2c_num(self.aria2c_x))
        
        ttk.Label(left_col1, text='服务器连接数 (-s):', style='Normal.TLabel').pack(anchor='w')
        self.aria2c_s = tk.StringVar(value='16')
        s_spin = ttk.Spinbox(left_col1, from_=1, to=16, textvariable=self.aria2c_s, width=10)
        s_spin.pack(anchor='w', pady=(5, 10))
        self.aria2c_s.trace_add('write', lambda *args: self.validate_aria2c_num(self.aria2c_s))
        
        ttk.Label(left_col1, text='并发任务数 (-j):', style='Normal.TLabel').pack(anchor='w')
        self.aria2c_j = tk.StringVar(value='16')
        j_spin = ttk.Spinbox(left_col1, from_=1, to=16, textvariable=self.aria2c_j, width=10)
        j_spin.pack(anchor='w')
        self.aria2c_j.trace_add('write', lambda *args: self.validate_aria2c_num(self.aria2c_j))
        
        right_col1 = ttk.Frame(self.aria2c_options_frame, style='Card.TFrame')
        right_col1.pack(side='right', fill='both', expand=True, padx=(20, 0))
        
        ttk.Label(right_col1, text='分片大小 (-k):', style='Normal.TLabel').pack(anchor='w')
        self.aria2c_k = tk.StringVar(value='5M')
        k_combo = ttk.Combobox(right_col1, textvariable=self.aria2c_k, values=['1M', '2M', '5M', '10M', '20M'], width=10)
        k_combo.pack(anchor='w', pady=(5, 10))
        
        ttk.Label(right_col1, text='Aria2c 路径:', style='Normal.TLabel').pack(anchor='w')
        aria2_path_frame = ttk.Frame(right_col1, style='Card.TFrame')
        aria2_path_frame.pack(fill='x', pady=(5, 0))
        self.aria2c_path_entry = ttk.Entry(aria2_path_frame)
        self.aria2c_path_entry.pack(side='left', fill='x', expand=True)
        ttk.Button(aria2_path_frame, text='浏览', command=lambda: self.browse_file(self.aria2c_path_entry)).pack(side='left', padx=(5, 0))
        
        self.aria2c_options_frame.pack_forget()
        
        advanced_frame = ttk.Frame(card, style='Card.TFrame')
        advanced_frame.pack(fill='x', pady=(10, 0))
        ttk.Label(advanced_frame, text='自定义参数:', style='Normal.TLabel').pack(anchor='w')
        self.aria2c_args_entry = ttk.Entry(advanced_frame)
        self.aria2c_args_entry.pack(fill='x', pady=(5, 0))
        self.aria2c_args_entry.insert(0, '')
        advanced_frame.pack_forget()
        
        self.aria2c_advanced_frame = advanced_frame
    
    def validate_aria2c_num(self, var):
        """验证 aria2c 的数值参数，确保在 1-16 范围内"""
        try:
            val = var.get()
            if val:  # 只有当有值时才验证
                num = int(val)
                if num < 1:
                    var.set('1')
                elif num > 16:
                    var.set('16')
        except ValueError:
            # 如果不是有效数字，恢复为默认值 16
            var.set('16')
    
    def toggle_aria2c_options(self):
        if self.use_aria2_var.get():
            self.aria2c_options_frame.pack(fill='x')
            self.aria2c_advanced_frame.pack(fill='x', pady=(10, 0))
        else:
            self.aria2c_options_frame.pack_forget()
            self.aria2c_advanced_frame.pack_forget()
    
    def create_advanced_tab(self, parent):
        tab = ttk.Frame(parent, style='Main.TFrame')
        parent.add(tab, text='  高级设置  ', padding=15)
        
        # 第一组：认证相关
        self.create_auth_card(tab)
        ttk.Separator(tab, orient='horizontal').pack(fill='x', pady=15)
        
        # 第二组：工具路径
        self.create_tools_card(tab)
        ttk.Separator(tab, orient='horizontal').pack(fill='x', pady=15)
        
        # 第三组：网络设置
        self.create_network_card(tab)
        ttk.Separator(tab, orient='horizontal').pack(fill='x', pady=15)
        
        # 第四组：其他高级选项
        self.create_misc_advanced_card(tab)
    
    def create_auth_card(self, parent):
        help_text = """🔐 认证设置帮助

【Cookie (SESSDATA)】
- 用于下载需要登录的视频（会员、付费等）
- 获取方法：
  1. 在浏览器中登录 B 站
  2. 按 F12 打开开发者工具
  3. 进入 Network 或 Application 标签
  4. 找到 Cookie 中的 SESSDATA
  5. 复制其值填入

- 注意：Cookie有有效期，过期需要重新获取

【Access Token】
- 用于 TV/APP 模式的认证
- 通过登录功能获取，或者从手机端提取
- 配合 BiliPlus 使用时需要
"""
        card = self.create_card_frame(parent, '🔐 认证设置', help_text)
        
        cookie_frame = ttk.Frame(card, style='Card.TFrame')
        cookie_frame.pack(side='left', fill='both', expand=True)
        ttk.Label(cookie_frame, text='Cookie (SESSDATA):', style='Normal.TLabel').pack(anchor='w')
        self.cookie_entry = ttk.Entry(cookie_frame)
        self.cookie_entry.pack(fill='x', pady=(5, 0))
        
        token_frame = ttk.Frame(card, style='Card.TFrame')
        token_frame.pack(side='right', fill='both', expand=True, padx=(20, 0))
        ttk.Label(token_frame, text='Access Token:', style='Normal.TLabel').pack(anchor='w')
        self.token_entry = ttk.Entry(token_frame)
        self.token_entry.pack(fill='x', pady=(5, 0))
    
    def create_tools_card(self, parent):
        help_text = """🛠️ 工具和配置帮助

【FFmpeg路径】
- 指定 FFmpeg 可执行文件的路径
- FFmpeg 用于音视频混流
- 如果不填，尝试从系统 PATH 中查找
- 如果找不到，下载功能可能受限

【MP4Box路径】
- 指定 MP4Box 可执行文件的路径
- MP4Box 用于 MP4 格式混流
- 配合"使用MP4Box"选项使用
- 如果不填，尝试从系统 PATH 中查找

【配置文件】
- 指定 BBDown 配置文件路径
- 这是 BBDown 命令行程序的原生配置文件
- 如果不填，使用默认配置（BBDown.config）
- 注意：GUI 的设置会自动保存到 BBDownGUI.config，无需手动配置此项
"""
        card = self.create_card_frame(parent, '🛠️ 工具和配置', help_text)
        
        ffmpeg_frame = ttk.Frame(card, style='Card.TFrame')
        ffmpeg_frame.pack(side='left', fill='both', expand=True)
        ttk.Label(ffmpeg_frame, text='FFmpeg 路径:', style='Normal.TLabel').pack(anchor='w')
        ffmpeg_input = ttk.Frame(ffmpeg_frame, style='Card.TFrame')
        ffmpeg_input.pack(fill='x', pady=(5, 0))
        self.ffmpeg_path_entry = ttk.Entry(ffmpeg_input)
        self.ffmpeg_path_entry.pack(side='left', fill='x', expand=True)
        ttk.Button(ffmpeg_input, text='浏览', command=lambda: self.browse_file(self.ffmpeg_path_entry)).pack(side='left', padx=(5, 0))
        
        mp4box_frame = ttk.Frame(card, style='Card.TFrame')
        mp4box_frame.pack(side='right', fill='both', expand=True, padx=(20, 0))
        ttk.Label(mp4box_frame, text='MP4Box 路径:', style='Normal.TLabel').pack(anchor='w')
        mp4box_input = ttk.Frame(mp4box_frame, style='Card.TFrame')
        mp4box_input.pack(fill='x', pady=(5, 0))
        self.mp4box_path_entry = ttk.Entry(mp4box_input)
        self.mp4box_path_entry.pack(side='left', fill='x', expand=True)
        ttk.Button(mp4box_input, text='浏览', command=lambda: self.browse_file(self.mp4box_path_entry)).pack(side='left', padx=(5, 0))
        
        config_frame = ttk.Frame(card, style='Card.TFrame')
        config_frame.pack(fill='x', pady=(15, 0))
        ttk.Label(config_frame, text='配置文件:', style='Normal.TLabel').pack(anchor='w')
        config_input = ttk.Frame(config_frame, style='Card.TFrame')
        config_input.pack(fill='x', pady=(5, 0))
        self.config_file_entry = ttk.Entry(config_input)
        self.config_file_entry.pack(side='left', fill='x', expand=True)
        ttk.Button(config_input, text='浏览', command=lambda: self.browse_file(self.config_file_entry)).pack(side='left', padx=(5, 0))
    
    def create_network_card(self, parent):
        help_text = """🌐 网络设置帮助

【UPOS Host】
- 自定义 UPOS（上传/下载）服务器地址
- 用于解决某些网络环境下的下载问题
- 通常不需要填写

【BiliPlus Host】
- 指定 BiliPlus 代理服务器地址
- 配合 Access Token 使用
- 用于下载某些受限内容

【BiliPlus EP Host】
- 指定 BiliPlus EP（番剧）代理服务器
- 用于代理番剧相关接口

【区域】
- 使用 BiliPlus 时必须指定
- 可选值：hk（香港）、tw（台湾）、th（泰国）

【分P下载间隔】
- 下载多个分P时，每个分P之间的等待时间（秒）
- 避免请求过快被服务器限制
- 建议：2-5秒

【User-Agent】
- 自定义浏览器 User-Agent
- 模拟特定浏览器访问
- 留空则使用随机 User-Agent
"""
        card = self.create_card_frame(parent, '🌐 网络设置', help_text)
        
        left_net = ttk.Frame(card, style='Card.TFrame')
        left_net.pack(side='left', fill='both', expand=True)
        
        ttk.Label(left_net, text='UPOS Host:', style='Normal.TLabel').pack(anchor='w')
        self.upos_host_entry = ttk.Entry(left_net)
        self.upos_host_entry.pack(fill='x', pady=(5, 10))
        
        ttk.Label(left_net, text='BiliPlus Host:', style='Normal.TLabel').pack(anchor='w')
        self.host_entry = ttk.Entry(left_net)
        self.host_entry.pack(fill='x', pady=(5, 0))
        
        right_net = ttk.Frame(card, style='Card.TFrame')
        right_net.pack(side='right', fill='both', expand=True, padx=(20, 0))
        
        ttk.Label(right_net, text='BiliPlus EP Host:', style='Normal.TLabel').pack(anchor='w')
        self.ep_host_entry = ttk.Entry(right_net)
        self.ep_host_entry.pack(fill='x', pady=(5, 10))
        
        ttk.Label(right_net, text='区域 (hk/tw/th):', style='Normal.TLabel').pack(anchor='w')
        self.area_entry = ttk.Entry(right_net)
        self.area_entry.pack(fill='x', pady=(5, 0))
    
    def create_misc_advanced_card(self, parent):
        help_text = """🔧 其他高级选项帮助

【调试模式】
- 输出详细的调试信息
- 遇到问题时开启，方便排查

【强制替换Host】
- 强制替换下载服务器 Host（默认开启）
- 通常能提高下载成功率

【显示所有分P】
- 解析时显示所有分P的标题
- 方便查看分P列表

【隐藏音视频流】
- 不显示所有可用的音视频流信息
- 简化输出
"""
        card = self.create_card_frame(parent, '🔧 其他高级选项', help_text)
        
        delay_frame = ttk.Frame(card, style='Card.TFrame')
        delay_frame.pack(fill='x', pady=(10, 0))
        ttk.Label(delay_frame, text='分P下载间隔 (秒):', style='Normal.TLabel').pack(anchor='w')
        self.delay_entry = ttk.Entry(delay_frame, width=10)
        self.delay_entry.pack(anchor='w', pady=(5, 0))
        
        ua_frame = ttk.Frame(card, style='Card.TFrame')
        ua_frame.pack(fill='x', pady=(10, 0))
        ttk.Label(ua_frame, text='User-Agent:', style='Normal.TLabel').pack(anchor='w')
        self.ua_entry = ttk.Entry(ua_frame)
        self.ua_entry.pack(fill='x', pady=(5, 0))
        
        self.debug_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(card, text='调试模式', variable=self.debug_var).pack(anchor='w', pady=(10, 0))
        
        self.force_replace_host_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(card, text='强制替换Host', variable=self.force_replace_host_var).pack(anchor='w')
        
        self.show_all_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(card, text='显示所有分P', variable=self.show_all_var).pack(anchor='w')
        
        self.hide_streams_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(card, text='隐藏音视频流', variable=self.hide_streams_var).pack(anchor='w')
    
    def create_command_preview(self, parent):
        help_text = """📋 生成的命令帮助

- 这里显示根据您的设置生成的完整命令
- 您可以复制命令在终端中手动执行
- 点击"生成命令"按钮更新此区域
- 命令会自动处理路径中的空格等特殊字符
"""
        card = self.create_card_frame(parent, '📋 生成的命令', help_text)
        card.pack(fill='both', expand=True)
        
        self.command_text = scrolledtext.ScrolledText(card, height=4, font=('Consolas', 9), wrap=tk.WORD)
        self.command_text.pack(fill='both', expand=True)
    
    def create_action_buttons(self, parent):
        frame = ttk.Frame(parent, style='Main.TFrame')
        frame.pack(fill='x', pady=(10, 0))
        
        btn_frame = ttk.Frame(frame, style='Main.TFrame')
        btn_frame.pack(side='right')
        
        ttk.Button(btn_frame, text='重置', command=self.clear_all, style='TButton').pack(side='left', padx=(0, 5))
        ttk.Button(btn_frame, text='生成命令', command=self.generate_command, style='TButton').pack(side='left', padx=5)
        ttk.Button(btn_frame, text='复制命令', command=self.copy_command, style='TButton').pack(side='left', padx=5)
        ttk.Button(btn_frame, text='开始下载', command=self.start_download, style='Primary.TButton').pack(side='left', padx=5)
        ttk.Button(btn_frame, text='登录(WEB)', command=lambda: self.run_command('login'), style='TButton').pack(side='left', padx=5)
        ttk.Button(btn_frame, text='登录(TV)', command=lambda: self.run_command('logintv'), style='TButton').pack(side='left', padx=5)
        ttk.Button(btn_frame, text='服务器模式', command=lambda: self.run_command('serve'), style='TButton').pack(side='left', padx=(5, 0))
    
    def browse_work_dir(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.work_dir_entry.delete(0, tk.END)
            self.work_dir_entry.insert(0, dir_path)
    
    def browse_file(self, entry_widget):
        file_path = filedialog.askopenfilename(filetypes=[('可执行文件', '*.exe'), ('配置文件', '*.config'), ('所有文件', '*.*')])
        if file_path:
            entry_widget.delete(0, tk.END)
            entry_widget.insert(0, file_path)
    
    def generate_command(self):
        self.save_config()
        cmd = ['BBDown']
        
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning('警告', '请输入视频链接！')
            return None
        
        api_mode = self.api_mode.get()
        if api_mode == 'tv':
            cmd.append('-tv')
        elif api_mode == 'app':
            cmd.append('-app')
        elif api_mode == 'intl':
            cmd.append('-intl')
        
        if self.use_mp4box_var.get():
            cmd.append('--use-mp4box')
        
        encoding = self.encoding_entry.get().strip()
        if encoding:
            cmd.extend(['-e', encoding])
        
        dfn = self.dfn_entry.get().strip()
        if dfn:
            cmd.extend(['-q', dfn])
        
        if self.only_info_var.get():
            cmd.append('-info')
        
        if self.show_all_var.get():
            cmd.append('--show-all')
        
        if self.use_aria2_var.get():
            cmd.append('-aria2')
            aria2_args = []
            
            def clamp_value(value_str, min_val=1, max_val=16):
                """确保值在允许范围内"""
                try:
                    val = int(value_str)
                    val = max(min_val, min(val, max_val))
                    return str(val)
                except ValueError:
                    return str(min_val)
            
            x = clamp_value(self.aria2c_x.get())
            s = clamp_value(self.aria2c_s.get())
            j = clamp_value(self.aria2c_j.get())
            k = self.aria2c_k.get()
            custom_args = self.aria2c_args_entry.get().strip()
            aria2_args.extend(['-x', x, '-s', s, '-j', j, '-k', k])
            if custom_args:
                aria2_args.append(custom_args)
            cmd.extend(['--aria2c-args', ' '.join(aria2_args)])
        
        if self.interactive_var.get():
            cmd.append('-ia')
        
        if self.hide_streams_var.get():
            cmd.append('-hs')
        
        if self.mt_var.get():
            cmd.append('-mt')
        
        if self.video_only_var.get():
            cmd.append('--video-only')
        if self.audio_only_var.get():
            cmd.append('--audio-only')
        if self.danmaku_only_var.get():
            cmd.append('--danmaku-only')
        if self.sub_only_var.get():
            cmd.append('--sub-only')
        if self.cover_only_var.get():
            cmd.append('--cover-only')
        
        if self.debug_var.get():
            cmd.append('--debug')
        if self.skip_mux_var.get():
            cmd.append('--skip-mux')
        if self.skip_subtitle_var.get():
            cmd.append('--skip-subtitle')
        if self.skip_cover_var.get():
            cmd.append('--skip-cover')
        if self.force_http_var.get():
            cmd.append('--force-http')
        if self.download_danmaku_var.get():
            cmd.append('-dd')
        if self.skip_ai_var.get():
            cmd.append('--skip-ai')
        if self.video_ascending_var.get():
            cmd.append('--video-ascending')
        if self.audio_ascending_var.get():
            cmd.append('--audio-ascending')
        if self.allow_pcdn_var.get():
            cmd.append('--allow-pcdn')
        if self.force_replace_host_var.get():
            cmd.append('--force-replace-host')
        if self.save_archives_var.get():
            cmd.append('--save-archives-to-file')
        
        language = self.language_entry.get().strip()
        if language:
            cmd.extend(['--language', language])
        
        ua = self.ua_entry.get().strip()
        if ua:
            cmd.extend(['-ua', ua])
        
        config_file = self.config_file_entry.get().strip()
        if config_file:
            cmd.extend(['--config-file', config_file])
        
        file_pattern = self.file_pattern_entry.get().strip()
        if file_pattern and file_pattern != '<videoTitle>':
            cmd.extend(['-F', file_pattern])
        
        multi_pattern = self.multi_file_pattern_entry.get().strip()
        if multi_pattern and multi_pattern != '<videoTitle>/[P<pageNumberWithZero>]<pageTitle>':
            cmd.extend(['-M', multi_pattern])
        
        page = self.page_entry.get().strip()
        if page:
            cmd.extend(['-p', page])
        
        cookie = self.cookie_entry.get().strip()
        if cookie:
            cmd.extend(['-c', cookie])
        
        token = self.token_entry.get().strip()
        if token:
            cmd.extend(['-token', token])
        
        work_dir = self.work_dir_entry.get().strip()
        if work_dir:
            cmd.extend(['--work-dir', work_dir])
        
        ffmpeg_path = self.ffmpeg_path_entry.get().strip()
        if ffmpeg_path:
            cmd.extend(['--ffmpeg-path', ffmpeg_path])
        
        mp4box_path = self.mp4box_path_entry.get().strip()
        if mp4box_path:
            cmd.extend(['--mp4box-path', mp4box_path])
        
        aria2c_path = self.aria2c_path_entry.get().strip()
        if aria2c_path:
            cmd.extend(['--aria2c-path', aria2c_path])
        
        upos_host = self.upos_host_entry.get().strip()
        if upos_host:
            cmd.extend(['--upos-host', upos_host])
        
        host = self.host_entry.get().strip()
        if host:
            cmd.extend(['--host', host])
        
        ep_host = self.ep_host_entry.get().strip()
        if ep_host:
            cmd.extend(['--ep-host', ep_host])
        
        area = self.area_entry.get().strip()
        if area:
            cmd.extend(['--area', area])
        
        delay = self.delay_entry.get().strip()
        if delay:
            cmd.extend(['--delay-per-page', delay])
        
        cmd.append(url)
        
        command_str = ' '.join(f'"{x}"' if ' ' in x else x for x in cmd)
        self.command_text.delete(1.0, tk.END)
        self.command_text.insert(1.0, command_str)
        
        return cmd
    
    def copy_command(self):
        cmd = self.generate_command()
        if cmd:
            command_str = ' '.join(f'"{x}"' if ' ' in x else x for x in cmd)
            self.root.clipboard_clear()
            self.root.clipboard_append(command_str)
            messagebox.showinfo('成功', '命令已复制到剪贴板！')
    
    def start_download(self):
        cmd = self.generate_command()
        if cmd:
            self.execute_command(cmd, open_qrcode=False)
    
    def run_command(self, command):
        cmd = ['BBDown', command]
        is_login = command in ['login', 'logintv']
        self.execute_command(cmd, open_qrcode=is_login)
    
    def execute_command(self, cmd, open_qrcode=False):
        def run():
            try:
                if os.name == 'nt':
                    # Windows: 使用start命令打开新窗口
                    cmd_str = ' '.join(f'"{x}"' if ' ' in x else x for x in cmd)
                    os.system(f'start cmd /k "{cmd_str}"')
                    
                    # 如果是登录命令，打开qrcode.png
                    if open_qrcode:
                        qrcode_path = os.path.join(os.getcwd(), 'qrcode.png')
                        if os.path.exists(qrcode_path):
                            os.startfile(qrcode_path)
                        else:
                            # 等待1秒后再次尝试，因为qrcode.png可能需要一点时间生成
                            def check_and_open():
                                import time
                                time.sleep(2)
                                if os.path.exists(qrcode_path):
                                    os.startfile(qrcode_path)
                            threading.Thread(target=check_and_open, daemon=True).start()
                else:
                    # Linux/macOS: 使用xterm或终端
                    cmd_str = ' '.join(f'"{x}"' if ' ' in x else x for x in cmd)
                    try:
                        subprocess.Popen(['xterm', '-e', cmd_str])
                    except:
                        subprocess.Popen(cmd)
                
            except Exception as e:
                messagebox.showerror('错误', f'执行命令时出错: {str(e)}')
        
        threading.Thread(target=run, daemon=True).start()
    
    def load_config(self):
        """加载配置文件"""
        config = configparser.ConfigParser()
        
        if not os.path.exists(self.gui_config_file):
            self.save_config()
            return
        
        try:
            config.read(self.gui_config_file, encoding='utf-8')
            
            if 'Basic' in config:
                self.url_entry.delete(0, tk.END)
                self.url_entry.insert(0, config['Basic'].get('url', ''))
                self.page_entry.delete(0, tk.END)
                self.page_entry.insert(0, config['Basic'].get('page', ''))
                self.api_mode.set(config['Basic'].get('api_mode', 'web'))
                self.dfn_entry.delete(0, tk.END)
                self.dfn_entry.insert(0, config['Basic'].get('dfn', '8K 超高清,4K 超清,1080P 高码率,1080P 高清,720P 高清'))
                self.encoding_entry.delete(0, tk.END)
                self.encoding_entry.insert(0, config['Basic'].get('encoding', 'hevc,av1,avc'))
            
            if 'Download' in config:
                self.interactive_var.set(config['Download'].getboolean('interactive', False))
                self.only_info_var.set(config['Download'].getboolean('only_info', False))
                self.show_all_var.set(config['Download'].getboolean('show_all', False))
                self.hide_streams_var.set(config['Download'].getboolean('hide_streams', False))
                self.mt_var.set(config['Download'].getboolean('mt', True))
                self.use_aria2_var.set(config['Download'].getboolean('use_aria2', False))
                self.video_only_var.set(config['Download'].getboolean('video_only', False))
                self.audio_only_var.set(config['Download'].getboolean('audio_only', False))
                self.danmaku_only_var.set(config['Download'].getboolean('danmaku_only', False))
                self.sub_only_var.set(config['Download'].getboolean('sub_only', False))
                self.cover_only_var.set(config['Download'].getboolean('cover_only', False))
                self.download_danmaku_var.set(config['Download'].getboolean('download_danmaku', False))
                self.skip_subtitle_var.set(config['Download'].getboolean('skip_subtitle', False))
                self.skip_cover_var.set(config['Download'].getboolean('skip_cover', False))
                self.skip_mux_var.set(config['Download'].getboolean('skip_mux', False))
                self.skip_ai_var.set(config['Download'].getboolean('skip_ai', True))
                self.use_mp4box_var.set(config['Download'].getboolean('use_mp4box', False))
                self.video_ascending_var.set(config['Download'].getboolean('video_ascending', False))
                self.audio_ascending_var.set(config['Download'].getboolean('audio_ascending', False))
                self.allow_pcdn_var.set(config['Download'].getboolean('allow_pcdn', False))
                self.force_http_var.set(config['Download'].getboolean('force_http', True))
                self.save_archives_var.set(config['Download'].getboolean('save_archives', False))
                self.force_replace_host_var.set(config['Download'].getboolean('force_replace_host', True))
                self.debug_var.set(config['Download'].getboolean('debug', False))
            
            if 'File' in config:
                self.work_dir_entry.delete(0, tk.END)
                self.work_dir_entry.insert(0, config['File'].get('work_dir', ''))
                self.file_pattern_entry.delete(0, tk.END)
                self.file_pattern_entry.insert(0, config['File'].get('file_pattern', '<videoTitle>'))
                self.multi_file_pattern_entry.delete(0, tk.END)
                self.multi_file_pattern_entry.insert(0, config['File'].get('multi_file_pattern', '<videoTitle>/[P<pageNumberWithZero>]<pageTitle>'))
                self.language_entry.delete(0, tk.END)
                self.language_entry.insert(0, config['File'].get('language', ''))
            
            if 'Auth' in config:
                self.cookie_entry.delete(0, tk.END)
                self.cookie_entry.insert(0, config['Auth'].get('cookie', ''))
                self.token_entry.delete(0, tk.END)
                self.token_entry.insert(0, config['Auth'].get('token', ''))
            
            if 'Tool' in config:
                self.ffmpeg_path_entry.delete(0, tk.END)
                self.ffmpeg_path_entry.insert(0, config['Tool'].get('ffmpeg_path', ''))
                self.mp4box_path_entry.delete(0, tk.END)
                self.mp4box_path_entry.insert(0, config['Tool'].get('mp4box_path', ''))
                self.config_file_entry.delete(0, tk.END)
                self.config_file_entry.insert(0, config['Tool'].get('config_file', ''))
            
            if 'Aria2c' in config:
                self.aria2c_path_entry.delete(0, tk.END)
                self.aria2c_path_entry.insert(0, config['Aria2c'].get('aria2c_path', ''))
                self.aria2c_x.set(config['Aria2c'].get('x', '16'))
                self.aria2c_s.set(config['Aria2c'].get('s', '16'))
                self.aria2c_j.set(config['Aria2c'].get('j', '16'))
                self.aria2c_k.set(config['Aria2c'].get('k', '5M'))
                self.aria2c_args_entry.delete(0, tk.END)
                self.aria2c_args_entry.insert(0, config['Aria2c'].get('args', ''))
                if self.use_aria2_var.get():
                    self.aria2c_options_frame.pack(fill='x')
                    self.aria2c_advanced_frame.pack(fill='x', pady=(10, 0))
            
            if 'Network' in config:
                self.upos_host_entry.delete(0, tk.END)
                self.upos_host_entry.insert(0, config['Network'].get('upos_host', ''))
                self.host_entry.delete(0, tk.END)
                self.host_entry.insert(0, config['Network'].get('host', ''))
                self.ep_host_entry.delete(0, tk.END)
                self.ep_host_entry.insert(0, config['Network'].get('ep_host', ''))
                self.area_entry.delete(0, tk.END)
                self.area_entry.insert(0, config['Network'].get('area', ''))
                self.delay_entry.delete(0, tk.END)
                self.delay_entry.insert(0, config['Network'].get('delay', ''))
                self.ua_entry.delete(0, tk.END)
                self.ua_entry.insert(0, config['Network'].get('ua', ''))
        
        except Exception as e:
            print(f'加载配置文件时出错: {str(e)}')
            self.save_config()
    
    def save_config(self):
        """保存配置文件"""
        config = configparser.ConfigParser()
        
        config['Basic'] = {
            'url': self.url_entry.get(),
            'page': self.page_entry.get(),
            'api_mode': self.api_mode.get(),
            'dfn': self.dfn_entry.get(),
            'encoding': self.encoding_entry.get()
        }
        
        config['Download'] = {
            'interactive': str(self.interactive_var.get()),
            'only_info': str(self.only_info_var.get()),
            'show_all': str(self.show_all_var.get()),
            'hide_streams': str(self.hide_streams_var.get()),
            'mt': str(self.mt_var.get()),
            'use_aria2': str(self.use_aria2_var.get()),
            'video_only': str(self.video_only_var.get()),
            'audio_only': str(self.audio_only_var.get()),
            'danmaku_only': str(self.danmaku_only_var.get()),
            'sub_only': str(self.sub_only_var.get()),
            'cover_only': str(self.cover_only_var.get()),
            'download_danmaku': str(self.download_danmaku_var.get()),
            'skip_subtitle': str(self.skip_subtitle_var.get()),
            'skip_cover': str(self.skip_cover_var.get()),
            'skip_mux': str(self.skip_mux_var.get()),
            'skip_ai': str(self.skip_ai_var.get()),
            'use_mp4box': str(self.use_mp4box_var.get()),
            'video_ascending': str(self.video_ascending_var.get()),
            'audio_ascending': str(self.audio_ascending_var.get()),
            'allow_pcdn': str(self.allow_pcdn_var.get()),
            'force_http': str(self.force_http_var.get()),
            'save_archives': str(self.save_archives_var.get()),
            'force_replace_host': str(self.force_replace_host_var.get()),
            'debug': str(self.debug_var.get())
        }
        
        config['File'] = {
            'work_dir': self.work_dir_entry.get(),
            'file_pattern': self.file_pattern_entry.get(),
            'multi_file_pattern': self.multi_file_pattern_entry.get(),
            'language': self.language_entry.get()
        }
        
        config['Auth'] = {
            'cookie': self.cookie_entry.get(),
            'token': self.token_entry.get()
        }
        
        config['Tool'] = {
            'ffmpeg_path': self.ffmpeg_path_entry.get(),
            'mp4box_path': self.mp4box_path_entry.get(),
            'config_file': self.config_file_entry.get()
        }
        
        config['Aria2c'] = {
            'aria2c_path': self.aria2c_path_entry.get(),
            'x': self.aria2c_x.get(),
            's': self.aria2c_s.get(),
            'j': self.aria2c_j.get(),
            'k': self.aria2c_k.get(),
            'args': self.aria2c_args_entry.get()
        }
        
        config['Network'] = {
            'upos_host': self.upos_host_entry.get(),
            'host': self.host_entry.get(),
            'ep_host': self.ep_host_entry.get(),
            'area': self.area_entry.get(),
            'delay': self.delay_entry.get(),
            'ua': self.ua_entry.get()
        }
        
        try:
            with open(self.gui_config_file, 'w', encoding='utf-8') as f:
                config.write(f)
        except Exception as e:
            print(f'保存配置文件时出错: {str(e)}')
    
    def clear_all(self):
        self.url_entry.delete(0, tk.END)
        self.page_entry.delete(0, tk.END)
        self.api_mode.set('web')
        self.dfn_entry.delete(0, tk.END)
        self.dfn_entry.insert(0, '8K 超高清,4K 超清,1080P 高码率,1080P 高清,720P 高清')
        self.encoding_entry.delete(0, tk.END)
        self.encoding_entry.insert(0, 'hevc,av1,avc')
        self.interactive_var.set(False)
        self.only_info_var.set(False)
        self.show_all_var.set(False)
        self.hide_streams_var.set(False)
        self.mt_var.set(True)
        self.use_aria2_var.set(False)
        self.aria2c_options_frame.pack_forget()
        self.aria2c_advanced_frame.pack_forget()
        self.video_only_var.set(False)
        self.audio_only_var.set(False)
        self.danmaku_only_var.set(False)
        self.sub_only_var.set(False)
        self.cover_only_var.set(False)
        self.download_danmaku_var.set(False)
        self.skip_subtitle_var.set(False)
        self.skip_cover_var.set(False)
        self.skip_mux_var.set(False)
        self.skip_ai_var.set(True)
        self.use_mp4box_var.set(False)
        self.video_ascending_var.set(False)
        self.audio_ascending_var.set(False)
        self.allow_pcdn_var.set(False)
        self.force_http_var.set(True)
        self.save_archives_var.set(False)
        self.force_replace_host_var.set(True)
        self.debug_var.set(False)
        self.work_dir_entry.delete(0, tk.END)
        self.file_pattern_entry.delete(0, tk.END)
        self.file_pattern_entry.insert(0, '<videoTitle>')
        self.multi_file_pattern_entry.delete(0, tk.END)
        self.multi_file_pattern_entry.insert(0, '<videoTitle>/[P<pageNumberWithZero>]<pageTitle>')
        self.language_entry.delete(0, tk.END)
        self.cookie_entry.delete(0, tk.END)
        self.token_entry.delete(0, tk.END)
        self.ffmpeg_path_entry.delete(0, tk.END)
        self.mp4box_path_entry.delete(0, tk.END)
        self.config_file_entry.delete(0, tk.END)
        self.aria2c_path_entry.delete(0, tk.END)
        self.aria2c_x.set('16')
        self.aria2c_s.set('16')
        self.aria2c_j.set('16')
        self.aria2c_k.set('5M')
        self.aria2c_args_entry.delete(0, tk.END)
        self.upos_host_entry.delete(0, tk.END)
        self.host_entry.delete(0, tk.END)
        self.ep_host_entry.delete(0, tk.END)
        self.area_entry.delete(0, tk.END)
        self.delay_entry.delete(0, tk.END)
        self.ua_entry.delete(0, tk.END)
        self.command_text.delete(1.0, tk.END)
        self.save_config()
    
    def create_about_tab(self, parent):
        tab = ttk.Frame(parent, style='Main.TFrame')
        parent.add(tab, text='  关于  ', padding=15)
        
        # 项目标题
        title_frame = ttk.Frame(tab, style='Main.TFrame')
        title_frame.pack(fill='x', pady=(0, 20))
        
        ttk.Label(title_frame, text='🎬 BBDown GUI', font=("Microsoft YaHei UI", 20, "bold")).pack()
        ttk.Label(title_frame, text='v1.0.0 - 哔哩哔哩下载器', font=("Microsoft YaHei UI", 10)).pack(pady=(5, 0))
        
        # 项目地址
        project_frame = ttk.LabelFrame(tab, text='项目地址', style='Card.TLabelframe', padding=15)
        project_frame.pack(fill='x', pady=(0, 15))
        
        project_link = ttk.Label(project_frame, text='https://github.com/WWSTA/BBDown-GUI', 
                              font=("Microsoft YaHei UI", 10, "underline"), foreground="#0066cc", cursor="hand2")
        project_link.pack()
        project_link.bind('<Button-1>', lambda e: self._open_link('https://github.com/WWSTA/BBDown-GUI'))
        
        # 感谢原作者
        thanks_frame = ttk.LabelFrame(tab, text='感谢原作者', style='Card.TLabelframe', padding=15)
        thanks_frame.pack(fill='x', pady=(0, 15))
        
        bbdown_link = ttk.Label(thanks_frame, text='BBDown - https://github.com/nilaoda/BBDown', 
                              font=("Microsoft YaHei UI", 10, "underline"), foreground="#0066cc", cursor="hand2")
        bbdown_link.pack(anchor='w')
        bbdown_link.bind('<Button-1>', lambda e: self._open_link('https://github.com/nilaoda/BBDown'))
        
        ttk.Label(thanks_frame, text='\n感谢 BBDown 原作者 nilaoda 提供的优秀下载工具！', 
                 font=("Microsoft YaHei UI", 10)).pack(anchor='w', pady=(10, 0))
        
        # 感谢其他项目
        credits_frame = ttk.LabelFrame(tab, text='感谢其他项目', style='Card.TLabelframe', padding=15)
        credits_frame.pack(fill='both', expand=True, pady=(0, 15))
        
        credits_list = [
            ('FFmpeg - https://github.com/FFmpeg/FFmpeg', 'https://github.com/FFmpeg/FFmpeg'),
            ('gpac (MP4Box) - https://github.com/gpac/gpac', 'https://github.com/gpac/gpac'),
            ('aria2 - https://github.com/aria2/aria2', 'https://github.com/aria2/aria2'),
            ('QRCoder - https://github.com/codebude/QRCoder', 'https://github.com/codebude/QRCoder'),
            ('SharpZipLib - https://github.com/icsharpcode/SharpZipLib', 'https://github.com/icsharpcode/SharpZipLib'),
            ('protobuf - https://github.com/protocolbuffers/protobuf', 'https://github.com/protocolbuffers/protobuf'),
            ('grpc - https://github.com/grpc/grpc', 'https://github.com/grpc/grpc'),
            ('command-line-api - https://github.com/dotnet/command-line-api', 'https://github.com/dotnet/command-line-api'),
            ('bilibili-API-collect - https://github.com/SocialSisterYi/bilibili-API-collect', 'https://github.com/SocialSisterYi/bilibili-API-collect'),
            ('bilibili-grpc-api - https://github.com/SeeFlowerX/bilibili-grpc-api', 'https://github.com/SeeFlowerX/bilibili-grpc-api')
        ]
        
        for text, link in credits_list:
            link_label = ttk.Label(credits_frame, text=text, 
                                font=("Microsoft YaHei UI", 9, "underline"), foreground="#0066cc", cursor="hand2")
            link_label.pack(anchor='w', pady=2)
            link_label.bind('<Button-1>', lambda e, url=link: self._open_link(url))
        
        # 版权信息
        copyright_frame = ttk.Frame(tab, style='Main.TFrame')
        copyright_frame.pack(fill='x', pady=(10, 0))
        ttk.Label(copyright_frame, text='© 2026 BBDown GUI. All rights reserved.', 
                 font=("Microsoft YaHei UI", 9), foreground="#666666").pack()
    
    def _open_link(self, url):
        """打开网页链接"""
        import webbrowser
        try:
            webbrowser.open_new(url)
        except Exception as e:
            print(f"打开链接失败: {e}")
            messagebox.showwarning('提示', f'无法打开链接，请手动访问：\n{url}')


def main():
    root = tk.Tk()
    app = ModernBBDownGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
