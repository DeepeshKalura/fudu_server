import os
import socket
import signal
import time
import errno
import select
import logging
import fcntl
import tempfile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("http_server")

class TCPConnection:
    """Class to handle TCP connections."""
    
    def __init__(self, address):
        self.address = address
        self.sock = None
        self.create_connection()
    
    def create_connection(self):
        """Create a socket and bind it to the address."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(self.address)
        self.sock.listen(5)
        logger.info(f"Listening on {self.address[0]}:{self.address[1]}")

    def accept_connection(self):
        """Accept incoming connections."""
        conn, addr = self.sock.accept()
        logger.info(f"Accepted connection from {addr}")
        return conn, addr
    
    def close_connection(self):
        """Close the connection."""
        if self.sock:
            self.sock.close()

class Worker:
    def __init__(self, worker_id, tmp_file):
        self.worker_id = worker_id
        self.tmp_file = tmp_file

class HTTPServer:
    LISTENERS = []
    PIPE = []
    WORKERS = {}

    def __init__(self, address=None, worker_processes=1, timeout=60):
        self.address = address if address else ("127.0.0.1", 8000)
        if worker_processes <= 0:
            exit("At least one worker is required.")
        else:
            self.worker_processes = worker_processes

        self.timeout = timeout
        self.master_pid = os.getpid()
        self.init_listeners()
        self.init_pipe()
        self.maintain_worker_count()

    def init_listeners(self):
        """Initialize TCP listeners."""
        try:
            listener = TCPConnection(self.address)
            self.LISTENERS.append(listener)
        except socket.error as e:
            if e.errno == errno.EADDRINUSE:
                logger.error(f"Address {self.address} already in use.")
            raise

    def init_pipe(self):
        """Create a pipe to manage communication between master and workers."""
        if self.PIPE:
            [io.close() for io in self.PIPE]
        self.PIPE = os.pipe()
        [fcntl.fcntl(io, fcntl.F_SETFD, fcntl.FD_CLOEXEC) for io in self.PIPE]

    def spawn_worker(self):
        """Spawn a new worker process."""
        pid = os.fork()
        if pid == 0:  # Worker process
            self.handle_requests()
            os._exit(0)
        else:  # Master process
            logger.info(f"Spawned worker with PID {pid}")
            self.WORKERS[pid] = Worker(len(self.WORKERS), tempfile.TemporaryFile())

    def spawn_missing_workers(self):
        """Ensure that the required number of workers are running."""
        for i in range(self.worker_processes):
            if i not in [w.worker_id for w in self.WORKERS.values()]:
                self.spawn_worker()

    def maintain_worker_count(self):
        """Ensure worker processes are running at the desired count."""
        while True:
            if (len(self.WORKERS.keys()) - self.worker_processes) < 0:
                self.spawn_missing_workers()
            time.sleep(1)

    def handle_requests(self):
        """Worker logic to handle incoming requests."""
        worker_pid = os.getpid()
        logger.info(f"Worker {worker_pid} is ready to handle requests.")
        while True:
            try:
                readable, _, _ = select.select([listener.sock for listener in self.LISTENERS], [], [], self.timeout)
                for sock in readable:
                    conn, addr = sock.accept()
                    self.process_client(conn, addr)
            except socket.error as e:
                if e.errno != errno.EINTR:
                    logger.error(f"Socket error in worker {worker_pid}: {e}")
            except KeyboardInterrupt:
                break
        logger.info(f"Worker {worker_pid} shutting down.")

    def process_client(self, conn, addr):
        """Process client requests."""
        logger.info(f"Processing request from {addr}")
        try:
            data = conn.recv(1024)
            conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nHello, world!\r\n")
        finally:
            conn.close()

    def kill_workers(self, sig=signal.SIGTERM):
        """Terminate all worker processes."""
        for pid in list(self.WORKERS.keys()):
            try:
                os.kill(pid, sig)
                logger.info(f"Worker {pid} killed.")
            except ProcessLookupError:
                pass

    def run(self):
        """Run the HTTP server."""
        try:
            self.maintain_worker_count()
        except KeyboardInterrupt:
            logger.info("Shutting down server...")
            self.kill_workers()
            self.close_listeners()

    def close_listeners(self):
        """Close all open listeners."""
        for listener in self.LISTENERS:
            listener.close_connection()

if __name__ == "__main__":
    server = HTTPServer(worker_processes=2)
    server.run()
