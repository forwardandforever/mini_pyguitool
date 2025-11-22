# -*- coding: utf-8 -*-
"""
文件名：main.py
日期：[2025/10/13 18:39]
描述：一个简单的python工具集
"""
import os
import re
import unicodedata
import traceback
import subprocess
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import urllib.parse
import random
import json
import base64

do_one_js_code_lock = threading.Lock()


def do_one_cmd(one_cmd):
    result = subprocess.run(one_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    return {'returncode': result.returncode, 'stdout': result.stdout.strip() if result.stdout else result.stdout, 'stderr': result.stderr}


def do_one_js_code(js_code_n):
    def get_randomstr() -> str:
        new_list = []
        for i in range(10):
            new_list.append(str(random.randint(0, 9)))
        return ''.join(new_list)

    def do():
        now_dir = os.path.dirname(os.path.realpath(__file__))
        js_path = os.path.join(now_dir, 'src', f'{get_randomstr()}.js')
        with open(js_path, 'w', encoding='utf-8') as js_file:
            js_file.write(js_code_n)
        result = do_one_cmd(f'node {js_path}')
        os.remove(js_path)
        return result

    with do_one_js_code_lock:
        return do()


class PyToolFn:
    def __init__(self):
        self.none = None
        self.curl_jscode = "import * as curl from 'curlconverter';function curl_converter(curl_cmd, type_n) {const fn = eval('curl.to' + type_n);console.log(fn(curl_cmd));}"

    def curl_converter(self, curl_cmd: str, out_type: str) -> str:
        curl_jscode_n = self.curl_jscode + f"curl_converter({str({curl_cmd})[1:-1]},'{out_type}')"
        result = do_one_js_code(curl_jscode_n)
        if result['returncode'] == 0:
            return result['stdout']
        else:
            return result['stderr']

    def copy_from_text_area(self, text_area):
        self.none = None
        text_area.clipboard_clear()
        text = text_area.get('1.0', tk.END)[:-1]
        text_area.clipboard_append(text)

    def get_text_from_text_area(self, text_area):
        self.none = None
        text = text_area.get('1.0', tk.END)[:-1]
        return text

    def delete_insert_text_to_text_area(self, text_area, text):
        self.none = None
        state = text_area['state']
        text_area.configure(state='normal')
        text_area.delete(1.0, tk.END)
        text_area.insert(1.0, text)
        text_area.configure(state=state)

    def insert_text_to_text_area(self, text_area, text):
        self.none = None
        state = text_area['state']
        text_area.configure(state='normal')
        text_area.insert(tk.END, text)
        text_area.configure(state=state)

    def delete_text_from_text_area(self, text_area_list: list):
        self.none = None
        for text_area in text_area_list:
            state = text_area['state']
            text_area.configure(state='normal')
            text_area.delete(1.0, tk.END)
            text_area.configure(state=state)

    def split_one_line(self, one_line, length_) -> list:
        new_list = []
        for idx in range(0, len(one_line), length_):
            try:
                new_list.append(one_line[idx:idx + length_])
            except IndexError as e:
                self.none = e
                new_list.append(one_line[idx:])
        return new_list

    def get_one_chr_info(self, ord_int: int = None, chr_str: str = None) -> dict:
        self.none = None
        if ord_int:
            or_str = chr(ord_int)
            h10 = ord_int
            h16 = hex(ord_int)
            result_dict = {'result': or_str, 'h16': h16}
        else:
            or_str = chr_str
            h10 = ord(chr_str)
            h16 = hex(h10)
            result_dict = {'h10': h10, 'h16': h16}
        if h10 < 128:
            unicode_str = f'\\u{h16[2:]:0>4}'
        else:
            unicode_str = json.dumps(or_str)[1:-1]
        char_name = unicodedata.name(or_str, "Unknown").lower()
        result_dict.update({'unicode_str': unicode_str, 'char_name': char_name})
        return result_dict


class Config:
    FONT_TITLE = ('宋体', 20, 'bold')
    FONT_NORMAL = ('宋体', 12)
    FONT_SMALL = ('宋体', 10)


class PyToolApp:
    def __init__(self, master):
        self.none = None
        self.master = master
        self.windows = {}
        self.master.title('PyTool')
        self.master.geometry('460x300+50+50')
        self.master.resizable(False, False)
        self.fn = PyToolFn()
        self.pages_fn = {
            'curlconverter': self.__curlct__,
            'b64_edc': self.__b64edc__,
            'urledc': self.__urledc___,
            'htmledc': self.__htmledc__,
            'treplace': self.__treplace__,
            'tsts': self.__tsts__,
            'tsplit': self.__tsplit__,
            'tss': self.__tss__,
            'tjoin': self.__tjoin__,
            'treverse': self.__treverse__,
            'tlsl': self.__tlsl__,
            'unicodetool': self.__unicodetool__,
        }

        self.main_notebook = ttk.Notebook(self.master)
        self.main_notebook.grid(row=0, column=0, sticky='nwse')

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        self.creat_text_deal_page()
        self.creat_en_decoding_page()
        self.curl_deal_page()

    def creat_text_deal_page(self):
        text_deal_page = tk.Frame(self.main_notebook)
        text_replace_button = tk.Button(text_deal_page, width=15, text='文本替换', command=lambda: self.creat_or_focus_window('treplace', '文本替换'))
        statistics_button = tk.Button(text_deal_page, width=15, text='文本统计', command=lambda: self.creat_or_focus_window('tsts', '文本统计'))
        text_split_button = tk.Button(text_deal_page, width=15, text='文本分割', command=lambda: self.creat_or_focus_window('tsplit', '文本分割'))
        text_ss_button = tk.Button(text_deal_page, width=15, text='多行文本去重/排序', command=lambda: self.creat_or_focus_window('tss', '多行文本去重/排序'))
        text_join_button = tk.Button(text_deal_page, width=15, text='文本合并', command=lambda: self.creat_or_focus_window('tjoin', '文本合并'))
        text_reverse_button = tk.Button(text_deal_page, width=15, text='文本逆序', command=lambda: self.creat_or_focus_window('treverse', '文本逆序'))
        text_lsl_button = tk.Button(text_deal_page, width=15, text='文本行定长', command=lambda: self.creat_or_focus_window('tlsl', '文本行定长'))
        unicode_tool_button = tk.Button(text_deal_page, width=15, text='Unicode工具', command=lambda: self.creat_or_focus_window('unicodetool', 'Unicode工具'))

        # text_deal_page.grid(row=0, column=0, sticky='nwse')
        text_replace_button.grid(row=0, column=0, sticky='')
        statistics_button.grid(row=0, column=1, sticky='')
        text_split_button.grid(row=0, column=2, sticky='')
        text_ss_button.grid(row=0, column=3, sticky='')
        text_join_button.grid(row=1, column=0, sticky='')
        text_reverse_button.grid(row=1, column=1, sticky='')
        text_lsl_button.grid(row=1, column=2, sticky='')
        unicode_tool_button.grid(row=1, column=3, sticky='')

        self.main_notebook.add(text_deal_page, text='文本处理')
        # self.main_notebook.rowconfigure(0, weight=1)
        # self.main_notebook.columnconfigure(0, weight=1)
        for col_t in range(4):
            text_deal_page.columnconfigure(col_t, weight=1)

    def creat_en_decoding_page(self):
        en_de_frame = tk.Frame(self.main_notebook)

        b64_edc_button = tk.Button(en_de_frame, width=15, text='base64', command=lambda: self.creat_or_focus_window('b64_edc', 'base64编码/解码'))
        url_edc_button = tk.Button(en_de_frame, width=15, text='URL编码/解码', command=lambda: self.creat_or_focus_window('urledc', 'URL编码/解码'))
        html_edc_button = tk.Button(en_de_frame, text='HTML编码/解码', width=15, command=lambda: self.creat_or_focus_window('htmledc', 'HTML编码/解码'))

        # en_de_frame.grid(row=0, column=0, sticky='')
        b64_edc_button.grid(row=0, column=0, sticky='nw')
        url_edc_button.grid(row=0, column=1, sticky='wn')
        html_edc_button.grid(row=0, column=2, sticky='nw')

        self.main_notebook.add(en_de_frame, text='编码/解码')

        for row in range(1):
            en_de_frame.rowconfigure(row, weight=1)

        # self.main_notebook.rowconfigure(0, weight=1)
        # self.main_notebook.columnconfigure(0, weight=1)

    def curl_deal_page(self):
        text_deal_page = tk.Frame(self.main_notebook)

        curlct_button = tk.Button(text_deal_page, width=15, text='CurlConverter', command=lambda: self.creat_or_focus_window('curlconverter', 'CurlConverter'))

        # text_deal_page.grid(row=0, column=0, sticky='')
        curlct_button.grid(row=0, column=0, sticky='nw')

        self.main_notebook.add(text_deal_page, text='CurlConverter')

        # self.main_notebook.rowconfigure(0, weight=1)
        # self.main_notebook.columnconfigure(0, weight=1)

        text_deal_page.columnconfigure(0, weight=1)
        text_deal_page.columnconfigure(0, weight=1)

    def __curlct__(self):
        def convert_fn():
            text = input_text_area.get(1.0, tk.END).strip()
            if text:
                type_n = options_widget.get()
                result = self.fn.curl_converter(text, type_n)
                self.fn.delete_insert_text_to_text_area(output_text_area, result)

        options = ['Ansible', 'C', 'CFML', 'CSharp', 'Clojure', 'Dart', 'Elixir', 'Go', 'HTTP', 'HarString', 'Httpie', 'Java', 'JavaHttpUrlConnection', 'JavaJsoup', 'JavaOkHttp', 'JavaScript', 'JavaScriptJquery', 'JavaScriptXHR', 'JsonObject', 'Julia', 'Kotlin', 'Lua', 'MATLAB', 'Node', 'NodeAxios', 'NodeGot', 'NodeHttp', 'NodeKy', 'NodeRequest', 'NodeSuperAgent', 'OCaml', 'ObjectiveC', 'Perl', 'Php', 'PhpGuzzle', 'PhpRequests', 'PowershellRestMethod', 'PowershellWebRequest', 'Python', 'PythonHttp', 'R', 'RHttr2', 'Ruby', 'RubyHttparty', 'Rust', 'Swift', 'Wget']
        n_window = self.windows['curlconverter']

        title_label = tk.Label(n_window, text='Convert curl commands to Python, JavaScript and more', font=('Arial', 20, 'bold'))
        hint_label = tk.Label(n_window, text='curl command', font=('Arial', 15, 'bold'))
        input_text_area = scrolledtext.ScrolledText(n_window)
        to_label = tk.Label(n_window, text='To', font=('Arial', 15))
        options_widget = ttk.Combobox(n_window, values=options, state="readonly")
        output_text_area = scrolledtext.ScrolledText(n_window, state='disabled')
        button_frame = tk.Frame(n_window)
        conversion_button = tk.Button(button_frame, width=10, text='Convert', font=('Arial', 12), command=convert_fn)
        copy_button = tk.Button(button_frame, width=10, text='Copy', font=('Arial', 12), command=lambda: self.fn.copy_from_text_area(output_text_area))
        clear_button = tk.Button(button_frame, text='Clear', font=('Arial', 12), command=lambda: self.fn.delete_text_from_text_area([input_text_area, output_text_area]))
        info_label = tk.Label(n_window, text='注：本页面来自(curlconverter) curlconverter.com', font=Config.FONT_SMALL)

        title_label.grid(row=0, columnspan=2, sticky='')
        hint_label.grid(row=1, columnspan=2, sticky='w', padx=5)
        input_text_area.grid(row=2, columnspan=2, sticky='we', padx=5, pady=5)
        to_label.grid(row=3, column=0, sticky='e')
        options_widget.grid(row=3, column=1, sticky='w')
        output_text_area.grid(row=4, columnspan=2, sticky='we', padx=5, pady=5)
        button_frame.grid(row=5, columnspan=2, sticky='nswe', padx=5)
        conversion_button.grid(row=0, column=0, sticky='we')
        copy_button.grid(row=0, column=1, sticky='we')
        clear_button.grid(row=1, column=0, columnspan=2, sticky='we')
        info_label.grid(row=6, columnspan=2, sticky='')

        options_widget.set('Python')
        output_text_area.configure(state='disabled')

        for row in [2, 4]:
            n_window.rowconfigure(row, weight=1, minsize=30)
        for col in range(2):
            n_window.columnconfigure(col, weight=1, minsize=30)
        for col_b in range(2):
            button_frame.columnconfigure(col_b, weight=1, minsize=30)

    def __b64edc__(self):
        def op_set():
            fn_options_widget.set('Base64')
            code_options_widget.set('utf-8')
            did_var.set('encode')

        def en_decode():
            de_var = did_var.get()
            fn_var = fn_options_widget.get()
            code_var = code_options_widget.get()
            text = self.fn.get_text_from_text_area(input_area)
            if text:
                if de_var == 'encode':
                    en_fn = eval(f'base64.{fn_options_h[fn_options_q.index(fn_var)]}encode')
                    try:
                        result = en_fn(text.encode(code_var)).decode('ascii')
                    except BaseException as e:
                        result = e
                    self.fn.delete_insert_text_to_text_area(output_area, result)
                else:
                    de_fn = eval(f'base64.{fn_options_h[fn_options_q.index(fn_var)]}decode')
                    try:
                        result = de_fn(text.encode('ascii')).decode(code_var)
                    except BaseException as e:
                        result = e
                    self.fn.delete_insert_text_to_text_area(output_area, result)

        code_options = [
            'ascii', 'big5', 'big5hkscs', 'cp037', 'cp273', 'cp424', 'cp437', 'cp500', 'cp720', 'cp737', 'cp775', 'cp850', 'cp852', 'cp855', 'cp856', 'cp857', 'cp858', 'cp860', 'cp861', 'cp862', 'cp863', 'cp864', 'cp865', 'cp866', 'cp869', 'cp874', 'cp875', 'cp932', 'cp949', 'cp950', 'cp1006', 'cp1026', 'cp1125', 'cp1140', 'cp1250', 'cp1251', 'cp1252', 'cp1253', 'cp1254', 'cp1255', 'cp1256', 'cp1257', 'cp1258', 'euc-jp', 'euc-jis-2004', 'euc-jisx0213', 'euc-kr', 'gb2312', 'gbk', 'gb18030', 'hz', 'iso2022-jp', 'iso2022-jp-1', 'iso2022-jp-2', 'iso2022-jp-2004', 'iso2022-jp-3', 'iso2022-jp-ext', 'iso2022-kr', 'latin-1', 'iso8859-2', 'iso8859-3', 'iso8859-4', 'iso8859-5', 'iso8859-6', 'iso8859-7', 'iso8859-8', 'iso8859-9', 'iso8859-10', 'iso8859-11', 'iso8859-13', 'iso8859-14', 'iso8859-15', 'iso8859-16', 'johab', 'koi8-r', 'koi8-t', 'koi8-u', 'kz1048', 'mac-cyrillic', 'mac-greek', 'mac-iceland', 'mac-latin2', 'mac-roman', 'mac-turkish', 'ptcp154', 'shift-jis', 'shift-jis-2004',
            'shift-jisx0213', 'utf-32', 'utf-32-be', 'utf-32-le', 'utf-16', 'utf-16-be', 'utf-16-le', 'utf-7', 'utf-8', 'utf-8-sig'
        ]
        fn_options_h = ['a85', 'b16', 'b32', 'b32hex', 'b64', 'b85', 'urlsafe_b64', 'z85']
        fn_options_q = ['Ascii85', 'Base16', 'Base32', 'Base32hex', 'Base64', 'Base85', 'UrlSafe_Base64', 'ZeroMQ-Base85']
        n_window = self.windows['b64_edc']
        did_var = tk.StringVar()

        title_label = tk.Label(n_window, text='base64编码/解码', font=Config.FONT_TITLE, anchor='center')
        input_area = scrolledtext.ScrolledText(n_window)
        fn_label = tk.Label(n_window, text='编码/解码方式: ', anchor='e', font=Config.FONT_NORMAL)
        fn_options_widget = ttk.Combobox(n_window, values=fn_options_q, state="readonly")
        enc_rbutton = tk.Radiobutton(n_window, value='encode', text='编码', font=Config.FONT_NORMAL, variable=did_var)
        dec_rburron = tk.Radiobutton(n_window, value='decode', text='解码', font=Config.FONT_NORMAL, variable=did_var)
        text_code_label = tk.Label(n_window, text='明文编码: ', font=Config.FONT_NORMAL, anchor='e')
        code_options_widget = ttk.Combobox(n_window, values=code_options, state="readonly")
        output_area = scrolledtext.ScrolledText(n_window)
        button_frame = tk.Frame(n_window)
        out_button = tk.Button(button_frame, text='输出', font=Config.FONT_NORMAL, command=en_decode)
        copy_button = tk.Button(button_frame, text='复制', font=Config.FONT_NORMAL, command=lambda: self.fn.copy_from_text_area(output_area))
        clear_button = tk.Button(button_frame, text='清空', font=Config.FONT_NORMAL, command=lambda: self.fn.delete_text_from_text_area([input_area, output_area]))
        info_label = tk.Label(n_window, font=Config.FONT_SMALL, anchor='center', text='本页方法均为python-base64库\t明文编码即base64.b64encode(str.encode(code))中的code，base解码时会用到')

        title_label.grid(row=0, columnspan=6, sticky='')
        input_area.grid(row=1, columnspan=6, sticky='nsew', padx=5, pady=5)
        fn_label.grid(row=2, column=0, sticky='e')
        fn_options_widget.grid(row=2, column=1, sticky='w')
        enc_rbutton.grid(row=2, column=2, sticky='')
        dec_rburron.grid(row=2, column=3, sticky='')
        text_code_label.grid(row=2, column=4, sticky='e')
        code_options_widget.grid(row=2, column=5, sticky='w')
        output_area.grid(row=3, columnspan=6, sticky='nsew', padx=5, pady=5)
        button_frame.grid(row=4, columnspan=6, sticky='nsew', padx=5)
        out_button.grid(row=0, column=0, sticky='we')
        copy_button.grid(row=0, column=1, sticky='we')
        clear_button.grid(row=1, columnspan=2, column=0, sticky='we')
        info_label.grid(row=6, columnspan=6, sticky='nsew')

        op_set()
        output_area.config(state='disabled')

        for row in [1, 3]:
            n_window.rowconfigure(row, weight=1, minsize=30)
        for col in range(6):
            n_window.columnconfigure(col, weight=1, minsize=30)
        for col_b in range(2):
            button_frame.columnconfigure(col_b, weight=1, minsize=30)

    def __urledc___(self):
        def url_ed():
            do_var = ed_var.get()
            text = self.fn.get_text_from_text_area(input_area)
            if text:
                if do_var == 'quote':
                    try:
                        result = urllib.parse.quote(text, safe='').lower()
                    except Exception as e:
                        result = e
                    self.fn.delete_insert_text_to_text_area(output_area, result)
                else:
                    try:
                        result = urllib.parse.unquote(text)
                    except Exception as e:
                        result = e
                    self.fn.delete_insert_text_to_text_area(output_area, result)

        n_window = self.windows['urledc']
        ed_var = tk.StringVar()

        title_label = tk.Label(n_window, text='URL编码/解码', font=Config.FONT_TITLE, anchor='center')
        input_area = scrolledtext.ScrolledText(n_window)
        e_rbutton = tk.Radiobutton(n_window, text='编码', value='quote', variable=ed_var, font=Config.FONT_NORMAL)
        d_rbutton = tk.Radiobutton(n_window, text='解码', value='unquote', variable=ed_var, font=Config.FONT_NORMAL)
        output_area = scrolledtext.ScrolledText(n_window)
        do_button = tk.Button(n_window, text='输出', font=Config.FONT_NORMAL, command=url_ed)
        copy_button = tk.Button(n_window, text='复制', font=Config.FONT_NORMAL, command=lambda: self.fn.copy_from_text_area(output_area))
        clear_button = tk.Button(n_window, text='清空', font=Config.FONT_NORMAL, command=lambda: self.fn.delete_text_from_text_area([input_area, output_area]))

        title_label.grid(row=0, columnspan=2, sticky='')
        input_area.grid(row=1, columnspan=2, sticky='nsew', padx=5, pady=5)
        e_rbutton.grid(row=2, column=0, sticky='e')
        d_rbutton.grid(row=2, column=1, sticky='w')
        output_area.grid(row=3, columnspan=2, sticky='nsew', padx=5, pady=5)
        do_button.grid(row=4, column=0, sticky='we', padx=(5, 0))
        copy_button.grid(row=4, column=1, sticky='we', padx=(0, 5))
        clear_button.grid(row=5, columnspan=2, sticky='we', padx=5, pady=(0, 5))

        ed_var.set('quote')
        output_area.config(state='disabled')

        for row in [1, 3]:
            n_window.rowconfigure(row, weight=1, minsize=30)
        for col in range(2):
            n_window.columnconfigure(col, weight=1, minsize=30)

    def __htmledc__(self):
        def html_ed():
            do_var = ed_var.get()
            fn = eval(f'html.{do_var}')
            text = self.fn.get_text_from_text_area(input_area)
            if text:
                result = fn(text)
                self.fn.delete_insert_text_to_text_area(output_area, result)

        n_window = self.windows['htmledc']
        ed_var = tk.StringVar()

        title_label = tk.Label(n_window, text='HTML编码/解码', font=Config.FONT_TITLE, anchor='center')
        input_area = scrolledtext.ScrolledText(n_window)
        e_rbutton = tk.Radiobutton(n_window, text='编码', value='escape', variable=ed_var, font=Config.FONT_NORMAL)
        d_rbutton = tk.Radiobutton(n_window, text='解码', value='unescape', variable=ed_var, font=Config.FONT_NORMAL)
        output_area = scrolledtext.ScrolledText(n_window)
        do_button = tk.Button(n_window, text='输出', font=Config.FONT_NORMAL, command=html_ed)
        copy_button = tk.Button(n_window, text='复制', font=Config.FONT_NORMAL, command=lambda: self.fn.copy_from_text_area(output_area))
        clear_button = tk.Button(n_window, text='清空', font=Config.FONT_NORMAL, command=lambda: self.fn.delete_text_from_text_area([input_area, output_area]))

        title_label.grid(row=0, columnspan=2, sticky='')
        input_area.grid(row=1, columnspan=2, sticky='nsew', padx=5, pady=5)
        e_rbutton.grid(row=2, column=0, sticky='e')
        d_rbutton.grid(row=2, column=1, sticky='w')
        output_area.grid(row=3, columnspan=2, sticky='nsew', padx=5, pady=5)
        do_button.grid(row=4, column=0, sticky='we', padx=(5, 0))
        copy_button.grid(row=4, column=1, sticky='we', padx=(0, 5))
        clear_button.grid(row=5, columnspan=2, sticky='we', padx=5, pady=(0, 5))

        ed_var.set('escape')
        output_area.config(state='disabled')

        for row in [1, 3]:
            n_window.rowconfigure(row, weight=1, minsize=30)
        for col in range(2):
            n_window.columnconfigure(col, weight=1, minsize=30)

    def __treplace__(self):
        def replace_n():
            text = self.fn.get_text_from_text_area(input_area)
            from_text = self.fn.get_text_from_text_area(from_entry)
            to_text = self.fn.get_text_from_text_area(to_entry)
            if text:
                result = text.replace(from_text, to_text)
                self.fn.delete_insert_text_to_text_area(output_area, result)

        n_window = self.windows['treplace']

        title_label = tk.Label(n_window, text='文本替换', font=Config.FONT_TITLE, anchor='center')
        input_area = scrolledtext.ScrolledText(n_window)
        function_frame = tk.Frame(n_window)
        from_label = tk.Label(function_frame, text='将', font=Config.FONT_NORMAL)
        from_entry = scrolledtext.ScrolledText(function_frame, width=30, height=1)
        to_label = tk.Label(function_frame, text='替换为', font=Config.FONT_NORMAL)
        to_entry = scrolledtext.ScrolledText(function_frame, width=30, height=1)
        output_area = scrolledtext.ScrolledText(n_window)
        button_frame = tk.Frame(n_window)
        replace_button = tk.Button(button_frame, text='替换', font=Config.FONT_NORMAL, command=replace_n)
        copy_button = tk.Button(button_frame, text='复制', font=Config.FONT_NORMAL, command=lambda: self.fn.copy_from_text_area(output_area))
        clear_button = tk.Button(button_frame, text='清空', font=Config.FONT_NORMAL, command=lambda: self.fn.delete_text_from_text_area([input_area, output_area, from_entry, to_entry]))
        info_label = tk.Label(n_window, text='可将其他字符替换为换行符，也可将换行符替换为其他字符', anchor='center')

        title_label.grid(row=0, sticky='')
        input_area.grid(row=1, sticky='nsew', padx=5, pady=5)
        function_frame.grid(row=2, sticky='nsew', padx=5)
        from_label.grid(row=0, column=0, sticky='e')
        from_entry.grid(row=0, column=1, sticky='w')
        to_label.grid(row=0, column=2, sticky='e')
        to_entry.grid(row=0, column=3, sticky='w')
        output_area.grid(row=3, sticky='nsew', padx=5, pady=5)
        button_frame.grid(row=4, column=0, sticky='wesn', padx=5)
        replace_button.grid(row=0, column=0, sticky='we')
        copy_button.grid(row=0, column=1, sticky='we')
        clear_button.grid(row=1, column=0, columnspan=2, sticky='we')
        info_label.grid(row=5, column=0, sticky='we')

        output_area.config(state='disabled')

        for row in [1, 3]:
            n_window.rowconfigure(row, weight=1, minsize=30)
        for col in range(1):
            n_window.columnconfigure(col, weight=1, minsize=30)
        function_frame.rowconfigure(0, weight=1, minsize=30)
        for col_f in range(4):
            function_frame.columnconfigure(col_f, weight=1, minsize=30)
        for col_b in range(2):
            button_frame.columnconfigure(col_b, weight=1, minsize=30)

    def __tsts__(self):
        def sts():
            text = self.fn.get_text_from_text_area(input_area)
            if text:
                str_total = len(text)
                dig_total = len(re.findall(r'\d', text))
                cn_str_total = len(re.findall(r'[\u4e00-\u9fff]', text))
                en_str_total = len(re.findall(r'[a-zA-Z]', text))
                en_p_total = 0
                for i in text:
                    if i in ['!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^', '_', '`', '{', '|', '}', '~']:
                        en_p_total += 1
                tl = text.split('\n')
                p_total = len(tl)
                yp_total = 0
                for line in tl:
                    if line:
                        yp_total += 1
                str_total_label.config(text=f'字符总数：{str_total}')
                dig_total_label.config(text=f'数字字符总数：{dig_total}')
                cn_total_label.config(text=f'中文字符总数：{cn_str_total}')
                en_total_label.config(text=f'英文字符总数：{en_str_total}, 英文标点总数：{en_p_total}')
                p_total_label.config(text=f'总行数：{p_total}')
                yp_total_label.config(text=f'段落数：{yp_total}')

        def clear_n(arg):
            self.fn.delete_text_from_text_area(arg)
            str_total_label.config(text='字符总数：0')
            dig_total_label.config(text='数字字符总数：0')
            cn_total_label.config(text='中文字符总数：0')
            en_total_label.config(text='英文字符总数：0, 英文标点总数：0')
            p_total_label.config(text='总行数：0')
            yp_total_label.config(text='段落数：0')

        n_window = self.windows['tsts']

        title_label = tk.Label(n_window, text='文本统计', font=Config.FONT_TITLE, anchor='center')
        input_area = scrolledtext.ScrolledText(n_window)
        str_total_label = tk.Label(n_window, text='字符总数：0', font=Config.FONT_NORMAL)
        dig_total_label = tk.Label(n_window, text='数字字符总数：0', font=Config.FONT_NORMAL)
        cn_total_label = tk.Label(n_window, text='中文字符总数：0', font=Config.FONT_NORMAL)
        en_total_label = tk.Label(n_window, text='英文字符总数：0, 英文标点总数：0', font=Config.FONT_NORMAL)
        p_total_label = tk.Label(n_window, text='总行数：0', font=Config.FONT_NORMAL)
        yp_total_label = tk.Label(n_window, text='段落数：0', font=Config.FONT_NORMAL)
        sts_button = tk.Button(n_window, text='统计', font=Config.FONT_NORMAL, command=sts)
        clear_button = tk.Button(n_window, text='清空', font=Config.FONT_NORMAL, command=lambda: clear_n([input_area]))
        info_label = tk.Label(n_window, text='本工具只统计常用字符，部分特殊字符请参阅：www.unicode.org/charts')

        title_label.grid(row=0, columnspan=2, sticky='we')
        input_area.grid(row=1, columnspan=2, sticky='nsew', padx=5, pady=5)
        str_total_label.grid(row=2, columnspan=2, sticky='w', padx=5)
        dig_total_label.grid(row=3, columnspan=2, sticky='w', padx=5)
        cn_total_label.grid(row=4, columnspan=2, sticky='w', padx=5)
        en_total_label.grid(row=5, columnspan=2, sticky='w', padx=5)
        p_total_label.grid(row=6, columnspan=2, sticky='w', padx=5)
        yp_total_label.grid(row=7, columnspan=2, sticky='w', padx=5)
        sts_button.grid(row=8, column=0, sticky='we', padx=(5, 0))
        clear_button.grid(row=8, column=1, sticky='we', padx=(0, 5))
        info_label.grid(row=9, columnspan=2, sticky='we', padx=5)

        for row in [1]:
            n_window.rowconfigure(row, weight=1, minsize=30)
        for col in range(2):
            n_window.columnconfigure(col, weight=1, minsize=30)

    def __tsplit__(self):
        def split_text():
            is_strip = strip_var.get()
            is_show_line = show_line_var.get()
            is_remove_empty = remove_empty_lines.get()
            text = self.fn.get_text_from_text_area(input_area)
            split_str = self.fn.get_text_from_text_area(fen_scroll)
            if text:
                if split_str:
                    text_list = text.split(split_str)
                else:
                    text_list = [x for x in text]

                if is_strip:
                    text_list = [x.strip() for x in text_list]
                if is_remove_empty:
                    text_list = [x for x in text_list if x]
                if is_show_line:
                    text_list = [f'{i + 1} {x}' for i, x in enumerate(text_list)]

                new_text = '\n'.join(text_list)
                self.fn.delete_insert_text_to_text_area(output_area, new_text)

        n_window = self.windows['tsplit']
        strip_var = tk.BooleanVar()
        show_line_var = tk.BooleanVar()
        remove_empty_lines = tk.BooleanVar()

        title_label = tk.Label(n_window, text='文本分割', font=Config.FONT_TITLE, anchor='center')
        input_area = scrolledtext.ScrolledText(n_window)
        split_frame = tk.Frame(n_window)
        fen_label = tk.Label(split_frame, text='分隔符：', font=Config.FONT_NORMAL)
        fen_scroll = scrolledtext.ScrolledText(split_frame, width=30, height=1)
        function_frame = tk.Label(n_window)
        strip_check = tk.Checkbutton(function_frame, variable=strip_var, text='去除行首尾空格')
        show_line_check = tk.Checkbutton(function_frame, variable=show_line_var, text='显示行号')
        remove_empty_lines_check = tk.Checkbutton(function_frame, variable=remove_empty_lines, text='(分割后)去除空行')
        output_area = scrolledtext.ScrolledText(n_window)
        button_frame = tk.Frame(n_window)
        do_button = tk.Button(button_frame, text='分割', font=Config.FONT_NORMAL, command=split_text)
        copy_button = tk.Button(button_frame, text='复制', font=Config.FONT_NORMAL, command=lambda: self.fn.copy_from_text_area(output_area))
        clear_button = tk.Button(button_frame, text='清空', font=Config.FONT_NORMAL, command=lambda: self.fn.delete_text_from_text_area([input_area, output_area, fen_scroll]))

        title_label.grid(row=0, sticky='we')
        input_area.grid(row=1, sticky='nsew', padx=5, pady=5)
        split_frame.grid(row=2, sticky='nsew', padx=5)
        fen_label.grid(row=0, column=0, sticky='e')
        fen_scroll.grid(row=0, column=1, sticky='w')
        function_frame.grid(row=3, sticky='nsew', padx=5)
        strip_check.grid(row=0, column=0, sticky='')
        show_line_check.grid(row=0, column=1, sticky='')
        remove_empty_lines_check.grid(row=0, column=2, sticky='')
        output_area.grid(row=4, column=0, sticky='nsew', padx=5, pady=5)
        button_frame.grid(row=5, column=0, sticky='nsew', padx=5, pady=(0, 5))
        do_button.grid(row=0, column=0, sticky='ew')
        copy_button.grid(row=0, column=1, sticky='ew')
        clear_button.grid(row=1, columnspan=2, sticky='ew')

        output_area.configure(state='disabled')
        strip_var.set(True)
        show_line_var.set(False)
        remove_empty_lines.set(True)

        for row in [1, 4]:
            n_window.rowconfigure(row, weight=1, minsize=30)
        n_window.columnconfigure(0, weight=1, minsize=30)
        for col_s in range(2):
            split_frame.columnconfigure(col_s, weight=1, minsize=30)
        for col_f in range(3):
            function_frame.columnconfigure(col_f, weight=1, minsize=30)
        for col_b in range(2):
            button_frame.columnconfigure(col_b, weight=1, minsize=30)

    def __tss__(self):
        def dealfn():
            is_remove_empty_line = remove_empty_line_var.get()
            is_strip = strip_var.get()
            is_remove_repeat = remove_repeat_var.get()
            is_sort = sort_var.get()
            text = self.fn.get_text_from_text_area(input_area)
            if text:
                text_list = text.split('\n')
                if is_strip:
                    text_list = [x.strip() for x in text_list]
                if is_remove_repeat:
                    text_list = list(set(text_list))
                if is_remove_empty_line:
                    text_list = [x for x in text_list if x]
                if is_sort:
                    text_list.sort()
                result = '\n'.join(text_list)
                self.fn.delete_insert_text_to_text_area(deal_output_area, result)

        def sticfn():
            stic_option = stic_combox.get()
            text = self.fn.get_text_from_text_area(input_area)
            if text:
                text_list = text.split('\n')
                new_dict = {}
                deal_list = []
                for x in text_list:
                    if x not in new_dict:
                        new_dict[x] = 1
                    else:
                        new_dict[x] += 1
                for x in new_dict:
                    deal_list.append([x, new_dict[x]])
                if stic_option == '原始数据排序':
                    new_list = []
                    for x in new_dict:
                        new_list.append(f'{x}出现了 {new_dict[x]} 次')
                elif stic_option == '重复次数降序':
                    deal_list.sort(key=lambda x1: x1[1], reverse=True)
                    new_list = []
                    for x in deal_list:
                        new_list.append(f'{x[0]}出现了 {x[1]} 次')
                else:
                    deal_list.sort(key=lambda x1: x1[1])
                    new_list = []
                    for x in deal_list:
                        new_list.append(f'{x[0]}出现了 {x[1]} 次')
                result = '\n'.join(new_list)
                self.fn.delete_insert_text_to_text_area(stic_output_area, result)

        n_window = self.windows['tss']
        sort_method_options = ['原始数据排序', '重复次数降序', '重复次数升序']
        remove_empty_line_var = tk.BooleanVar()
        strip_var = tk.BooleanVar()
        remove_repeat_var = tk.BooleanVar()
        sort_var = tk.BooleanVar()

        title_label = tk.Label(n_window, text='多行文本去重/排序', font=Config.FONT_TITLE, anchor='center')
        input_area = scrolledtext.ScrolledText(n_window)
        content_deal_frame = tk.Frame(n_window)
        deal_notebook = ttk.Notebook(content_deal_frame)
        deal_frame = ttk.Frame(deal_notebook)
        stic_frame = ttk.Frame(deal_notebook)

        deal_remove_empty_line_check = tk.Checkbutton(deal_frame, text='去除空白行', variable=remove_empty_line_var)
        deal_strip_check = tk.Checkbutton(deal_frame, text='去除行首尾空格', variable=strip_var)
        deal_remove_repeat_check = tk.Checkbutton(deal_frame, text='去重', variable=remove_repeat_var)
        deal_sort_check = tk.Checkbutton(deal_frame, text='排序', variable=sort_var)
        deal_output_area = scrolledtext.ScrolledText(deal_frame)
        deal_button_frame = tk.Frame(deal_frame)
        deal_deal_button = tk.Button(deal_button_frame, text='处理', font=Config.FONT_NORMAL, command=dealfn)
        deal_copy_button = tk.Button(deal_button_frame, text='复制', font=Config.FONT_NORMAL, command=lambda: self.fn.copy_from_text_area(deal_output_area))
        deal_clear_button = tk.Button(deal_button_frame, text='清空', font=Config.FONT_NORMAL, command=lambda: self.fn.delete_text_from_text_area([deal_output_area, input_area]))

        stic_p_label = tk.Label(stic_frame, text='排序方式：', font=Config.FONT_NORMAL)
        stic_combox = ttk.Combobox(stic_frame, values=sort_method_options, state="readonly")
        stic_output_area = scrolledtext.ScrolledText(stic_frame)
        stic_button_frame = tk.Frame(stic_frame)
        stic_deal_button = tk.Button(stic_button_frame, text='统计', font=Config.FONT_NORMAL, command=sticfn)
        stic_copy_button = tk.Button(stic_button_frame, text='复制', font=Config.FONT_NORMAL, command=lambda: self.fn.copy_from_text_area(stic_output_area))
        stic_clear_button = tk.Button(stic_button_frame, text='清空', font=Config.FONT_NORMAL, command=lambda: self.fn.delete_text_from_text_area([stic_output_area, input_area]))

        deal_notebook.add(deal_frame, text='文本行去重/排序')
        deal_notebook.add(stic_frame, text='文本行重复统计')

        title_label.grid(row=0, column=0, sticky='we')
        input_area.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        content_deal_frame.grid(row=2, column=0, sticky='nsew')
        deal_notebook.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)

        deal_remove_empty_line_check.grid(row=0, column=0)
        deal_strip_check.grid(row=0, column=1)
        deal_remove_repeat_check.grid(row=0, column=2)
        deal_sort_check.grid(row=0, column=3)
        deal_output_area.grid(row=1, column=0, columnspan=4, sticky='nsew')
        deal_button_frame.grid(row=2, column=0, columnspan=4, sticky='nsew')
        deal_deal_button.grid(row=0, column=0, sticky='we')
        deal_copy_button.grid(row=0, column=1, sticky='we')
        deal_clear_button.grid(row=1, column=0, columnspan=2, sticky='we')

        stic_p_label.grid(row=0, column=0, sticky='e')
        stic_combox.grid(row=0, column=1, sticky='w')
        stic_output_area.grid(row=1, columnspan=2, sticky='nsew')
        stic_button_frame.grid(row=2, column=0, columnspan=2, sticky='nsew')
        stic_deal_button.grid(row=0, column=0, sticky='we')
        stic_copy_button.grid(row=0, column=1, sticky='we')
        stic_clear_button.grid(row=1, column=0, columnspan=2, sticky='we')

        deal_output_area.config(state='disabled')
        stic_output_area.config(state='disabled')
        remove_empty_line_var.set(value=True)
        strip_var.set(value=True)
        remove_repeat_var.set(value=True)
        sort_var.set(value=True)
        stic_combox.set(value='原始数据排序')

        for raw_m in [1, 2]:
            n_window.rowconfigure(raw_m, weight=1, minsize=30)
        n_window.columnconfigure(0, weight=1, minsize=30)
        content_deal_frame.rowconfigure(0, weight=1, minsize=30)
        content_deal_frame.columnconfigure(0, weight=1, minsize=30)
        deal_notebook.rowconfigure(0, weight=1, minsize=30)
        deal_notebook.columnconfigure(0, weight=1, minsize=30)
        for row_d in [1]:
            deal_frame.rowconfigure(row_d, weight=1, minsize=30)
        for col_d in range(4):
            deal_frame.columnconfigure(col_d, weight=1, minsize=30)
        for col_d_b in range(2):
            deal_button_frame.columnconfigure(col_d_b, weight=1, minsize=30)
        for row_s in [1]:
            stic_frame.rowconfigure(row_s, weight=1, minsize=30)
        for col_s in range(2):
            stic_frame.columnconfigure(col_s, weight=1, minsize=30)
        for col_s_b in range(2):
            stic_button_frame.columnconfigure(col_s_b, weight=1, minsize=30)

    def __tjoin__(self):
        def tjoin():
            is_strip = strip_var.get()
            text = self.fn.get_text_from_text_area(input_area)
            fen_p = self.fn.get_text_from_text_area(fen_scroll)
            if text:
                text_list = text.split('\n')
                if is_strip:
                    text_list = [x.strip() for x in text_list]
                result = fen_p.join(text_list)
                self.fn.delete_insert_text_to_text_area(output_area, result)

        n_window = self.windows['tjoin']
        strip_var = tk.BooleanVar()

        title_label = tk.Label(n_window, text='文本合并', font=Config.FONT_TITLE, anchor='center')
        input_area = scrolledtext.ScrolledText(n_window)
        fen_label = tk.Label(n_window, text='分隔符：', font=Config.FONT_NORMAL)
        fen_scroll = tk.scrolledtext.ScrolledText(n_window, width=30, height=1)
        strip_check = tk.Checkbutton(n_window, variable=strip_var, text='去除行首尾空格')
        output_area = scrolledtext.ScrolledText(n_window)
        button_frame = tk.Frame(n_window)
        do_button = tk.Button(button_frame, text='合并', font=Config.FONT_NORMAL, command=tjoin)
        copy_button = tk.Button(button_frame, text='复制', font=Config.FONT_NORMAL, command=lambda: self.fn.copy_from_text_area(output_area))
        clear_button = tk.Button(button_frame, text='清空', font=Config.FONT_NORMAL, command=lambda: self.fn.delete_text_from_text_area([input_area, output_area, fen_scroll]))

        title_label.grid(row=0, column=0, columnspan=3, sticky='we')
        input_area.grid(row=1, column=0, columnspan=3, sticky='nsew', padx=5, pady=5)
        fen_label.grid(row=2, column=0, sticky='e')
        fen_scroll.grid(row=2, column=1, sticky='w')
        strip_check.grid(row=2, column=2, sticky='')
        output_area.grid(row=3, column=0, columnspan=3, sticky='nsew', padx=5, pady=5)
        button_frame.grid(row=4, column=0, columnspan=3, sticky='nsew', padx=5, pady=(0, 5))
        do_button.grid(row=0, column=0, sticky='we')
        copy_button.grid(row=0, column=1, sticky='we')
        clear_button.grid(row=1, columnspan=2, sticky='we')

        strip_var.set(value=True)
        output_area.config(state='disabled')

        for row in [1, 3]:
            n_window.rowconfigure(row, weight=1, minsize=30)
        for col in range(3):
            n_window.columnconfigure(col, weight=1, minsize=30)
        for col_b in range(2):
            button_frame.columnconfigure(col_b, weight=1, minsize=30)

    def __treverse__(self):
        def treverse():
            reverseop = reverseop_var.get()
            text = self.fn.get_text_from_text_area(input_area)
            if text:
                text_list = text.split('\n')
                if reverseop == 'h':
                    new_list = [x[::-1] for x in text_list]
                else:
                    new_list = text_list[::-1]
                    new_list = [x[::-1] for x in new_list]
                result = '\n'.join(new_list)
                self.fn.delete_insert_text_to_text_area(output_area, result)

        n_window = self.windows['treverse']
        reverseop_var = tk.StringVar()

        title_label = tk.Label(n_window, text='文本逆序', font=Config.FONT_TITLE, anchor='center')
        input_area = scrolledtext.ScrolledText(n_window)
        hreverse_rbutton = tk.Radiobutton(n_window, text='每行逆序', variable=reverseop_var, value='h')
        areverse_rbutton = tk.Radiobutton(n_window, text='全部逆序', variable=reverseop_var, value='a')
        output_area = scrolledtext.ScrolledText(n_window)
        button_frame = tk.Frame(n_window)
        do_button = tk.Button(button_frame, text='处理', font=Config.FONT_NORMAL, command=treverse)
        copy_button = tk.Button(button_frame, text='复制', font=Config.FONT_NORMAL, command=lambda: self.fn.copy_from_text_area(output_area))
        clear_button = tk.Button(button_frame, text='清空', font=Config.FONT_NORMAL, command=lambda: self.fn.delete_text_from_text_area([input_area, output_area]))

        title_label.grid(row=0, column=0, columnspan=2, sticky='we')
        input_area.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
        hreverse_rbutton.grid(row=2, column=0, sticky='e')
        areverse_rbutton.grid(row=2, column=1, sticky='w')
        output_area.grid(row=3, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
        button_frame.grid(row=4, column=0, columnspan=2, sticky='nsew', padx=5, pady=(0, 5))
        do_button.grid(row=0, column=0, sticky='we')
        copy_button.grid(row=0, column=1, sticky='we')
        clear_button.grid(row=1, columnspan=2, sticky='we')

        reverseop_var.set('h')
        output_area.config(state='disabled')

        for row in [1, 3]:
            n_window.rowconfigure(row, weight=1, minsize=30)
        for col in range(2):
            n_window.columnconfigure(col, weight=1, minsize=30)
        for col_b in range(2):
            button_frame.columnconfigure(col_b, weight=1, minsize=30)

    def __tlsl__(self):
        def tlsl():
            max_length = max_length_entry.get()
            text = self.fn.get_text_from_text_area(input_area)
            text_list = text.split('\n')
            if text:
                try:
                    int_length = int(max_length)
                    if int_length and int_length > 0:
                        new_list = []
                        for line in text_list:
                            new_list.append('\n'.join(self.fn.split_one_line(line, int_length)))
                        result = '\n'.join(new_list)
                        self.fn.delete_insert_text_to_text_area(output_area, result)
                    else:
                        messagebox.showerror('错误', f'请输入大于0的有效数字')
                except BaseException as e:
                    self.none = e
                    err_info = traceback.format_exc()
                    messagebox.showerror('错误', f'请输入大于0的有效数字\n\n{err_info}')

        n_window = self.windows['tlsl']

        title_label = tk.Label(n_window, text='文本行定长', font=Config.FONT_TITLE, anchor='center')
        input_area = scrolledtext.ScrolledText(n_window)
        max_length_label = tk.Label(n_window, text='单行最大长度', font=Config.FONT_NORMAL)
        max_length_entry = tk.Entry(n_window)
        output_area = scrolledtext.ScrolledText(n_window)
        button_frame = tk.Frame(n_window)
        do_button = tk.Button(button_frame, text='处理', font=Config.FONT_NORMAL, command=tlsl)
        copy_button = tk.Button(button_frame, text='复制', font=Config.FONT_NORMAL, command=lambda: self.fn.copy_from_text_area(output_area))
        clear_button = tk.Button(button_frame, text='清空', font=Config.FONT_NORMAL, command=lambda: self.fn.delete_text_from_text_area([input_area, output_area]))

        title_label.grid(row=0, column=0, columnspan=2, sticky='we')
        input_area.grid(row=1, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
        max_length_label.grid(row=2, column=0, sticky='e')
        max_length_entry.grid(row=2, column=1, sticky='w')
        output_area.grid(row=3, column=0, columnspan=2, sticky='nsew', padx=5, pady=5)
        button_frame.grid(row=4, column=0, columnspan=2, sticky='nsew', padx=5, pady=(0, 5))
        do_button.grid(row=0, column=0, sticky='we')
        copy_button.grid(row=0, column=1, sticky='we')
        clear_button.grid(row=1, columnspan=2, sticky='we')

        output_area.config(state='disabled')

        for row in [1, 3]:
            n_window.rowconfigure(row, weight=1, minsize=30)
        for col in range(2):
            n_window.columnconfigure(col, weight=1, minsize=30)
        for col_b in range(2):
            button_frame.columnconfigure(col_b, weight=1, minsize=30)

    def __unicodetool__(self):
        def out_log(content):
            result_dict = self.fn.get_one_chr_info(chr_str=content)
            info_str = f"Original: {content}\nUnicode: {result_dict['unicode_str']}\n16进制: {result_dict['h16']}\n10进制: {result_dict['h10']}\nName: {result_dict['char_name']}"
            self.fn.delete_insert_text_to_text_area(info_log, info_str)
            logout_scroll.clipboard_clear()
            logout_scroll.clipboard_append(content)
            self.fn.insert_text_to_text_area(logout_scroll, f'已复制{content}到剪切板\n')
            logout_scroll.see(tk.END)

        def place_symbol_button(master_frame, symbols: str):
            symbols = sorted(set(symbols))
            symbols = ''.join(symbols)
            symbols_list = self.fn.split_one_line(symbols, 10)
            for idl, line in enumerate(symbols_list):
                for ids, symbol in enumerate(line):
                    n_button = tk.Button(master_frame, text=symbol, font=('', 32))
                    n_button.config(command=lambda s=symbol: out_log(s))
                    n_button.grid(row=idl + 1, column=ids, sticky='we', padx=1, pady=1)
                    master_frame.rowconfigure(idl + 1, weight=1)
                    master_frame.columnconfigure(ids, weight=1)

        def place_content(master_content_frame, content_title: str, content_symbol: str, row_start: int):
            content_symbol_frame = tk.Frame(master_content_frame)
            content_title_label = tk.Label(content_symbol_frame, text=content_title, font=Config.FONT_NORMAL, anchor='w')
            place_symbol_button(content_symbol_frame, content_symbol)

            content_title_label.grid(row=0, column=0, columnspan=10, sticky='nw', pady=(10, 0))
            content_symbol_frame.grid(row=row_start, column=0, sticky='nswe')

            master_content_frame.rowconfigure(row_start, weight=1)
            content_symbol_frame.rowconfigure(0, weight=1)

        def creat_sesymbol_page(title_n: str, info_n: str | None = None, esmode: str = 's'):
            nonlocal right_side_frame

            def on_canvas_configure(event):
                canvas.configure(scrollregion=canvas.bbox("all"))
                canvas.itemconfig(canvas_window, width=event.width)

            def on_frame_configure(event):
                canvas.configure(scrollregion=canvas.bbox("all"))

            def canvas_wheel(event):
                canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            def bind_wheel_to_children(widget_n):
                widget_n.bind("<MouseWheel>", canvas_wheel)
                for child in widget_n.winfo_children():
                    bind_wheel_to_children(child)

            ssymbol_info = [
                ["上标符号", "⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾"],
                ["下标符号", "₀₁₂₃₄₅₆₇₈₉₊₋₌₍₎"],
                ["数字符号", "⓪①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳❶❷❸❹❺❻❼❽❾❿０１２３４５６７８９⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽⑾⑿⒀⒁⒂⒃⒄⒅⒆⒇⒈⒉⒊⒋⒌⒍⒎⒏⒐⒑⒒⒓⒔⒕⒖⒗⒘⒙⒚⒛"],
                ["数学符号", "+-*/%≠≡≤≥∈∅∑∫∞∴∵∀∃∪∩⊂⊆∇∂∏√∝∣∥∧∨⊢⊤⊥∼≈≅≃≪≫≮≯≰≱≲≳⊕⊗⊙⊎⊓⊔⋀⋁⋂⋃⋯⋮⋰⋱∁∄∆−∓∔∕∖∗∘∙∛∜∟∠∡∢∤∦∽∾∿≀≁≂≄≆≇≉≊≋≌≍≎≏≐≑≒≓≔≕≖≗≘≙≚≛≜≝≞≟≢≣≨≩≬≭≴≵≶≷≸≹≺≻≼≽≾≿⊀⊁⊄⊅⊈⊉⊊⊋⊌⊍⊏⊐⊑⊒⊖⊘⊚⊛⊜⊝⊞⊟⊠⊡⊣⊦⊧⊨⊩⊪⊫⊬⊭⊮⊯⊰⊱⊲⊳⊴⊵⊶⊷⊸⊹⊺⊻⊼⊽⊾⊿⋄⋅⋆⋇⋈⋉⋊⋋⋌⋍⋎⋏⋐⋑⋒⋓⋔⋕⋖⋗⋘⋙⋚⋛⋜⋝⋞⋟⋠⋡⋢⋣⋤⋥⋦⋧⋨⋩⋪⋫⋬⋭⋲⋳⋴⋵⋶⋷⋸⋹⋺⋻⋼⋽⋾⋿"],
                ["汉字数字", "㊀㊁㊂㊃㊄㊅㊆㊇㊈㊉㈠㈡㈢㈣㈤㈥㈦㈧㈨㈩"],
                ["罗马数字", "ⅰⅱⅲⅳⅴⅵⅶⅷⅸⅹⅺⅻⅠⅡⅢⅣⅤⅥⅦⅧⅨⅩⅪⅫ"],
                ["中文字符", "零壹贰叁肆伍陆柒捌玖拾佰仟万亿吉太拍艾分厘毫微卍卐卄巜弍弎弐朤氺曱甴囍兀々〆のぁ〡〢〣〤〥〦〧〨〩㊎㊍㊌㊋㊏㊚㊛㊐㊊㊣㊤㊥㊦㊧㊨㊒㊫㊑㊓㊔㊕㊖㊗㊘㊜㊝㊞㊟㊠㊡㊢㊩㊪㊬㊭㊮㊯㊰"],
                ["希腊字母大写", "ΑΒΓΔΕΖΗΘΙΚ∧ΜΝΞΟ∏Ρ∑ΤΥΦΧΨΩ"],
                ["希腊字母小写", "αβγδεζηθικλμνξοπρστυφχψω"],
                ["俄文字母大写", "АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"],
                ["俄文字母小写", "абвгдежзийклмнопрстуфхцчшщъыьэюя"],
                ["日期时间", "㋀㋁㋂㋃㋄㋅㋆㋇㋈㋉㋊㋋㏠㏡㏢㏣㏤㏥㏦㏧㏨㏩㏪㏫㏬㏭㏮㏯㏰㏱㏲㏳㏴㏵㏶㏷㏸㏹㏺㏻㏼㏽㏾㍘㍙㍚㍛㍜㍝㍞㍟㍠㍡㍢㍣㍤㍥㍦㍧㍨㍩㍪㍫㍬㍭㍮㍯㍰"],
                ["货币符号", "€£Ұ₴$₰¢₤¥₳₲₪₵元₣₱฿¤₡₮₭₩ރ円₢₥₫₦zł﷼₠₧₯₨Kčर₹ƒ₸￠"],
                ["音乐符号", "♩♪♫♬♯♭♮"],
                ["天气符号", "ϟ☀☁☂☃☄☉☼☽☾♁♨❄❅❆"],
                ["星星符号", "★✰☆✩✫✬✭✮✡⋆✢✣✤✥✦✧✪✯❂❉✱✲✳✴✵✶✷✸✹❊✻✼❆❇❈⁂⁑"],
                ["国际象棋符号", "♚♛♝♞♜♟♔♕♗♘♖♟"],
                ["宗教符号", "†☨✞✝☥☦☓☩☯☧☠☬☸♁✙♆✚✛✜✟卍卐"],
                ["箭头符号", "↑↓←→↖↗↙↘↔↕➻➼➽➸➳➺➻➴➵➶➷➹▶➩➪➫➬➭➮➯➱➲➾➔➘➙➚➛➜➝➞➟➠➡➢➣➤➥➦➧➨↚↛↜↝↞↟↠↠↡↢↣↤↤↥↦↧↨⇄⇅⇆⇇⇈⇉⇊⇋⇌⇍⇎⇏⇐⇑⇒⇓⇔⇖⇗⇘⇙⇜↩↪↫↬↭↮↯↰↱↲↳↴↵↶↷↸↹☇☈↼↽↾↿⇀⇁⇂⇃⇞⇟⇠⇡⇢⇣⇤⇥⇦⇧⇨⇩⇪↺↻"],
                ["三角形符号", "∆⊿▲△▴▵▶▷▸▹►▻▼▽▾▿◀◁◂◃◄◅◢◣◤◥◬◭◮◸◹◺◿∇"],
                ["圆形符号", "⊖⊘⊙⊚⊛⊜⊝◉○◌◍◎●◐◑◒◓◔◕◖◗◯◴◵◶◷⚫❍⦁⦶⦸⦾⦿⊕⊗"],
                ["正方形、长方形、菱形和填色方块的符号", "ˍ∎⊞⊟⊠⊡⋄⎔▀▁▂▃▄▅▆▇█▉▊▋▋▌▍▎▏▐░▒▓▔▖▗▘▙▚▛▜▝▞▟■□▢▣▤▥▦▧▨▩▪▫▬▭▮▯▰▱►◄◆◇◈◢◣◤◥◧◨◩◪◫◰◱◲◳◻◼◽◾❏❐❑❒❘❙❚⧈⧫⬒⬓⬔⬕⬖⬗⬘⬙⬚⬠⬡⬢⬣"],
            ]
            esymbol_info = [
                ['Faces', '😀😁😂😃😄😅😆😇😈😉😊😋😌😍😎😏😐😑😒😓😔😕😖😗😘😙😚😛😜😝😞😟😠😡😢😣😤😥😦😧😨😩😪😫😬😭😮😯😰😱😲😳😴😵😶😷🙁🙂🙃🙄🥰🥱🥲🥳🥴🥵🥶🥷🥸🥹🥺🫠🫡🫢🫣🫤🫥🫨'],
                ['Emoticon faces', '🤐🤑🤒🤓🤔🤕🤖🤗🤠🤡🤢🤣🤤🤥🤦🤧🤨🤩🤪🤫🤬🤭🤮🤯'],
                ['Cat faces', '😸😹😺😻😼😽😾😿🙀'],
                ['Gesture symbols', '🙅🙆🙇🙈🙉🙊🙋🙌🙍🙎🙏'],
                ['Hand symbols', '👆👇👈👉👊👋👌👍👎👏👐🖎🖏🖐🖑🖒🖓🖔🖕🖖🖗🖘🖙🖚🖛🖜🖝🖞🖟🖠🖡🖢🖣🤌🤏🤘🤙🤚🤛🤜🤝🤞🤟🫰🫱🫲🫳🫴🫵🫶🫷🫸'],
                ['Facial parts symbols', '👀👁👂👃👄👅'],
                ['Body parts', '🦴🦵🦶🦷🫀🫁'],
                ['Heart symbols', '💓💔💕💖💗💘💙💚💛💜💝💞💟🖤'],
                ['Colored heart symbols', '🤍🤎🩵🩶🩷'],
                ['Romance symbols', '💋💌💍💎💏💐💑💒'],
                ['People', '🫂🫃🫄🫅'],
                ['Portrait and role symbols', '👤👥👦👧👨👩👪👫👬👭👮👯👰👱👲👳👴👵👶👷🤰🤱🤲🤳🤴🤵🤶🤷🧐🧑🧒🧓🧔🧕🧖🧗🧘'],
                ['Role symbols', '💁💂💃🕺🦸🦹'],
                ['Fantasy beings', '🧌🧙🧚🧛🧜🧝🧞🧟'],
                ['Fairy tale symbols', '👸👹👺👻👼👽👾👿💀'],
                ['Animal faces', '🐭🐮🐯🐰🐱🐲🐳🐴🐵🐶🐷🐸🐹🐺🐻🐼🐽'],
                ['Animal symbols', '🐀🐁🐂🐃🐄🐅🐆🐇🐈🐉🐊🐋🐌🐍🐎🐏🐐🐑🐒🐓🐔🐕🐖🐗🐘🐙🐚🐛🐜🐝🐞🐟🐠🐡🐢🐣🐤🐥🐦🐧🐨🐩🐪🐫🐬🐾🐿🕷🕸🦀🦁🦂🦃🦄🦅🦆🦇🦈🦉🦊🦋🦌🦍🦎🦏🦐🦑🦒🦓🦔🦕🦖🦗🦘🦙🦚🦛🦜🦝🦞🦟🦠🦡🦢🦣🦤🦥🦦🦧🦨🦩🦪🦫🦬🦭'],
                ['Animals and nature', '🪰🪱🪲🪳🪴🪵🪶🪷🪸🪹🪺🪻🪼🪽🪿🫎🫏'],
                ['Plant symbols', '🌰🌱🌲🌳🌴🌵🌶🌷🌸🌹🌺🌻🌼🌽🌾🌿🍀🍁🍂🍃🍄'],
                ['Fruit and vegetable symbols', '🍅🍆🍇🍈🍉🍊🍋🍌🍍🍎🍏🍐🍑🍒🍓'],
                ['Food symbols', '🌭🌮🌯🍔🍕🍖🍗🍘🍙🍚🍛🍜🍝🍞🍟🍠🍡🍢🍣🍤🍥🍦🍧🍨🍩🍪🍫🍬🍭🍮🍯🍰🍱🍲🍳🍴🥐🥑🥒🥓🥔🥕🥖🥗🥘🥙🥚🥛🥜🥝🥞🥟🥠🥡🥢🥣🥤🥥🥦🥧🥨🥩🥪🥫🥬🥭🥮🥯🧀🧁🧂🧃🧄🧅🧆🧇🧈🧉🧊🧋'],
                ['Beverage symbols', '🍵🍶🍷🍸🍹🍺🍻🍼'],
                ['Food and drink', '🫐🫑🫒🫓🫔🫕🫖🫗🫘🫙🫚🫛'],
                ['Beverage and food symbols', '🍾🍿'],
                ['Clothing and accessories', '👑👒👓👔👕👖👗👘👙👚👛👜👝👞👟👠👡👢👣'],
                ['Clothing', '🥻🥼🥽🥾🥿🩰🩱🩲🩳🩴'],
                ['Personal care symbols', '💄💅💆💇💈'],
                ['Medical symbols', '💉💊🩸🩹🩺'],
                ['Medical and healing symbols', '☤☥'],
                ['Accessibility symbols', '🦮🦯🦺🦻🦼🦽🦾🦿'],
                ['Portrait and accessibility symbols', '🧍🧎🧏'],
                ['Weather symbols', '☔🌡🌢🌣🌤🌥🌦🌧🌨🌩🌪🌫🌬'],
                ['Weather and astrological symbols', '☀☁☂☃☄★☆☇☈☉☊☋☌☍'],
                ['Weather, landscape, and sky symbols', '🌀🌁🌂🌃🌄🌅🌆🌇🌈🌉🌊🌋🌌'],
                ['Weather symbols from ARIB STD B24', '⛄⛅⛆⛇⛈'],
                ['Moon, sun, and star symbols', '🌑🌒🌓🌔🌕🌖🌗🌘🌙🌚🌛🌜🌝🌞🌟🌠'],
                ['Globe symbols', '🌍🌎🌏🌐'],
                ['Astrological symbols', '☽☾☿♀♁♂♃♄♅♆♇'],
                ['Zodiacal symbols', '♈♉♊♋♌♍♎♏♐♑♒♓'],
                ['Zodiacal symbol', '⛎'],
                ['Astrological signs', '⚳⚴⚵⚶⚷⚸'],
                ['Astrological aspects', '⚹⚺⚻⚼'],
                ['Astronomical symbol', '⛢'],
                ['Stars and asterisks', '✡✢✣✤✥✦✧✨✩✪✫✬✭✮✯✰✱✲✳✴✵✶✷✸✹✺✻✼✽'],
                ['Stars, asterisks and snowflakes', '❂❃❄❅❆❇❈❉❊❋'],
                ['Crosses', '✙✚✛✜✝✞✟✠'],
                ['Syriac cross symbols', '♰♱'],
                ['Fleurons', '✾✿❀❁❦❧'],
                ['Pentagram symbols', '⛤⛥⛦⛧'],
                ['Geometric shapes', '🔲🔳🔴🔵🔶🔷🔸🔹'],
                ['Shadowed geometric shapes', '🔾🔿'],
                ['Circles', '⚪⚫⚬'],
                ['Dingbat arrows', '➔➘➙➚➛➜➝➞➟➠➡➢➣➤➥➦➧➨➩➪➫➬➭➮➯➱➲➳➴➵➶➷➸➹➺➻➼➽➾'],
                ['Words with arrows', '🔙🔚🔛🔜🔝'],
                ['Pointing hand symbols', '☚☛☜☝☞☟'],
                ['Heavy variants of arithmetic symbols', '➕➖➗'],
                ['Punctuation mark ornaments', '❛❜❝❞❟❠❡❢❣❤❥'],
                ['Ornamental brackets', '❨❩❪❫❬❭❮❯❰❱❲❳❴❵'],
                ['Dingbat circled digits', '❶❷❸❹❺❻❼❽❾❿➀➁➂➃➄➅➆➇➈➉➊➋➌➍➎➏➐➑➒➓'],
                ['Enclosed alphanumeric symbols', '🔞🔟'],
                ['User interface symbols', '🔀🔁🔂🔃🔄🔅🔆🔇🔈🔉🔊🔋🔌🔍🔎🔏🔐🔑🔒🔓🔔🔕🔖🔗🔘🔺🔻🔼🔽🖿🗀🗁🗂🗃🗄🗅🗆🗇🗈🗉🗊🗋🗌🗍🗎🗏🗐🗑🗒🗓🗔🗕🗖🗗🗘🗙🗚🗛🗜🗝'],
                ['User interface input status symbols', '🔠🔡🔢🔣🔤'],
                ['Communication symbols', '📝📞📟📠📡📢📣📤📥📦📧📨📩📪📫📬📭📮📯📰📱📲📳📴📵📶🕨🕩🕪🕫🕬🕻🕼🕽🕾🕿🖀🖁🖂🖃🖄🖅🖆🖇🖈🖉🖊🖋🖌🖍'],
                ['Audio and video symbols', '📷📸📹📺📻📼📽📾'],
                ['Computer symbols', '🖥🖦🖧🖨🖩🖪🖫🖬🖭🖮🖯🖰🖱🖲🖳🖴🖵🖶🖷🖸'],
                ['Tool symbols', '🔥🔦🔧🔨🔩🔪🔫🔬🔭🔮'],
                ['Office symbols', '💺💻💼💽💾💿📀📁📂📃📄📅📆📇📈📉📊📋📌📍📎📏📐📑📒📓📔📕📖📗📘📙📚📛📜🖹🖺🖻🖼🖽🖾'],
                ['Objects', '🧪🧫🧬🧭🧮🧯🧰🧱🧲🧳🧴🧵🧶🧷🧸🧹🧺🧻🧼🧽🧾🧿'],
                ['Money symbols', '💰💱💲💳💴💵💶💷💸💹'],
                ['Playing card symbols', '♠♡♢♣♤♥♦♧'],
                ['Game symbols', '🎮🎯🎰🎱🎲🎳🎴🕹'],
                ['Sport symbols', '⚽⚾🎽🎾🎿🏀🏁🏂🏃🏄🏅🏆🏇🏈🏉🏊🏋🏌🏍🏎🏏🏐🏑🏒🏓🏸🏹🤸🤹🤺🤻🤼🤽🤾🤿'],
                ['Toys and sport symbols', '🪀🪁🪂🪃🪄🪅🪆'],
                ['Entertainment symbols', '🎞🎟🎠🎡🎢🎣🎤🎥🎦🎧🎨🎩🎪🎫🎬🎭'],
                ['Celebration symbols', '🎀🎁🎂🎃🎄🎅🎆🎇🎈🎉🎊🎋🎌🎍🎎🎏🎐🎑🎒🎓🎔🎕🎖🎗'],
                ['Musical symbols', '♩♪♫♬♭♮♯🎘🎙🎚🎛🎜🎝🎵🎶🎷🎸🎹🎺🎻🎼'],
                ['Musical instruments', '🪇🪈'],
                ['Recycling symbols', '♲♳♴♵♶♷♸♹♺♻♼♽'],
                ['Warning signs', '☠☡☢☣'],
                ['Traffic signs', '🚥🚦🚧🚨'],
                ['Traffic signs from ARIB STD B24', '⛏⛐⛑⛒⛓⛔⛕⛖⛗⛘⛙⛚⛛⛜⛝⛞⛟⛠⛡'],
                ['Vehicles', '🚀🚁🚂🚃🚄🚅🚆🚇🚈🚉🚊🚋🚌🚍🚎🚏🚐🚑🚒🚓🚔🚕🚖🚗🚘🚙🚚🚛🚜🚝🚞🚟🚠🚡🚢🚣🚤🛥🛦🛧🛨🛩🛪🛫🛬🛰🛱🛲🛳🛴🛵🛶🛷🛸🛹🛺🛻🛼'],
                ['Signage and other symbols', '🚩🚪🚫🚬🚭🚮🚯🚰🚱🚲🚳🚴🚵🚶🚷🚸🚹🚺🚻🚼🚽🚾🚿🛀🛁🛂🛃🛄🛅🛆🛇🛈🛉🛊🛐🛑🛒'],
                ['Building and map symbols', '🏔🏕🏖🏗🏘🏙🏚🏛🏜🏝🏞🏟🏠🏡🏢🏣🏤🏥🏦🏧🏨🏩🏪🏫🏬🏭🏮🏯🏰'],
                ['Map symbols', '🗺🛕🛖🛗'],
                ['Map symbols from ARIB STD B24', '⛨⛩⛪⛫⛬⛭⛮⛯⛰⛱⛲⛳⛴⛵⛶⛷⛸⛹⛺⛻⛼⛽⛾⛿'],
                ['Map symbol from ARIB STD B24', '⛣'],
                ['Dictionary and map symbols', '⚐⚑⚒⚓⚔⚕⚖⚗⚘⚙⚚⚛'],
                ['Cultural symbols', '🗻🗼🗽🗾🗿'],
                ['Flag symbols', '🏱🏲🏳🏴'],
                ['Rosettes', '🏵🏶'],
                ['Accommodation symbols', '🛋🛌🛍🛎🛏'],
                ['Accommodation symbol', '🍽'],
                ['Religious symbols', '📿🕀🕁🕂🕃🕄🕅🕆🕇🕈🕉🕊🕋🕌🕍🕎🪯'],
                ['Religious and political symbols', '☦☧☨☩☪☫☬☭☮☯'],
                ['Gender symbols', '⚢⚣⚤⚥⚦⚧⚨⚩⚲'],
                ['Genealogical symbols', '⚭⚮⚯⚰⚱'],
                ['Japanese school grade symbols', '💮💯'],
                ['Japanese chess symbols', '☖☗'],
                ['Chess symbols', '♔♕♖♗♘♙♚♛♜♝♞♟'],
                ['Symbols for draughts and checkers', '⛀⛁⛂⛃'],
                ['Go markers', '⚆⚇⚈⚉'],
                ['Dice', '⚀⚁⚂⚃⚄⚅'],
                ['Yijing trigram symbols', '☰☱☲☳☴☵☶☷'],
                ['Yijing monogram and digram symbols', '⚊⚋⚌⚍⚎⚏'],
                ['Symbols for closed captioning from ARIB STD B24', '⚞⚟'],
                ['Game symbols from ARIB STD B24', '⛉⛊⛋'],
                ['Ballot symbols', '🗳🗴🗵🗶🗷🗸🗹'],
                ['Bubble symbols', '🗨🗩🗪🗫🗬🗭🗮🗯🗰🗱🗲'],
                ['Sound symbols', '🗤🗥🗦🗧'],
                ['Rating symbols', '🗡🗢🗣'],
                ['Clock face symbols', '🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚🕛🕜🕝🕞🕟🕠🕡🕢🕣🕤🕥🕦🕧'],
                ['Comic style symbols', '💠💡💢💣💤💥💦💧💨💩💪💫💬💭'],
                ['Miscellaneous', '☎☏☐☑☒☓☕☘☙☸☼♨♾♿⚜⚝⚠⚡⚿✀✁✂✃✄✅✆✇✈✉✊✋✌✍✎✏✐✑✒✓✔✕✖✗✘❌❍❎❏❐❑❒❓❔❕❖❗❘❙❚➰➿🏷🏺🔯🔰🔱🕭🕮🕯🕰🕱🕲🕳🕴🕵🕶🗞🗟🗠🛜🛝🛞🛟🛠🛡🛢🛣🛤🥀🥁🥂🥃🥄🥅🥆🥇🥈🥉🥊🥋🥌🥍🥎🥏🧠🧡🧢🧣🧤🧥🧦🪐🪑🪒🪓🪔🪕🪖🪗🪘🪙🪚🪛🪜🪝🪞🪟🪠🪡🪢🪣🪤🪥🪦🪧🪨🪩🪪🪫🪬🪭🪮🫦🫧'],
                ['Activities', '🧧🧨🧩'],
            ]

            right_side_frame.destroy()
            right_side_frame = tk.Frame(n_window)
            self.fn.delete_text_from_text_area([info_log, logout_scroll])
            right_side_frame.grid(row=0, column=1, sticky='nsew', pady=(0, 5))

            canvas = tk.Canvas(right_side_frame)
            v_scrollbar = tk.Scrollbar(right_side_frame, orient='vertical', command=canvas.yview)
            content_frame = tk.Frame(canvas)
            canvas_window = canvas.create_window(0, 0, anchor='nw', window=content_frame)

            canvas.grid(row=0, column=0, sticky='nsew')
            v_scrollbar.grid(row=0, column=1, sticky='ns')

            canvas.config(yscrollcommand=v_scrollbar.set)
            canvas.bind('<Configure>', on_canvas_configure)
            content_frame.bind('<Configure>', on_frame_configure)
            content_frame.bind('<MouseWheel>', canvas_wheel)

            title_label = tk.Label(content_frame, text=title_n, font=Config.FONT_TITLE, anchor='center')
            title_label.grid(row=0, column=0, sticky='n')

            if info_n:
                info_label = tk.Label(content_frame, text=info_n, font=('宋体', 10), anchor='center')
                info_label.grid(row=1, column=0, sticky='n')
                start_row = 2
            else:
                start_row = 1

            if esmode == 's':
                for info_group in ssymbol_info:
                    place_content(content_frame, info_group[0], info_group[1], start_row)
                    start_row += 1
            else:
                for info_group in esymbol_info:
                    place_content(content_frame, info_group[0], info_group[1], start_row)
                    start_row += 1

            bind_wheel_to_children(content_frame)

            for row_c in range(2):
                content_frame.rowconfigure(row_c, weight=1)
            content_frame.columnconfigure(0, weight=1)
            right_side_frame.rowconfigure(0, weight=1)
            right_side_frame.columnconfigure(0, weight=1)
            n_window.columnconfigure(1, weight=40, minsize=100)

        def creat_unitool_page():
            def single_left_ord_output():
                text = char_entry.get()
                if text:
                    if len(text) == 1:
                        result_dict = self.fn.get_one_chr_info(chr_str=text)
                        info_str = f"Original: {text}\nUnicode: {result_dict['unicode_str']}\n16进制: {result_dict['h16']}\n10进制: {result_dict['h10']}\nName: {result_dict['char_name']}"
                        self.fn.delete_insert_text_to_text_area(left_extra_output, info_str)
                    else:
                        messagebox.showerror('错误', '格式错误，请输入单个字符！')
                        return
                else:
                    self.fn.delete_text_from_text_area([left_extra_output])

            def single_right_ord_output():
                hdh_var = s_h_var.get()
                if hdh_var == 10:
                    text = s_h10_entry.get()
                else:
                    text = s_h16_entry.get()
                if text:
                    try:
                        h10_str = int(text, hdh_var)
                        result_dict = self.fn.get_one_chr_info(ord_int=h10_str)
                        info_str = f"result: {result_dict['result']}\nUnicode: {result_dict['unicode_str']}\n16进制: {result_dict['h16']}\n10进制: {h10_str}\nName: {result_dict['char_name']}"
                        self.fn.delete_insert_text_to_text_area(s_r_scroll, info_str)
                    except Exception as e:
                        messagebox.showerror('错误', str(e))
                else:
                    self.fn.delete_text_from_text_area([s_r_scroll])

            def range_deal_output():
                hd_var = r_hd_var.get()
                min_10 = max_10 = None
                if hd_var == 10:
                    try:
                        min_10 = int(rd_min_entry.get(), hd_var)
                        max_10 = int(rd_max_entry.get(), hd_var)
                    except Exception as e:
                        messagebox.showerror('错误', str(e))
                else:
                    try:
                        min_10 = int(rh_min_entry.get(), hd_var)
                        max_10 = int(rh_max_entry.get(), hd_var)
                    except Exception as e:
                        messagebox.showerror('错误', str(e))
                if min_10 and max_10:
                    if max_10 > min_10:
                        strings = ''.join([x['result'] for x in [self.fn.get_one_chr_info(y) for y in range(min_10, max_10 + 1)]])
                        self.fn.delete_insert_text_to_text_area(r_out_scroll, strings)
                    else:
                        messagebox.showerror('错误', f'{min_10}<={max_10}')

            def range_copy():
                self.fn.copy_from_text_area(r_out_scroll)
                self.fn.insert_text_to_text_area(logout_scroll, f'成功复制\n')

            for widget in right_side_frame.winfo_children():
                widget.destroy()

            self.fn.delete_text_from_text_area([info_log, logout_scroll])

            title_label = tk.Label(right_side_frame, text='UnicodeTool', font=Config.FONT_TITLE, anchor='center')
            content_notebook = ttk.Notebook(right_side_frame)

            single_deal_frame = tk.Frame(content_notebook)
            left_frame = tk.Frame(single_deal_frame)
            left_title_label = tk.Label(left_frame, text='ord', font=Config.FONT_TITLE, anchor='center')
            tisi_label = tk.Label(left_frame, text='Single character:', font=Config.FONT_NORMAL, anchor='e')
            char_entry = tk.Entry(left_frame)
            left_output_button = tk.Button(left_frame, text='Obtain information', command=single_left_ord_output)
            left_extra_output = scrolledtext.ScrolledText(left_frame, font=Config.FONT_TITLE, state='disabled')

            right_frame = tk.Frame(single_deal_frame)
            right_title_label = tk.Label(right_frame, text='chr', font=Config.FONT_TITLE, anchor='center')
            s_h_var = tk.IntVar()
            s_r_h0_rbutton = tk.Radiobutton(right_frame, text='Decimal in [0-1114111]:', value=10, variable=s_h_var, anchor='w')
            s_h10_entry = tk.Entry(right_frame)
            s_r_h16_rbutton = tk.Radiobutton(right_frame, text='Hexadecimal in [0-10FFFF]:', anchor='w', value=16, variable=s_h_var)
            s_h16_entry = tk.Entry(right_frame)
            s_r_out_button = tk.Button(right_frame, text='Obtain information', command=single_right_ord_output)
            s_r_scroll = scrolledtext.ScrolledText(right_frame, font=Config.FONT_TITLE, state='disabled')

            range_deal_page = tk.Frame(content_notebook)
            r_hd_var = tk.IntVar()
            r_title_label = tk.Label(range_deal_page, text='Generate all characters within the range', font=Config.FONT_TITLE, anchor='center')
            r_10_tisi = tk.Radiobutton(range_deal_page, text='Decimal in [0-1114111]', value=10, variable=r_hd_var, anchor='w')
            rd_min_label = tk.Label(range_deal_page, text='Min:', anchor='e')
            rd_min_entry = tk.Entry(range_deal_page)
            rd__label = tk.Label(range_deal_page, text='-', anchor='center')
            rd_max_label = tk.Label(range_deal_page, text='Max:', anchor='e')
            rd_max_entry = tk.Entry(range_deal_page)
            r_16_tisi = tk.Radiobutton(range_deal_page, text='Hexadecimal in [0-10FFFF]', value=16, variable=r_hd_var, anchor='w')
            rh_min_label = tk.Label(range_deal_page, text='Min:', anchor='e')
            rh_min_entry = tk.Entry(range_deal_page)
            rh__label = tk.Label(range_deal_page, text='-', anchor='center')
            rh_max_label = tk.Label(range_deal_page, text='Max:', anchor='e')
            rh_max_entry = tk.Entry(range_deal_page)
            r_output_button = tk.Button(range_deal_page, text='Obtain information', command=range_deal_output)
            r_deal_button_frame = tk.Frame(range_deal_page)
            r_copy_button = tk.Button(r_deal_button_frame, text='Copy', command=range_copy)
            r_clear_button = tk.Button(r_deal_button_frame, text='Clear', command=lambda: self.fn.delete_text_from_text_area([r_out_scroll]))
            r_out_scroll = scrolledtext.ScrolledText(range_deal_page, font=Config.FONT_NORMAL, state='disabled')

            title_label.grid(row=0, column=0, sticky='n')
            content_notebook.grid(row=1, column=0, sticky='nswe')
            left_frame.grid(row=0, column=0, sticky='nswe')
            left_title_label.grid(row=0, column=0, columnspan=2, sticky='n')
            tisi_label.grid(row=1, column=0, sticky='we')
            char_entry.grid(row=1, column=1, sticky='we')
            left_output_button.grid(row=2, column=0, columnspan=2, sticky='we')
            left_extra_output.grid(row=3, column=0, columnspan=2, sticky='nswe', pady=(5, 0))

            right_frame.grid(row=0, column=1, sticky='nswe')
            right_title_label.grid(row=0, column=0, columnspan=2, sticky='n')
            s_r_h0_rbutton.grid(row=1, column=0, sticky='we')
            s_h10_entry.grid(row=1, column=1, sticky='we')
            s_r_h16_rbutton.grid(row=2, column=0, sticky='we')
            s_h16_entry.grid(row=2, column=1, sticky='we')
            s_r_out_button.grid(row=3, column=0, columnspan=2, sticky='we')
            s_r_scroll.grid(row=4, column=0, columnspan=2, sticky='wens', pady=(5, 0))

            r_title_label.grid(row=0, column=0, columnspan=6, sticky='n')
            r_10_tisi.grid(row=1, column=0, sticky='we')
            rd_min_label.grid(row=1, column=1, sticky='we')
            rd_min_entry.grid(row=1, column=2, sticky='we')
            rd__label.grid(row=1, column=3, sticky='we')
            rd_max_label.grid(row=1, column=4, sticky='we')
            rd_max_entry.grid(row=1, column=5, sticky='we')
            r_16_tisi.grid(row=2, column=0, sticky='we')
            rh_min_label.grid(row=2, column=1, sticky='we')
            rh_min_entry.grid(row=2, column=2, sticky='we')
            rh__label.grid(row=2, column=3, sticky='we')
            rh_max_label.grid(row=2, column=4, sticky='we')
            rh_max_entry.grid(row=2, column=5, sticky='we')
            r_output_button.grid(row=3, column=0, columnspan=6, sticky='we')
            r_deal_button_frame.grid(row=4, column=0, columnspan=6, sticky='nswe')
            r_copy_button.grid(row=0, column=0, sticky='we')
            r_clear_button.grid(row=0, column=1, sticky='we')
            r_out_scroll.grid(row=5, column=0, columnspan=6, sticky='wens', pady=(5, 0))

            content_notebook.add(single_deal_frame, text='single')
            content_notebook.add(range_deal_page, text='rangle')
            s_h_var.set(10)
            r_hd_var.set(10)

            for row_s_l in [1, 2, 3]:
                left_frame.rowconfigure(row_s_l, weight=1, minsize=25)
            for col_s_l in range(2):
                left_frame.columnconfigure(col_s_l, weight=1, minsize=25)
            for row_s_r in [1, 2, 3, 4]:
                right_frame.rowconfigure(row_s_r, weight=1, minsize=25)
            for col_s_r in range(2):
                right_frame.columnconfigure(col_s_r, weight=1, minsize=25)

            single_deal_frame.rowconfigure(0, weight=1, minsize=25)
            for col_s in range(2):
                single_deal_frame.columnconfigure(col_s, weight=1, minsize=50)

            r_deal_button_frame.rowconfigure(0, weight=1, minsize=25)
            for col_r_d in range(2):
                r_deal_button_frame.columnconfigure(col_r_d, weight=1, minsize=25)
            for row_r in [1, 2, 3, 4]:
                range_deal_page.rowconfigure(row_r, weight=1, minsize=25)
            for col_r in range(6):
                range_deal_page.columnconfigure(col_r, weight=1, minsize=25)
            right_side_frame.rowconfigure(1, weight=1, minsize=25)
            right_side_frame.columnconfigure(0, weight=1, minsize=25)

        n_window = self.windows['unicodetool']

        left_side_frame = tk.Frame(n_window)
        right_side_frame = tk.Frame(n_window)

        ssymbol = tk.Button(left_side_frame, text='特殊符号', font=Config.FONT_NORMAL, command=lambda: creat_sesymbol_page('部分特殊符号', None, 's'))
        esymbol = tk.Button(left_side_frame, text='Emoji & Pictographs', font=Config.FONT_NORMAL, command=lambda: creat_sesymbol_page('Emoji & Pictographs', '更多请参阅：http://www.unicode.org/charts/', 'e'))
        uni_tool = tk.Button(left_side_frame, text='UnicodeTool', font=Config.FONT_NORMAL, command=lambda: creat_unitool_page())
        info_log = scrolledtext.ScrolledText(left_side_frame, width=5)
        logout_scroll = scrolledtext.ScrolledText(left_side_frame, width=5)

        left_side_frame.grid(row=0, column=0, sticky='nsew', padx=(5, 0), pady=(0, 5))
        right_side_frame.grid(row=0, column=1, sticky='nsew', pady=(0, 5))
        ssymbol.grid(row=0, column=0, sticky='wen')
        esymbol.grid(row=1, column=0, sticky='wen')
        uni_tool.grid(row=2, column=0, sticky='wen')
        info_log.grid(row=3, column=0, sticky='nsew')
        logout_scroll.grid(row=4, column=0, sticky='wesn')

        info_log.config(state='disabled')
        logout_scroll.config(state='disabled')

        n_window.columnconfigure(0, weight=1, minsize=175)
        n_window.columnconfigure(1, weight=40, minsize=100)
        n_window.rowconfigure(0, weight=1, minsize=30)

        for row_l in range(5):
            left_side_frame.rowconfigure(row_l, weight=1, minsize=30)
        left_side_frame.columnconfigure(0, weight=1, minsize=30)

    def creat_or_focus_window(self, window_id, window_title):
        if window_id in self.windows and self.windows[window_id].winfo_exists():
            window = self.windows[window_id]
            window.lift()
            window.focus_force()
        else:
            new_window = tk.Toplevel(self.master)
            new_window.protocol("WM_DELETE_WINDOW", lambda: self.on_window_close(window_id))
            self.windows[window_id] = new_window
            new_window.title(window_title)
            new_window.geometry('800x600+200+200')
            new_window.minsize(650, 400)
        self.pages_fn[window_id]()

    def on_window_close(self, window_id):
        if window_id in self.windows:
            try:
                self.windows[window_id].destroy()
            except Exception as e:
                self.none = e
                pass
            finally:
                if window_id in self.windows:
                    del self.windows[window_id]


if __name__ == "__main__":
    root = tk.Tk()
    pytool = PyToolApp(root)
    root.mainloop()
