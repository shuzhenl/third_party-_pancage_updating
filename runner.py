
import logging
from common_utils.test_runner import BaseRunner
from ios_agent.xcodebuild.test_suites import TestSuites
from common_utils.job_config_model import JobConfig
from . import simctl_service
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class iOSRunner(BaseRunner):

    def __init__(self, config: JobConfig):
        super(iOSRunner, self).__init__(config)
        self.device = None
        self.report_dir = None

    def set_up(self):
        super(iOSRunner, self).set_up()
        new_device_name = '%s_%d_%s' % (self.config.device_type,
                                        self.config.instance_id,
                                        self.config.locale)
        self.device = simctl_service.create_and_boot_simulator(new_device_name,
                                                               self.config.device_type,
                                                               self.config.system_version)
        self.device.install(self.app_path)

    def run(self):
        test_suites = TestSuites(
            path=self.repo_path,
            device_id=self.device.udid,
            locale=self.config.locale
        )
        test_suites.filter_case_id_by_list(self.config.test_cases)
        report_dir = test_suites.run_test(self.config.instance_id)
        logger.info('tests run complete')
        self.report_dir = report_dir

    def tear_down(self):
        if self.device:
            simctl_service.delete_simulator(self.device)

    @classmethod
    def clean(cls):
        simctl_service.delete_all_overdue_simulator()
