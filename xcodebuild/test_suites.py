import subprocess
import os
from config import config as Config
from common_utils import utils
import logging
logger = logging.getLogger()

append_command='SecureMailUITests/AccountConfigurationTests/testLoginWithInvalidCredential_2547 SecureMailUITests/AccountConfigurationTests/testAccountIsConfiguredSuccessfully_2545 SecureMailUITests/AccountConfigurationTests/testMultipleExchangeAccount_14422'
'''
'-only-testing:SecureMailUITests/FileRepositoryTests/testAttachmentsOption_15057 -only-testing:SecureMailUITests/FileRepositoryTests/testSearchAttachmentsByAll_16367 -only-testing:SecureMailUITests/FileRepositoryTests/testSearchAttachmentsBySubject_16131 -only-testing:SecureMailUITests/FileRepositoryTests/testSearchAttachmentsByFileName_16369 -only-testing:SecureMailUITests/FileRepositoryTests/testSearchAttachmentsByFrom_16368 -only-testing:SecureMailUITests/FileRepositoryTests/testSortAttachmentsBySize_16386 -only-testing:SecureMailUITests/FileRepositoryTests/testSortAttachmentsByFileName_16370 -only-testing:SecureMailUITests/FileRepositoryTests/testSortAttachmentsByDate_16387 -only-testing:SecureMailUITests/FileRepositoryTests/testRemoveOfflineFileWhichHasNoOriginalMail_16397 -only-testing:SecureMailUITests/FileRepositoryTests/testEditOfflineAccessToRemove_16391 -only-testing:SecureMailUITests/FileRepositoryTests/testEditOfflineAccessToSave_16390 -only-testing:SecureMailUITests/FileRepositoryTests/testSaveOfflineFiles_16388 -only-testing:SecureMailUITests/FileRepositoryTests/testDeleteOfflineFiles_16389 -only-testing:SecureMailUITests/MailFolderTests/testBasicFolderSearch_14477 -only-testing:SecureMailUITests/MailUITests/testSearchMail_14474 -only-testing:SecureMailUITests/MailUITests/testSelectMultiMailWhenSearchMail_14476 -only-testing:SecureMailUITests/MailUITests/testPriorityInComposeView_14439 -only-testing:SecureMailUITests/MailUITests/testMailTxtAttachment_14455 -only-testing:SecureMailUITests/MailUITests/testMailZipAttachment_14456 -only-testing:SecureMailUITests/MailUITests/testMailAudioAttachment_14457 -only-testing:SecureMailUITests/MailUITests/testMailVideoAttachment_14458 -only-testing:SecureMailUITests/MailUITests/testMailEMLAttachmentWithTXTAttachmentsInside_18640 -only-testing:SecureMailUITests/MailUITests/testMailEmlAttachment_14451 -only-testing:SecureMailUITests/MailUITests/testMailMsgAttachment_14454 -only-testing:SecureMailUITests/MailUITests/testDownloadAttachment_14462 -only-testing:SecureMailUITests/MailUITests/testCheckAttachmentsDetail_16395 -only-testing:SecureMailUITests/MailUITests/testCheckAttachmentsDetail_16394 -only-testing:SecureMailUITests/MailUITests/testForwardEmailWithAttachemt_14436 -only-testing:SecureMailUITests/MailUITests/testForwardEmailWithoutAttachemt_14464 -only-testing:SecureMailUITests/MailUITests/testImportPublicCertFromWithAttachemt_18496 -only-testing:SecureMailUITests/MailFolderTests/testMovingMailsAcrossFoldersFromMessageView_14618 -only-testing:SecureMailUITests/MailFolderTests/testMovingMailsAcrossFoldersUsingSwipe_19035 -only-testing:SecureMailUITests/MailFolderTests/testMovingMailAcrossFolderUsingMultiEdit_19034 -only-testing:SecureMailUITests/MailUITests/testEWSSendAndWMForwardMail_18629 -only-testing:SecureMailUITests/MailUITests/testEWSSendAndWMReplyMail_17369 -only-testing:SecureMailUITests/MailUITests/testWMSendAndEWSReplyMail_17370 -only-testing:SecureMailUITests/MailUITests/testDeleteMultiSelecteMail_14621 -only-testing:SecureMailUITests/MailUITests/testForwardARepliedMail_14448 -only-testing:SecureMailUITests/MailUITests/testAutoSaveMessageInDrafts_14445 -only-testing:SecureMailUITests/MailUITests/testCheckUrlInEmail_14442 -only-testing:SecureMailUITests/AccountSyncTests/testSyncMail_18579 -only-testing:SecureMailUITests/AccountSyncTests/testSyncCalendar_18580 -only-testing:SecureMailUITests/AccountSyncTests/testSyncContact_14469 -only-testing:SecureMailUITests/MailFolderTests/testBasicFolderOperations_16598 -only-testing:SecureMailUITests/ContactsUITests/testCreateContact_AddDistributionList_18584 -only-testing:SecureMailUITests/MailUITests/testOrganiseByConversationEnabled_18573 -only-testing:SecureMailUITests/MailUITests/testOrganiseByConversationDisabled_14463 -only-testing:SecureMailUITests/SlideViewTests/testEmailSlideView_EmailSlideMenuOperationsWorkForMailConversation_14428 -only-testing:SecureMailUITests/SlideViewTests/testEmailSlideView_EmailSlideMenuOperationsWorkForSingleMail_18578 -only-testing:SecureMailUITests/SlideViewTests/testEmailSlideView_OperationsWorkForMultipleMailSelection_14617 -only-testing:SecureMailUITests/ContactsUITests/testSearchContact_ValidateBasicSearchOperation_14615 -only-testing:SecureMailUITests/ContactsUITests/testSearchContact_ValidateSearchOperationInMRU -only-testing:SecureMailUITests/ContactsUITests/testSearchContact_ValidateActionableOperationForSearchedContact -only-testing:SecureMailUITests/ContactsUITests/testSearchContact_ValidateSearchOperation -only-testing:SecureMailUITests/ContactsUITests/testDeleteContact_17368 -only-testing:SecureMailUITests/ContactsUITests/testLocalSearchContact_14475 -only-testing:SecureMailUITests/ContactsUITests/testCallOperationContacts_OutgoingCallsVerify -only-testing:SecureMailUITests/ContactsUITests/testMultiSelectContact_14467 -only-testing:SecureMailUITests/MailUITests/testInsertPicture_14434 -only-testing:SecureMailUITests/MailUITests/testPastePicture_14433 -only-testing:SecureMailUITests/MailUITests/testSendMailWithAttachment_16393 -only-testing:SecureMailUITests/MailUITests/testReceiveMailContainsAttachmentsFromOutlook_16130 -only-testing:SecureMailUITests/MailUITests/testSendMailWithAttachments_16392 -only-testing:SecureMailUITests/MailUITests/testNewMailWithPhotoAttachment_14459 -only-testing:SecureMailUITests/MailUITests/testNewMailWithCameraAttachment_14460 -only-testing:SecureMailUITests/MailUITests/testNewMailWithAttachment_16396 -only-testing:SecureMailUITests/MailUITests/testSendMailWithShareFileAttachment_14438 -only-testing:SecureMailUITests/TriageViewTests/testMail_Triage_View_GestureMovesMailOutOfTriageView_14449 -only-testing:SecureMailUITests/TriageViewTests/testMail_Triage_View_Settings_14450 -only-testing:SecureMailUITests/ContactsUITests/testPersonalDLSync_16537 -only-testing:SecureMailUITests/ContactsUITests/testPersonalDLSupportInMessageCompostScreen_16538 -only-testing:SecureMailUITests/ReplyReplyAllMeetingTests/testEWSCreateAndWMReplyMeeting_16426 -only-testing:SecureMailUITests/ContactsUITests/testContactMessage_ValidateMessageOperations -only-testing:SecureMailUITests/ContactsUITests/testContactMessage_ValidateMessageOperations_MutlipleMessages -only-testing:SecureMailUITests/ContactsUITests/testDeleteContact_BasicContactDeletion -only-testing:SecureMailUITests/ContactsUITests/testDeleteContact_UsingSlideOutMenu -only-testing:SecureMailUITests/PrivateMeetingTests/testPrivateMeeting_OrganizerCreate_NonRecurringMeeting_18599 -only-testing:SecureMailUITests/DeleteMeetingTests/testDeleteMeeting_OrganizerWM_SingleOccurrenceOfRecurringMeeting_18600 -only-testing:SecureMailUITests/DeleteMeetingTests/testDeleteMeeting_OrganizerWM_WholeSeriesOfRecurringMeeting_16413 -only-testing:SecureMailUITests/ContactsUITests/testContactGalLookUp_BasicGalLookUpValidation -only-testing:SecureMailUITests/ContactsUITests/testContactGalLookUp_ContactIsEdittedFromServer -only-testing:SecureMailUITests/ContactsUITests/testContactMRU_BasicMRUOperations_14440 -only-testing:SecureMailUITests/ForwardMeetingTests/testMeetingForward_WhenOrganizerEdits_NonRecurringMeeting_18648 -only-testing:SecureMailUITests/ForwardMeetingTests/testMeetingForward_RecurringMeeting_fromInviteeCalendar_16427 -only-testing:SecureMailUITests/ContactsUITests/testExportContactToLocalSystem_14461 -only-testing:SecureMailUITests/ContactsUITests/testExportMultiContactToLocalSystem_18627 -only-testing:SecureMailUITests/ContactsUITests/testShareContactViaSecureMail_16554 -only-testing:SecureMailUITests/ContactsUITests/testExportContact_AddContactFromServerAndExportToPhone -only-testing:SecureMailUITests/ContactsUITests/testExportContact_ValidateExportOperationInLandscapeAndPortrait -only-testing:SecureMailUITests/ContactsUITests/testExportContact_ValidateExportOperationWhenExportContactPolicyIsOFF -only-testing:SecureMailUITests/ContactsUITests/testsyncWithLocalContact_19559 -only-testing:SecureMailUITests/ContactsUITests/testSaveContactFromCalendar_18582 -only-testing:SecureMailUITests/ContactsUITests/testSaveContactFromMail_17366 -only-testing:SecureMailUITests/ContactsUITests/testSaveContactFromMailAndMarkAsVip_14470 -only-testing:SecureMailUITests/ContactsUITests/testSaveContactFromGALLookUp_18583 -only-testing:SecureMailUITests/CalendarUITest/testCreateGoToMeetingConference_18589 -only-testing:SecureMailUITests/CalendarUITest/testSkypeForBusinessMeetingConferenceID_19053 -only-testing:SecureMailUITests/CalendarUITest/testCreateCustomConference_18590 -only-testing:SecureMailUITests/CalendarUITest/testEWSCreateAndWMRespondMeeting_16428 -only-testing:SecureMailUITests/CalendarUITest/testEWSCreateAndWMRespondMeetingFromMailBody_18651 -only-testing:SecureMailUITests/CalendarUITest/testWMCreateAndEWSRespondMeeting_18598 -only-testing:SecureMailUITests/CalendarUITest/testCheckInviteeAvailability_16398 -only-testing:SecureMailUITests/CalendarUITest/testImportPersonalCalendar_16543 -only-testing:SecureMailUITests/CalendarUITest/testSyncPersonalCalendar_19557 -only-testing:SecureMailUITests/CalendarUITest/testEventView_16401 -only-testing:SecureMailUITests/AccountConfigurationTests/testLoginWithInvalidCredential_2547 -only-testing:SecureMailUITests/AccountConfigurationTests/testAccountIsConfiguredSuccessfully_2545 -only-testing:SecureMailUITests/AccountConfigurationTests/testMultipleExchangeAccount_14422 -only-testing:SecureMailUITests/SettingsTests/testOOO_InsideMyOrganisation_2562 -only-testing:SecureMailUITests/SettingsTests/testSettings_PrivacyPolicyIsDisplayed_2555 -only-testing:SecureMailUITests/SettingsTests/testSettings_verifyServerFieldInAccountSettingsIsEditable_18581 -only-testing:SecureMailUITests/SettingsTests/testSettings_SlideOperationsSettings_16520 -only-testing:SecureMailUITests/SettingsTests/testPictureSettingForInlinePicture_14435 -only-testing:SecureMailUITests/SettingsTests/testAddTextAndGraphicalContactToSignature_18499 -only-testing:SecureMailUITests/SettingsTests/testSignatureForMultipleAccounts_17367 -only-testing:SecureMailUITests/SettingsTests/testExportSettingsForOnlyOneLoggedInAcount_14426 -only-testing:SecureMailUITests/SettingsTests/testExportSettingsForMultipulLoggedInAcount_14427 -only-testing:SecureMailUITests/SettingsTests/testWeekNumerSetting_2554 -only-testing:SecureMailUITests/ContactsUITests/testValidateContact_ValidateBasicContactViewAndOperations -only-testing:SecureMailUITests/ContactsUITests/testValidateContact_ValidateSortingAndDisplayOrder_14468 -only-testing:SecureMailUITests/ContactsUITests/testValidateContact_ValidateContactOperations -only-testing:SecureMailUITests/ContactsUITests/testEditContact_BasicEditContact_14466 -only-testing:SecureMailUITests/ContactsUITests/testEditContactVipOption_14471'
'''
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
    #     def run_test(self, scheme, device_id, test_case_ids):

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
        # test_suites = TestSuites(
        #     path='/Users/yangwa/Automation/secure-web-automation')
        # cases = ['GSTC-16570', 'GSTC-16578', 'GSTC-16578']
        # target = 'SecureWebUITest'
        # test_suites.filter_case_id_by_list(target, cases)
