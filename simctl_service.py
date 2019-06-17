from xcrun import simctl
from subprocess import CalledProcessError
from retrying import retry
import re
import time

from config import config
import logging
logger = logging.getLogger()


@retry(retry_on_exception=lambda e: isinstance(e, CalledProcessError),
       stop_max_attempt_number=3,
       wait_fixed=2000)
def create_and_boot_simulator(device_name, device_type, runtime=None):

    device = create_simulator(device_name, device_type, runtime)
    if(device.state != 'Booted'):
        try:
            device.boot()
            while(device.state != 'Booted'):
                logger.info(
                    'sumulator: %s is not booted, waiting now',
                    device_name)
                time.sleep(5.0)
                device.refresh_state()
            logger.info('simulator %s booted' % device_name)
            return device
        except CalledProcessError as error:
            if device.state == 'Booted':
                return device
            else:
                raise error


@retry(retry_on_exception=lambda e: isinstance(e, CalledProcessError),
       stop_max_attempt_number=3,
       wait_fixed=2000)
def create_simulator(new_device_name, device_type_name, runtime=None):
    """device_name: iPhone 6, iPhone X etc."""
    if runtime is None:
        runtime = config.DEFAULT_RUNTIME

    try:
        runtime = simctl.runtime.from_name(config.DEFAULT_RUNTIME)
    except simctl.runtime.RuntimeNotFoundError as error:
        logger.info(
            'runtime not found, going to auto discover an exist runtime')
        runtimes = simctl.listall.runtimes()
        runtime = [x for x in runtimes if x.name.startswith(runtime) or x.name.startswith('iOS')][-1]
        if runtime is not None:
            logger.info('runtime detected :' + runtime.name)
        else:
            raise simctl.runtime.RuntimeNotFoundError('Runtime not found')
    try:
        device_type = simctl.device_type.from_name(device_type_name)
        logger.info('device_type <%s> found!', device_type_name)
    except simctl.device_type.DeviceTypeNotFoundError as error:
        logger.info('device_type <%s> not found!', device_type_name)
        raise error

    try:
        logger.info('create device with deivce name:%s, type:%s, runtime:%s' %
                    (new_device_name, device_type_name, runtime))
        device = simctl.device.create(new_device_name, device_type, runtime)
        logger.info('device created: %s', new_device_name)
    except CalledProcessError as error:
        logger.exception(error)
        # if we got exception when try to create device, will check if this
        # device created success again
        device = simctl.device.from_name(new_device_name, runtime)
        if device is not None:
            return device
        else:
            raise CalledProcessError
    return device


@retry(retry_on_exception=lambda e: isinstance(e, CalledProcessError),
       stop_max_attempt_number=3,
       wait_fixed=2000)
def delete_simulator(device):
    device_id = device.udid
    try:
        device.delete()
        logger.info('device:%s deleted', device.name)
    except CalledProcessError as error:
        if simctl.device.from_identifier(device_id) is None:
            return
        else:
            raise error


def _delete_devices_match_regex(regex):
    regex = re.compile(regex)
    devices = simctl.device.from_regex_of_name(regex)
    if devices is None:
        return
    for device in devices:
        try:
            delete_simulator(device)
        except Exception as error:
            logger.warning(
                "Error:%s happened when delete overdue device: %s", str(error),
                device.name)


def delete_all_overdue_simulator():
    _delete_devices_match_regex(r"\d+_[\w-]+$")


def delete_simulators_about_instance(instance_id):
    _delete_devices_match_regex(str(instance_id) + r"_[\w-]+$")
