"""
(*)~---------------------------------------------------------------------------
Pupil - eye tracking platform
Copyright (C) 2012-2020 Pupil Labs

Distributed under the terms of the GNU
Lesser General Public License (LGPL v3.0).
See COPYING and COPYING.LESSER for license details.
---------------------------------------------------------------------------~(*)
"""
import abc
import typing as T


# TODO: Consider extending this pattern for notifications through the entire codebase and/or replace with dataclasses with Python 3.7


class _NotificationMixin:

    subject = None

    @classmethod
    def from_dict(cls, dict_: dict):
        assert self.subject is not None
        dict_ = dict_.copy()
        if "subject" not in dict_:
            raise ValueError(f'Argument should contain "subject" key')
        if dict_["subject"] != cls.subject:
            raise ValueError(f'Argument "subject" expected to be {cls.subject}, but got {dict_["subjcet"]}')
        del dict_["subject"]
        if "topic" in dict_:
            del dict_["topic"]
        return cls(**dict_)

    def as_dict(self) -> dict:
        assert self.subject is not None
        return {
            "subject": self.subject,
            **self.__dict__,
        }


class _VersionedNotificationMixin(_NotificationMixin):

    version = None

    @classmethod
    def from_dict(cls, dict_: dict):
        assert self.version is not None
        dict_ = dict_.copy()
        if "version" not in dict_:
            raise ValueError(f'Argument should contain "version" key')
        if dict_["version"] != cls.version:
            raise ValueError(f'Argument "version" expected to be {cls.version}, but got {dict_["version"]}')
        del dict_["version"]
        return super().from_dict(dict_)

    def as_dict(self) -> dict:
        assert self.version is not None
        return {
            "version": self.version,
            **super().as_dict(),
        }


### Notifications


class CalibrationSuccessNotification(_NotificationMixin):

    # _NotificationMixin

    subject = "calibration.successful"

    def __init__(self, *, gazer_class_name: str, timestamp: float, record: bool = False):
        self.gazer_class_name = gazer_class_name
        self.timestamp = timestamp
        self.record = record


class CalibrationFailureNotification(_NotificationMixin):

    # _NotificationMixin

    subject = "calibration.failed"

    def __init__(self, *, reason: str, gazer_class_name: str, timestamp: float, record: bool = False):
        self.reason = reason
        self.gazer_class_name = gazer_class_name
        self.timestamp = timestamp
        self.record = record


class CalibrationSetupNotification(_VersionedNotificationMixin):

    @classmethod
    def calibration_format_version(cls) -> int:
        return cls.version

    @staticmethod
    def file_name() -> str:
        return f"prerecorded_calibration_setup"

    # _VersionedNotificationMixin

    version = 2

    # _NotificationMixin

    subject = f"calibration.setup.v{version}"

    def __init__(self, *, gazer_class_name: str, timestamp: float, calib_data: dict, record: bool = False):
        self.reason = reason
        self.gazer_class_name = gazer_class_name
        self.timestamp = timestamp
        self.calib_data = calib_data
        self.record = record


class CalibrationResultNotification(_VersionedNotificationMixin):

    @classmethod
    def calibration_format_version(cls) -> int:
        return cls.version

    @staticmethod
    def file_name() -> str:
        return f"prerecorded_calibration_result"

    # _VersionedNotificationMixin

    @classmethod
    def version(cls):
        return 2

    # _NotificationMixin

    subject = f"calibration.result.v{version}"

    def __init__(self, *, gazer_class_name: str, timestamp: float, params: dict, record: bool = False):
        self.reason = reason
        self.gazer_class_name = gazer_class_name
        self.timestamp = timestamp
        self.params = params
        self.record = record
