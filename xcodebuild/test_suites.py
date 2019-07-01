import subprocess
import os
from config import config as Config
from common_utils import utils
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

append_command='-only-testing:SecureMailUITests/FileRepositoryTests/testAttachmentsOption_15057 -only-testing:SecureMailUITests/FileRepositoryTests/testSearchAttachmentsByAll_16367 -only-testing:SecureMailUITests/FileRepositoryTests/testEditOfflineAccessToSave_16390 -only-testing:SecureMailUITests/FileRepositoryTests/testSaveOfflineFiles_16388 -only-testing:SecureMailUITests/MailFolderTests/testBasicFolderSearch_14477 -only-testing:SecureMailUITests/MailUITests/testSelectMultiMailWhenSearchMail_14476 -only-testing:SecureMailUITests/MailUITests/testMailEmlAttachment_14451 -only-testing:SecureMailUITests/MailUITests/testMailMsgAttachment_14454 -only-testing:SecureMailUITests/MailUITests/testDownloadAttachment_14462 -only-testing:SecureMailUITests/MailUITests/testForwardEmailWithAttachemt_14436 -only-testing:SecureMailUITests/MailUITests/testForwardEmailWithoutAttachemt_14464 -only-testing:SecureMailUITests/MailUITests/testEWSSendAndWMForwardMail_18629 -only-testing:SecureMailUITests/MailUITests/testEWSSendAndWMReplyMail_17369 -only-testing:SecureMailUITests/MailUITests/testWMSendAndEWSReplyMail_17370 -only-testing:SecureMailUITests/MailUITests/testForwardARepliedMail_14448 -only-testing:SecureMailUITests/MailUITests/testCheckUrlInEmail_14442 -only-testing:SecureMailUITests/AccountSyncTests/testSyncMail_18579 -only-testing:SecureMailUITests/AccountSyncTests/testSyncCalendar_18580 -only-testing:SecureMailUITests/SlideViewTests/testEmailSlideView_OperationsWorkForMultipleMailSelection_14617 -only-testing:SecureMailUITests/ContactsUITests/testCallOperationContacts_OutgoingCallsVerify -only-testing:SecureMailUITests/ContactsUITests/testMultiSelectContact_14467 -only-testing:SecureMailUITests/MailUITests/testReceiveMailContainsAttachmentsFromOutlook_16130 -only-testing:SecureMailUITests/MailUITests/testSendMailWithAttachments_16392 -only-testing:SecureMailUITests/MailUITests/testNewMailWithPhotoAttachment_14459 -only-testing:SecureMailUITests/TriageViewTests/testMail_Triage_View_Settings_14450 -only-testing:SecureMailUITests/ReplyReplyAllMeetingTests/testEWSCreateAndWMReplyMeeting_16426 -only-testing:SecureMailUITests/PrivateMeetingTests/testPrivateMeeting_OrganizerCreate_NonRecurringMeeting_18599 -only-testing:SecureMailUITests/ContactsUITests/testContactMRU_BasicMRUOperations_14440 -only-testing:SecureMailUITests/ForwardMeetingTests/testMeetingForward_RecurringMeeting_fromInviteeCalendar_16427 -only-testing:SecureMailUITests/ContactsUITests/testExportContactToLocalSystem_14461 -only-testing:SecureMailUITests/CalendarUITest/testEventView_16401 -only-testing:SecureMailUITests/SettingsTests/testSettings_SlideOperationsSettings_16520 -only-testing:SecureMailUITests/SettingsTests/testSignatureForMultipleAccounts_17367 -only-testing:SecureMailUITests/SettingsTests/testExportSettingsForOnlyOneLoggedInAcount_14426 -only-testing:SecureMailUITests/SettingsTests/testExportSettingsForMultipulLoggedInAcount_14427'
class TestSuites(object):

    def __init__(self, path, device_id, locale, scheme=None, target=None):
        self.append_command=append_command
        self.path = path
        self.scheme = scheme
        self.target = target
        self.device_id = device_id
        self.locale = locale
        '''
        config = build_util.get_build_config(self.path)
        if(scheme is None):
            self.scheme = config.get('project').get('schemes')[0]
        if(target is None):
            self.target = config.get('project').get('targets')[0]
        '''
        self._all_test_cases = self.load_all_cases_from_path(path=path)
        self.select_test_cases = self._all_test_cases

    def _run_grep_cases_command(self, path):
        """Run an xcrun simctl command."""
        full_command = "grep -e '^-\s*(void)\s*test\w*_\d*.*$'  -r '%s'" \
            % (path,)
        # Deliberately don't catch the exception - we want it to bubble up
        return subprocess.check_output(full_command,
                                       universal_newlines=True,
                                       shell=True)

    def load_all_cases_from_path(self, path='.'):
        lines = self._run_grep_cases_command(path).split('\n')
        test_case_ids = []
        for line in lines:
            if(len(line) > 0):
                file_path, matched_line = line.split(':')

                file_name = os.path.basename(file_path)
                class_name = os.path.splitext(file_name)[0].split('+')[0]

                method_name = matched_line.split(')')[-1]
                test_case_ids.append("%s/%s" % (class_name, method_name))
        return test_case_ids

    def filter_case_id_by_list(self):
        self.select_test_cases = []
        for case in self._all_test_cases:
            self.select_test_cases.append(self.target + "/" + case)
        return self.select_test_cases

    def run_test(self, instance_id):
        report_dir = os.path.join(
            Config.BASE_DIR,
            Config.REPORT_SAVE_RELATIVE_PATH,
            str(instance_id)
        )
        utils.ensure_dir(report_dir)

        build_util.run_test(self.scheme,
                            self.device_id,
                            self.select_test_cases,
                            self.locale,
                            self.path,
                            report_dir)

        return report_dir
