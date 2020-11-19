import signal
import logging
import threading

from contextlib import contextmanager
from threading import Lock
from kubernetes import client, config, watch

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.DEBUG)
logging.info("reading in-cluster config")
config.load_incluster_config()
logging.info("building client")
logger_lock = Lock()
v1 = client.CoreV1Api()

class TimeoutException(Exception): pass

@contextmanager
def time_limit(seconds):
  def signal_handler(signum, frame):
    raise TimeoutException("Timed out!")
  signal.signal(signal.SIGALRM, signal_handler)
  signal.alarm(seconds)
  try:
    yield
  finally:
    signal.alarm(0)

def watchApi(id, type):
  w = watch.Watch()
  try:
    with logger_lock:
      logging.info(f"start {type} watch")
    with time_limit(480):
      for event in w.stream(id, timeout_seconds=360):
        pass
      #logging.info(f"{type} Event: %s %s" % (event['type'], event['object'].metadata.name))
    with logger_lock:
      logging.info(f"{type} watch shutdown")
  except TimeoutException as e:
    w.stop()
    with logger_lock:
      logging.info(f"!!! manually abort the {type} watch !!!!")
  except Exception as e:
    with logger_lock:
      logging.info(f"{type} got exception:", e)    
  watchApi(id, type)

def main():
  watchApi(v1.list_pod_for_all_namespaces, "pod")

if __name__ == "__main__":
  main()