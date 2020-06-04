# -*- coding: utf-8 -*-
import os
import psutil
import platform
import logging
import pickle
from mio.util.Helper import get_root_path, file_lock, file_unlock, write_txt_file
from mio.util.Logs import LogHandler


class WebDriver(object):
    logger = None
    driver = None
    display = None
    cw_pid = None

    def __init__(self, prefs=None, arguments=None, cookies=None, executable_path=None, is_display=True,
                 script_timeout=60, page_load_timeout=60, log_file=False, log_level=logging.DEBUG, check_process=False,
                 extension=None):
        """
        根据之前的经验，经常会发生的状况是
        python的进程挂了，但是浏览器还在
        因此启动的时候，应该先扫一次python的pid
        存储结构应该为，python.pid，内容为selenium的pid
        """
        pid = os.getpid()
        log_file_default = os.path.join(get_root_path(), 'logs', 'WebDriver_{pid}.log'.format(pid=str(pid)))
        if log_file is None:
            log_file = log_file_default
        else:
            if isinstance(log_file, bool) and not log_file:
                log_file = None
            else:
                log_file = log_file_default
        self.logger = LogHandler('CrawlerWebDriver', log_file=log_file, log_level=log_level)
        pid_path = os.path.join(get_root_path(), 'pid')
        if not os.path.exists(pid_path):
            os.makedirs(pid_path)
        # 检查是否有lock文件
        if check_process:
            locker = 'wd_check.lock'
            self.logger.info(u'{pid}：检查残留进程……'.format(pid=pid))
            code, _ = file_lock(locker, exp=60)
            if code == 1:
                """
                锁定以避免重复检查的问题，只需要一个进程检查就可以了，其他进程就不需要再做了
                逻辑就是先读入文件夹，存成变量，然后读取当前ps list，对比存活状态
                """
                self.logger.info(u'{pid}：读取当前文件的文件列表'.format(pid=pid))
                files = os.listdir(pid_path)
                # 读取当前PS信息
                for item in files:
                    item = os.path.join(pid_path, item)
                    if os.path.isdir(item):
                        # 如果不是文件就退出
                        continue
                    temp = item.split('.')
                    if len(temp) <= 1:
                        continue
                    ext = temp[-1]
                    if ext != 'pid':
                        continue
                    _, filename = os.path.split(item)
                    self.logger.info(u'{pid}：正在处理pid文件[{filename}]'.format(pid=pid, filename=filename))
                    temp = filename.split('.')
                    py_pid = temp[0]
                    try:
                        py_pid = int(py_pid)
                    except Exception as e:
                        self.logger.error(u'{pid}：处理pid文件[{filename}]时发生异常：\n{err}'
                                          .format(pid=pid, filename=filename, err=str(e)))
                        os.unlink(item)
                        continue
                    if psutil.pid_exists(py_pid):
                        self.logger.info(u'{pid}：父进程[{py_pid}]进程存活，忽略操作……'.format(pid=pid, py_pid=py_pid))
                        continue
                    # 如果不存在，就读取文件
                    self.logger.info(u'{pid}：父进程[{py_pid}]进程已经关闭，开始处理后续……'.format(pid=pid, py_pid=py_pid))
                    with open(item, 'r', encoding='utf-8') as reader:
                        cw_pid = reader.read()
                    try:
                        cw_pid = int(cw_pid)
                    except Exception as e:
                        self.logger.error(u'{pid}：读取pid文件[{filename}]时发生异常：\n{err}'
                                          .format(pid=pid, filename=filename, err=str(e)))
                        continue
                    if not psutil.pid_exists(cw_pid):
                        self.logger.info(u'{pid}：浏览器进程[{cw_pid}]进程已关闭，继续检测……'.format(pid=pid, cw_pid=cw_pid))
                        os.unlink(item)
                        continue
                    self.logger.info(u'{pid}：浏览器进程[{cw_pid}]未关闭，处理后续操作……'.format(pid=pid, cw_pid=cw_pid))
                    try:
                        cw = psutil.Process(cw_pid)
                        cw.kill()
                    except Exception as e:
                        self.logger.error(u'{pid}：关闭浏览器进程[{cw_pid}]时发生异常：\n{err}'
                                          .format(pid=pid, cw_pid=cw_pid, err=str(e)))
                    os.unlink(item)
                file_unlock(locker)
        # 创建selenium
        from selenium import webdriver
        self.logger.info(u'{pid}：正在初始化浏览器……'.format(pid=pid))
        chrome_options = webdriver.ChromeOptions()
        incognito = True
        if extension is not None and isinstance(extension, list):
            for ext in extension:
                # 这里需要传入绝对路径
                chrome_options.add_extension(ext)
                incognito = False
        # prefs = {"profile.managed_default_content_settings.images": 2}
        if prefs is not None and isinstance(prefs, dict):
            chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-images")
        chrome_options.add_argument("--disable-breakpad")
        chrome_options.add_argument("--disable-background-networking")
        chrome_options.add_argument("--disable-push-api-background-mode")
        chrome_options.add_argument("--disable-quic")
        chrome_options.add_argument("--disable-remote-fonts")
        chrome_options.add_argument("--no-service-autorun")
        chrome_options.add_argument("--disable-infobars")
        if incognito:
            chrome_options.add_argument("--incognito")
        if arguments is not None and isinstance(arguments, list):
            for arg in arguments:
                if arg is None:
                    continue
                arg = arg.strip()
                if len(arg) <= 0:
                    continue
                chrome_options.add_argument(arg)
            pass
        _, chrome_driver, self.display = self.__get_chrome_driver(is_display)
        if executable_path is None:
            executable_path = chrome_driver
        self.driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
        if script_timeout is not None:
            try:
                script_timeout = int(script_timeout)
            except Exception as e:
                self.logger.error(u'{pid}：处理script_timeout时发生异常：\n{err}'
                                  .format(pid=pid, err=str(e)))
                script_timeout = 60
            self.driver.set_script_timeout(script_timeout)
        if page_load_timeout is not None:
            try:
                page_load_timeout = int(page_load_timeout)
            except Exception as e:
                self.logger.error(u'{pid}：处理page_load_timeout时发生异常：\n{err}'
                                  .format(pid=pid, err=str(e)))
                page_load_timeout = 60
            self.driver.set_page_load_timeout(page_load_timeout)
        p = psutil.Process(self.driver.service.process.pid)
        chrome = p.children(recursive=False)[0]
        self.cw_pid = chrome.pid
        write_txt_file(os.path.join(pid_path, '{pid}.pid'.format(pid=pid)), str(chrome.pid))
        self.add_cookies(cookies)

    def __del__(self):
        pid = os.getpid()
        try:
            # 销毁浏览器
            if self.cw_pid is not None:
                cw = psutil.Process(self.cw_pid)
                cw.kill()
        except Exception as e:
            self.logger.error(u'{pid}：销毁浏览器时发生异常：\n{err}'.format(pid=pid, err=str(e)))
        try:
            # 销毁虚拟显示器
            if self.display is not None:
                self.display.stop()
        except Exception as e:
            self.logger.error(u'{pid}：销毁虚拟显示器时发生异常：\n{err}'.format(pid=pid, err=str(e)))
        self.logger.info(u'{pid}：完全结束流程'.format(pid=pid))

    @staticmethod
    def __get_chrome_driver(is_display=True):
        system = platform.platform().split('-')[0]
        system = system.lower()
        if system == 'linux':
            bit, plf = platform.architecture()
            if bit == '64bit':
                chrome_driver = os.path.join(get_root_path(), 'drivers', 'linux', '64bit', 'chromedriver')
            else:
                chrome_driver = os.path.join(get_root_path(), 'drivers', 'linux', '32bit', 'chromedriver')
        elif system == 'windows':
            chrome_driver = os.path.join(get_root_path(), 'drivers', 'windows', 'chromedriver')
        else:
            chrome_driver = os.path.join(get_root_path(), 'drivers', system, 'chromedriver')
        chrome_driver = os.path.abspath(chrome_driver)
        display = None
        if system == 'linux' and not is_display:
            from pyvirtualdisplay import Display
            display = Display(visible=0, size=(1024, 768))
            display.start()
        return system, chrome_driver, display

    def get_driver(self):
        return self.driver

    def add_cookies(self, cookies=None):
        if cookies is None:
            return
        pid = os.getpid()
        if not isinstance(cookies, list):
            self.logger.error(u'{pid}：试图加载非列表型变量……'.format(pid=pid))
            return
        keys = ['name', 'value']
        for cookie in cookies:
            is_err = False
            for key in keys:
                if key not in cookie:
                    is_err = True
                    break
            if is_err:
                continue
            kv = {'name': cookie['name'], 'value': cookie['value']}
            self.driver.add_cookie(kv)

    def get_cookies(self):
        return self.driver.get_cookies()

    def get_cookie(self, key):
        return self.driver.get_cookie(key)

    def save_cookies(self, filename=None):
        if filename is None:
            return False, u'请传入文件名'
        pid = os.getpid()
        try:
            path, _ = os.path.split(filename)
            if not os.path.exists(path):
                os.makedirs(path)
            # 尝试删除
            if os.path.isfile(filename):
                os.unlink(filename)
            # 写入数据
            pickle.dump(self.get_cookies(), open(filename, 'wb'))
            self.logger.info(u'{pid}：已保存Cookie到文件[{filename}]'.format(pid=pid, filename=filename))
            return True, u'保存成功'
        except Exception as e:
            self.logger.error(u'{pid}：保存Cookie时发生异常：\n{err}'.format(pid=pid, err=str(e)))
            return False, str(e)

    def load_cookie(self, filename=None):
        if filename is None:
            return False, u'请传入文件名'
        pid = os.getpid()
        try:
            if not os.path.isfile(filename):
                return False, u'Cookie文件不存在，忽略'
            # 载入Cookies
            cookies = pickle.load(open(filename, 'rb'))
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        except Exception as e:
            self.logger.error(u'{pid}：读取Cookie时发生异常：\n{err}'.format(pid=pid, err=str(e)))
            return False, str(e)

    def clear_cookies(self):
        self.driver.delete_all_cookies()

    def del_cookie(self, key):
        self.driver.delete_cookie(key)

    def get_source_code(self):
        elem = self.driver.find_element_by_xpath('//*')
        source_code = elem.get_attribute('outerHTML')
        return source_code

    def go_back(self):
        self.driver.execute_script('window.history.go(-1)')

    def get_chrome_pid(self):
        return self.cw_pid
