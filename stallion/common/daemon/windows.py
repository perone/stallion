from stallion import main
import win32serviceutil
import win32service
import win32event
import servicemanager
import threading


class StallionSvc(win32serviceutil.ServiceFramework):

    _svc_name_ = 'Stallion'
    _svc_display_name_ = 'Stallion - Python Package Manager'
    _svc_description_ = 'A Python Package Manager interface.'

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.hWaitResume = win32event.CreateEvent(None, 0, 0, None)
        self.timeout = 1000
        self.resumeTimeout = 1000
        self._paused = False
        self.server = None

    def SvcStop(self):
        self.server._Thread__stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STOPPED,
                              (self._svc_name_, ''))

    def SvcPause(self):
        self.ReportServiceStatus(win32service.SERVICE_PAUSE_PENDING)
        self._paused = True
        self.ReportServiceStatus(win32service.SERVICE_PAUSED)
        servicemanager.LogInfoMsg('Paused')

    def SvcContinue(self):
        self.ReportServiceStatus(win32service.SERVICE_CONTINUE_PENDING)
        win32event.SetEvent(self.hWaitResume)
        self.ReportServiceStatus(win32service.SERVICE_RUNNING)
        servicemanager.LogInfoMsg('Resumed')

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        try:
            self.server = threading.Thread(target=main.run_main, args=())
            self.server.start()
        except:
            servicemanager.LogInfoMsg('Error. service will be restarted')
            self.SvcStop()
            self.SvcDoRun()

        while True:
            rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
            if rc == win32event.WAIT_OBJECT_0:
                servicemanager.LogInfoMsg('Bye!')
                break
            if self._paused:
                servicemanager.LogInfoMsg('I\'m paused... Keep waiting...')
            while self._paused:
                rc = win32event.WaitForSingleObject(self.hWaitResume,
                                                    self.resumeTimeout)
                if rc == win32event.WAIT_OBJECT_0:
                    self._paused = False
                    servicemanager.LogInfoMsg('Yeah! Let\'s continue!')
                    break


def run():
    win32serviceutil.HandleCommandLine(StallionSvc)
