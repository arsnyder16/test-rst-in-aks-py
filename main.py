import logging
from kubernetes import client, config, watch

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.DEBUG)
logging.info("reading in-cluster config")
config.load_incluster_config()
logging.info("building client")
v1 = client.CoreV1Api()


def watch_ns():
    w = watch.Watch()
    try:
        for event in w.stream(v1.list_namespace, timeout_seconds=2400):
            logging.info("Event: %s %s" % (event['type'], event['object'].metadata.name))
    except Exception as e:
        logging.info("got exception:", e)
        watch_ns()
    logging.info("manually abort the watch")


if __name__ == "__main__":
    watch_ns()
