from subprocess import Popen, PIPE, STDOUT, TimeoutExpired
import logging
import datetime


logger = logging.getLogger(__name__)


class Noise(Popen):
    def __init__(self, id, endpoint_ip, endpoint_port, bw='100Mbps', timeout=10, parallel=1):
        self.id = id
        self.endpoint_ip = endpoint_ip
        self.endpoint_port = endpoint_port
        self.bw = bw
        self.timeout = timeout
        self.status = 'Running'
        self.start = datetime.datetime.now()
        self.parallel = parallel
        self.end = None
        self.out = None
        cmd = "iperf3 -c {} -p {} -u -b {} -t {} --connect-timeout 3000 -P {}".format(
            self.endpoint_ip,
            self.endpoint_port,
            self.bw,
            self.timeout,
            self.parallel)
        logger.debug("Noise cmd {}".format(cmd))
        super().__init__(cmd.split(" "), stdout=PIPE, stderr=STDOUT, text=True)


    def stop(self):
        self.terminate()
        if self.status == 'Running':
            try:
                self.out = self.communicate(timeout=2)
                self.end = datetime.datetime.now()
                self.status = 'Stopped'
            except TimeoutExpired:
                self.kill()
                self.out = self.communicate()
                self.end = datetime.datetime.now()
                self.status = 'Stopped'

    def as_dict(self):
        if self.status == 'Running' and self.poll() is not None:
            self.out = self.communicate(timeout=1)
            if self.returncode != 0:
                self.status = 'Failed'
            else:
                self.status = 'Stopped'
                self.end = self.start + datetime.timedelta(seconds=self.timeout)
        return {'id': self.id,
                'endpoint_ip': self.endpoint_ip,
                'endpoint_port': self.endpoint_port,
                'status': self.status,
                'out': self.out if self.status == 'Failed' else None,
                'bw': self.bw,
                'timeout': self.timeout,
                'start': self.start,
                'end': self.end
                }
